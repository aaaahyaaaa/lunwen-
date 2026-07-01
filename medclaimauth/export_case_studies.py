"""Command-line case-study exporter for CM-EGQA experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from medclaimauth.case_studies import (
    format_case_studies_markdown,
    select_case_studies,
)
from medclaimauth.data import load_evidence, load_samples
from medclaimauth.experiment import compare_methods


def main() -> int:
    parser = argparse.ArgumentParser(description="Export CM-EGQA case studies.")
    parser.add_argument("--samples", required=True, help="Path to sample JSONL.")
    parser.add_argument("--evidence", required=True, help="Path to evidence JSONL.")
    parser.add_argument("--output-json", required=True, help="Case-study JSON path.")
    parser.add_argument("--output-md", required=True, help="Case-study Markdown path.")
    args = parser.parse_args()

    samples = load_samples(args.samples)
    evidence = load_evidence(args.evidence)
    cases = select_case_studies(compare_methods(samples, evidence))

    json_path = Path(args.output_json)
    md_path = Path(args.output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(format_case_studies_markdown(cases), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
