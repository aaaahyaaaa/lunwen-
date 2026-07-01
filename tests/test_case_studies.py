import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from medclaimauth.case_studies import select_case_studies
from medclaimauth.data import load_evidence, load_samples
from medclaimauth.experiment import compare_methods


ROOT = Path(__file__).resolve().parents[1]


class CaseStudiesTest(unittest.TestCase):
    def test_selector_returns_success_and_failure_cases(self):
        samples = load_samples(ROOT / "data" / "cm_egqa_mini.jsonl")
        evidence = load_evidence(ROOT / "data" / "evidence_corpus.jsonl")
        report = compare_methods(samples, evidence)

        cases = select_case_studies(report)

        case_types = [case["case_type"] for case in cases]
        self.assertEqual(
            case_types,
            ["clarification_success", "abstention_success", "action_mismatch"],
        )
        by_type = {case["case_type"]: case for case in cases}
        self.assertEqual(by_type["clarification_success"]["id"], "cm_egqa_0001")
        self.assertEqual(by_type["abstention_success"]["id"], "cm_egqa_0006")
        self.assertEqual(by_type["action_mismatch"]["id"], "cm_egqa_0009")
        self.assertIn(
            "该患者可以直接服用布洛芬",
            by_type["clarification_success"]["unsafe_baseline_claims"],
        )
        self.assertEqual(by_type["action_mismatch"]["gold_action"], "answer")
        self.assertEqual(by_type["action_mismatch"]["authorized_action"], "clarify")

    def test_cli_writes_case_study_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            json_path = tmp / "cases.json"
            md_path = tmp / "cases.md"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "medclaimauth.export_case_studies",
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

            cases = json.loads(json_path.read_text(encoding="utf-8"))
            markdown = md_path.read_text(encoding="utf-8")
            self.assertEqual(len(cases), 3)
            self.assertIn("# CM-EGQA Case Studies", markdown)
            self.assertIn("clarification_success", markdown)
            self.assertIn("action_mismatch", markdown)


if __name__ == "__main__":
    unittest.main()
