# support-ops

Run a support queue on numbers from a ticket export: SLA attainment on the
clock your contract uses, how many agents each hour needs, and which ticket
topics belong in the help center, in a macro or in engineering's backlog.
Three stdlib Python scripts; no helpdesk API, no credentials.

| Script | Answers |
|---|---|
| `sla_check.py` | Are we meeting first-response and resolution targets in business hours? Which open tickets breach next? |
| `staffing_plan.py` | How many agents per interval for phone and chat (Erlang C) or email (workload), and where is the roster short? |
| `deflection_finder.py` | Which contact reasons to deflect, automate or fix at the source? |

```bash
/plugin install support-ops@claude-code-skills
/cs-support-sla tickets.csv sla_policy.json
/cs-support-staffing --intervals volumes.csv --aht 420 --concurrency 2
/cs-support-deflection tickets.csv
```

Agent: `cs-support-ops-lead`. References cite Erlang (1917), Gans, Koole and
Mandelbaum (2003), Little (1961), the KCS v6 Practices Guide and ITIL 4. License: MIT.
