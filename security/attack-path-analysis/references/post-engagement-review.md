# Post-Incident Review Questions

1. Did the attack paths identified pre-engagement match the paths actually taken during the red team operation? What was the accuracy rate of the path scoring model?
2. Were all choke points identified correctly? Were any critical choke points missed that, if hardened, would have blocked the actual attack path?
3. Did the cloud and hybrid path analysis surface any findings that were not identified by traditional on-premises AD analysis?
4. Were there paths discovered during execution that were not in the pre-engagement graph? What data gaps caused the missed paths?
5. Did the hardening recommendations accurately represent the remediation effort? Were any recommendations found to be impractical?
6. How did the blast radius of the actual compromise compare to the path analysis prediction? Was the impact assessment accurate?
7. Were entry point assumptions validated by the engagement results? Should the entry point model be revised?
8. Did the scoring model correctly rank the path that was actually exploited as a high-scoring path?
