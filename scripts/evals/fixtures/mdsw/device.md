# InfuSmart P2 volumetric infusion pump: software overview

Target markets: EU (MDR class IIb) and US (510(k), class II).

## Software system "InfuCore" (runs on the pump's main processor)

| Item | Function | Notes |
|---|---|---|
| DoseEngine | Calculates flow rate from the prescribed dose, drives the motor | A wrong rate can overdose the patient; worst case is death |
| DoseGuard | Re-checks every commanded rate against the drug library limits and stops the motor on a mismatch | Same executable and processor as DoseEngine |
| UI | Touchscreen, alarms display, theme and language settings | Team claims class A ("it only draws screens"); no architecture document yet |
| LogSync | Sends event logs to a nurse tablet app over Bluetooth Low Energy | |

There is also a USB-C service port used for firmware updates.

## SOUP

| Name | Version in register | Notes |
|---|---|---|
| FreeRTOS | latest | No requirements recorded; nobody has read its known-issues list |
| NimBLE (Bluetooth stack) | 1.6.0 | |
| LVGL (graphics) | 8.3.11 | |

Our plan: classify everything as class B because DoseGuard catches dosing errors, keep UI at class A, and submit Basic documentation to FDA.
