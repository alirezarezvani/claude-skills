---
name: "ha-config-as-code"
description: "Home Assistant Configuration as Code - manage automations, scenes, dashboards, and integrations via Python + REST/WebSocket APIs"
---

# Home Assistant Configuration as Code

**Tier:** POWERFUL
**Category:** Engineering
**Domain:** IoT / Home Automation / Infrastructure as Code

---

## Overview

Manage Home Assistant automations, scenes, dashboards, and device settings as code using Python scripts and the HA REST/WebSocket APIs. This skill packages a Git-friendly, idempotent, layered deployment model for full HA configuration lifecycle management.

**Core principle:** Every HA configuration change is expressed as a Python script that calls the HA API — no manual UI clicks required, and every change is reviewable via `git diff`.

---

## Core Capabilities

- **API-first workflow** via `/api/*` and `/api/websocket`
- **Idempotent scripts** (safe to re-run; upsert semantics)
- **Git-friendly** change tracking and rollback
- **Layered deployment model** (switches → scenes → automations → groups → dashboard → integrations)
- **Entity validation** — scan live entities, detect drift, verify expected entities exist
- **Automation diffing** — compare desired vs current automation state
- **Dashboard generation** — Lovelace YAML config written via WebSocket

---

## When to Use

- Setting up a new HA instance from scratch
- Migrating HA config to a new host
- Auditing automation drift (manual UI changes vs git state)
- Safely deploying bulk changes across multiple devices/areas
- Onboarding a team member to manage HA config programmatically

---

## Quick Start

```bash
# 1. Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install requests websocket-client urllib3 python-dotenv

# 2. Configure and connect (interactive wizard — sets up .env and tests connection)
python3 scripts/ha_setup.py

# 3. List entities to verify connection
python3 scripts/ha_entity_lister.py --domain light

# 4. Validate config before deploying
python3 scripts/ha_config_validator.py --check-entities

# 5. Diff current vs desired automations
python3 scripts/ha_automation_diff.py
```

---

## Recommended Deployment Order

Run scripts in this order for a clean first-time deployment or full re-apply:

```bash
# 1) Wireless switch setup (first-time only)
python3 scripts/setup_wireless_switches.py --set-wireless

# 2) Remove legacy automations, bind event automations
python3 scripts/setup_wireless_switches.py --cleanup --bind

# 3) Scenes
python3 scripts/setup_scenes.py

# 4) Automations + helpers
python3 scripts/setup_automations.py

# 5) Light groups
python3 scripts/create_groups.py

# 6) Dashboard
python3 scripts/setup_dashboard.py --theme md3_yellow

# 7) Adaptive Lighting
python3 scripts/setup_adaptive_lighting.py

# 8) HomeKit Bridge
python3 scripts/setup_homekit.py

# 9) Power-on behavior
python3 scripts/setup_power_on_state.py

# 10) Forecast template sensors
python3 scripts/setup_weather_forecast.py
```

---

## Script Reference

### Core API Client

| Script | Purpose |
|--------|---------|
| `scripts/ha_api.py` | Shared REST client, auth headers, upsert helpers for automations/scenes |

### Analysis & Validation Tools

| Script | Purpose |
|--------|---------|
| `scripts/ha_entity_lister.py` | List/filter live entities by domain, area, state, or keyword |
| `scripts/ha_config_validator.py` | Validate entity IDs exist, check expected devices are reachable |
| `scripts/ha_automation_diff.py` | Diff current HA automations vs local YAML definitions |

### Configuration Scripts

| Script | Purpose |
|--------|---------|
| `scripts/setup_wireless_switches.py` | `--set-wireless` / `--cleanup` / `--bind` switch event automations |
| `scripts/setup_scenes.py` | Create Guest/Cinema/Sleep scenes, set Chinese display names/icons |
| `scripts/setup_automations.py` | Deploy environment/safety/presence/pet/leave-home automations |
| `scripts/create_groups.py` | Create area light groups and whole-home strip groups |
| `scripts/setup_dashboard.py` | Generate and write Lovelace dashboard via WebSocket |
| `scripts/setup_adaptive_lighting.py` | Create per-area Adaptive Lighting entries |
| `scripts/setup_homekit.py` | Configure HomeKit Bridge, exclude Matter-direct devices |
| `scripts/setup_power_on_state.py` | Auto-discover power-on select entities, set memory/previous mode |
| `scripts/setup_weather_forecast.py` | Write template sensor YAML for multi-day forecast data |

---

## Environment Variables

```env
HA_URL=http://YOUR_HA_IP:8123
HA_EXTERNAL_URL=https://your-domain.com:PORT
HA_TOKEN=your_long_lived_access_token
HA_SSH_HOST=YOUR_HA_IP
HA_SSH_USER=hassio
HA_SSH_PASSWORD=your_password
```

- `ha_api.py` uses `HA_EXTERNAL_URL` first, falls back to `HA_URL`
- SSH vars only needed for `setup_weather_forecast.py` (writes HA config files)

---

## Required Integrations & Plugins

### HACS Integrations
- **Adaptive Lighting** — per-area circadian color temperature/brightness curves
- **Xiaomi Miot Auto** — Xiaomi/Mi Home device support

### HACS Frontend Cards
- **Mushroom** — primary card components
- **button-card** — custom button styling
- **card-mod** — shadow DOM CSS injection for deep card styling

### Official Integrations
- **Matter** — Matter light device support
- **HomeKit Bridge** — expose non-Matter devices to Apple Home
- **ESPHome** — ESP-based devices (e-ink displays, sensors)

---

## Dashboard Themes

Supported themes in `setup_dashboard.py`:

| Theme | Description |
|-------|-------------|
| `md3_yellow` | Material Design 3, yellow accent (default) |
| `apple_home` | Clean Apple Home-inspired light theme |
| `tech_scifi` | Dark, high-contrast sci-fi aesthetic |
| `minimal_dark` | Minimal dark mode |
| `warm_cabin` | Warm amber tones for cozy environments |

```bash
python3 scripts/setup_dashboard.py --theme apple_home
```

---

## Reference Docs

- `references/ha-rest-api.md` — HA REST API endpoint reference
- `references/ha-automation-patterns.md` — common automation patterns and YAML examples
- `references/ha-deployment-checklist.md` — layered deployment checklist and rollback guide

---

## Common Pitfalls

- **Entity ID drift** — HA can rename entities on re-discovery; run `ha_entity_lister.py` after any device re-pair
- **WebSocket auth timeout** — long-running scripts may need reconnect logic; wrap in retry loops
- **SSH-based config writes** — `setup_weather_forecast.py` requires `sshpass` installed locally and sudo on the HA host
- **Matter vs HomeKit** — Matter-native devices should be excluded from HomeKit Bridge to avoid duplicate control
- **Token expiry** — Long-lived access tokens don't expire, but revocation invalidates all scripts; rotate with care

## Best Practices

1. Commit before and after major runs to keep clean `git diff` output
2. Use `ha_config_validator.py` before bulk automation deploys
3. Test on a dev HA instance first if available
4. Keep entity ID mapping constants at the top of each script for easy migration
5. Add `--dry-run` flags to destructive operations in your own scripts
