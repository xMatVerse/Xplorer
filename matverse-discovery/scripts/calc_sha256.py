#!/usr/bin/env python3
import hashlib
import sys
import pathlib


def main() -> None:
    if len(sys.argv) < 2:
        print("uso: python calc_sha256.py <arquivo...>")
        sys.exit(1)
    for path_str in sys.argv[1:]:
        path = pathlib.Path(path_str)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{digest}  {path}")


if __name__ == "__main__":
    main()
