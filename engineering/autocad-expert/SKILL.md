---
name: "autocad-expert"
description: "Use when the user asks to create engineering drawings, manage CAD layers, set up dimensions and annotations, work with AutoCAD blocks, configure plot styles, or export DWG/DXF/PDF files."
---

# AutoCAD Expert

## Overview

A comprehensive AutoCAD skill for 2D engineering drafting, layer management, annotation, block creation, and plot-ready output. Covers architectural, mechanical, civil, and electrical disciplines following ASME Y14.5 and ISO 128 standards.

## Core Competencies

### 2D Drafting
- **Geometry Creation**: Lines, polylines, arcs, circles, splines with exact coordinates
- - **Editing Commands**: Trim, extend, offset, fillet, chamfer, array, mirror, stretch
  - - **Coordinate Systems**: World vs User Coordinate System; absolute, relative, polar input
    - - **Object Snaps**: Endpoint, midpoint, center, intersection, perpendicular, tangent
      - - **Precision Drawing**: Ortho, polar tracking, grid snap, object snap tracking
       
        - ### Layer Management
        - - **Layer Standards**: Industry naming (A-WALL-CONSTR, M-PIPE-SUPL, E-POWR-LITE)
          - - **Layer Properties**: Color, linetype, lineweight, plot style, transparency
            - - **Layer States**: Save and restore visibility configs for review sets
              - - **Layer Filters**: Property and group filters for large drawings
                - - **Audit & Cleanup**: Purge unused layers; enforce with CAD Standards Checker
                 
                  - ### Dimensioning & Annotation
                  - - **Dimension Types**: Linear, aligned, angular, radius, diameter, ordinate, baseline
                    - - **GD&T**: Geometric tolerances per ASME Y14.5 using TOLERANCE command
                      - - **Annotative Scaling**: Annotative dimensions and text for automatic viewport scaling
                        - - **Text & Tables**: MTEXT, DTEXT, TABLE; field codes for dynamic values
                          - - **Leaders**: MLEADER with arrowhead styles; standard callout blocks
                           
                            - ### Block Library
                            - - **Static Blocks**: Title blocks, north arrows, section markers, standard symbols
                              - - **Dynamic Blocks**: Parameters and actions for parametric components (doors, valves)
                                - - **Block Attributes**: ATTDEF, ATTEDIT, ATTEXT for automated BOMs and schedules
                                  - - **Xrefs**: Attach, overlay, bind, and reload external references
                                   
                                    - ### Sheet & Plot Setup
                                    - - **Layouts**: Model space vs paper space; multiple layouts per project
                                      - - **Viewports**: MVIEW, VPCLIP, VPLAYER for per-viewport layer overrides
                                        - - **Plot Styles**: CTB (color-dependent) vs STB (named); lineweight mapping
                                          - - **Publish**: Multi-sheet PDF/DWF export via PUBLISH command
                                           
                                            - ## Decision Framework
                                           
                                            - | Gate | Question | Action |
                                            - |------|----------|--------|
                                            - | Discipline | Architecture, mechanical, civil, or electrical? | Apply discipline layer standard |
                                            - | Units | Imperial (inches) or metric (mm)? | Set at file creation with UNITS |
                                            - | Output | PDF, DWF, or physical plot? | Define plot style and page setup |
                                            - | Version | Minimum DWG version required? | SAVEAS to compatible format |
                                            - | Scale | Drawing scale for annotation? | Set annotative scale or DIMSCALE |
                                           
                                            - ## Command Quick Reference
                                           
                                            - | Category | Command | Alias | Purpose |
                                            - |----------|---------|-------|---------|
                                            - | Draw | LINE | L | Create line segments |
                                            - | Draw | POLYLINE | PL | Connected polyline |
                                            - | Draw | CIRCLE | C | Create circle |
                                            - | Edit | TRIM | TR | Trim to boundary |
                                            - | Edit | OFFSET | O | Offset by distance |
                                            - | Edit | ARRAY | AR | Rectangular or polar array |
                                            - | Annotation | DIMLINEAR | DLI | Linear dimension |
                                            - | Annotation | MTEXT | MT | Multiline text |
                                            | Annotation | MLEADER | MLD | Multileader callout |
| Layer | LAYER | LA | Layer Properties Manager |
| Block | BLOCK | B | Define block |
                                   
| Block | INSERT | I | Insert block || Block | XREF | XR | External reference manager |
| Plot | PUBLISH | — | Multi-sheet publish |

## Layer Naming Conventions

| Discipline | Prefix | Example | Content |
|-----------|--------|---------|---------|
| Architecture | A- | A-WALL-CONSTR | Construction walls |
| Mechanical | M- | M-PIPE-SUPL | Supply piping |
| Electrical | E- | E-POWR-LITE | Power/lighting |
| Civil | C- | C-ROAD-CNTR | Road centerlines |
| Structural | S- | S-BEAM-WIDE | Wide flange beams |
| General | G- | G-ANNO-DIMS | Dimensions |

## Risk & Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Objects won't trim | Boundary not co-planar | Check Z elevation; use edge mode |
| Wrong dimension value | Snap to wrong point | Use OSNAP overrides; verify endpoint |
| Plot is blank | Layer frozen or viewport off | Check LAYER visibility; activate viewport |
| Xref not loading | Path broken | XREF RELOAD; verify path and DWG version |
| Hatch invisible | Boundary not closed | Use BOUNDARY to create closed polyline |
| Slow performance | Proxy objects or duplicates | OVERKILL; PURGE unused objects |

## Standard Workflow

```
Standards Setup  -> Set units, layers, dim styles, text styles
Template (DWT)   -> Save preconfigured template for reuse
Drawing          -> Geometry on correct layers with precision
Annotation       -> Dimensions, text, symbols at annotative scale
Blocks           -> Standard symbols; dynamic components
Layout/Plot      -> Viewports, plot style, page setup
Output           -> Publish to PDF/DWF or plot to printer
```

## Related Skills

| Combination | Workflow |
|-------------|----------|
| AutoCAD + Revit | DWG underlays for BIM coordination |
| AutoCAD + Civil 3D | Survey and alignment data exchange |
| AutoCAD + Inventor | 2D drawings from 3D parametric model |
| AutoCAD + SolidWorks | DWG/DXF interchange for mechanical |

## Cross-References

- **automotive-embedded** — embedded C/C++ for vehicle systems using CAD-generated schematics
- - **database-designer** — store drawing metadata, revision history, and BOM data
  - - **spec-driven-workflow** — drive CAD drawing requirements from specifications
