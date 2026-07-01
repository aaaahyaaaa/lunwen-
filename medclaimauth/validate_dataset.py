"""Command-line dataset validation for CM-EGQA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from medclaimauth.data import load_samples
from medclaimauth.dataset_validation import (
    format_validation_markdown,
    validate_samples,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a CM-EGQA JSONL file.")
    parser.add_argument("--samples", required=True, help="Path to sample JSONL.")
    parser.add_argument("--output-json", required=True, help="Validation JSON path.")
    parser.add_argument("--output-md", required=True, help="Validation Markdown path.")
    args = parser.parse_args()

    samples = load_samples(args.samples)
    summary = validate_samples(samples)

    json_path = Path(args.output_json)
    md_path = Path(args.output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(format_validation_markdown(summary), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
