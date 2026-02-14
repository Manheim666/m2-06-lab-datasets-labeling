#!/usr/bin/env python3
"""Verify a YOLO dataset before submission.

Checks:
  - Every ImageID has an image file
  - Every ImageID has a label file (may be empty)
  - Every label line has 5 fields with class_id=0 and floats in [0,1]
  - Width and height are positive

Usage:
  python verify_yolo_dataset.py \
    --images images \
    --labels labels \
    --imageids my_imageids.txt
"""

import argparse
import math
from pathlib import Path


def load_ids(path):
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--images", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--imageids", required=True)
    args = ap.parse_args()

    img_dir = Path(args.images)
    lbl_dir = Path(args.labels)
    ids = load_ids(args.imageids)

    missing_images = []
    missing_labels = []
    bad_lines = []

    for image_id in ids:
        # Check image
        if not (img_dir / f"{image_id}.jpg").exists():
            missing_images.append(image_id)

        # Check label
        lbl_path = lbl_dir / f"{image_id}.txt"
        if not lbl_path.exists():
            missing_labels.append(image_id)
            continue

        text = lbl_path.read_text(encoding="utf-8").strip()
        if not text:
            continue  # Empty label file is valid

        for ln_no, line in enumerate(text.splitlines(), 1):
            parts = line.strip().split()
            if len(parts) != 5:
                bad_lines.append((image_id, ln_no, "expected 5 fields", line))
                continue

            try:
                cls_id = int(parts[0])
                vals = [float(v) for v in parts[1:]]
            except ValueError:
                bad_lines.append((image_id, ln_no, "parse error", line))
                continue

            if cls_id != 0:
                bad_lines.append((image_id, ln_no, f"class_id={cls_id}, expected 0", line))
            elif not all(math.isfinite(v) and 0.0 <= v <= 1.0 for v in vals):
                bad_lines.append((image_id, ln_no, "values out of [0,1]", line))
            elif vals[2] <= 0 or vals[3] <= 0:
                bad_lines.append((image_id, ln_no, "width or height <= 0", line))

    # Report
    print("=== YOLO DATASET VERIFICATION ===")
    print(f"ImageIDs checked:  {len(ids)}")
    print(f"Missing images:    {len(missing_images)}")
    print(f"Missing labels:    {len(missing_labels)}")
    print(f"Bad label lines:   {len(bad_lines)}")

    for label, items in [("Missing images", missing_images), ("Missing labels", missing_labels)]:
        if items:
            print(f"\n{label} (first 20):")
            for x in items[:20]:
                print(f"  - {x}")

    if bad_lines:
        print(f"\nBad label lines (first 20):")
        for image_id, ln_no, reason, line in bad_lines[:20]:
            print(f"  - {image_id}:{ln_no} [{reason}] {line}")

    if not missing_images and not missing_labels and not bad_lines:
        print("\nPASS: Dataset is valid for upload.")
    else:
        print("\nFAIL: Fix the issues above before submitting.")


if __name__ == "__main__":
    main()
