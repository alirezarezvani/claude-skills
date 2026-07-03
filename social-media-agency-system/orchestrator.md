# Orchestrator - Multi-Agent Social Media System

## Secuencia principal
1. Cliente completa `business-brief-template.md`.
2. STRATEGY produce plan, personas, KPIs y calendario.
3. CONTENT genera piezas segun plan aprobado.
4. COMMUNITY publica, responde y clasifica interacciones.
5. ANALYTICS consolida resultados y propone optimizaciones.
6. STRATEGY ajusta el siguiente ciclo (loop continuo).

## Contrato de handoff entre agentes
Cada handoff debe incluir:
- `context_summary`
- `input_payload`
- `expected_outputs`
- `deadline`
- `owner`

## Eventos de escalacion
- Crisis reputacional -> COMMUNITY -> responsable de crisis.
- Desviacion KPI >20% por 2 periodos -> ANALYTICS -> STRATEGY.
- Bloqueo por aprobacion >24h -> ORCHESTRATOR -> account owner.

## Cadencia operativa recomendada
- Daily: seguimiento de ejecucion (15 min).
- Weekly: rendimiento y ajustes tacticos.
- Monthly: revision de objetivos y rediseno de plan.
