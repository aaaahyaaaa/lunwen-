import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from medclaimauth.data import load_samples
from medclaimauth.dataset_validation import validate_samples


ROOT = Path(__file__).resolve().parents[1]


class DatasetValidationTest(unittest.TestCase):
    def test_validator_reports_distributions_for_valid_mini_dataset(self):
        samples = load_samples(ROOT / "data" / "cm_egqa_mini.jsonl")

        summary = validate_samples(samples)

        self.assertTrue(summary["valid"], summary["errors"])
        self.assertEqual(summary["sample_count"], 10)
        self.assertEqual(summary["stats"]["risk_level"]["high"], 7)
        self.assertEqual(summary["stats"]["risk_level"]["medium"], 3)
        self.assertEqual(summary["stats"]["gold_action"]["clarify"], 4)
        self.assertEqual(summary["stats"]["gold_action"]["answer"], 4)
        self.assertEqual(summary["stats"]["gold_action"]["abstain"], 2)
        self.assertEqual(summary["stats"]["gap_type"]["patient_info_gap"], 4)
        self.assertEqual(summary["stats"]["gap_type"]["authorization_gap"], 2)
        self.assertEqual(summary["stats"]["support_label"]["supported"], 12)
        self.assertEqual(summary["stats"]["support_label"]["not_authorized"], 6)

    def test_validator_flags_action_gap_mismatch(self):
        broken = [
            {
                "id": "bad_001",
                "question": "我头疼可以吃布洛芬吗？",
                "risk_level": "high",
                "missing_slots": ["是否怀孕"],
                "gold_action": "clarify",
                "gap_type": "none",
                "gold_claims": [
                    {
                        "claim": "该患者可以直接服用布洛芬",
                        "support_label": "not_authorized",
                    }
                ],
            }
        ]

        summary = validate_samples(broken)

        self.assertFalse(summary["valid"])
        self.assertIn("bad_001", summary["errors"][0])
        self.assertIn("clarify", summary["errors"][0])
        self.assertIn("patient_info_gap", summary["errors"][0])

    def test_cli_writes_markdown_validation_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            json_path = tmp / "validation.json"
            md_path = tmp / "validation.md"

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "medclaimauth.validate_dataset",
                    "--samples",
                    str(ROOT / "data" / "cm_egqa_mini.jsonl"),
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

            summary = json.loads(json_path.read_text(encoding="utf-8"))
            markdown = md_path.read_text(encoding="utf-8")
            self.assertTrue(summary["valid"], summary["errors"])
            self.assertIn("# CM-EGQA Dataset Validation", markdown)
            self.assertIn("patient_info_gap", markdown)
            self.assertIn("support_label", markdown)


if __name__ == "__main__":
    unittest.main()
