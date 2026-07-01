"""Deterministic baseline and claim-authorization pipeline for the pilot."""

from __future__ import annotations

from typing import Any

from medclaimauth.retrieval import retrieve_evidence


def run_llm_only(
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    draft = _draft_answer(sample["question"], [])
    claims = _extract_claims(sample["question"], draft)
    verified_claims = _verify_claims(claims, sample, [])
    emitted_claims = [{**claim, "emitted": True} for claim in verified_claims]
    return {
        "id": sample["id"],
        "question": sample["question"],
        "risk_level": sample.get("risk_level", "medium"),
        "gold_action": sample.get("gold_action"),
        "gold_gap_type": sample.get("gap_type"),
        "action": "answer",
        "gap_type": "none",
        "retrieved_evidence_ids": [],
        "claims": emitted_claims,
        "final_answer": draft,
    }


def run_vanilla_rag(
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    retrieved = retrieve_evidence(sample["question"], evidence)
    draft = _draft_answer(sample["question"], retrieved)
    claims = _extract_claims(sample["question"], draft)
    verified_claims = _verify_claims(claims, sample, retrieved)
    emitted_claims = [{**claim, "emitted": True} for claim in verified_claims]
    return {
        "id": sample["id"],
        "question": sample["question"],
        "risk_level": sample.get("risk_level", "medium"),
        "gold_action": sample.get("gold_action"),
        "gold_gap_type": sample.get("gap_type"),
        "action": "answer",
        "gap_type": "none",
        "retrieved_evidence_ids": [item["evidence_id"] for item in retrieved],
        "claims": emitted_claims,
        "final_answer": draft,
    }


def run_query_rewrite_rag(
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    rewritten_query = _rewrite_query(sample)
    retrieved = retrieve_evidence(rewritten_query, evidence)
    draft = _draft_answer(sample["question"], retrieved)
    claims = _extract_claims(sample["question"], draft)
    verified_claims = _verify_claims(claims, sample, retrieved)
    emitted_claims = [{**claim, "emitted": True} for claim in verified_claims]
    return {
        "id": sample["id"],
        "question": sample["question"],
        "rewritten_query": rewritten_query,
        "risk_level": sample.get("risk_level", "medium"),
        "gold_action": sample.get("gold_action"),
        "gold_gap_type": sample.get("gap_type"),
        "action": "answer",
        "gap_type": "none",
        "retrieved_evidence_ids": [item["evidence_id"] for item in retrieved],
        "claims": emitted_claims,
        "final_answer": draft,
    }


def run_self_reflection_rag(
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    retrieved = retrieve_evidence(sample["question"], evidence)
    draft = _draft_answer(sample["question"], retrieved)
    claims = _extract_claims(sample["question"], draft)
    verified_claims = _verify_claims(claims, sample, retrieved)
    emitted_claims = [{**claim, "emitted": True} for claim in verified_claims]
    warning = ""
    if any(claim["support_label"] in {"unsupported", "not_authorized"} for claim in emitted_claims):
        warning = " 需要谨慎：上述建议仍需结合个人情况和医生判断。"
    return {
        "id": sample["id"],
        "question": sample["question"],
        "risk_level": sample.get("risk_level", "medium"),
        "gold_action": sample.get("gold_action"),
        "gold_gap_type": sample.get("gap_type"),
        "action": "answer",
        "gap_type": "self_reflection_only",
        "retrieved_evidence_ids": [item["evidence_id"] for item in retrieved],
        "claims": emitted_claims,
        "final_answer": draft + warning,
    }


def run_source_trust_rag(
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    retrieved = [
        item
        for item in retrieve_evidence(sample["question"], evidence)
        if item.get("source_level") == "high"
    ]
    draft = _draft_answer(sample["question"], retrieved)
    claims = _extract_claims(sample["question"], draft)
    verified_claims = _verify_claims(claims, sample, retrieved)
    emitted_claims = [{**claim, "emitted": True} for claim in verified_claims]
    return {
        "id": sample["id"],
        "question": sample["question"],
        "risk_level": sample.get("risk_level", "medium"),
        "gold_action": sample.get("gold_action"),
        "gold_gap_type": sample.get("gap_type"),
        "action": "answer",
        "gap_type": "none",
        "retrieved_evidence_ids": [item["evidence_id"] for item in retrieved],
        "claims": emitted_claims,
        "final_answer": draft,
    }


def run_claim_verification_only(
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    retrieved = retrieve_evidence(sample["question"], evidence)
    draft = _draft_answer(sample["question"], retrieved)
    claims = _extract_claims(sample["question"], draft)
    verified_claims = _verify_claims(claims, sample, retrieved)
    emitted_claims = [
        {
            **claim,
            "emitted": claim["support_label"] in {"supported", "partially_supported"},
        }
        for claim in verified_claims
    ]
    return {
        "id": sample["id"],
        "question": sample["question"],
        "risk_level": sample.get("risk_level", "medium"),
        "gold_action": sample.get("gold_action"),
        "gold_gap_type": sample.get("gap_type"),
        "action": "answer",
        "gap_type": "verification_only",
        "retrieved_evidence_ids": [item["evidence_id"] for item in retrieved],
        "claims": emitted_claims,
        "final_answer": _verification_only_answer(emitted_claims),
    }


def run_claim_authorization(
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    retrieved = retrieve_evidence(sample["question"], evidence)
    draft = _draft_answer(sample["question"], retrieved)
    claims = _extract_claims(sample["question"], draft)
    verified_claims = _verify_claims(claims, sample, retrieved)
    gap_type = _classify_gap(sample, verified_claims, retrieved)
    action = _decide_action(sample, verified_claims, gap_type)
    emitted_claims = _mark_emitted_claims(verified_claims, action)
    final_answer = _authorized_answer(sample, emitted_claims, action, gap_type)
    return {
        "id": sample["id"],
        "question": sample["question"],
        "risk_level": sample.get("risk_level", "medium"),
        "gold_action": sample.get("gold_action"),
        "gold_gap_type": sample.get("gap_type"),
        "action": action,
        "gap_type": gap_type,
        "retrieved_evidence_ids": [item["evidence_id"] for item in retrieved],
        "claims": emitted_claims,
        "final_answer": final_answer,
    }


def _draft_answer(question: str, evidence: list[dict[str, Any]]) -> str:
    if "布洛芬" in question:
        return "布洛芬可用于缓解头痛；根据资料，该患者可以直接服用布洛芬。"
    if "阿莫西林" in question or "抗生素" in question:
        return "抗生素可用于部分细菌感染；该患者可以直接使用阿莫西林。"
    if "胸痛" in question:
        return "胸痛可能与多种情况有关；如果突发胸痛，应及时就医。"
    if "降压药" in question or "血压" in question:
        return "高血压用药需要结合血压水平、合并疾病和既往用药；该患者可以自行调整降压药。"
    if "咳嗽" in question:
        return "普通咳嗽可能由感染、过敏或刺激引起；若症状持续或加重，需要就医评估。"
    if evidence:
        return f"根据检索证据，{evidence[0]['text']}"
    return "当前证据不足，无法给出可靠医学结论。"


def _extract_claims(question: str, answer: str) -> list[dict[str, Any]]:
    if "布洛芬" in question and "孕晚期" in question:
        return [
            {"claim": "孕晚期应避免使用布洛芬"},
            {"claim": "该患者可以直接服用布洛芬"},
        ]
    if "布洛芬" in question and "胃溃疡" in question:
        return [
            {"claim": "胃溃疡患者使用布洛芬需要谨慎"},
            {"claim": "该患者可以直接服用布洛芬"},
        ]
    if "布洛芬" in question:
        return [
            {"claim": "布洛芬可用于缓解头痛"},
            {"claim": "该患者可以直接服用布洛芬"},
        ]
    if "阿莫西林" in question or "抗生素" in question:
        return [
            {"claim": "抗生素可用于部分细菌感染"},
            {"claim": "该患者可以直接使用阿莫西林"},
        ]
    if "胸痛" in question:
        return [
            {"claim": "胸痛可能与多种情况有关"},
            {"claim": "突发胸痛应及时就医"},
        ]
    if "降压药" in question or "血压" in question:
        return [
            {"claim": "高血压用药需要结合血压水平和合并疾病"},
            {"claim": "该患者可以自行调整降压药"},
        ]
    if "咳嗽" in question:
        return [
            {"claim": "咳嗽可能由感染、过敏或刺激引起"},
            {"claim": "症状持续或加重需要就医评估"},
        ]
    return [{"claim": answer}]


def _verify_claims(
    claims: list[dict[str, Any]],
    sample: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    verified: list[dict[str, Any]] = []
    trusted_text = " ".join(
        item["text"] for item in evidence if item.get("source_level") == "high"
    )
    all_text = " ".join(item["text"] for item in evidence)
    missing_slots = sample.get("missing_slots", [])

    for claim in claims:
        text = claim["claim"]
        label = "unsupported"
        reason = "no_matching_evidence"
        if _is_patient_specific_treatment(text) and _has_known_contraindication(sample):
            label = "not_authorized"
            reason = "known_contraindication"
        elif _is_patient_specific_treatment(text) and missing_slots:
            label = "not_authorized"
            reason = "missing_patient_information"
        elif _is_supported_by_text(text, trusted_text):
            label = "supported"
            reason = "supported_by_high_trust_evidence"
        elif _is_supported_by_text(text, all_text):
            label = "partially_supported"
            reason = "supported_by_non_high_trust_evidence"
        verified.append({**claim, "support_label": label, "reason": reason})
    return verified


def _classify_gap(
    sample: dict[str, Any],
    claims: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
) -> str:
    labels = {claim["support_label"] for claim in claims}
    if "not_authorized" in labels and _has_known_contraindication(sample):
        return "authorization_gap"
    if "not_authorized" in labels and sample.get("missing_slots"):
        return "patient_info_gap"
    if not evidence:
        return "retrieval_gap"
    if labels == {"partially_supported"}:
        return "source_trust_gap"
    if "unsupported" in labels:
        return "retrieval_gap"
    return "none"


def _decide_action(
    sample: dict[str, Any],
    claims: list[dict[str, Any]],
    gap_type: str,
) -> str:
    if gap_type == "patient_info_gap":
        return "clarify"
    if gap_type == "retrieval_gap":
        return "retrieve_more"
    if gap_type == "source_trust_gap":
        return "retrieve_more"
    if gap_type == "authorization_gap":
        return "abstain"
    if any(claim["support_label"] == "contradicted" for claim in claims):
        return "abstain"
    return "answer"


def _authorized_answer(
    sample: dict[str, Any],
    claims: list[dict[str, Any]],
    action: str,
    gap_type: str,
) -> str:
    supported = [
        claim["claim"]
        for claim in claims
        if claim["support_label"] in {"supported", "partially_supported"}
    ]
    if action == "clarify":
        slots = "、".join(sample.get("missing_slots", []))
        base = "；".join(supported)
        return f"{base}。请补充{slots}后，才能判断是否适合给出具体用药建议。"
    if action == "retrieve_more":
        return "当前证据不足，需要继续检索更权威或更直接的医学证据。"
    if action == "abstain":
        return "当前信息不足或风险较高，不能给出具体诊疗结论，建议及时咨询医生。"
    if supported:
        return "；".join(supported) + "。"
    return "当前没有足够证据支持医学结论。"


def _verification_only_answer(claims: list[dict[str, Any]]) -> str:
    emitted = [
        claim["claim"]
        for claim in claims
        if claim["emitted"]
    ]
    if not emitted:
        return "当前没有足够证据支持医学结论。"
    return "；".join(emitted) + "。"


def _mark_emitted_claims(
    claims: list[dict[str, Any]],
    action: str,
) -> list[dict[str, Any]]:
    emitted_claims: list[dict[str, Any]] = []
    for claim in claims:
        if action in {"retrieve_more", "abstain"}:
            emitted = False
        else:
            emitted = claim["support_label"] in {"supported", "partially_supported"}
        emitted_claims.append({**claim, "emitted": emitted})
    return emitted_claims


def _is_patient_specific_treatment(claim: str) -> bool:
    direct_markers = ["该患者可以", "可以直接", "自行调整", "直接使用"]
    treatment_terms = ["服用", "使用", "调整", "阿莫西林", "布洛芬", "降压药"]
    return any(marker in claim for marker in direct_markers) and any(
        term in claim for term in treatment_terms
    )


def _rewrite_query(sample: dict[str, Any]) -> str:
    question = sample.get("question", "")
    slot_terms = " ".join(sample.get("missing_slots", []))
    safety_terms = "禁忌 慎用 权威证据 用药风险"
    return f"{question} {slot_terms} {safety_terms}".strip()


def _is_supported_by_text(claim: str, evidence_text: str) -> bool:
    if not evidence_text:
        return False
    support_patterns = {
        "布洛芬可用于缓解头痛": ["布洛芬", "缓解", "疼痛"],
        "孕晚期应避免使用布洛芬": ["孕晚期", "布洛芬", "避免"],
        "胃溃疡患者使用布洛芬需要谨慎": ["胃溃疡", "布洛芬", "谨慎"],
        "抗生素可用于部分细菌感染": ["抗生素", "细菌感染"],
        "胸痛可能与多种情况有关": ["胸痛", "多种原因"],
        "突发胸痛应及时就医": ["突发胸痛", "及时就医"],
        "高血压用药需要结合血压水平和合并疾病": ["高血压", "合并疾病"],
        "咳嗽可能由感染、过敏或刺激引起": ["咳嗽", "感染", "过敏"],
        "症状持续或加重需要就医评估": ["持续", "就医"],
    }
    required = support_patterns.get(claim)
    if required:
        return all(term in evidence_text for term in required)
    return claim in evidence_text


def _has_known_contraindication(sample: dict[str, Any]) -> bool:
    question = sample.get("question", "")
    contraindications = ["孕晚期", "胃溃疡", "严重肾功能不全", "抗凝药"]
    return any(term in question for term in contraindications)
