"""Metrics helpers for causal discovery experiments."""
from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score


def shd(adj_true: np.ndarray, adj_pred: np.ndarray) -> int:
    """Compute the structural Hamming distance between two adjacency matrices."""
    return int(np.sum(adj_true != adj_pred))


def auprc_edges(adj_true: np.ndarray, scores: np.ndarray) -> float:
    """Compute edge-level AUPRC given a score matrix."""
    labels = adj_true.flatten()
    ranked_scores = scores.flatten()
    return float(average_precision_score(labels, ranked_scores))


def bootstrap(values: list[float], n_bootstrap: int = 1000, seed: int | None = None) -> tuple[float, float, float]:
    """Return (lower, mean, upper) confidence interval bounds via bootstrap."""
    rng = np.random.default_rng(seed)
    array = np.asarray(values, dtype=float)
    n = array.size
    samples = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        samples.append(float(np.mean(array[idx])))
    samples.sort()
    lower = samples[int(0.025 * n_bootstrap)]
    upper = samples[int(0.975 * n_bootstrap)]
    return lower, float(np.mean(array)), upper
