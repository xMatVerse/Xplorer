#!/usr/bin/env python3
import hashlib
import os
import sys
from pathlib import Path


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def leaf_hash(path: Path) -> str:
    return sha256_hex(path.read_bytes())


def build_level_hashes(hashes: list[str]) -> list[str]:
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    return [sha256_hex((hashes[i] + hashes[i + 1]).encode()) for i in range(0, len(hashes), 2)]


def main() -> None:
    if len(sys.argv) != 2:
        print("uso: python calc_merkle_root.py <dir>")
        sys.exit(1)
    base = Path(sys.argv[1])
    if not base.exists() or not base.is_dir():
        print("diretório inválido")
        sys.exit(1)
    files = [p for p in sorted(base.iterdir()) if p.is_file()]
    if not files:
        print("pasta vazia")
        sys.exit(1)
    level = [leaf_hash(p) for p in files]
    while len(level) > 1:
        level = build_level_hashes(level)
    print(level[0])


if __name__ == "__main__":
    main()
