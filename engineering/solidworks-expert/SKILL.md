---
name: "solidworks-expert"
description: "Use when the user asks to model parts or assemblies in SolidWorks, create engineering drawings with GD&T, design sheet metal flat patterns, run FEA simulation, export STEP/IGES/STL, or troubleshoot SolidWorks rebuild errors."
---

# SolidWorks Expert

## Overview

Parametric 3D CAD skill for SolidWorks: part modeling, assembly design, engineering drawings, sheet metal, weldments, and FEA simulation. Follows ASME Y14.5-2018 for GD&T and supports DFM guidance.

## Core Competencies

### Part Modeling
- Extrude, Revolve, Sweep, Loft, Shell, Rib features
- - Fillet, Chamfer, Draft, Hole Wizard, Thread
  - - Fully constrained sketches with design intent
    - - Configurations and Design Tables for parametric variants
     
      - ### Assembly Design
      - - Bottom-up (parts first) and top-down (in-context) workflows
        - - Mates: Coincident, Concentric, Distance, Angle, Gear, Cam, Slot
          - - Interference Detection; Large Assembly Mode with SpeedPak
           
            - ### Engineering Drawings
            - - Views: Front, Top, Section, Detail, Broken-out, Isometric
              - - GD&T per ASME Y14.5-2018: form, orientation, location, runout
                - - Auto-generated Bill of Materials; title block linked to properties
                 
                  - ### Sheet Metal
                  - - Base Flange, Edge Flange, Miter Flange, Hem
                    - - Flat Pattern with bend lines for laser/punch
                      - - K-Factor and bend allowance tables
                       
                        - ### Simulation (COSMOSWorks / Simulation)
                        - - Static FEA: Von Mises stress, displacement, factor of safety
                          - - Thermal: temperature distribution, heat flux
                            - - Frequency: natural frequencies and mode shapes
                              - - Curvature-based mesh with refinement at stress concentrations
                               
                                - ## Decision Framework
                               
                                - | Gate | Question | Action |
                                - |------|----------|--------|
                                - | Scope | Single part, assembly, or drawing? | Choose document type |
                                - | Approach | Bottom-up or top-down? | Define assembly strategy |
                                - | Output | Prototype, production, mold/tooling? | Select manufacturing method |
                                - | Format | SW native, STEP, IGES, or STL? | Plan export strategy |
                                - | Tolerance | Fit critical? | Apply GD&T per ASME Y14.5 |
                               
                                - ## Workflow
                               
                                - ```
                                  Concept       -> Constrained 2D sketch with dimensions
                                  Part Design   -> Base feature + dependent features
                                  Validation    -> Interference check, mass properties, FEA
                                  Assembly      -> Mates; top-down for contextual parts
                                  Documentation -> Drawings with dims, tolerances, BOM, notes
                                  Mfg Prep      -> Sheet metal flat patterns; mold tooling
                                  Release       -> PDM check-in; STEP/PDF export
                                  ```

                                  ## Troubleshooting

                                  | Problem | Cause | Solution |
                                  |---------|-------|----------|
                                  | Rebuild fails | Over-constrained sketch | Rollback bar; fix sketch first |
                                  | Mate won't apply | Components misaligned | Move closer; use SmartMates |
                                  | Fillet fails | Edge radius too small | Variable Radius Fillet |
                                  | Large assembly slow | Too many loaded parts | Large Assembly Mode; SpeedPak |
                                  | Drawing dims wrong | View misaligned | Orient view; verify ref geometry |
                                  | Missing material | Custom material absent | Add to custom library |

                                  ## Interoperability

                                  | Format | Use Case |
                                  |--------|----------|
                                  | STEP AP214 | Neutral 3D exchange with any CAD |
                                  | IGES | Legacy CAD interchange |
                                  | STL | 3D printing and prototyping |
                                  | DXF/DWG | 2D drawing exchange with AutoCAD |
                                  | Parasolid | Native kernel for NX and Solid Edge |
                                  | 3D PDF | Review without CAD license |

                                  ## Cross-References

                                  - **autocad-expert** — 2D DWG layout drawings and wiring harness documentation
                                  - - **automotive-embedded** — ECU and sensor housing mechanical packaging
                                    - - **spec-driven-workflow** — requirements-driven mechanical design
