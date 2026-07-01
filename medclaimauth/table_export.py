"""CSV table builders for CM-EGQA experiment reports."""

from __future__ import annotations

from typing import Any


def build_main_metric_rows(report: dict[str, Any]) -> list[dict[str, str]]:
    metrics = report["metrics"]
    method_names = list(metrics)
    metric_names = sorted(set().union(*(method_metrics for method_metrics in metrics.values())))
    rows: list[dict[str, str]] = []
    for metric in metric_names:
        row = {"metric": metric}
        for method in method_names:
            row[method] = f"{metrics[method].get(metric, 0.0):.4f}"
        rows.append(row)
    return rows


def build_gap_confusion_rows(report: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for method, matrix in report["gap_confusion"].items():
        for gold_gap_type, predicted_counts in sorted(matrix.items()):
            for predicted_gap_type, count in sorted(predicted_counts.items()):
                rows.append(
                    {
                        "method": method,
                        "gold_gap_type": gold_gap_type,
                        "predicted_gap_type": predicted_gap_type,
                        "count": str(count),
                    }
                )
    return rows
