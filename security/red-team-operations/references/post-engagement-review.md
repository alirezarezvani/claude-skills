# Post-Incident Review Questions

1. Did the C2 infrastructure remain undetected for the duration of the engagement? If it was detected, at which phase and what indicator triggered the detection?
2. Were the selected lateral movement techniques appropriate for the environment? Which techniques produced unexpected artifacts that increased detection risk?
3. Did the OPSEC plan hold throughout the operation, or were there deviations? What caused the deviations?
4. Were all IOCs accounted for in the pre-operation IOC management plan, or did the operation generate unexpected indicators?
5. Did the exfiltration staging work as designed? Were data volume and transfer rate limits respected?
6. Were all C2 components taken offline cleanly at engagement conclusion? Is the kill switch procedure sufficient?
7. Were findings pushed to findings-tracker in real time, or were there gaps in finding documentation?
8. What would the operation have looked like if conducted by an actual threat actor with no safety constraints? Where did red team operational constraints create unrealistic conditions?
