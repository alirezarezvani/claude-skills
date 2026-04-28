---
name: "embedded-systems-engineer"
description: "Use when the user asks to write firmware for microcontrollers (ARM Cortex-M, STM32, ESP32, AVR), implement RTOS tasks with FreeRTOS or Zephyr, design hardware interfaces (I2C, SPI, UART, CAN), optimize for resource constraints, or debug embedded systems."
---

# Embedded Systems Engineer

## Overview

Elite firmware development skill for resource-constrained embedded systems. Covers bare-metal and RTOS programming (FreeRTOS, Zephyr), ARM Cortex-M / STM32 / ESP32 microcontrollers, hardware protocols, power optimization, and field debugging.

## Core Competencies

### Microcontroller Platforms
- **ARM Cortex-M**: M0/M3/M4/M7 core features, NVIC, SysTick, MPU
- - **STM32**: HAL/LL drivers, CubeMX configuration, HRTIM, ADC, DMA
  - - **ESP32**: FreeRTOS integration, WiFi/BLE stack, deep sleep modes
    - - **AVR/PIC**: Legacy 8-bit patterns; migrating to ARM
     
      - ### RTOS — FreeRTOS & Zephyr
      - - **Tasks**: Priority-based preemptive scheduling; stack sizing
        - - **Synchronization**: Mutex (priority inheritance), Semaphore, EventGroup
          - - **Communication**: Queue, StreamBuffer, MessageBuffer; Zbus for Zephyr
            - - **Power**: Tickless idle, device PM suspend/resume, sleep states
              - - **Zephyr-Specific**: Devicetree, Kconfig, West workspace, SMF state machines
               
                - ### Hardware Interfaces
                - - **I2C**: Master/slave; clock stretching; multi-master arbitration
                  - - **SPI**: CPOL/CPHA modes; DMA transfers; chip select management
                    - - **UART**: Baud rate config; DMA circular buffer; hardware flow control
                      - - **CAN/CAN-FD**: Frame types, filters, error handling; ISO-TP
                        - - **USB**: CDC-ACM, HID device classes; DFU for firmware updates
                         
                          - ### Memory & Resource Management
                          - - **Static allocation only**: No malloc in production firmware
                            - - **Memory pools**: Fixed-size blocks for predictable heap-like usage
                              - - **Stack analysis**: uxTaskGetStackHighWaterMark; worst-case estimation
                                - - **Flash optimization**: Const data in ROM; XIP configuration
                                  - - **DMA**: Free CPU during data transfers; double-buffer patterns
                                   
                                    - ### Debugging & Diagnostics
                                    - - **JTAG/SWD**: GDB + OpenOCD; breakpoints, watchpoints, live variables
                                      - - **UART logging**: Compile-time log levels; deferred logging for speed
                                        - - **Circular trace buffer**: Overwrites old entries; post-mortem analysis
                                          - - **LED blink codes**: Error state indication in field deployments
                                            - - **Core dumps**: Zephyr core dump for crash analysis
                                             
                                              - ## Design Hierarchy
                                             
                                              - ```
                                                1. Resource Constraints  -> RAM/flash budget; power budget
                                                2. Real-Time Requirements-> Hard deadlines; interrupt latency
                                                3. Reliability & Safety  -> Watchdog; fail-safe states; CRC checks
                                                4. Debuggability         -> JTAG; UART log; trace buffers; assert macros
                                                5. Hardware Abstraction  -> HAL layer; BSP; driver layer separation
                                                ```

                                                ## Decision Framework

                                                | Gate | Question | Action |
                                                |------|----------|--------|
                                                | Platform | MCU family and constraints? | Choose HAL/LL vs register direct |
                                                | OS | Bare-metal or RTOS? | FreeRTOS if >2 tasks; Zephyr for connectivity |
                                                | Memory | RAM available for RTOS overhead? | FreeRTOS ~10KB; Zephyr ~20KB minimum |
                                                | Power | Battery-powered? | Tickless idle + device PM |
                                                | Safety | ASIL or IEC 62304? | Add to automotive-embedded or misra-automotive-c skill |
                                                | Debug | Production or development build? | Strip logs; enable asserts; size optimize |

                                                ## Zephyr RTOS Key Patterns

                                                ### Devicetree Node
                                                ```dts
                                                /* Board overlay for STM32 UART */
                                                &usart1 {
                                                    status = "okay";
                                                    current-speed = <115200>;
                                                    pinctrl-0 = <&usart1_tx_pa9 &usart1_rx_pa10>;
                                                };
                                                ```

                                                ### FreeRTOS Task
                                                ```c
                                                static void SensorTask(void *pvParameters)
                                                {
                                                    TickType_t xLastWake = xTaskGetTickCount();
                                                    for (;;) {
                                                        Sensor_Sample();
                                                        vTaskDelayUntil(&xLastWake, pdMS_TO_TICKS(10U));
                                                    }
                                                }
                                                /* Stack and priority */
                                                xTaskCreate(SensorTask, "Sensor", 256U, NULL, 3U, NULL);
                                                ```

                                                ### Zephyr Thread
                                                ```c
                                                K_THREAD_DEFINE(sensor_tid, 1024,
                                                                sensor_thread_fn, NULL, NULL, NULL,
                                                                5, 0, 0);
                                                ```

                                                ### ISR-Safe Queue Send
                                                ```c
                                                /* From ISR: use FromISR variant */
                                                BaseType_t xHigherPriorityTaskWoken = pdFALSE;
                                                xQueueSendFromISR(xEventQueue, &event, &xHigherPriorityTaskWoken);
                                                portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
                                                ```

                                                ## Troubleshooting

                                                | Problem | Cause | Solution |
                                                |---------|-------|----------|
                                                | Stack overflow | Undersized task stack | Increase stack; check high-water mark |
                                                | Priority inversion | Mutex held by low-priority task | Use priority-inheritance mutex |
                                                | Spurious ISR | Interrupt not cleared | Clear pending flag first in ISR |
                                                | DMA transfer corrupt | Cache coherency | Flush/invalidate D-cache around DMA buffers |
                                                | Watchdog reset loop | Main task blocked | Refresh WDT only from main loop |
                                                | I2C hang | Missing STOP condition | Software reset I2C peripheral |
                                                | ESP32 crash | Stack overflow or heap fragmentation | Increase stack; use static allocation |

                                                ## Power Optimization

                                                | Technique | Saving | Notes |
                                                |-----------|--------|-------|
                                                | Tickless idle | 30–60% | Disable SysTick during idle |
                                                | Clock gating | 10–20% | Disable unused peripheral clocks |
                                                | Voltage scaling | 20–40% | Reduce Vcore at low frequencies |
                                                | Deep sleep | 90%+ | Retain RAM; GPIO wakeup |
                                                | DMA vs CPU copy | 5–15% | Free CPU for sleep during transfers |

                                                ## Cross-References

                                                - **automotive-embedded** — MISRA/AUTOSAR/ISO 26262 for safety-critical automotive firmware
                                                - - **misra-automotive-c** — live MISRA C:2012 code review for embedded C
                                                  - - **ci-cd-pipeline-builder** — automate firmware builds, unit tests, and HIL in CI
                                                    - - **autocad-expert** — hardware enclosure and PCB layout documentation
