"""Command-line CSV exporter for CM-EGQA report tables."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from medclaimauth.table_export import (
    build_gap_confusion_rows,
    build_main_metric_rows,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export CM-EGQA report tables.")
    parser.add_argument("--report-json", required=True, help="Experiment report JSON.")
    parser.add_argument("--output-dir", required=True, help="Directory for CSV tables.")
    args = parser.parse_args()

    report = json.loads(Path(args.report_json).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metric_rows = build_main_metric_rows(report)
    gap_rows = build_gap_confusion_rows(report)
    _write_csv(output_dir / "main_metrics.csv", metric_rows)
    _write_csv(output_dir / "gap_confusion.csv", gap_rows)

    print(f"Wrote {output_dir / 'main_metrics.csv'}")
    print(f"Wrote {output_dir / 'gap_confusion.csv'}")
    return 0


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
