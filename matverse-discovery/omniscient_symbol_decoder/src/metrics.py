"""Métricas auxiliares para o Omniscient Symbol Decoder."""
from __future__ import annotations

import numpy as np


def iou(box_a: np.ndarray, box_b: np.ndarray) -> float:
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])
    inter = max(0, x_b - x_a) * max(0, y_b - y_a)
    area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    denom = max(1e-9, (area_a + area_b - inter))
    return inter / denom


def average_precision(matches: list[int], scores: list[float]) -> float:
    order = np.argsort(-np.asarray(scores))
    matches_arr = np.asarray(matches)[order]
    tp = np.cumsum(matches_arr)
    fp = np.cumsum(1 - matches_arr)
    precision = tp / np.maximum(1, tp + fp)
    recall = tp / max(1, matches_arr.sum())
    return float(np.trapz(precision, recall))
