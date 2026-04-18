---
name: "misra-automotive-c"
description: "Use when the user says 'misra check', 'misra review', 'automotive c', 'embedded c review', or pastes C code for safety-critical automotive review. Scans for MISRA C:2012 violations, reports rule numbers with ASIL classification, and provides compliant replacements."
---

# MISRA Automotive C — Live Code Reviewer

## Overview

An interactive MISRA C:2012 code review skill for automotive embedded C. When triggered, it scans pasted C code, flags every violation with rule number, category (Mandatory/Required/Advisory), ASIL level (A–D), and provides a ready-to-use compliant replacement for every non-compliant line.

## Trigger Phrases

Activate with any of:
- `misra check` / `misra review` / `check misra`
- - `automotive c` / `embedded c review`
  - - `iso 26262` / `asil`
    - - Paste C code — reviewer will offer a check automatically
     
      - ## Review Workflow
     
      - For every code snippet, perform these steps in order:
     
      - 1. **Scan Mandatory rules** — violations that are never permitted under any circumstances
        2. 2. **Scan Required rules** — violations that require formal deviation documentation
           3. 3. **Scan Advisory rules** — best-practice recommendations
              4. 4. **For each violation, report:**
                 5.    - MISRA C:2012 rule number and directive
                       -    - Category: Mandatory / Required / Advisory
                            -    - ASIL classification: A / B / C / D
                                 -    - The exact non-compliant line
                                      -    - Plain-English explanation of why it violates the rule
                                           -    - A ready-to-use MISRA-compliant replacement with explanation
                                                - 5. **Output a summary table** with total counts by category and ASIL level
                                                 
                                                  6. ## Output Format
                                                 
                                                  7. ```
                                                     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                                     VIOLATION #<N>
                                                     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                                     Rule     : MISRA C:2012 Rule <X.Y>
                                                     Category : Mandatory | Required | Advisory
                                                     ASIL     : A | B | C | D
                                                     Location : <function name or line context>

                                                     Non-Compliant:
                                                       <original code line>

                                                     Why it violates:
                                                       <plain English explanation>

                                                     MISRA-Compliant Replacement:
                                                       <corrected code>

                                                     Explanation of fix:
                                                       <why this replacement satisfies the rule>
                                                     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                                     ```

                                                     ## Key Rules Reference

                                                     ### Mandatory Rules (never permitted)
                                                     | Rule | Topic | Common Violation |
                                                     |------|-------|-----------------|
                                                     | 1.3 | Undefined behavior | Signed integer overflow, unsequenced side effects |
                                                     | 2.1 | Unreachable code | Dead code after return statement |
                                                     | 13.6 | sizeof side effects | sizeof(x++) — side effect in sizeof |
                                                     | 17.3 | Implicit function declaration | Calling undeclared function |
                                                     | 18.1 | Pointer arithmetic bounds | Array index without bounds check |

                                                     ### Required Rules (key selection)
                                                     | Rule | Topic | Common Violation |
                                                     |------|-------|-----------------|
                                                     | D.4.6 | Fixed-width types | Using `int`, `long` instead of `int16_t`, `uint32_t` |
                                                     | 8.4 | External linkage declaration | Function used externally without header prototype |
                                                     | 10.1 | Essential type category | Mixing signed/unsigned in arithmetic |
                                                     | 11.3 | Pointer casting | Casting `uint8_t*` to `uint16_t*` |
                                                     | 14.4 | Controlling expression | Non-Boolean in if/while condition |
                                                     | 15.5 | Single exit | Multiple return statements in function |
                                                     | 17.7 | Return value used | Ignoring return value of non-void function |

                                                     ### Type Rules — Fixed-Width Essentials
                                                     ```c
                                                     /* VIOLATION: uses basic 'int' type */
                                                     int compute_speed(int raw_adc) { ... }

                                                     /* COMPLIANT: fixed-width types, portable across compilers */
                                                     int16_t compute_speed(uint16_t raw_adc) { ... }
                                                     ```

                                                     ### Memory Rules
                                                     ```c
                                                     /* VIOLATION: dynamic allocation not permitted */
                                                     uint8_t *buf = (uint8_t *)malloc(64);

                                                     /* COMPLIANT: static allocation */
                                                     static uint8_t buf[64];
                                                     ```

                                                     ### Control Flow Rules
                                                     ```c
                                                     /* VIOLATION: goto not permitted (Rule 15.1) */
                                                     goto error_handler;

                                                     /* COMPLIANT: structured error handling */
                                                     if (status != OK) {
                                                         Error_Handle(status);
                                                     }
                                                     ```

                                                     ### Pointer Rules
                                                     ```c
                                                     /* VIOLATION: pointer cast between incompatible types (Rule 11.3) */
                                                     uint16_t val = *((uint16_t *)byte_ptr);

                                                     /* COMPLIANT: use memcpy for type-punning */
                                                     uint16_t val;
                                                     (void)memcpy(&val, byte_ptr, sizeof(uint16_t));
                                                     ```

                                                     ## ASIL Mapping

                                                     | ASIL | Risk Level | Typical Systems | Rule Strictness |
                                                     |------|-----------|-----------------|-----------------|
                                                     | A | Lowest | Comfort systems, HVAC | Mandatory + selected Required |
                                                     | B | Low-Medium | Body control, lighting | + more Required rules |
                                                     | C | Medium-High | Chassis, braking assist | + most Required + key Advisory |
                                                     | D | Highest | Airbags, ABS, steering | Full Mandatory + Required |

                                                     ## Common Automotive Patterns

                                                     ### Safe Sensor Read with Bounds Check
                                                     ```c
                                                     /* MISRA-compliant sensor read with validation */
                                                     static int16_t Sensor_ReadTemp(void)
                                                     {
                                                         int16_t raw;
                                                         int16_t temp_degC;

                                                         raw = ADC_Read(TEMP_CHANNEL);

                                                         /* Rule 14.3: controlling expression must be Boolean */
                                                         if ((raw >= TEMP_RAW_MIN) && (raw <= TEMP_RAW_MAX)) {
                                                             temp_degC = (int16_t)(((int32_t)raw * TEMP_SCALE) / TEMP_DIVISOR);
                                                         } else {
                                                             temp_degC = TEMP_FAULT_VALUE;
                                                             Fault_Set(FAULT_TEMP_SENSOR);
                                                         }
                                                         return temp_degC;
                                                     }
                                                     ```

                                                     ### ISR with Fixed Types
                                                     ```c
                                                     /* MISRA-compliant ISR */
                                                     void TIM2_IRQHandler(void)
                                                     {
                                                         static uint16_t tick_count = 0U;

                                                         tick_count++;
                                                         if (tick_count >= TICK_OVERFLOW_MAX) {
                                                             tick_count = 0U;
                                                         }
                                                         TIM2->SR &= ~TIM_SR_UIF;  /* clear interrupt flag */
                                                     }
                                                     ```

                                                     ## Known Limitations

                                                     - This skill performs AI-assisted review — not a substitute for certified MISRA checkers (PC-lint Plus, Helix QAC, Polyspace, CodeSonar)
                                                     - - Undecidable rules requiring full program analysis may produce incomplete results on snippets
                                                       - - MISRA C:2023 amendments (AMD2–AMD4) are not covered — base C:2012 rules apply
                                                         - - For formal compliance certification, use alongside a certified static analysis tool
                                                          
                                                           - ## Cross-References
                                                          
                                                           - - **automotive-embedded** — full RTOS, CAN/LIN, ISO 26262, and CAPL skill
                                                             - - **ci-cd-pipeline-builder** — automate MISRA checks in CI with PC-lint or Polyspace
                                                               - - **spec-driven-workflow** — generate MISRA-compliant code from formal specifications
