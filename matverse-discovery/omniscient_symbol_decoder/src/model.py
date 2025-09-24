"""Modelo placeholder para o decodificador simbólico."""
from __future__ import annotations

import torch
import torch.nn as nn


class TinyDetector(nn.Module):
    """Pequeno backbone conv para experimentos rápidos."""

    def __init__(self, n_classes: int) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Linear(32 * 56 * 56, n_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        feats = self.features(x)
        return self.classifier(feats.view(feats.size(0), -1))
