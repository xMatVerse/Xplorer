"""Merkle tree utilities for SYMBIOS proofs."""
from __future__ import annotations

from hashlib import sha256
from typing import List, Tuple


def _hash(data: bytes) -> str:
    return sha256(data).hexdigest()


def build_root(leaves: List[bytes]) -> Tuple[str, List[List[str]]]:
    """Return Merkle root and intermediate levels."""
    if not leaves:
        raise ValueError("é necessário fornecer ao menos uma folha")
    level = [_hash(item) for item in leaves]
    tree: List[List[str]] = [level.copy()]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        level = [_hash((level[i] + level[i + 1]).encode()) for i in range(0, len(level), 2)]
        tree.append(level.copy())
    return level[0], tree


def inclusion_proof(index: int, leaves: List[bytes], tree_levels: List[List[str]]) -> List[Tuple[str, str]]:
    """Return the inclusion proof for the leaf at *index*.

    Each tuple is (hash, side) where side ∈ {"L", "R"}.
    """
    if not 0 <= index < len(leaves):
        raise IndexError("índice de folha inválido")
    proof: List[Tuple[str, str]] = []
    position = index
    for level in tree_levels[:-1]:
        if len(level) % 2 == 1 and position == len(level) - 1:
            sibling = level[position]
            side = "R"
        elif position % 2 == 0:
            sibling = level[position + 1]
            side = "R"
        else:
            sibling = level[position - 1]
            side = "L"
        proof.append((sibling, side))
        position //= 2
    return proof
