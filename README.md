# Challenge QA GenAI — Salud Andina

Evaluador determinístico de conversaciones del asistente "Ana" (triaje, turnos y coberturas).

> En construcción. La versión final de este README documentará el criterio y las decisiones tomadas.

## Cómo correrlo

1. Copiar los archivos del kit (`casos_visibles.jsonl`, `clave_visibles.csv`, `manual.json`) en `kit/`.
2. Ejecutar:

```bash
python evaluar.py kit/casos_visibles.jsonl kit/manual.json > mis_resultados.csv
```

Requiere Python 3.10+, solo biblioteca estándar.
