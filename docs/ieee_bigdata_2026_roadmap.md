# IEEE BigData 2026 Main-Conference Roadmap

## Target

**Conference:** IEEE International Conference on Big Data 2026  
**Track framing:** Main conference first; healthcare/data-centric benchmark framing as the natural fit.  
**Working title:** CM-EGQA: Risk-Calibrated Claim Authorization for Safer Chinese Medical RAG

Official constraints checked on 2026-07-01:

| Item | Current official information |
|---|---|
| CFP | https://bigdataieee.org/BigData2026/calls/papers/ |
| Deadline | 2026-08-21 |
| Notification | 2026-10-24 |
| Camera-ready | 2026-11-14 |
| Conference | 2026-12-14 to 2026-12-17, Phoenix, AZ, USA |
| Format | IEEE Computer Society Proceedings, up to 10 pages, references counted |
| Review | Single-blind |

## BigData Fit

The paper should not be framed as "a medical chatbot." It should be framed as a Big Data paper about **responsible dataset development and evaluation for high-risk medical RAG**.

The strongest CFP mappings are:

- **Big Data for Science / Medicine and Health Science**
- **Big Data Benchmarks / Responsible Dataset Development**
- **Big Data Benchmarks / Benchmarks and Evaluation Frameworks**
- **Data Ecosystem / Trust management in Big Data systems**
- **Foundation Models for Big Data / Prompt Engineering and Management**

## Core Claim

The falsifiable claim:

> Risk-calibrated claim authorization can reduce high-risk unsupported medical claims in Chinese patient-style RAG while keeping the safety-coverage trade-off measurable rather than hidden behind generic abstention.

This is stronger than:

> We build a Dynamic Evidence Tree medical RAG system.

DET can remain an internal representation, but the main contribution is **claim-level authorization under evidence gaps**.

## Current State

Implemented mini pilot:

- `data/cm_egqa_mini.jsonl`: 10 seed samples
- `data/evidence_corpus.jsonl`: 10 seed evidence records
- `medclaimauth/`: deterministic pilot package
- `tests/`: unit tests for schema, authorization, metrics, and CLI
- `outputs/mini_experiment_report.md`: reproducible pilot report
- `outputs/dataset_validation.md`: dataset QA and label-distribution report
- `outputs/case_studies.md`: paper-ready case-study candidates
- `outputs/tables/`: CSV tables for paper figures and progress slides
- `outputs/cm_egqa_progress_report.pptx`: teacher progress-report deck draft
- `docs/cm_egqa_annotation_guidelines.md`: dataset expansion and annotation rules
- `docs/source_repo_audit.md`: reusable information from `medicalLLM`, `lunwen-`, and `intent-router`

Run:

```bash
python3 -m unittest \
  tests/test_claim_authorization.py \
  tests/test_run_experiment_cli.py \
  tests/test_dataset_validation.py \
  tests/test_case_studies.py \
  tests/test_export_tables.py
python3 -m medclaimauth.run_experiment \
  --samples data/cm_egqa_mini.jsonl \
  --evidence data/evidence_corpus.jsonl \
  --output-json outputs/mini_experiment_report.json \
  --output-md outputs/mini_experiment_report.md
python3 -m medclaimauth.validate_dataset \
  --samples data/cm_egqa_mini.jsonl \
  --output-json outputs/dataset_validation.json \
  --output-md outputs/dataset_validation.md
python3 -m medclaimauth.export_case_studies \
  --samples data/cm_egqa_mini.jsonl \
  --evidence data/evidence_corpus.jsonl \
  --output-json outputs/case_studies.json \
  --output-md outputs/case_studies.md
python3 -m medclaimauth.export_tables \
  --report-json outputs/mini_experiment_report.json \
  --output-dir outputs/tables
```

Current mini result:

| Metric | LLM Only | Vanilla RAG | Query Rewrite | Self-Reflection | Source-Trust | Verification Only | Authorization |
|---|---:|---:|---:|---:|---:|---:|---:|
| Unsupported Claim Rate | 1.0000 | 0.3500 | 0.3500 | 0.3500 | 0.3500 | 0.0000 | 0.0000 |
| Risk-Weighted Unsupported Claim Rate | 1.0000 | 0.3824 | 0.3824 | 0.3824 | 0.3824 | 0.0000 | 0.0000 |
| Unsafe Direct Answer Rate | 1.0000 | 0.8571 | 0.8571 | 0.8571 | 0.8571 | 0.0000 | 0.0000 |
| Necessary Clarification Recall | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| Gap Type Accuracy | 0.4000 | 0.4000 | 0.4000 | 0.0000 | 0.4000 | 0.0000 | 0.9000 |
| Answer Coverage | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3000 |
| Action Accuracy | 0.4000 | 0.4000 | 0.4000 | 0.4000 | 0.4000 | 0.4000 | 0.9000 |

Interpretation:

- LLM-only answers without evidence and emits unsafe claims in every audited claim in this mini setting.
- Query rewriting, source-trust filtering, and post-hoc self-reflection do not fix patient-information or authorization gaps.
- Claim verification alone filters unsafe claims, but still answers instead of clarifying or abstaining.
- The authorization method blocks unsafe claims and improves action/gap accuracy, but reduces direct-answer coverage.
- This is the right early signal: the paper can study the **safety-coverage trade-off** instead of pretending safety is free.

## Minimum Publishable Contribution

For a BigData main-conference attempt, the minimum credible package is:

