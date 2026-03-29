# Home Assistant REST API Reference

Source: https://developers.home-assistant.io/docs/api/rest

## Authentication

All requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <long_lived_access_token>
Content-Type: application/json
```

Create a token at: **Profile → Long-Lived Access Tokens**

---

## Base URL

```
http://<HA_IP>:8123/api/
```

For external access (HTTPS):
```
https://<your-domain>:<port>/api/
```

---

## Core Endpoints

### GET /api/
Check API is running.

**Response:**
```json
{"message": "API running."}
```

### GET /api/config
Return HA configuration information (version, location, components, etc.)

### GET /api/states
Return array of all entity states.

**Response:**
```json
[
  {
    "entity_id": "light.living_room",
    "state": "on",
    "attributes": {
      "friendly_name": "Living Room",
      "brightness": 200,
      "color_mode": "color_temp"
    },
    "last_changed": "2024-01-01T12:00:00+00:00",
    "last_updated": "2024-01-01T12:00:01+00:00"
  }
]
```

### GET /api/states/{entity_id}
Return state for a single entity.

### POST /api/states/{entity_id}
Set state for an entity (creates virtual state, does not control device).

```json
{"state": "on", "attributes": {"brightness": 255}}
```

---

## Services

### GET /api/services
List all available services by domain.

### POST /api/services/{domain}/{service}
Call a service.

**Example — turn on a light:**
```json
POST /api/services/light/turn_on
{
  "entity_id": "light.living_room",
  "brightness": 200,
  "color_temp": 4000
}
```

**Common service domains:**

| Domain | Common Services |
|--------|----------------|
| `light` | `turn_on`, `turn_off`, `toggle` |
| `switch` | `turn_on`, `turn_off`, `toggle` |
| `scene` | `turn_on` |
| `automation` | `trigger`, `turn_on`, `turn_off`, `reload` |
| `script` | `turn_on`, `reload` |
| `homeassistant` | `reload_all`, `restart`, `stop` |
| `input_boolean` | `turn_on`, `turn_off`, `toggle` |
| `input_select` | `select_option`, `select_next` |
| `notify` | `notify` (and per-integration variants) |

---

## Config API (Automations, Scenes)

### GET /api/config/automation/config
List all automation configs (requires `config_entries` component).

### POST /api/config/automation/config
Create new automation. Returns `{"result": "ok", "id": "<uuid>"}`.

**Automation payload:**
```json
{
  "alias": "Turn off lights at night",
  "description": "Auto lights off at 23:00",
  "trigger": [
    {
      "platform": "time",
      "at": "23:00:00"
    }
  ],
  "condition": [],
  "action": [
    {
      "service": "light.turn_off",
      "target": {"area_id": "living_room"}
    }
  ],
  "mode": "single"
}
```

### DELETE /api/config/automation/config/{id}
Delete automation by ID (not entity_id — use the UUID from creation).

### POST /api/config/scene/config
Create/update a scene.

```json
{
  "id": "cinema_mode",
  "name": "Cinema",
  "entities": {
    "light.living_room": {"state": "on", "brightness": 50},
    "light.floor_lamp": {"state": "off"}
  }
}
```

---

## Entity Registry

### POST /api/config/entity_registry/update
Update entity display settings.

```json
{
  "entity_id": "light.living_room",
  "name": "客厅灯",
  "icon": "mdi:ceiling-light"
}
```

---

## Template Rendering

### POST /api/template
Render a Jinja2 template against live HA state.

```json
{"template": "{{ states('sensor.temperature') }}"}
```

Useful for complex queries:
```json
{"template": "{{ states | selectattr('entity_id', 'match', 'light.*') | list | length }}"}
```

---

## Events

### POST /api/events/{event_type}
Fire a custom event.

```json
{"entity_id": "switch.wall_button", "click_type": "single"}
```

---

## Error Codes

| HTTP Code | Meaning |
|-----------|---------|
| 200 | Success |
| 400 | Bad request / invalid payload |
| 401 | Unauthorized — bad or missing token |
| 404 | Entity or endpoint not found |
| 405 | Method not allowed |

---

## WebSocket API (Lovelace)

For dashboard writes, use WebSocket at `/api/websocket`:

```javascript
// Auth flow
→ {"type": "auth_required"}
← {"type": "auth", "access_token": "<token>"}
→ {"type": "auth_ok"}

// Save Lovelace config
← {"id": 1, "type": "lovelace/config/save", "config": {...}}
→ {"id": 1, "type": "result", "success": true}
```

---

## Rate Limiting

HA has no hard rate limit, but:
- Avoid parallel calls to config APIs (automation/scene writes are not atomic)
- Add 0.2–0.5s sleeps between bulk upsert operations
- WebSocket connections: one at a time per script is safest

---

## Long-Lived Access Token Best Practices

1. Create a dedicated token per use-case (CI, scripts, etc.)
2. Store in `.env` file, never commit to git
3. Revoke immediately if leaked — all scripts using that token must be updated
4. Tokens don't expire but are invalidated on profile deletion or explicit revocation
