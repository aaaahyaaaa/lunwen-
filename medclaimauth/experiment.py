"""Run baseline comparisons for the CM-EGQA mini experiment."""

from __future__ import annotations

from typing import Any

from medclaimauth.metrics import compute_gap_confusion_matrix, compute_metrics
from medclaimauth.pipeline import (
    run_claim_authorization,
    run_claim_verification_only,
    run_llm_only,
    run_query_rewrite_rag,
    run_self_reflection_rag,
    run_source_trust_rag,
    run_vanilla_rag,
)


def compare_methods(
    samples: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    llm_only_predictions = [run_llm_only(sample, evidence) for sample in samples]
    vanilla_predictions = [run_vanilla_rag(sample, evidence) for sample in samples]
    rewrite_predictions = [
        run_query_rewrite_rag(sample, evidence) for sample in samples
    ]
    self_reflection_predictions = [
        run_self_reflection_rag(sample, evidence) for sample in samples
    ]
    source_trust_predictions = [
        run_source_trust_rag(sample, evidence) for sample in samples
    ]
    verification_only_predictions = [
        run_claim_verification_only(sample, evidence) for sample in samples
    ]
    authorization_predictions = [
        run_claim_authorization(sample, evidence) for sample in samples
    ]

    return {
        "metrics": {
            "llm_only": compute_metrics(llm_only_predictions),
            "vanilla_rag": compute_metrics(vanilla_predictions),
            "query_rewrite_rag": compute_metrics(rewrite_predictions),
            "self_reflection_rag": compute_metrics(self_reflection_predictions),
            "source_trust_rag": compute_metrics(source_trust_predictions),
            "claim_verification_only": compute_metrics(
                verification_only_predictions
            ),
            "claim_authorization": compute_metrics(authorization_predictions),
        },
        "predictions": {
            "llm_only": llm_only_predictions,
            "vanilla_rag": vanilla_predictions,
            "query_rewrite_rag": rewrite_predictions,
            "self_reflection_rag": self_reflection_predictions,
            "source_trust_rag": source_trust_predictions,
            "claim_verification_only": verification_only_predictions,
            "claim_authorization": authorization_predictions,
        },
        "gap_confusion": {
            "llm_only": compute_gap_confusion_matrix(llm_only_predictions),
            "vanilla_rag": compute_gap_confusion_matrix(vanilla_predictions),
            "query_rewrite_rag": compute_gap_confusion_matrix(rewrite_predictions),
            "self_reflection_rag": compute_gap_confusion_matrix(
                self_reflection_predictions
            ),
            "source_trust_rag": compute_gap_confusion_matrix(
                source_trust_predictions
            ),
            "claim_verification_only": compute_gap_confusion_matrix(
                verification_only_predictions
            ),
            "claim_authorization": compute_gap_confusion_matrix(
                authorization_predictions
            ),
        },
    }
