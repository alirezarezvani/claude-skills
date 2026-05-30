# Kubernetes Operator

End-to-end discipline for building Kubernetes Operators correctly. Catches the recurring reconcile-loop bugs (missing finalizers, blocking calls, status drift, RBAC over-grants, no requeue) before they reach a cluster.

## What's inside

- **3 stdlib Python tools** — CRD validator, reconcile-loop linter, OperatorHub capability auditor
- **4 reference docs** — operator pattern, CRD design, reconcile patterns, framework comparison
- **Asset templates** — production CRD YAML + Go controller skeleton (both pass the linters)
- **`/operator-audit` slash command** — runs all 3 tools and produces a report

## Install

```bash
# Via Claude Code marketplace
/plugin install kubernetes-operator

# Or clone the repo
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills/engineering/kubernetes-operator
```

## Quick start

```bash
SKILL=engineering/kubernetes-operator/skills/kubernetes-operator

python "$SKILL/scripts/crd_validator.py" --crd config/crd/myapp.yaml
python "$SKILL/scripts/reconcile_lint.py" --controller controllers/myapp_controller.go
python "$SKILL/scripts/operator_capability_audit.py" --operator-dir .
```

## Scope

This is the **Operator pattern** specifically. For other Kubernetes work:

- Helm chart authoring → `helm-chart-builder`
- Kubectl operations / blue-green deploys → `senior-devops`
- General k8s security → `cloud-security`
- Cloud architecture → `aws-solution-architect`, `azure-cloud-architect`, `gcp-cloud-architect`

## Key principles

1. **Reconcile is idempotent**, declarative, and bounded in time
2. **Status subresource is non-negotiable** — without it, status updates loop spec reconciles
3. **Finalizers protect external resources** — cascade deletion is the operator pattern's free gift, but only for owned k8s resources
4. **RBAC is least-privilege** — controllers shouldn't read secrets they don't need
5. **Capability levels are an SLA**, not a label — aim for L3 (Full Lifecycle) before public release

## Skill structure

```
kubernetes-operator/
├── README.md
├── .claude-plugin/plugin.json
└── skills/kubernetes-operator/
    ├── SKILL.md
    ├── scripts/
    │   ├── crd_validator.py
    │   ├── reconcile_lint.py
    │   └── operator_capability_audit.py
    ├── references/
    │   ├── operator_pattern.md
    │   ├── crd_design.md
    │   ├── reconcile_loop.md
    │   └── tooling_landscape.md
    └── assets/
        ├── crd_template.yaml
        └── reconcile_skeleton.go
```

## Verifiable success

A team using this skill should achieve:

- 100% of new CRDs pass `crd_validator.py` before merge
- All reconcile functions pass `reconcile_lint.py` strict mode
- Operators reach OperatorHub Capability Level 3 before public release
- Mean time to fix a reconcile bug: <1 day (no infinite loops in production)

## License

MIT — see repo root LICENSE.
