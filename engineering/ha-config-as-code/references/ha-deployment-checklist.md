# Home Assistant Config-as-Code Deployment Checklist

Use this checklist for first-time setup, migration to a new host, or major configuration changes.

---

## Pre-Deployment

- [ ] HA instance is running and accessible (`python3 scripts/ha_api.py ping`)
- [ ] Long-lived access token created and set in `.env`
- [ ] `.env` is in `.gitignore` — never committed
- [ ] All entity ID constants updated in scripts to match this home's devices
- [ ] Git working tree is clean — commit before starting (`git status`)
- [ ] Optional: snapshot/backup taken in HA UI (Settings → System → Backups)

---

## Layer 1: Device Switches

```bash
python3 scripts/setup_wireless_switches.py --set-wireless
```

- [ ] All physical switches set to wireless mode
- [ ] Verify in HA: switch buttons no longer trigger device directly

```bash
python3 scripts/setup_wireless_switches.py --cleanup
```

- [ ] Old on/off toggle automations removed

```bash
python3 scripts/setup_wireless_switches.py --bind
```

- [ ] New event-based button automations created
- [ ] Entity display names/icons updated

**Rollback:** Manually set switches back to wired mode via device app or HA integration settings.

---

## Layer 2: Scenes

```bash
python3 scripts/setup_scenes.py
```

- [ ] Guest scene created
- [ ] Cinema scene created
- [ ] Sleep scene created
- [ ] Scenes reloaded (`scene.reload`)
- [ ] Display names and icons set in entity registry

**Verify:**
```bash
python3 scripts/ha_entity_lister.py --domain scene
```

**Rollback:** Delete unwanted scenes via HA UI (Helpers → Scenes).

---

## Layer 3: Automations

```bash
python3 scripts/setup_automations.py
```

- [ ] Environment automations deployed (temperature, humidity, CO2)
- [ ] Safety automations deployed (smoke, water, door)
- [ ] Presence automations deployed (home/away)
- [ ] Helper input_boolean/input_select entities created
- [ ] Automations visible and enabled in HA UI

**Diff check:**
```bash
python3 scripts/ha_automation_diff.py --local automations.yaml
```

**Rollback:** `python3 scripts/ha_api.py` → delete specific automations by alias.

---

## Layer 4: Groups

```bash
python3 scripts/create_groups.py
```

- [ ] Area light groups created (bedroom, living room, kitchen, etc.)
- [ ] Whole-home group created
- [ ] Groups appear in HA Entities list

**Verify:**
```bash
python3 scripts/ha_entity_lister.py --domain light --keyword group
```

**Rollback:** Remove `light_group` entries via HA UI or `helpers` YAML.

---

## Layer 5: Dashboard

```bash
python3 scripts/setup_dashboard.py --theme md3_yellow
```

- [ ] Lovelace config written via WebSocket
- [ ] Dashboard loads correctly in HA UI
- [ ] All cards display without errors
- [ ] Theme applied correctly

**Rollback:** HA UI → Dashboard → Edit → Raw config editor → paste backup JSON.

---

## Layer 6: Adaptive Lighting

```bash
python3 scripts/setup_adaptive_lighting.py
```

- [ ] Per-area adaptive lighting switch entities created
- [ ] Adaptive Lighting HACS integration installed and loaded
- [ ] Circadian curves active for each area

**Verify:**
```bash
python3 scripts/ha_entity_lister.py --keyword adaptive_lighting
```

---

## Layer 7: HomeKit Bridge

```bash
python3 scripts/setup_homekit.py
```

- [ ] HomeKit Bridge integration configured
- [ ] Matter-native devices excluded from bridge
- [ ] Non-Matter devices exposed to Apple Home
- [ ] HomeKit pairing code displayed/noted

**Note:** After running, complete pairing in Apple Home app within 5 minutes.

---

## Layer 8: Power-On Behavior

```bash
python3 scripts/setup_power_on_state.py
```

- [ ] Power-on select entities discovered
- [ ] All devices set to "memory" or "previous" mode
- [ ] Verify no devices reset to default white on next power cycle

---

## Layer 9: Weather Forecast Sensors

```bash
python3 scripts/setup_weather_forecast.py
```

- [ ] SSH connection to HA host successful
- [ ] Template sensor YAML written to `/homeassistant/`
- [ ] Templates reloaded in HA
- [ ] Forecast sensor entities appear (`sensor.forecast_*`)

**Prerequisites:** `sshpass` installed locally, SSH+sudo access to HA host.

---

## Post-Deployment Validation

```bash
# Full validation run
python3 scripts/ha_config_validator.py

# Check for unavailable entities
python3 scripts/ha_entity_lister.py --state unavailable

# Final git commit
git add -p
git commit -m "chore: apply HA configuration deployment $(date +%Y-%m-%d)"
```

- [ ] `ha_config_validator.py` passes with 0 failures
- [ ] No critical entities in `unavailable` state
- [ ] Git commit made with deployment notes
- [ ] HA UI verified: automations, scenes, dashboard all working
- [ ] Physical test: walk through each room, press each switch

---

## Rollback Procedure

### Full rollback from HA backup:
1. Settings → System → Backups
2. Select pre-deployment backup
3. Restore

### Partial rollback (specific script):
1. Identify which script introduced the issue
2. Manually reverse changes via HA UI or API
3. Run the corrected script version

### Git-based rollback:
```bash
git log --oneline -10           # find the commit to revert to
git diff HEAD~1 HEAD            # review what changed
git stash                       # or checkout specific files
```

---

## Migration to New HA Host

1. Install HA on new host
2. Install all required HACS integrations and frontend cards
3. Copy `.env` and update `HA_URL` and `HA_SSH_HOST`
4. Run full deployment in layer order
5. Re-pair HomeKit in Apple Home app
6. Re-pair any Bluetooth/Zigbee devices if needed

---

## Recurring Maintenance

| Task | Frequency | Command |
|------|-----------|---------|
| Validate entity health | Weekly | `ha_config_validator.py` |
| Check unavailable devices | Weekly | `ha_entity_lister.py --state unavailable` |
| Diff automations vs code | After HA update | `ha_automation_diff.py` |
| Rotate HA token | Quarterly | Update `.env` and re-run scripts |
| Backup HA config | Monthly | HA UI → Backups |
