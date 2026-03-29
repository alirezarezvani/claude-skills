#!/usr/bin/env python3
"""
ha_api.py — Shared Home Assistant REST + WebSocket client.

Usage (as library):
    from ha_api import HAAPI
    api = HAAPI()
    states = api.get_states()

Usage (CLI):
    python3 ha_api.py --help
    python3 ha_api.py states
    python3 ha_api.py state light.living_room
    python3 ha_api.py services
    python3 ha_api.py config
"""

import argparse
import json
import os
import sys
import time
import threading
from typing import Any, Dict, List, Optional

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    sys.exit("Missing dependency: pip install requests urllib3")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv optional


class HAAPI:
    """Home Assistant REST API client with upsert helpers."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        verify_ssl: bool = False,
    ):
        self.base_url = (
            base_url
            or os.environ.get("HA_EXTERNAL_URL")
            or os.environ.get("HA_URL", "http://homeassistant.local:8123")
        ).rstrip("/")
        self.token = token or os.environ.get("HA_TOKEN", "")
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        )

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/{path.lstrip('/')}"

    def get(self, path: str) -> Any:
        resp = self.session.get(self._url(path), verify=self.verify_ssl)
        resp.raise_for_status()
        return resp.json()

    def post(self, path: str, data: Dict) -> Any:
        resp = self.session.post(self._url(path), json=data, verify=self.verify_ssl)
        resp.raise_for_status()
        return resp.json()

    def delete(self, path: str) -> Any:
        resp = self.session.delete(self._url(path), verify=self.verify_ssl)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            return {}

    # ------------------------------------------------------------------
    # Core endpoints
    # ------------------------------------------------------------------

    def ping(self) -> bool:
        """Return True if HA is reachable and token is valid."""
        try:
            result = self.get("/")
            return result.get("message") == "API running."
        except Exception:
            return False

    def get_config(self) -> Dict:
        return self.get("config")

    def get_states(self) -> List[Dict]:
        return self.get("states")

    def get_state(self, entity_id: str) -> Dict:
        return self.get(f"states/{entity_id}")

    def set_state(self, entity_id: str, state: str, attributes: Dict = None) -> Dict:
        payload = {"state": state}
        if attributes:
            payload["attributes"] = attributes
        return self.post(f"states/{entity_id}", payload)

    def call_service(self, domain: str, service: str, data: Dict = None) -> List:
        return self.post(f"services/{domain}/{service}", data or {})

    def get_services(self) -> List[Dict]:
        return self.get("services")

    # ------------------------------------------------------------------
    # Entity registry
    # ------------------------------------------------------------------

    def get_entity_registry(self) -> List[Dict]:
        """Return all entity registry entries (requires HA 2021.6+)."""
        return self.post("template", {"template": "{{ states | list | tojson }}"})

    # ------------------------------------------------------------------
    # Automations
    # ------------------------------------------------------------------

    def list_automations(self) -> List[Dict]:
        """Return all automation entities with full state."""
        states = self.get_states()
        return [s for s in states if s["entity_id"].startswith("automation.")]

    def get_automation_config(self, automation_id: str) -> Dict:
        """Fetch raw config for a single automation via the config API."""
        return self.get(f"config/automation/config/{automation_id}")

    def upsert_automation(self, config: Dict) -> Dict:
        """
        Create or update an automation.
        Matches by 'alias'. Deletes existing before re-creating.
        config must include 'alias', 'trigger', 'action' keys.
        """
        alias = config.get("alias")
        if not alias:
            raise ValueError("Automation config must include 'alias'")

        existing = self._find_automation_by_alias(alias)
        if existing:
            auto_id = existing["entity_id"].replace("automation.", "")
            self.delete(f"config/automation/config/{auto_id}")
            time.sleep(0.3)

        return self.post("config/automation/config", config)

    def _find_automation_by_alias(self, alias: str) -> Optional[Dict]:
        for auto in self.list_automations():
            attrs = auto.get("attributes", {})
            if attrs.get("friendly_name") == alias or attrs.get("alias") == alias:
                return auto
        return None

    def delete_automation(self, alias: str) -> bool:
        """Delete automation by alias. Returns True if found and deleted."""
        existing = self._find_automation_by_alias(alias)
        if not existing:
            return False
        auto_id = existing["entity_id"].replace("automation.", "")
        self.delete(f"config/automation/config/{auto_id}")
        return True

    def reload_automations(self) -> None:
        self.call_service("automation", "reload")

    # ------------------------------------------------------------------
    # Scenes
    # ------------------------------------------------------------------

    def list_scenes(self) -> List[Dict]:
        states = self.get_states()
        return [s for s in states if s["entity_id"].startswith("scene.")]

    def upsert_scene(self, config: Dict) -> Dict:
        """
        Create or update a scene.
        config must include 'name' and 'entities' keys.
        """
        return self.post("config/scene/config", config)

    def reload_scenes(self) -> None:
        self.call_service("scene", "reload")

    # ------------------------------------------------------------------
    # Entity customization (display names, icons)
    # ------------------------------------------------------------------

    def set_entity_name(self, entity_id: str, name: str) -> Dict:
        return self.post(
            "config/entity_registry/update",
            {"entity_id": entity_id, "name": name},
        )

    def set_entity_icon(self, entity_id: str, icon: str) -> Dict:
        return self.post(
            "config/entity_registry/update",
            {"entity_id": entity_id, "icon": icon},
        )

    # ------------------------------------------------------------------
    # Input helpers (input_boolean, input_select, etc.)
    # ------------------------------------------------------------------

    def ensure_input_boolean(self, name: str, entity_id: str) -> None:
        """Create an input_boolean if it doesn't already exist."""
        existing = [
            s for s in self.get_states()
            if s["entity_id"] == f"input_boolean.{entity_id}"
        ]
        if existing:
            return
        self.post(
            "config/input_boolean/config",
            {"id": entity_id, "name": name, "initial": False},
        )

    # ------------------------------------------------------------------
    # WebSocket helpers (for Lovelace dashboard writes)
    # ------------------------------------------------------------------

    def lovelace_save_config(self, dashboard_config: Dict, url_path: str = None) -> Dict:
        """
        Write Lovelace dashboard config via WebSocket.
        url_path=None targets the default dashboard; pass a slug for extra dashboards.
        """
        try:
            import websocket as ws_lib
        except ImportError:
            sys.exit("Missing dependency: pip install websocket-client")

        ws_url = self.base_url.replace("https://", "wss://").replace("http://", "ws://")
        ws_url += "/api/websocket"

        result = {}
        done = threading.Event()

        def on_message(ws, message):
            msg = json.loads(message)
            msg_type = msg.get("type")
            if msg_type == "auth_required":
                ws.send(json.dumps({"type": "auth", "access_token": self.token}))
            elif msg_type == "auth_ok":
                payload = {
                    "id": 1,
                    "type": "lovelace/config/save",
                    "config": dashboard_config,
                }
                if url_path:
                    payload["url_path"] = url_path
                ws.send(json.dumps(payload))
            elif msg.get("id") == 1:
                result.update(msg)
                done.set()
                ws.close()

        def on_error(ws, error):
            result["error"] = str(error)
            done.set()

        wsa = ws_lib.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
        )
        t = threading.Thread(target=wsa.run_forever, kwargs={"sslopt": {"cert_reqs": 0}})
        t.daemon = True
        t.start()
        done.wait(timeout=15)
        return result


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Home Assistant API CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("ping", help="Check HA connectivity")
    sub.add_parser("config", help="Show HA configuration")
    sub.add_parser("states", help="List all entity states")
    sub.add_parser("services", help="List all services")

    state_p = sub.add_parser("state", help="Get state of a single entity")
    state_p.add_argument("entity_id", help="e.g. light.living_room")

    call_p = sub.add_parser("call", help="Call a service")
    call_p.add_argument("domain", help="e.g. light")
    call_p.add_argument("service", help="e.g. turn_on")
    call_p.add_argument("--data", default="{}", help="JSON payload")

    return p


def main():
    parser = _build_parser()
    args = parser.parse_args()

    api = HAAPI()

    if args.cmd == "ping":
        ok = api.ping()
        print("OK — HA is reachable" if ok else "FAIL — cannot reach HA")
        sys.exit(0 if ok else 1)

    elif args.cmd == "config":
        print(json.dumps(api.get_config(), indent=2, ensure_ascii=False))

    elif args.cmd == "states":
        states = api.get_states()
        for s in states:
            print(f"{s['entity_id']}: {s['state']}")

    elif args.cmd == "state":
        s = api.get_state(args.entity_id)
        print(json.dumps(s, indent=2, ensure_ascii=False))

    elif args.cmd == "services":
        services = api.get_services()
        for svc in services:
            domain = svc.get("domain")
            for name in svc.get("services", {}).keys():
                print(f"{domain}.{name}")

    elif args.cmd == "call":
        data = json.loads(args.data)
        result = api.call_service(args.domain, args.service, data)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
