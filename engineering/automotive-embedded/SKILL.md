---
name: "automotive-embedded"
description: "Use when the user asks to write safety-critical automotive embedded C/C++ code, apply MISRA C:2012 or AUTOSAR C++14 guidelines, implement ISO 26262 functional safety, work with CAN/LIN/Ethernet protocols, write CAPL scripts for CANoe, or configure RTOS tasks for vehicle ECUs."
---

# Automotive Embedded C/C++

## Overview

A comprehensive skill for AI-assisted development of safety-critical automotive embedded software. Covers MISRA C:2012, AUTOSAR C++14, ISO 26262 functional safety, ISO 21434 cybersecurity, CAN/LIN/Ethernet protocols, RTOS patterns, and Vector CANoe/CAPL toolchain.

## Core Competencies

### Coding Standards
- **MISRA C:2012**: Mandatory, required, and advisory rules for safety-critical C
- - **AUTOSAR C++14**: Adaptive platform guidelines for modern C++ in vehicles
  - - **CERT C**: Secure coding to prevent memory corruption and undefined behavior
    - - **Rule Enforcement**: Static analysis integration (PC-lint, Polyspace, Coverity, LDRA)
     
      - ### Functional Safety — ISO 26262
      - - **ASIL Decomposition**: Assign ASIL A–D to software components based on hazard analysis
        - - **Safety Architecture**: Freedom from interference; software component independence
          - - **Safe State Design**: Define safe state transitions for fault reactions
            - - **Diagnostic Coverage**: Fault detection and handling; watchdog patterns
              - - **SW-C Design**: AUTOSAR Software Component modeling for safety-critical functions
               
                - ### Cybersecurity — ISO 21434
                - - **Secure Coding**: Input validation, bounds checking, integer overflow prevention
                  - - **Key Management**: Hardware Security Module (HSM) integration patterns
                    - - **Secure Boot**: Trust chain verification for ECU firmware
                      - - **Attack Surface Reduction**: Minimal interfaces; disable unused communication stacks
                       
                        - ### RTOS & Real-Time Patterns
                        - - **Task Design**: Fixed-priority preemptive scheduling; AUTOSAR OS tasks
                          - - **Timing Constraints**: Worst-case execution time (WCET) analysis and deadlines
                            - - **Resource Management**: Mutex, semaphore, event flag usage; priority inversion prevention
                              - - **Memory Protection**: MPU configuration; stack overflow detection
                                - - **Interrupt Handling**: ISR design rules; deferred processing patterns
                                 
                                  - ### Communication Protocols
                                  - - **CAN**: Frame types, arbitration, error handling; Classic CAN and CAN FD
                                    - - **LIN**: Master/slave schedule tables; diagnostic frames
                                      - - **Automotive Ethernet**: DoIP, SOME/IP service discovery, AVB/TSN
                                        - - **UDS (ISO 14229)**: Diagnostic services; session management; security access
                                          - - **XCP**: Calibration and measurement protocol for A2L/DBC integration
                                           
                                            - ### Vector CANoe / CAPL
                                            - - **CAPL Scripts**: Event-driven simulation nodes; message handlers; timer events
                                              - - **Test Automation**: vTESTstudio test cases; CAPL test modules
                                                - - **DBC Files**: Message and signal definitions; value tables
                                                  - - **Diagnostic Sessions**: UDS test sequences in CAPL
                                                    - - **Measurement & Calibration**: XCP/A2L integration; signal panel configuration
                                                     
                                                      - ## Decision Framework
                                                     
                                                      - | Gate | Question | Action |
                                                      - |------|----------|--------|
                                                      - | ASIL Level | What is the ASIL target (A/B/C/D)? | Apply appropriate safety architecture |
                                                      - | Language | C or C++? | Apply MISRA C:2012 or AUTOSAR C++14 |
                                                      - | OS | Bare-metal or RTOS (AUTOSAR OS / FreeRTOS)? | Choose task/ISR patterns accordingly |
                                                      - | Protocol | CAN, LIN, or Ethernet? | Select appropriate driver and stack |
                                                      - | Toolchain | GCC, Green Hills, TASKING, or IAR? | Configure compiler flags and linker |
                                                      - | Analysis | PC-lint, Polyspace, Coverity, or LDRA? | Set up rule configuration file |
                                                     
                                                      - ## MISRA C:2012 Key Rules
                                                     
                                                      - | Rule | Category | Description |
                                                      - |------|----------|-------------|
                                                      - | Dir 1.1 | Required | Any implementation-defined behavior shall be documented |
                                                      - | Rule 1.3 | Required | No undefined behavior |
                                                      - | Rule 2.1 | Required | A project shall not contain unreachable code |
                                                      - | Rule 8.4 | Required | Compatible declaration for every function with external linkage |
                                                      - | Rule 10.1 | Required | Operands of inappropriate essential type |
                                                      - | Rule 11.3 | Required | No cast between pointer to object and pointer to different type |
                                                      - | Rule 14.4 | Required | Controlling expression of if/loop must be Boolean |
                                                      - | Rule 15.5 | Advisory | A function should have a single point of exit |
                                                      - | Rule 17.7 | Required | Return value of non-void function must be used |
                                                     
                                                      - ## Code Patterns
                                                     
                                                      - ### Safe State Machine
                                                      - ```c
                                                        typedef enum {
                                                            STATE_INIT,
                                                            STATE_NORMAL,
                                                            STATE_FAULT,
                                                            STATE_SAFE
                                                        } EcuState_t;

                                                        static EcuState_t currentState = STATE_INIT;

                                                        void ECU_HandleFault(void) {
                                                            /* Transition to SAFE state on any unrecoverable fault */
                                                            currentState = STATE_SAFE;
                                                            /* Disable actuators, set safe outputs */
                                                            Actuator_DisableAll();
                                                        }
                                                        ```

                                                        ### CAN Receive Handler (MISRA-compliant)
                                                        ```c
                                                        void CAN_RxCallback(uint32_t msgId, const uint8_t *data, uint8_t dlc) {
                                                            if ((data == NULL) || (dlc == 0U)) {
                                                                return; /* Guard: invalid frame */
                                                            }
                                                            if (msgId == SPEED_MSG_ID) {
                                                                vehicleSpeed_kph = (uint16_t)((uint16_t)data[0] | ((uint16_t)data[1] << 8U));
                                                            }
                                                        }
                                                        ```

                                                        ### RTOS Task with Deadline Monitoring
                                                        ```c
                                                        void VehicleControl_Task(void *pvParameters) {
                                                            TickType_t xLastWakeTime = xTaskGetTickCount();
                                                            const TickType_t xPeriod = pdMS_TO_TICKS(10U); /* 10 ms cycle */

                                                            for (;;) {
                                                                SensorData_Read();
                                                                ControlAlgorithm_Execute();
                                                                Actuator_SetOutput();
                                                                vTaskDelayUntil(&xLastWakeTime, xPeriod);
                                                            }
                                                        }
                                                        ```

                                                        ### CAPL Script — CAN Message Handler
                                                        ```capl
                                                        on message 0x100 {
                                                          float speed;
                                                          speed = this.word(0) * 0.1;
                                                          write("Vehicle speed: %.1f km/h", speed);
                                                        }

                                                        on timer periodicTimer {
                                                          message 0x200 reqMsg;
                                                          reqMsg.word(0) = 0x0000;
                                                          output(reqMsg);
                                                          setTimer(periodicTimer, 100); /* restart 100ms timer */
                                                        }
                                                        ```

                                                        ## Static Analysis Configuration

                                                        | Tool | Config File | Key Settings |
                                                        |------|------------|--------------|
                                                        | PC-lint Plus | lnt/au-misra-c.lnt | Enable MISRA 2012 mandatory + required |
                                                        | Polyspace | polyspace.cfg | ASIL B or higher; prove absence of RTE |
                                                        | Coverity | coverity-config.xml | Enable CERT C checkers + misra_c_2012 |
                                                        | LDRA | ldra.cfg | Enable all MISRA required + advisory |

                                                        ## Standards Reference

                                                        | Standard | Scope | Key Parts |
                                                        |----------|-------|-----------|
                                                        | MISRA C:2012 | C coding guidelines | Mandatory, Required, Advisory rules |
                                                        | AUTOSAR C++14 | C++ for adaptive platform | Core type safety, templates, concurrency |
                                                        | ISO 26262:2018 | Functional safety, road vehicles | Parts 4 (system), 6 (SW), 8 (processes) |
                                                        | ISO 21434:2021 | Cybersecurity engineering | Secure development lifecycle, TARA |
                                                        | ISO 14229 (UDS) | Unified Diagnostic Services | Session, security, DTC management |
                                                        | SAE J1939 | Heavy vehicle CAN protocol | PGN definitions, address claiming |

                                                        ## Troubleshooting

                                                        | Problem | Cause | Solution |
                                                        |---------|-------|----------|
                                                        | Stack overflow | Task stack undersized | Increase stack; use uxTaskGetStackHighWaterMark |
                                                        | CAN bus-off | Persistent TX errors | Check termination; verify baud rate; reset CAN controller |
                                                        | MISRA violation flood | Legacy code integrated | Suppress with documented deviations; isolate in wrapper |
                                                        | Polyspace orange check | Unbounded pointer arithmetic | Add array bounds check; use MISRA Rule 18.1 pattern |
                                                        | UDS security access fail | Wrong seed/key algorithm | Verify SecurityAccess plugin config; check byte order |
                                                        | Priority inversion | Mutex held by low-priority task | Use priority inheritance mutex or priority ceiling protocol |

                                                        ## Cross-References

                                                        - **autocad-expert** — CAD schematics and wiring harness drawings for vehicle systems
                                                        - - **spec-driven-workflow** — translate AUTOSAR SWC specifications into code
                                                          - - **ci-cd-pipeline-builder** — integrate static analysis and HIL test into CI pipeline
                                                            - - **database-designer** — store calibration data, DTC definitions, and diagnostic logs
