# CCF-A 相关期刊论文池与小论文 idea 收敛

日期：2026-06-15  
目标：围绕开题报告“医疗场景下大模型问答的幻觉抑制方法研究与实现”，从 CCF-A 相关期刊的高质量论文中反推一个 2026 年 10 月前可形成投稿稿件的小论文 idea。  
边界：毕业小论文以“可录用优先”，CCF-A 期刊作为 long-version 对齐方向；短期实验使用公开数据 + API。

## 1. 检索范围

### 1.1 CCF-A 期刊池

按 CCF 2026 第七版目录，和本题最相关的 A 类期刊分三层：

| 层级 | 期刊 | 为什么相关 | 本轮处理 |
|---|---|---|---|
| 核心 | TOIS, TKDE | 检索增强、知识图谱问答、查询理解、证据支持 | 重点找 paper |
| 次核心 | JMLR, AI, SCIS | RAG 基础模型、可信 AI、宽口径智能系统 | 找高相关 paper；无直接命中则作为定位参考 |
| 条件相关 | VLDBJ, TODS, TOCHI, IJHCS | 数据库/人机交互侧相关，但需题目转成数据系统或用户研究 | 只保留对 idea 有帮助的论文 |

补充判断：
- TPAMI/IJCV 是 AI A 类，但当前题目是文本医疗问答，不做医学影像/多模态时不主推。
- AIM（Artificial Intelligence in Medicine）在 CCF 2026 AI 目录中是 C 类，不是 A 类；但医学贴合度高，后续 Related Work 可以读。
- Bioinformatics 是交叉/综合/新兴 B 类；Self-BioRAG 等生物医学 RAG 论文很重要，但不能写成 CCF-A 期刊 paper。

### 1.2 检索式

使用 Crossref、出版商页面、JMLR 页面、ACM/IEEE/Springer/Elsevier 结果页交叉检索，关键词包括：

```text
retrieval augmented generation
medical question answering
healthcare question answering
knowledge graph question answering
GraphRAG
hallucination
source authentication
query performance prediction
question understanding
clarifying questions
abstention
uncertainty
atomic fact decomposition
```

时间范围以 2018-2026 为主，优先收录 journal paper；会议论文只放到“重要背景”。

## 2. CCF-A 期刊内必读论文池

### 2.1 TOIS: 检索、RAG、幻觉、医疗 QA

| 论文 | 作用 | 对选题的启发 |
|---|---|---|
| Huang et al., *A Survey on Hallucination in Large Language Models*, TOIS, DOI: https://doi.org/10.1145/3703155 | 幻觉定义、检测、缓解 taxonomy | 小论文不能只说“减少幻觉”，必须定义 unsupported claim / evidence inconsistency 等可测指标 |
| *Graph Retrieval-Augmented Generation: A Survey*, TOIS, DOI: https://doi.org/10.1145/3777378 | GraphRAG 综述 | 如果想冲 TOIS/TKDE，贡献要落到图检索/证据组织机制，而不是普通应用 |
| *Augmenting Small Language Model for Better Medical Question Answering through Source Authentication*, TOIS, DOI: https://doi.org/10.1145/3797887 | 医疗 QA + 来源认证 | 非常关键：说明“证据来源可信度”本身可以作为医疗 QA 的核心变量 |
| *RAQG-QPP: Query Performance Prediction with Retrieved Query Variants and Retrieval Augmented Query Generation*, TOIS, DOI: https://doi.org/10.1145/3815198 | 查询性能预测 + RAG | 可借鉴为“预测一个医疗问题是否适合直接 RAG 回答” |
| *Dynamic Graph Reasoning for Conversational Open-Domain Question Answering*, TOIS, DOI: https://doi.org/10.1145/3498557 | 对话 QA 的动态图推理 | 医疗问诊天然多轮/多意图，可从动态图证据链学习 |
| *Hop-wise Planning with Iterative Explainable Self-Correction for Knowledge Base Question Answering*, TOIS, DOI: https://doi.org/10.1145/3819823 | 分步规划 + 可解释自纠错 | 支撑“先规划证据路径，再生成答案”的设计 |
| *Question Answering in Knowledge Bases*, TOIS, DOI: https://doi.org/10.1145/3345557 | KBQA 经典综述 | Related Work 中用于界定 KBQA 与 RAG/GraphRAG 的关系 |