1. **Dataset contribution:** CM-EGQA with 500-700 Chinese patient-style medical QA items.
2. **Taxonomy contribution:** Evidence-gap labels:
   - `none`
   - `retrieval_gap`
   - `patient_info_gap`
   - `source_trust_gap`
   - `evidence_conflict`
   - `authorization_gap`
3. **Method contribution:** Risk-calibrated claim authorization:
   - retrieve evidence
   - draft answer
   - extract medical claims
   - verify claim support
   - classify evidence gap
   - decide answer / clarify / retrieve_more / abstain
4. **Evaluation contribution:** Safety and coverage metrics:
   - Unsupported Claim Rate
   - Risk-Weighted Unsupported Claim Rate
   - Unsafe Direct Answer Rate
   - Necessary Clarification Recall
   - Answer Coverage
   - Response Coverage
   - Over-Abstention Rate
   - Action Accuracy
5. **Empirical contribution:** Baseline and ablation comparison.

## Required Baselines

Implemented smoke-test baselines:

| Baseline | Current status |
|---|---|
| LLM only | Implemented as deterministic no-retrieval hallucination-risk baseline |
| Vanilla RAG | Implemented |
| Query Rewrite RAG | Implemented as deterministic retrieval-query expansion |
| Self-Reflection RAG | Implemented as post-hoc warning without action-policy baseline |
| Source-Trust RAG | Implemented as high-trust evidence filtering baseline |
| Claim Verification Only | Implemented as verification without action policy |
| Full Claim Authorization | Implemented |

For submission, still strengthen:

| Baseline | Purpose |
|---|---|
| LLM-backed LLM only | Replace deterministic draft with a real model call |
| LLM-backed Self-Reflection RAG | Test whether a real reflection prompt changes the safety/coverage trade-off |
| GraphRAG / FAISS RAG | Use `medicalLLM/medical-rag` as stronger retrieval baseline source |
| Source-Trust RAG on source-trust cases | Requires 100-item pilot with low-trust and conflicting evidence |

Optional if time allows:

- Hybrid / GraphRAG
- MedTrust-like iterative retrieval-verification
- Flat evidence table vs. Dynamic Evidence Tree

## Ablations

| Ablation | Question |
|---|---|
| w/o risk level | Does risk weighting matter? |
| w/o gap classifier | Is unsupported/supported too coarse? |
| w/o clarification | Do missing patient slots cause unsafe direct answers? |
| w/o abstention | Does refusing high-risk answers help? |
| w/o source trust | Does evidence authority matter? |
| flat table instead of tree | Is the tree representation actually useful? |

## Data Expansion Plan

Stage 1: 100-item pilot by 2026-07-10

- 30 ordinary answerable questions
- 20 missing patient-information questions
- 15 medication contraindication questions
- 15 emergency/urgent-risk questions
- 10 source-trust questions
- 10 evidence-conflict or retrieval-gap questions

Gate:

- Full method must reduce `RW-UCR` by at least 40% vs. vanilla RAG.
- Full method must reduce `Unsafe Direct Answer Rate`.
- `Over-Abstention Rate` should stay below 0.20.
- `Necessary Clarification Recall` should exceed 0.70.

Stage 2: 300-item pre-submission pilot by 2026-07-25

- Replace deterministic smoke-test baselines with LLM-backed or retrieval-backed variants where feasible.
- Add inter-annotator agreement on at least 50 manually reviewed items.
- Produce first main table and 3 case studies.

Stage 3: 500-700 item submission set by 2026-08-08

- Freeze dataset schema.
- Freeze metrics.
- Run baselines and ablations.
- Produce final figures/tables.

## Paper Outline

Target length: 10 pages including references.

1. Introduction
   - Patient-style medical RAG fails when evidence is incomplete.
   - The core risk is not only wrong answers, but unsupported medical claims that should never be authorized.
   - Contributions: dataset, taxonomy, method, metrics, empirical study.
2. Related Work
   - Medical RAG and medical QA benchmarks.
   - RAG hallucination and attribution.
   - Source authentication.
   - Claim/fact decomposition.
   - Abstention and clarification.
3. CM-EGQA Dataset
   - Data sources and construction.
   - Evidence-gap taxonomy.
   - Claim support labels.
   - Annotation protocol.
4. Method
   - Retrieval.
   - Claim extraction.
   - Claim-evidence verification.
   - Gap classification.
   - Action policy.
5. Experiments
   - Baselines.
   - Metrics.
   - Main results.
   - Ablations.
6. Case Study and Error Analysis
   - Successful clarification.
   - Successful abstention.
   - Failure case.
7. Limitations
   - Dataset size.
   - LLM-judge risk.
   - Medical expert validation still limited.
8. Conclusion

## Next Implementation Tasks

Priority 1:

- Expand `cm_egqa_mini.jsonl` to 100 examples.
- Integrate `intent-router` labels as optional `intent_labels` for data expansion.
- Add retrieval/source-trust/evidence-conflict samples so the new baselines are meaningful.

Priority 2:

- Add 100-item annotation QA report with label distributions and failed checks.
- Add 3 manually reviewed case studies with expert comments.
- Decide whether `Q_sem` is a formal method module or a future upstream gate.

Priority 3:

- Replace keyword retriever with BM25 or embedding retriever.
- Add LLM-backed draft generation and claim extraction.
- Add human annotation sheet export.

## Kill Criteria

Stop or reframe if any of these happen after the 100-item pilot:

- Full method does not reduce `RW-UCR` against a stronger baseline.
- Safety improvement is achieved only by excessive abstention.
- Gap labels are too ambiguous for humans to annotate consistently.
- The tree representation has no measurable value over flat claim-evidence records.
