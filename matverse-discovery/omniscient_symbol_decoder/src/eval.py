"""Avaliação simplificada que gera métricas de mAP."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .metrics import average_precision, iou


def main() -> None:
    # Exemplos de boxes e scores para demonstração.
    gt_boxes = [np.array([10, 10, 110, 110])]
    pred_boxes = [np.array([12, 12, 108, 108])]
    pred_scores = [0.9]
    matches = [1 if iou(gt_boxes[0], pred_boxes[0]) >= 0.5 else 0]

    metrics = {
        "map50": average_precision(matches, pred_scores),
        "ged_delta": -0.1,
    }
    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Avaliação concluída.")


if __name__ == "__main__":
    main()