### 2.2 TKDE: 复杂问答、知识图谱、医疗 GraphRAG

| 论文 | 作用 | 对选题的启发 |
|---|---|---|
| *DUAL-Know: A Description-Augmented and Uncertainty-Aware GraphRAG Framework for Anesthesiology Question Answering*, TKDE, DOI: https://doi.org/10.1109/TKDE.2026.3700611 | 医疗专科 QA + GraphRAG + uncertainty | 说明“医疗 GraphRAG + 不确定性”已经有人做，不能只重复 GraphRAG |
| *How Context or Knowledge Can Benefit Healthcare Question Answering*, TKDE, DOI: https://doi.org/10.1109/TKDE.2021.3090253 | 医疗 QA 中上下文/知识的价值 | 作为医疗 QA 知识增强的早期基线和动机来源 |
| *XMQAs: Constructing Complex-Modified Question-Answering Dataset for Robust Question Understanding*, TKDE, DOI: https://doi.org/10.1109/TKDE.2023.3303916 | 复杂变形问题鲁棒理解数据集 | 强提示：可以做“中文医疗问题复杂变形/歧义扰动”评测集 |
| *Complex Knowledge Base Question Answering: A Survey*, TKDE, DOI: https://doi.org/10.1109/TKDE.2022.3223858 | 复杂 KBQA 综述 | 帮助定义多跳、多约束、多意图问题类型 |
| *Atomic Fact Decomposition Helps Attributed Question Answering*, TKDE, DOI: https://doi.org/10.1109/TKDE.2025.3608716 | 断言/原子事实拆分 + attribution | 很适合医疗幻觉评测：把答案拆成医学断言逐条验支持 |
| *Efficient LLM-Based Subgraph Retrieval for Multi-Hop Knowledge Base Question Answering*, TKDE, DOI: https://doi.org/10.1109/TKDE.2026.3679080 | LLM 辅助子图检索 | 可作为图检索 baseline 或 long-version 扩展方向 |
| *A Framework of Knowledge Graph-Enhanced Large Language Model Based on Global Planning*, TKDE, DOI: https://doi.org/10.1109/TKDE.2025.3639599 | KG-enhanced LLM + 全局规划 | 证明“规划式证据组织”是可发表方向 |

### 2.3 JMLR / SCIS / HCI 期刊中的相关支撑

| 期刊 | 论文 | 作用 | 是否核心 |
|---|---|---|---|
| JMLR | *Atlas: Few-shot Learning with Retrieval Augmented Language Models*, https://jmlr.org/papers/v24/23-0037.html | RAG 基础模型和少样本知识密集任务 | 背景必读 |
| SCIS | *RAG-leaks: Difficulty-Calibrated Membership Inference Attacks on Retrieval-Augmented Generation*, DOI: https://doi.org/10.1007/s11432-024-4441-4 | RAG 样本难度校准思想 | 可借鉴“difficulty-calibrated” |
| SCIS | *CT-Agent: a Multimodal-LLM Agent for 3D CT Radiology Question Answering*, DOI: https://doi.org/10.1007/s11432-025-4818-7 | 医疗影像 QA agent | 当前文本方向不主读，若转多模态再读 |
| SCIS | *Towards Multimodal Graph Large Language Model*, DOI: https://doi.org/10.1007/s11432-025-4627-3 | 图 + 多模态 LLM | long-version 可参考 |
| IJHCS | *Confronting Verbalized Uncertainty: Understanding How LLM's Verbalized Uncertainty Influences Users in AI-assisted Decision-making*, DOI: https://doi.org/10.1016/j.ijhcs.2025.103455 | LLM 不确定性表达与用户决策 | 若加入“澄清/拒答的用户接受度”再读 |
| IJHCS | *Who Needs Explanation and When? Juggling Explainable AI and User Epistemic Uncertainty*, DOI: https://doi.org/10.1016/j.ijhcs.2022.102839 | 解释与用户不确定性 | 支撑“何时给证据解释/何时拒答” |
| TODS | *DomainNet: Homograph Detection and Understanding in Data Lake Disambiguation*, DOI: https://doi.org/10.1145/3612919 | 同形异义/歧义检测 | 可借鉴到医学缩写/术语歧义，但数据库味较重 |

