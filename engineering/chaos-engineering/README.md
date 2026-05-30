# Chaos Engineering

End-to-end discipline for chaos experiments — design, run, learn — without becoming an outage.

## What's inside

- **3 stdlib Python tools** — experiment designer, blast-radius calculator, postmortem generator
- **4 reference docs** — principles, experiment design, attack taxonomy, tooling landscape
- **2 templates** — experiment plan, postmortem
- **`/chaos-experiment` slash command** — interactive design wizard

## Install

```bash
# Via Claude Code marketplace
/plugin install chaos-engineering

# Or clone the repo
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills/engineering/chaos-engineering
```

## Quick start

```bash
SKILL=engineering/chaos-engineering/skills/chaos-engineering

# 1. Design an experiment
python "$SKILL/scripts/experiment_designer.py" \
  --target checkout-svc \
  --hypothesis "p99 < 500ms when payment slows" \
  --attack latency --magnitude "+200ms" \
  --abort-if "p99 > 1000ms OR error_rate > +1pp"

# 2. Calculate blast radius
python "$SKILL/scripts/blast_radius_calculator.py" \
  --traffic-share 0.05 --user-pop 1000000 \
  --duration-min 15

# 3. Generate postmortem after running
python "$SKILL/scripts/experiment_postmortem.py" \
  --plan plan.json --result-log results.txt
```

## Key principles

1. **Build a hypothesis around steady-state behavior** — measurable, falsifiable
2. **Vary real-world events** — realistic failures only, not astronomy-grade
3. **Run experiments in production** — staging never has prod failure modes
4. **Automate experiments to run continuously** — single experiment = press release; continuous = engineering
5. **Define abort criteria up front** — chaos without abort = outage

## The 7 attack types

| Attack | Tests | Magnitude examples |
|---|---|---|
| **Latency** | Timeouts, retries, circuit breakers | +200ms, +2s |
| **Error** | Error handling, fallback paths | 1%, 50%, 100% |
| **Resource** | Saturation, autoscaling, OOM | 80% CPU, 90% memory, fill /var |
| **Network partition** | Consensus, leader election, failover | drop 100% to peer X |
| **Dependency failure** | Graceful degradation | timeout 100% to dep X |
| **Time skew** | Clocks, TTLs, retry backoff | +5min, +1day |
| **Infrastructure** | Auto-recovery, replica maintenance | kill 1 of N |

## Composition with other skills

| Skill | Composition |
|---|---|
| `feature-flags-architect` | Kill switches there are abort triggers here |
| `kubernetes-operator` | Operators are common chaos targets |
| `incident-response` | Chaos that escalates becomes an incident |

## Skill structure

```
chaos-engineering/
├── README.md
├── .claude-plugin/plugin.json
└── skills/chaos-engineering/
    ├── SKILL.md
    ├── scripts/
    │   ├── experiment_designer.py
    │   ├── blast_radius_calculator.py
    │   └── experiment_postmortem.py
    ├── references/
    │   ├── chaos_principles.md
    │   ├── experiment_design.md
    │   ├── attack_taxonomy.md
    │   └── tooling_landscape.md
    └── assets/
        ├── experiment_template.md
        └── postmortem_template.md
```

## Verifiable success

A team using this skill should achieve:

- 100% of chaos experiments have written hypothesis, abort criteria, blast-radius calc
- Blast radius for any single experiment ≤10% of monthly error budget
- Mean time between chaos experiments <14 days (continuous, not one-off)
- Each experiment produces ≥1 follow-up action that gets shipped
- No chaos experiment escalates to a customer-impacting incident in trailing 90 days

## License

MIT — see repo root LICENSE.
