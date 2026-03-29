# Home Assistant Automation Patterns

Common patterns and YAML templates for HA automations, organized by use case.

---

## 1. Time-Based Patterns

### Daily Schedule

```yaml
alias: "Morning routine"
trigger:
  - platform: time
    at: "07:00:00"
condition:
  - condition: time
    weekday: [mon, tue, wed, thu, fri]
action:
  - service: scene.turn_on
    target:
      entity_id: scene.morning
```

### Sunset/Sunrise Offset

```yaml
alias: "Turn on outdoor lights at sunset"
trigger:
  - platform: sun
    event: sunset
    offset: "-00:30:00"   # 30 min before sunset
action:
  - service: light.turn_on
    target:
      area_id: outdoor
    data:
      brightness_pct: 100
```

### Time Range Condition

```yaml
alias: "Motion lights — nighttime only"
trigger:
  - platform: state
    entity_id: binary_sensor.motion_hallway
    to: "on"
condition:
  - condition: time
    after: "22:00:00"
    before: "06:00:00"
action:
  - service: light.turn_on
    target:
      entity_id: light.hallway
```

---

## 2. Motion & Presence Patterns

### Motion with Auto-Off

```yaml
alias: "Motion light with timeout"
trigger:
  - platform: state
    entity_id: binary_sensor.motion_bathroom
    to: "on"
action:
  - service: light.turn_on
    target:
      entity_id: light.bathroom
  - wait_for_trigger:
      - platform: state
        entity_id: binary_sensor.motion_bathroom
        to: "off"
        for: "00:05:00"
  - service: light.turn_off
    target:
      entity_id: light.bathroom
mode: restart
```

### Person Arrives Home

```yaml
alias: "Welcome home"
trigger:
  - platform: state
    entity_id: person.alice
    to: "home"
condition:
  - condition: state
    entity_id: input_boolean.vacation_mode
    state: "off"
action:
  - service: scene.turn_on
    target:
      entity_id: scene.welcome
  - service: notify.mobile_app_alice
    data:
      message: "Welcome home! Lights are on."
```

### Everyone Leaves

```yaml
alias: "All away — power saving"
trigger:
  - platform: state
    entity_id:
      - person.alice
      - person.bob
    to: "not_home"
    for: "00:05:00"
condition:
  - condition: state
    entity_id: person.alice
    state: "not_home"
  - condition: state
    entity_id: person.bob
    state: "not_home"
action:
  - service: homeassistant.turn_off
    target:
      area_id:
        - living_room
        - bedroom
  - service: climate.set_preset_mode
    target:
      entity_id: climate.main
    data:
      preset_mode: away
```

---

## 3. Device Event Patterns

### Wireless Button (Event-Based)

```yaml
alias: "Wall button — single press toggle living room"
trigger:
  - platform: event
    event_type: zha_event          # or zhimi_event, mqtt, etc.
    event_data:
      device_ieee: "00:11:22:33:44:55:66:77"
      command: "single"
action:
  - service: light.toggle
    target:
      area_id: living_room
```

### Button Multi-Actions

```yaml
alias: "Button single/double/hold"
trigger:
  - platform: event
    event_type: zha_event
    event_data:
      device_ieee: "00:11:22:33:44:55:66:77"
variables:
  click: "{{ trigger.event.data.command }}"
action:
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ click == 'single' }}"
        sequence:
          - service: light.toggle
            target: {area_id: living_room}
      - conditions:
          - condition: template
            value_template: "{{ click == 'double' }}"
        sequence:
          - service: scene.turn_on
            target: {entity_id: scene.cinema}
      - conditions:
          - condition: template
            value_template: "{{ click == 'hold' }}"
        sequence:
          - service: homeassistant.turn_off
            target: {area_id: living_room}
```

---

## 4. Sensor Threshold Patterns

### Temperature Alert

```yaml
alias: "High temperature alert"
trigger:
  - platform: numeric_state
    entity_id: sensor.temperature_bedroom
    above: 30
    for: "00:10:00"
action:
  - service: notify.mobile_app
    data:
      title: "Temperature Alert"
      message: "Bedroom is {{ states('sensor.temperature_bedroom') }}°C"
```

### Door Left Open

