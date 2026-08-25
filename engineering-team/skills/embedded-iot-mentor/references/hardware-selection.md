# Hardware selection — datasheet-anchored notes behind the MCU table

The SKILL.md decision table is the fast path. This reference carries the
datasheet-level facts behind it, so recommendations survive a "why that board?"
follow-up and stay checkable against primary sources.

## MCU families — what actually differentiates them

| Family | Anchor facts (from vendor docs) | Pick it when |
|---|---|---|
| **ESP32 family** (ESP32, -S3, -C3) | Wi-Fi + BLE on chip; -S3 adds vector instructions for edge inference; -C3 is RISC-V single-core for cost-down. Deep-sleep current ~10 µA class (ESP32-S3 datasheet §Electrical Characteristics). First-class ESPHome/Arduino/ESP-IDF support. | Wi-Fi-connected sensing/actuation, Home Assistant integration, fastest firmware-reuse path. |
| **Raspberry Pi Pico W** (RP2040 + CYW43439) | Dual M0+ @133 MHz, 264 KB SRAM, PIO state machines for cycle-accurate custom I/O (RP2040 datasheet ch. 3). No hardware crypto acceleration. MicroPython/C SDK. | Custom protocol bit-banging (PIO), education, tight-budget Wi-Fi nodes. |
| **STM32 series** (F0/F4/L4/H7 …) | Broadest peripheral + package range; L-series shutdown current down to ~30 nA class (STM32L4 datasheet); mature HAL/LL + CubeMX codegen; industrial temperature grades. | Battery-first designs, motor control, anything headed to a certified/industrial product. |
| **nRF52 / nRF53** (Nordic) | BLE 5.x leader; sub-µA system-off retention current (nRF52840 PS §Power); SoftDevice/Zephyr stacks; strong DFU story. | BLE-first wearables/beacons, coin-cell budgets, Thread/Matter-over-Thread experiments. |

## Toolchain notes

- **ESPHome / Tasmota / WLED / Meshtastic** — configuration-first firmware; the reuse-first doctrine's step 1. ESPHome docs list supported sensors; if the sensor is listed, firmware cost ≈ zero.
- **PlatformIO** — one build system across all four families; pins toolchain versions in `platformio.ini`, which is what makes a hobby repo reproducible a year later.
- **Zephyr RTOS** — Nordic's first-class path and the vendor-neutral industrial default; steeper ramp, pays off at product stage.

## Power-budget arithmetic (the part most projects skip)

Battery life ≈ capacity (mAh) ÷ average current (mA). Average current for a
duty-cycled sensor node = (t_active × I_active + t_sleep × I_sleep) ÷ period.
A 2500 mAh cell with 5 s @ 80 mA every 10 min and ~10 µA sleep averages
≈ 0.68 mA → roughly 5 months. Radio choice dominates I_active; sleep current
dominates everything past ~15-minute reporting intervals — which is why the
deep-sleep figures in the table above, not CPU speed, decide battery designs.

## Sources

1. Espressif — *ESP32-S3 Series Datasheet* and *ESP-IDF Programming Guide* (docs.espressif.com) — radio/power figures and supported-peripheral matrix.
2. Raspberry Pi — *RP2040 Datasheet* (datasheets.raspberrypi.com), ch. 3 "PIO" — the programmable-I/O capability the Pico row leans on.
3. STMicroelectronics — *STM32L4 Series Datasheet* + AN4746 low-power application note (st.com) — stop/shutdown-mode current classes and wake latency.
4. Nordic Semiconductor — *nRF52840 Product Specification* (infocenter.nordicsemi.com) — system-off retention currents and BLE stack architecture.
5. ESPHome documentation (esphome.io) — the supported-components index used by the firmware-reuse-first step.
6. PlatformIO documentation (docs.platformio.org) — cross-family builds and version pinning.
7. Zephyr Project documentation (docs.zephyrproject.org) — supported-boards catalog and power-management subsystem.
