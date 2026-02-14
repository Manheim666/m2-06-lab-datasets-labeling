#!/usr/bin/env python3
"""Compute your 0-based rank in the lexicographically sorted roster.

Usage:
  python compute_rank.py --roster roster.txt --my-id s12345
"""

import argparse


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--roster", required=True)
    ap.add_argument("--my-id", required=True)
    args = ap.parse_args()

    with open(args.roster, encoding="utf-8") as f:
        ids = sorted(line.strip() for line in f if line.strip())

    if args.my_id not in ids:
        raise SystemExit(f"ERROR: '{args.my_id}' not found in roster")

    rank = ids.index(args.my_id)
    print(f"N={len(ids)}")
    print(f"rank={rank}")


if __name__ == "__main__":
    main()
