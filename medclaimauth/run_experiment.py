"""Command-line runner for the CM-EGQA mini experiment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from medclaimauth.data import load_evidence, load_samples
from medclaimauth.experiment import compare_methods


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the CM-EGQA mini claim-authorization experiment."
    )
    parser.add_argument("--samples", required=True, help="Path to sample JSONL.")
    parser.add_argument("--evidence", required=True, help="Path to evidence JSONL.")
    parser.add_argument("--output-json", required=True, help="Report JSON path.")
    parser.add_argument("--output-md", required=True, help="Report Markdown path.")
    args = parser.parse_args()

    samples = load_samples(args.samples)
    evidence = load_evidence(args.evidence)
    report = compare_methods(samples, evidence)

    json_path = Path(args.output_json)
    md_path = Path(args.output_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_format_markdown_report(report), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


def _format_markdown_report(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    rows = []
    method_names = list(metrics)
    metric_names = sorted(set().union(*(method_metrics for method_metrics in metrics.values())))
    for metric in metric_names:
        values = " | ".join(f"{metrics[method].get(metric, 0.0):.4f}" for method in method_names)
        rows.append(f"| `{metric}` | {values} |")

    lines = [
        "# CM-EGQA Mini Experiment Report",
        "",
        "Target: IEEE BigData 2026 main-conference evidence-building pilot.",
        "",
        "## Metrics",
        "",
        f"| Metric | {' | '.join(method_names)} |",
        f"|---|{'|'.join(['---:'] * len(method_names))}|",
        *rows,
        "",
        "## Gap Confusion",
        "",
    ]
    for method in method_names:
        lines.extend(_format_gap_confusion_table(method, report["gap_confusion"][method]))
    lines.extend(
        [
            "## Interpretation",
            "",
            "- `unsupported_claim_rate` and `risk_weighted_unsupported_claim_rate` measure unsafe emitted medical claims.",
            "- `unsafe_direct_answer_rate` measures high-risk questions where the system directly answers while emitting an unsafe claim.",
            "- `gap_type_accuracy` and the confusion tables show whether the system identifies the evidence gap, not only whether it suppresses unsafe claims.",
            "- `answer_coverage` is the fraction of questions receiving a direct answer; `response_coverage` also counts clarification and retrieve-more actions.",
            "",
        ]
    )
    return "\n".join(lines)


def _format_gap_confusion_table(method: str, matrix: dict[str, dict[str, int]]) -> list[str]:
    predicted_labels = sorted({label for row in matrix.values() for label in row})
    lines = [
        f"### {method}",
        "",
        f"| Gold gap | {' | '.join(predicted_labels)} |",
        f"|---|{'|'.join(['---:'] * len(predicted_labels))}|",
    ]
    for gold_gap, row in sorted(matrix.items()):
        values = " | ".join(str(row.get(label, 0)) for label in predicted_labels)
        lines.append(f"| `{gold_gap}` | {values} |")
    lines.append("")
    return lines


if __name__ == "__main__":
    raise SystemExit(main())
