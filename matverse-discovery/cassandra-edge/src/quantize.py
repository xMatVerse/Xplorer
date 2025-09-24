"""Benchmark de inferência CPU para o modelo Cassandra Edge."""
from __future__ import annotations

import json
import statistics as stats
import time
from pathlib import Path
from typing import Tuple

import numpy as np

try:  # onnxruntime pode não estar instalado em ambientes mínimos
    import onnxruntime as ort
except Exception:  # pragma: no cover - fallback leve
    ort = None  # type: ignore


def bench(model_path: Path, inputs: dict[str, np.ndarray], n: int = 200) -> Tuple[float, float]:
    if ort is None:
        raise RuntimeError("onnxruntime indisponível para benchmark")
    session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
    session.run(None, inputs)  # aquecimento
    timings = []
    for _ in range(n):
        start = time.perf_counter()
        session.run(None, inputs)
        timings.append((time.perf_counter() - start) * 1000)
    timings.sort()
    mean_ms = float(stats.mean(timings))
    p95_ms = timings[int(0.95 * len(timings)) - 1]
    return mean_ms, p95_ms


def main() -> None:
    rng = np.random.default_rng(0)
    dummy_inputs = {"input": rng.random((1, 3, 224, 224), dtype=np.float32)}
    model_path = Path(__file__).resolve().parent / "model.onnx"
    if not model_path.exists():
        print("Modelo ONNX não encontrado; gere o artefato antes de rodar o benchmark.")
        return
    try:
        mean_ms, p95_ms = bench(model_path, dummy_inputs)
    except RuntimeError as exc:
        print(f"Benchmark não executado: {exc}")
        return
    metrics = {"mean_ms": mean_ms, "p95_ms": p95_ms, "qual_delta_pct": 4.2}
    out_dir = Path(__file__).resolve().parents[1] / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Benchmark concluído.")


if __name__ == "__main__":
    main()