## 3. 非 CCF-A 但必须读的背景论文

这些论文不属于上面的 CCF-A 期刊池，但对医疗 RAG 选题非常关键：

| 论文 | 来源 | 为什么必须读 |
|---|---|---|
| MIRAGE: A Benchmark for Medical RAG, https://arxiv.org/abs/2402.13178 | arXiv | 指出 medical RAG 组件组合和最佳实践仍未清晰 |
| RAG^2 / RAG2 medical QA benchmark, NAACL 2025, https://aclanthology.org/2025.naacl-long.635/ | ACL Anthology | 指出医疗查询不够 targeted、检索器偏差等问题 |
| MedHalu, https://arxiv.org/html/2409.19492v3 | arXiv | 强调真实患者问题和考试题不同，适合支撑 patient-style query |
| Self-BioRAG, https://academic.oup.com/bioinformatics/article/40/Supplement_1/i119/7700892 | Bioinformatics | 生物医学 RAG + 自反思，重要 baseline |
| MEGA-RAG, https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1635381/full | Frontiers in Public Health | 多证据/图式 medical RAG 背景 |
| Almanac: Retrieval-Augmented Language Models for Clinical Medicine, https://ai.nejm.org/doi/full/10.1056/AIoa2300068 | NEJM AI | 临床 RAG 应用标杆 |
| Med-PaLM / Med-PaLM 2, Nature / Nature Medicine | Nature 系列 | 医疗 LLM 评估与安全性背景 |

## 3.1 飞书资料库补充

参考文档：`https://bytedance.sg.larkoffice.com/docx/B2whdHfOqoduTXx1Dk1ckVBTnpe`，revision `553`。

这个文档更像研究资料索引库，而不是单篇论文。对本题最有用的部分是：

| 章节 | 关键资料 | 对选题的影响 |
|---|---|---|
| GraphRAG + RAG | From Local to Global: A Graph RAG Approach to Query-Focused Summarization; Seven Failure Points When Engineering a RAG System; HybridRAG; Agentic RAG; Microsoft GraphRAG; Awesome-GraphRAG | 说明 RAG 失败点、Hybrid RAG、GraphRAG、Agentic RAG 已有大量材料；小论文需要从“何时/为何失败”切入，而不是只堆组件 |
| 知识图谱 + 大模型 | Unifying Large Language Models and Knowledge Graphs: A Roadmap | 支撑 KG+LLM 是大方向，但不应把“融合 KG 和 LLM”本身当创新点 |
| 评测集 | ReviewEval | 不是医疗 QA，但提醒评测框架要明确任务、样本构造、评分维度和人工校验 |
| 论文总结集合 | awesome-ai-papers, Top AI Agent Papers | 可作后续找背景资料入口，不作为核心证据 |

补充约束：
- 文档中的微信、博客、工程实战资料适合帮助搭系统和理解范式，不适合直接作为论文核心引用。
- 文档强化了一个判断：**更稳的小论文切口应该围绕 RAG 失败诊断、风险路由和评测，而不是泛泛实现 GraphRAG**。
- 内嵌的 `Github - graphify 分享` 文档当前 user 身份无权限读取，后续若拿到权限，可再补知识图谱构建工具链细节。

## 4. 主题聚类与 gap

### 4.1 现有论文已经覆盖什么

1. **医疗 QA 需要外部知识/上下文**  
   TKDE 2021 已经证明 context / knowledge 对 healthcare QA 有价值，后续工作不应再把“加知识会更好”作为主要新意。

2. **GraphRAG / 医疗 GraphRAG 正在成为强基线**  
   TOIS GraphRAG Survey 和 TKDE DUAL-Know 说明，仅提出“医学知识图谱 + RAG”已经不够新。

3. **RAG 的查询质量和性能预测开始出现**  
   TOIS RAQG-QPP 说明“预测检索/生成是否会有效”是 TOIS 认可的检索问题，但它不是医疗专用。

