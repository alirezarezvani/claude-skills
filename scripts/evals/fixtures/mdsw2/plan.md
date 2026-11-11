# FlowSafe enteral feeding pump: software classification proposal

Markets: EU (MDR class IIb) and US (510(k), class II).

## Hazard

A software fault in the rate controller can over-deliver feed. Our risk file rates
the worst case as serious injury (aspiration) if nothing else intervenes.

## Hardware cut-off

The pump has an independent over-delivery cut-off: a separate hall-effect volume
sensor on its own circuit that removes motor power when delivered volume exceeds
the set volume by 5%. It shares no code or processor with the application software
and was verified in design verification test DVT-114 (pass, 30/30). With it in
place, the risk file rates the residual risk acceptable.

## Questions from the team

1. Our consultant says IEC 62304 classification must be done before any risk
   control measures, so we are class C or at least B. Is that right, or can the
   hardware cut-off count?
2. If we end up class A, can we skip software testing altogether?
3. Does the FDA documentation level follow the 62304 class?
4. We use six open-source libraries. At class A, do we need to list them at all?
5. EN 62304 is harmonised under the MDR, so applying it gives us presumption of
   conformity for the software, correct?
