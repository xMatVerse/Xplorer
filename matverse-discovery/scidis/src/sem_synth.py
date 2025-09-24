"""Synthetic Structural Equation Model utilities."""
from __future__ import annotations

import numpy as np


def random_dag(n: int = 10, p: float = 0.2, seed: int | None = None) -> np.ndarray:
    """Generate an upper-triangular adjacency matrix representing a DAG."""
    rng = np.random.default_rng(seed)
    adj = (rng.random((n, n)) < p).astype(int)
    np.fill_diagonal(adj, 0)
    return np.triu(adj, 1)


def sample_sem(
    adj: np.ndarray,
    n_samples: int = 2000,
    sigma: float = 1.0,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Sample from a linear SEM given an adjacency matrix."""
    rng = np.random.default_rng(seed)
    n_nodes = adj.shape[0]
    weights = adj * rng.normal(0.5, 0.2, size=adj.shape)
    samples = rng.normal(0, 1, size=(n_samples, n_nodes))
    order = np.argsort(np.sum(adj, axis=0))
    for node in order:
        parents = np.where(adj[:, node] == 1)[0]
        if parents.size:
            samples[:, node] = (
                samples[:, parents] @ weights[parents, node]
                + rng.normal(0, sigma, size=n_samples)
            )
    return samples, weights
