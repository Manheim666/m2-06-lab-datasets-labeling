#!/usr/bin/env python3
"""Pick a deterministic, non-overlapping subset of ImageIDs for one student.

Selection rule: take ImageID[rank], ImageID[rank+N], ImageID[rank+2N], ...
until k IDs are collected.

Usage:
  python pick_my_imageids.py \
    --master master_cat_imageids.txt \
    --rank 7 --N 30 --k 100 \
    --out my_imageids.txt
"""

import argparse


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--master", required=True, help="Path to the sorted master ImageID list")
    ap.add_argument("--rank", type=int, required=True, help="Your 0-based rank")
    ap.add_argument("--N", type=int, required=True, help="Total number of students")
    ap.add_argument("--k", type=int, default=100, help="Number of images to pick")
    ap.add_argument("--out", required=True, help="Output file for your ImageIDs")
    args = ap.parse_args()

    with open(args.master, encoding="utf-8") as f:
        master = [line.strip() for line in f if line.strip()]

    if args.N <= 0:
        raise SystemExit("ERROR: N must be > 0")
    if not (0 <= args.rank < args.N):
        raise SystemExit(f"ERROR: rank must be in [0, {args.N - 1}]")

    picked = master[args.rank :: args.N][: args.k]

    if len(picked) < args.k:
        raise SystemExit(f"ERROR: only {len(picked)} IDs available, need {args.k}")

    with open(args.out, "w", encoding="utf-8") as f:
        for image_id in picked:
            f.write(image_id + "\n")

    print(f"Picked {len(picked)} ImageIDs → {args.out}")


if __name__ == "__main__":
    main()
