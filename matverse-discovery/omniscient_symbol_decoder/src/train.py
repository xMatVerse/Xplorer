"""Loop de treino simplificado para o detector simbólico."""
from __future__ import annotations

import torch
from torch.utils.data import DataLoader, Dataset

from .model import TinyDetector


class DummyDataset(Dataset[tuple[torch.Tensor, int]]):
    def __len__(self) -> int:  # type: ignore[override]
        return 10

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:  # type: ignore[override]
        return torch.rand(3, 224, 224), idx % 3


def main() -> None:
    dataset = DummyDataset()
    loader = DataLoader(dataset, batch_size=2)
    model = TinyDetector(n_classes=3)
    optim = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.CrossEntropyLoss()

    model.train()
    for epoch in range(2):
        for inputs, labels in loader:
            optim.zero_grad()
            logits = model(inputs)
            loss = loss_fn(logits, labels)
            loss.backward()
            optim.step()
        print(f"epoch {epoch}: loss={loss.item():.3f}")


if __name__ == "__main__":
    main()