```yaml
alias: "Door open too long"
trigger:
  - platform: state
    entity_id: binary_sensor.front_door
    to: "on"
    for: "00:10:00"
action:
  - service: notify.mobile_app
    data:
      message: "Front door has been open for 10 minutes"
```

---

## 5. Safety & Emergency Patterns

### Smoke Detector

```yaml
alias: "Smoke alarm — all lights on"
trigger:
  - platform: state
    entity_id: binary_sensor.smoke_sensor
    to: "on"
action:
  - service: light.turn_on
    target:
      entity_id: all
    data:
      brightness_pct: 100
      color_name: red
  - service: media_player.play_media
    target:
      entity_id: media_player.living_room_speaker
    data:
      media_content_id: /local/alarm.mp3
      media_content_type: music
mode: single
max_exceeded: silent
```

### Water Leak

```yaml
alias: "Water leak detected"
trigger:
  - platform: state
    entity_id: binary_sensor.water_sensor_kitchen
    to: "on"
action:
  - service: switch.turn_off
    target:
      entity_id: switch.water_main_valve
  - service: notify.all_phones
    data:
      title: "WATER LEAK"
      message: "Kitchen water leak detected — main valve shut off"
```

---

## 6. Scene Automation Patterns

### Adaptive Lighting Scenes

```yaml
alias: "Auto scene by time of day"
trigger:
  - platform: time
    at: "08:00:00"
  - platform: time
    at: "17:00:00"
  - platform: time
    at: "22:00:00"
variables:
  hour: "{{ now().hour }}"
action:
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ hour >= 8 and hour < 17 }}"
        sequence:
          - service: scene.turn_on
            target: {entity_id: scene.daytime}
      - conditions:
          - condition: template
            value_template: "{{ hour >= 17 and hour < 22 }}"
        sequence:
          - service: scene.turn_on
            target: {entity_id: scene.evening}
      - conditions:
          - condition: template
            value_template: "{{ hour >= 22 or hour < 8 }}"
        sequence:
          - service: scene.turn_on
            target: {entity_id: scene.night}
```

---

## 7. Helper Entity Patterns

### Input Boolean Toggle

```yaml
alias: "Guest mode toggle"
trigger:
  - platform: state
    entity_id: input_boolean.guest_mode
action:
  - choose:
      - conditions:
          - condition: state
            entity_id: input_boolean.guest_mode
            state: "on"
        sequence:
          - service: scene.turn_on
            target: {entity_id: scene.guest}
      - conditions:
          - condition: state
            entity_id: input_boolean.guest_mode
            state: "off"
        sequence:
          - service: scene.turn_on
            target: {entity_id: scene.normal}
```

---

## 8. Notification Patterns

### Mobile Push with Action Buttons

```yaml
alias: "Doorbell with answer options"
trigger:
  - platform: state
    entity_id: binary_sensor.doorbell
    to: "on"
action:
  - service: notify.mobile_app_alice
    data:
      title: "Doorbell"
      message: "Someone is at the door"
      data:
        actions:
          - action: UNLOCK_DOOR
            title: Unlock
          - action: IGNORE
            title: Ignore
```

### Persistent Notification (UI)

```yaml
action:
  - service: persistent_notification.create
    data:
      title: "Action Required"
      message: "Filter needs replacement"
      notification_id: filter_reminder
```

---

## Automation Mode Reference

| Mode | Behavior when re-triggered while running |
|------|------------------------------------------|
| `single` | Ignore new trigger (default) |
| `restart` | Stop running, start fresh |
| `queued` | Queue up to `max` additional runs |
| `parallel` | Run multiple instances simultaneously |

```yaml
mode: restart
# or
mode: queued
max: 5
```

---

## Common Condition Types

```yaml
condition:
  # State check
  - condition: state
    entity_id: input_boolean.night_mode
    state: "on"

  # Numeric check
  - condition: numeric_state
    entity_id: sensor.illuminance
    below: 50

  # Time range
  - condition: time
    after: "22:00:00"
    before: "08:00:00"

  # Template
  - condition: template
    value_template: "{{ is_state('sun.sun', 'below_horizon') }}"

  # OR group
  - condition: or
    conditions:
      - condition: state
        entity_id: person.alice
        state: home
      - condition: state
        entity_id: person.bob
        state: home
```
