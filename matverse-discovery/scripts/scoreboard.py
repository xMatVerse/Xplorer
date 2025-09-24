#!/usr/bin/env python3
"""Aggregates project metrics and decides Go/No-Go status."""
from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"

PROJECT_GATES: dict[str, Callable[[dict[str, Any]], bool]] = {
    "scidis": lambda m: (m.get("delta_shd", 0.0) >= 0.20)
    and (m.get("auprc_causal", 0.0) > m.get("auprc_base", 0.0)),
    "symbios": lambda m: (m.get("proof_complexity", "") == "logn")
    and (m.get("reproducible_artifacts", 0) >= 3),
    "rhi-sim": lambda m: (m.get("overhead_mean_pct", float("inf")) <= 20.0)
    and (m.get("overhead_p95_pct", float("inf")) <= 20.0),
    "omniscient_symbol_decoder": lambda m: (m.get("map50", 0.0) >= 0.70)
    and (m.get("ged_delta", 0.0) <= -0.10),
    "daq-routing": lambda m: (m.get("p95_improv_pct", float("inf")) <= -15.0),
    "cassandra-edge": lambda m: (m.get("p95_ms", float("inf")) < 200.0)
    and (m.get("qual_delta_pct", float("inf")) <= 5.0),
    "fiveD": lambda m: (m.get("scenarios_formais", 0) >= 2)
    and (m.get("simulacoes_toy", 0) >= 1),
    "qtvr": lambda m: (m.get("overhead_pct", float("inf")) <= 5.0),
}


def load_metrics(project: str) -> dict[str, Any]:
    metrics_path = ROOT / project / "results" / "metrics.json"
    if not metrics_path.exists():
        return {}
    try:
        return json.loads(metrics_path.read_text())
    except json.JSONDecodeError:
        return {}


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rows: list[dict[str, Any]] = []
    timestamp = int(time.time())

    for project, gate_fn in PROJECT_GATES.items():
        metrics = load_metrics(project)
        status = "GO" if gate_fn(metrics) else "NO-GO/PIVOT"
        rows.append({"project": project, "gate": status, **metrics})

    fieldnames = sorted({key for row in rows for key in row.keys()})
    with (RESULTS_DIR / "scoreboard.csv").open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    (RESULTS_DIR / "scoreboard.ts").write_text(str(timestamp))
    print("Scoreboard salvo em results/scoreboard.csv")


if __name__ == "__main__":
    main()
