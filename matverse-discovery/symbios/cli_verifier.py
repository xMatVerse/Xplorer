#!/usr/bin/env python3
"""CLI para validar provas de inclusão Merkle geradas pelo SYMBIOS."""
from __future__ import annotations

import json
import sys
from hashlib import sha256
from pathlib import Path
from typing import Iterable


def _hash(data: bytes) -> str:
    return sha256(data).hexdigest()


def verify_inclusion(leaf_hash: str, path: Iterable[dict[str, str]], root: str) -> bool:
    current = leaf_hash
    for step in path:
        sibling = step["hash"]
        side = step["side"].upper()
        if side == "L":
            current = _hash((sibling + current).encode())
        else:
            current = _hash((current + sibling).encode())
    return current == root


def main() -> None:
    if len(sys.argv) != 2:
        print("uso: python cli_verifier.py <prova.json>")
        sys.exit(1)
    proof_path = Path(sys.argv[1])
    proof = json.loads(proof_path.read_text())
    ok = verify_inclusion(proof["leaf_hash"], proof["path"], proof["root"])
    print("OK" if ok else "FAIL")


if __name__ == "__main__":
    main()
