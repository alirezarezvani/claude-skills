# Logging Change Pre-Flight

Before recommending any change to log configuration (enabling TCP syslog, increasing log verbosity, switching from batch to stream delivery), validate the following pre-conditions. A logging change on a firewall under load can cause measurable performance degradation.

| Pre-Flight Check | Threshold | Action if Threshold Exceeded |
|---|---|---|
| Current firewall CPU utilization | Below 60% under current load | If CPU > 60%: recommend buffered TCP syslog with rate limit, not unbounded real-time push |
| Current EPS (events per second) baseline | Below 80% of SIEM rated capacity | If near capacity: verify SIEM ingestion headroom before enabling continuous push |
| SIEM ingestion architecture | Real-time capable (agent-based or streaming) | If SIEM uses batch poll by design: switching to push requires SIEM collector reconfiguration, not just firewall-side change |
| TCP syslog vs UDP syslog trade-off | TCP adds per-message acknowledgment overhead | For high-EPS firewalls (>10,000 EPS), this overhead must be modeled against CPU budget |
| Disk buffer on firewall | Sufficient to absorb burst without dropping logs | If flash storage is near capacity, enabling verbose logging can cause log drops and fill storage |

All five pre-flight checks must be included in the logging change intent block as `prerequisite_checks`. If any check cannot be validated, flag it as `UNVERIFIED` and escalate to the SIEM operations team before recommending the change.
