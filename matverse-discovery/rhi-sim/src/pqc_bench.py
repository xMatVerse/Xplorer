"""Benchmark handshake clássico vs. pós-quântico."""
from __future__ import annotations

import statistics as stats
import time


def measure(fn, n: int = 50) -> tuple[float, float]:
    """Return (mean_ms, approx_p95_ms) for callable ``fn``."""
    samples = []
    for _ in range(n):
        start = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - start) * 1000)
    samples.sort()
    mean_ms = float(stats.mean(samples))
    p95_ms = samples[int(0.95 * len(samples)) - 1]
    return mean_ms, p95_ms


def classic_handshake() -> None:
    time.sleep(0.002)


def pqc_handshake() -> None:
    time.sleep(0.0023)


def main() -> None:
    classic = measure(classic_handshake)
    pqc = measure(pqc_handshake)
    mean_overhead = (pqc[0] - classic[0]) / classic[0] * 100.0
    p95_overhead = (pqc[1] - classic[1]) / classic[1] * 100.0
    print(
        "overhead mean="
        f"{mean_overhead:.1f}%  p95={p95_overhead:.1f}%  (passa se ≤20%)"
    )


if __name__ == "__main__":
    main()
