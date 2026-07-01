import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from medclaimauth.data import load_evidence, load_samples
from medclaimauth.experiment import compare_methods
from medclaimauth.table_export import build_gap_confusion_rows, build_main_metric_rows


ROOT = Path(__file__).resolve().parents[1]


class ExportTablesTest(unittest.TestCase):
    def test_builds_main_metric_rows_from_report(self):
        report = compare_methods(
            load_samples(ROOT / "data" / "cm_egqa_mini.jsonl"),
            load_evidence(ROOT / "data" / "evidence_corpus.jsonl"),
        )

        rows = build_main_metric_rows(report)

        gap_accuracy = next(row for row in rows if row["metric"] == "gap_type_accuracy")
        self.assertEqual(gap_accuracy["llm_only"], "0.4000")
        self.assertEqual(gap_accuracy["vanilla_rag"], "0.4000")
        self.assertEqual(gap_accuracy["query_rewrite_rag"], "0.4000")
        self.assertEqual(gap_accuracy["self_reflection_rag"], "0.0000")
        self.assertEqual(gap_accuracy["source_trust_rag"], "0.4000")
        self.assertEqual(gap_accuracy["claim_verification_only"], "0.0000")
        self.assertEqual(gap_accuracy["claim_authorization"], "0.9000")

    def test_builds_gap_confusion_rows_from_report(self):
        report = compare_methods(
            load_samples(ROOT / "data" / "cm_egqa_mini.jsonl"),
            load_evidence(ROOT / "data" / "evidence_corpus.jsonl"),
        )

        rows = build_gap_confusion_rows(report)

        self.assertIn(
            {
                "method": "claim_authorization",
                "gold_gap_type": "none",
                "predicted_gap_type": "patient_info_gap",
                "count": "1",
            },
            rows,
        )

    def test_cli_writes_csv_tables(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            report_json = tmp / "report.json"
            output_dir = tmp / "tables"

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "medclaimauth.run_experiment",
                    "--samples",
                    str(ROOT / "data" / "cm_egqa_mini.jsonl"),
                    "--evidence",
                    str(ROOT / "data" / "evidence_corpus.jsonl"),
                    "--output-json",
                    str(report_json),
                    "--output-md",
                    str(tmp / "report.md"),
                ],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "medclaimauth.export_tables",
                    "--report-json",
                    str(report_json),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            main_metrics = output_dir / "main_metrics.csv"
            gap_confusion = output_dir / "gap_confusion.csv"
            self.assertTrue(main_metrics.exists())
            self.assertTrue(gap_confusion.exists())

            with main_metrics.open("r", encoding="utf-8", newline="") as handle:
                metric_rows = list(csv.DictReader(handle))
            self.assertEqual(metric_rows[0]["metric"], "action_accuracy")

            with gap_confusion.open("r", encoding="utf-8", newline="") as handle:
                gap_rows = list(csv.DictReader(handle))
            self.assertIn("predicted_gap_type", gap_rows[0])


if __name__ == "__main__":
    unittest.main()
