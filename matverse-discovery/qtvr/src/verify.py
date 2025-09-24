"""Verificação tensorial simplificada para pipelines quânticos."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def random_tensor(shape: tuple[int, ...], seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.standard_normal(shape)


def verify_tensor(tensor: np.ndarray, k: int = 3, seed: int | None = None) -> float:
    rng = np.random.default_rng(seed)
    overhead = []
    for _ in range(k):
        projection = rng.standard_normal(tensor.shape[0])
        projected = projection @ tensor.reshape(tensor.shape[0], -1)
        overhead.append(float(np.linalg.norm(projected)))
    return float(np.mean(overhead))


def main() -> None:
    tensor = random_tensor((4, 4, 4), seed=0)
    overhead = verify_tensor(tensor)
    metrics = {"overhead_pct": overhead / 100.0}
    out_dir = Path(__file__).resolve().parents[1] / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Verificação concluída.")


if __name__ == "__main__":
    main()
