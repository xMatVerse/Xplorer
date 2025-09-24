"""Simulação de roteamento heurístico DAQ versus ECMP."""
from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import numpy as np


def gen_graph(n: int = 40, p: float = 0.06, seed: int | None = None) -> nx.Graph:
    rng = np.random.default_rng(seed)
    graph = nx.erdos_renyi_graph(n, p, seed=seed)
    for u, v in graph.edges():
        graph[u][v]["lat"] = rng.uniform(0.2, 2.0)
    return graph


def path_latency(graph: nx.Graph, path: list[int]) -> float:
    return sum(graph[u][v]["lat"] for u, v in zip(path[:-1], path[1:]))


def ecmp(graph: nx.Graph, source: int, target: int) -> list[int]:
    paths = nx.all_simple_paths(graph, source, target, cutoff=6)
    return min(paths, key=lambda p: path_latency(graph, p))


def daq(graph: nx.Graph, source: int, target: int, beta: float = 0.6) -> list[int]:
    bc = nx.betweenness_centrality(graph, normalized=True)
    best: list[int] | None = None
    best_latency = float("inf")
    rng = np.random.default_rng()
    for _ in range(32):
        current = source
        path = [current]
        visited = {current}
        while current != target and len(path) < 10:
            neighbours = [n for n in graph.neighbors(current) if n not in visited]
            if not neighbours:
                break
            weights = np.array(
                [
                    (1.0 / (graph[current][n]["lat"] + 1e-6)) * (1 + beta * bc[n])
                    for n in neighbours
                ]
            )
            weights /= weights.sum()
            current = rng.choice(neighbours, p=weights)
            path.append(current)
            visited.add(current)
        if path[-1] == target:
            latency = path_latency(graph, path)
            if latency < best_latency:
                best_latency = latency
                best = path
    if best is None:
        raise RuntimeError("não foi possível encontrar caminho DAQ")
    return best


def benchmark(n_pairs: int = 200, seed: int | None = None) -> dict[str, float]:
    graph = gen_graph(seed=seed)
    rng = np.random.default_rng(seed)
    nodes = list(graph.nodes())
    latencies = []
    for _ in range(n_pairs):
        src, dst = rng.choice(nodes, 2, replace=False)
        path_ecmp = ecmp(graph, src, dst)
        path_daq = daq(graph, src, dst)
        latencies.append(
            (
                path_latency(graph, path_ecmp),
                path_latency(graph, path_daq),
            )
        )
    arr = np.asarray(latencies)
    p95 = np.quantile(arr, 0.95, axis=0)
    improv_p95 = (p95[1] - p95[0]) / p95[0] * 100.0
    return {"p95_improv_pct": float(improv_p95)}


def main() -> None:
    metrics = benchmark()
    out_dir = Path(__file__).resolve().parents[2] / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Simulação finalizada.")


if __name__ == "__main__":
    main()
