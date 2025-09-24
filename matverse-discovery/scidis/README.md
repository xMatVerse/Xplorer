# SCIDIS — Inferência Causal Distribuída

Este módulo contém geradores de dados sintéticos, métricas e um script de avaliação
rápida para acompanhar o progresso rumo ao gate de 30 dias (ΔSHD ≥ 0,20 e AUPRC
melhor que o baseline).

## Como executar

```bash
python scidis/src/run_eval.py
```

O comando gera `results/metrics.json` com métricas iniciais e pode ser usado como
smoke test após alterações no pipeline causal.