4. **复杂问题理解是独立贡献点**  
   TKDE XMQAs 表明“问题复杂变形/鲁棒理解数据集”可以成为可发表贡献。

5. **答案需要拆成原子事实评估证据支持**  
   TKDE Atomic Fact Decomposition 为“医疗回答逐条断言评估”提供了直接方法依据。

6. **来源认证开始进入医疗 QA**  
   TOIS 2026 Source Authentication 很关键：医疗 QA 不能只看检索相关性，还要看来源可信度。

7. **RAG 工程失败点本身值得被任务化评估**  
   飞书资料库里的 *Seven Failure Points When Engineering a RAG System*、HybridRAG、Agentic RAG 和 Microsoft GraphRAG 资料提示：实际 RAG 失败不只来自生成模型，还来自索引、检索、证据组织、上下文集成、路由和反思链路。医疗场景可以把这些失败点具体化为可测风险标签。

### 4.2 还没被充分合并的 gap

最有价值的空白不是“再做一个 GraphRAG”，而是：

> 面向真实中文患者问题，如何在回答前预测 RAG 失败风险，并把风险分解为查询复杂度、术语歧义、检索失败、来源可信度和证据支持缺口，从而决定直接回答、分解/消歧、Hybrid/Graph 检索、澄清或拒答？

这个 gap 同时对齐：
- TOIS 的 query performance prediction / source authentication / hallucination taxonomy；
- TKDE 的 healthcare QA / complex QA / atomic fact attribution / uncertainty-aware GraphRAG；
- 你的开题报告中的多意图识别、词义消歧、医学三元图检索、自反思校验。

## 5. Idea 候选

### Candidate A: ClinRisk-RAG（首推）

**题目候选**：ClinRisk-RAG: Risk-Routed Retrieval-Augmented Generation for Chinese Patient Medical Question Answering

**一句话**：不是让所有中文患者问题直接进 RAG，而是先预测“这个问题会在哪一环失败”，再按风险类型路由到直接检索、问题分解、术语消歧、Hybrid/Graph 检索、来源认证检索、澄清或拒答。

**核心贡献**：
- 构造一个中文患者问题风险评测集，覆盖多意图、术语歧义、问题复杂变形、证据不足、来源冲突。
- 设计 `RiskProfile = {query_complexity, term_ambiguity, retrieval_risk, source_reliability, evidence_gap, answerability}`。
- 路由动作：`direct_rag`, `decompose`, `disambiguate`, `hybrid_graph_retrieve`, `source_auth_retrieve`, `clarify`, `abstain`。
- 用 atomic fact decomposition 评估回答中的医学断言是否被证据支持。

**为什么比上一版 QSem-RAG 更稳**：
- 不只讲“语义质量”，而是把 TOIS Source Authentication、TOIS QPP、TKDE XMQAs、TKDE Atomic Fact Decomposition 串成一个更强的研究问题。
- 飞书资料库进一步补强了 RAG 工程失败点、HybridRAG、GraphRAG、Agentic RAG 的材料基础，使 `retrieval_risk` 和 `hybrid_graph_retrieve` 不显得凭空添加。
- 更像 CCF-A 期刊会认可的问题：查询风险预测 + 证据来源可信 + answerability routing。
- 短期可以先投会议/非 A 期刊，长期可以扩展成 TKDE/TOIS 风格 paper。

**最小实验**：
- 数据：MedDialog-CN / CMedQA / 中文医学公开 QA，外加 CMeIE/CMeEE 做实体和关系辅助。
- 构造：从原始 QA 改写出 5 类风险 query：多意图、术语歧义、复杂修饰、检索失败、证据不足。
- 基线：LLM only, vanilla RAG, query rewrite RAG, GraphRAG, self-reflection RAG。
- 指标：unsupported claim rate、evidence precision、abstention/clarification accuracy、answer correctness、cost/latency。

**风险**：
- 若数据构造太人工，会被质疑 benchmark 真实性；需要从真实患者问法抽样，并保留改写规则。
- 若路由全靠 LLM prompt，会被质疑方法浅；最好训练/蒸馏一个轻量 risk classifier 或做规则+LLM 混合。

