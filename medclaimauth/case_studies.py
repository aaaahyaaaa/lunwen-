"""Case-study selection and formatting for CM-EGQA reports."""

from __future__ import annotations

from typing import Any, Callable

from medclaimauth.metrics import UNSAFE_LABELS


def select_case_studies(
    report: dict[str, Any],
    method: str = "claim_authorization",
    baseline: str = "vanilla_rag",
) -> list[dict[str, Any]]:
    predictions = report["predictions"][method]
    baseline_by_id = {
        item["id"]: item for item in report["predictions"].get(baseline, [])
    }
    selectors: list[tuple[str, Callable[[dict[str, Any]], bool]]] = [
        (
            "clarification_success",
            lambda item: item.get("gold_action") == "clarify"
            and item.get("action") == "clarify",
        ),
        (
            "abstention_success",
            lambda item: item.get("gold_action") == "abstain"
            and item.get("action") == "abstain",
        ),
        (
            "action_mismatch",
            lambda item: item.get("gold_action") != item.get("action"),
        ),
    ]

    cases: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    for case_type, predicate in selectors:
        selected = next(
            (item for item in predictions if item["id"] not in used_ids and predicate(item)),
            None,
        )
        if selected is None:
            continue
        used_ids.add(selected["id"])
        cases.append(_build_case(case_type, selected, baseline_by_id.get(selected["id"])))
    return cases


def format_case_studies_markdown(cases: list[dict[str, Any]]) -> str:
    lines = ["# CM-EGQA Case Studies", ""]
    for case in cases:
        lines.extend(
            [
                f"## {case['case_type']}",
                "",
                f"- ID: `{case['id']}`",
                f"- Question: {case['question']}",
                f"- Gold action: `{case['gold_action']}`",
                f"- Baseline action: `{case['baseline_action']}`",
                f"- Authorized action: `{case['authorized_action']}`",
                f"- Gap type: `{case['gap_type']}`",
                f"- Unsafe baseline claims: {_format_list(case['unsafe_baseline_claims'])}",
                f"- Blocked authorized claims: {_format_list(case['blocked_authorized_claims'])}",
                f"- Final answer: {case['final_answer']}",
                "",
            ]
        )
    return "\n".join(lines)


def _build_case(
    case_type: str,
    prediction: dict[str, Any],
    baseline_prediction: dict[str, Any] | None,
) -> dict[str, Any]:
    baseline_claims = baseline_prediction.get("claims", []) if baseline_prediction else []
    return {
        "case_type": case_type,
        "id": prediction["id"],
        "question": prediction["question"],
        "gold_action": prediction.get("gold_action"),
        "baseline_action": baseline_prediction.get("action") if baseline_prediction else None,
        "authorized_action": prediction.get("action"),
        "gap_type": prediction.get("gap_type"),
        "retrieved_evidence_ids": prediction.get("retrieved_evidence_ids", []),
        "unsafe_baseline_claims": [
            claim["claim"]
            for claim in baseline_claims
            if claim.get("emitted", True) and claim.get("support_label") in UNSAFE_LABELS
        ],
        "blocked_authorized_claims": [
            claim["claim"] for claim in prediction.get("claims", []) if not claim.get("emitted", True)
        ],
        "final_answer": prediction.get("final_answer", ""),
    }


def _format_list(values: list[str]) -> str:
    if not values:
        return "None"
    return "; ".join(values)
