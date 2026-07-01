import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RunExperimentCliTest(unittest.TestCase):
    def test_cli_writes_json_and_markdown_reports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            json_path = tmp / "report.json"
            md_path = tmp / "report.md"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "medclaimauth.run_experiment",
                    "--samples",
                    str(ROOT / "data" / "cm_egqa_mini.jsonl"),
                    "--evidence",
                    str(ROOT / "data" / "evidence_corpus.jsonl"),
                    "--output-json",
                    str(json_path),
                    "--output-md",
                    str(md_path),
                ],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())

            report = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("metrics", report)
            self.assertIn("claim_authorization", report["metrics"])

            markdown = md_path.read_text(encoding="utf-8")
            self.assertIn("# CM-EGQA Mini Experiment Report", markdown)
            self.assertIn("llm_only", markdown)
            self.assertIn("self_reflection_rag", markdown)
            self.assertIn("source_trust_rag", markdown)
            self.assertIn("unsafe_direct_answer_rate", markdown)
            self.assertIn("## Gap Confusion", markdown)
            self.assertIn("patient_info_gap", markdown)
            self.assertIn("IEEE BigData 2026", markdown)


if __name__ == "__main__":
    unittest.main()
