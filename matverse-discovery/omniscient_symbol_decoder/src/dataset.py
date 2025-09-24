"""Funções utilitárias para carregar datasets anotados para OCR simbólico."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple

from PIL import Image


Annotation = Tuple[str, Tuple[int, int, int, int], str]


def load_annotations(path: Path) -> List[Annotation]:
    """Lê um arquivo de anotações simples (CSV-like) e retorna boxes e classes."""
    annotations: List[Annotation] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        image_path, left, top, right, bottom, label = line.split(",")
        annotations.append(
            (
                image_path,
                (int(left), int(top), int(right), int(bottom)),
                label,
            )
        )
    return annotations


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")