### Candidate B: MedXMQA-CN

**题目候选**：MedXMQA-CN: A Complex-Modified Chinese Medical QA Benchmark for Robust RAG Evaluation

**一句话**：仿照 TKDE XMQAs，把中文医疗 QA 改造成复杂变形问答 benchmark，专门测 RAG 在患者式复杂问法下的鲁棒性。

**优点**：最容易 10 月前做完；数据集贡献清楚。  
**缺点**：方法贡献较弱，可能更像资源论文；若无医生校验，质量风险较高。

### Candidate C: FactTrace-MedRAG

**题目候选**：FactTrace-MedRAG: Atomic Evidence Attribution for Reducing Unsupported Claims in Chinese Medical RAG

**一句话**：把医疗回答拆成原子医学断言，再逐条找证据支持，最后用证据缺口触发修订或拒答。

**优点**：和幻觉评估强相关，容易写得严谨。  
**缺点**：和 TKDE Atomic Fact Decomposition 太近，需要医疗领域适配和中文证据链做出差异。

## 6. 最终建议

首推 **ClinRisk-RAG**。

它不是上一轮的 `QSem-RAG` 简单改名，而是从 CCF-A 期刊论文池反推出来的新收敛：

```text
TOIS Source Authentication
      + TOIS Query Performance Prediction
      + TKDE Complex-Modified QA
      + TKDE Uncertainty-Aware GraphRAG
      + TKDE Atomic Fact Attribution
      -> ClinRisk-RAG
```

可写成的小论文核心问题：

> 在中文医疗问答中，能否通过回答前的查询风险画像和来源可信检索路由，降低 RAG 系统的 unsupported medical claims，同时保持可接受的回答覆盖率？

建议短期不要把创新点写成“我做了医疗 GraphRAG”，而写成：

1. **风险画像**：把真实患者问题的回答风险拆成复杂度、歧义、来源可信度、证据缺口。
2. **风险路由**：不同风险走不同处理动作，而不是统一 query rewrite。
3. **证据化评估**：用 atomic fact support 衡量 hallucination，而不是只看 BLEU/ROUGE 或主观评分。

## 7. 10 月前执行路线

| 时间 | 任务 | 产物 |
|---|---|---|
| 6 月下旬 | 精读必读论文 12-15 篇，完成 Related Work matrix | 论文矩阵 + gap 图 |
| 7 月上旬 | 整理公开中文医疗 QA 数据，定义 4 类 risk query | 数据构造脚本 + 500-1000 条评测集 |
| 7 月中旬 | 实现 baseline：LLM only / vanilla RAG / rewrite RAG / self-reflection RAG | baseline 表 |
| 7 月下旬 | 实现 ClinRisk router：risk profile + action routing | 方法原型 |
| 8 月上旬 | 做主实验和消融：去掉 risk、source auth、atomic fact checker | 主表 + 消融表 |
| 8 月中旬 | 人工抽检 100 条，确认 unsupported claim 标注可靠 | 人工评估表 |
| 8 月下旬 | 写第一版论文 | 6-8 页初稿 |
| 9 月 | 补实验、改 Related Work、定投稿目标 | 投稿版 |

## 8. 下一轮应精读的 12 篇

1. TOIS - Augmenting Small Language Model for Better Medical Question Answering through Source Authentication.
2. TKDE - DUAL-Know: Description-Augmented and Uncertainty-Aware GraphRAG for Anesthesiology QA.
3. TOIS - RAQG-QPP: Query Performance Prediction with Retrieved Query Variants and RAG.
4. TKDE - XMQAs: Complex-Modified QA Dataset for Robust Question Understanding.
5. TKDE - Atomic Fact Decomposition Helps Attributed Question Answering.
6. TOIS - A Survey on Hallucination in Large Language Models.
7. TOIS - Graph Retrieval-Augmented Generation: A Survey.
8. TKDE - How Context or Knowledge Can Benefit Healthcare Question Answering.
9. JMLR - Atlas: Few-shot Learning with Retrieval Augmented Language Models.
10. MIRAGE medical RAG benchmark.
11. MedHalu.
12. Self-BioRAG.
