"""Dataset validation utilities for CM-EGQA samples."""

from __future__ import annotations

from collections import Counter
from typing import Any


REQUIRED_SAMPLE_FIELDS = {
    "id",
    "question",
    "risk_level",
    "missing_slots",
    "gold_action",
    "gap_type",
    "gold_claims",
}
VALID_RISK_LEVELS = {"low", "medium", "high"}
VALID_ACTIONS = {"answer", "clarify", "retrieve_more", "abstain"}
VALID_GAP_TYPES = {
    "none",
    "patient_info_gap",
    "retrieval_gap",
    "source_trust_gap",
    "evidence_conflict",
    "authorization_gap",
}
VALID_SUPPORT_LABELS = {
    "supported",
    "partially_supported",
    "unsupported",
    "contradicted",
    "not_authorized",
}
ACTION_GAP_COMPATIBILITY = {
    "answer": {"none"},
    "clarify": {"patient_info_gap"},
    "retrieve_more": {"retrieval_gap", "source_trust_gap", "evidence_conflict"},
    "abstain": {"authorization_gap", "evidence_conflict"},
}


def validate_samples(samples: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    stats = {
        "risk_level": Counter(),
        "gold_action": Counter(),
        "gap_type": Counter(),
        "support_label": Counter(),
    }

    for index, sample in enumerate(samples, start=1):
        sample_id = sample.get("id", f"line_{index}")
        missing_fields = sorted(REQUIRED_SAMPLE_FIELDS - set(sample))
        if missing_fields:
            errors.append(
                f"{sample_id}: missing required fields {', '.join(missing_fields)}"
            )
            continue

        if sample_id in seen_ids:
            errors.append(f"{sample_id}: duplicate sample id")
        seen_ids.add(sample_id)

        _count_and_validate(
            errors,
            stats["risk_level"],
            sample_id,
            "risk_level",
            sample["risk_level"],
            VALID_RISK_LEVELS,
        )
        _count_and_validate(
            errors,
            stats["gold_action"],
            sample_id,
            "gold_action",
            sample["gold_action"],
            VALID_ACTIONS,
        )
        _count_and_validate(
            errors,
            stats["gap_type"],
            sample_id,
            "gap_type",
            sample["gap_type"],
            VALID_GAP_TYPES,
        )
        _validate_action_gap_pair(errors, sample)
        _validate_missing_slots(errors, sample)
        _validate_claims(errors, stats["support_label"], sample)

    return {
        "valid": not errors,
        "sample_count": len(samples),
        "errors": errors,
        "stats": {name: dict(counter) for name, counter in stats.items()},
    }


def format_validation_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# CM-EGQA Dataset Validation",
        "",
        f"Valid: `{str(summary['valid']).lower()}`",
        f"Samples: `{summary['sample_count']}`",
        "",
        "## Label Distributions",
        "",
    ]
    for stat_name, counts in summary["stats"].items():
        lines.extend([f"### {stat_name}", "", "| Label | Count |", "|---|---:|"])
        for label, count in sorted(counts.items()):
            lines.append(f"| `{label}` | {count} |")
        lines.append("")

    lines.extend(["## Errors", ""])
    if summary["errors"]:
        lines.extend(f"- {error}" for error in summary["errors"])
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def _count_and_validate(
    errors: list[str],
    counter: Counter,
    sample_id: str,
    field: str,
    value: str,
    valid_values: set[str],
) -> None:
    counter[value] += 1
    if value not in valid_values:
        errors.append(
            f"{sample_id}: invalid {field} `{value}`, expected one of {sorted(valid_values)}"
        )


def _validate_action_gap_pair(errors: list[str], sample: dict[str, Any]) -> None:
    action = sample["gold_action"]
    gap_type = sample["gap_type"]
    compatible_gaps = ACTION_GAP_COMPATIBILITY.get(action)
    if compatible_gaps and gap_type not in compatible_gaps:
        expected = ", ".join(sorted(compatible_gaps))
        errors.append(
            f"{sample['id']}: gold_action `{action}` expects gap_type in [{expected}], got `{gap_type}`"
        )


def _validate_missing_slots(errors: list[str], sample: dict[str, Any]) -> None:
    missing_slots = sample["missing_slots"]
    if not isinstance(missing_slots, list):
        errors.append(f"{sample['id']}: missing_slots must be a list")
        return
    if sample["gold_action"] == "clarify" and not missing_slots:
        errors.append(f"{sample['id']}: clarify action requires at least one missing slot")


def _validate_claims(
    errors: list[str],
    support_counter: Counter,
    sample: dict[str, Any],
) -> None:
    claims = sample["gold_claims"]
    if not isinstance(claims, list) or not claims:
        errors.append(f"{sample['id']}: gold_claims must be a non-empty list")
        return
    for claim_index, claim in enumerate(claims, start=1):
        claim_ref = f"{sample['id']}:claim_{claim_index}"
        if "claim" not in claim or "support_label" not in claim:
            errors.append(f"{claim_ref}: claim and support_label are required")
            continue
        support_label = claim["support_label"]
        support_counter[support_label] += 1
        if support_label not in VALID_SUPPORT_LABELS:
            errors.append(
                f"{claim_ref}: invalid support_label `{support_label}`, expected one of {sorted(VALID_SUPPORT_LABELS)}"
            )
