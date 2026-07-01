# 三个源仓库可用信息审计

## 审计范围

本文件记录截图中三个 GitHub 仓库对当前论文方向的可复用信息：

- `github.com/aaaahyaaaa/medicalLLM`
- `github.com/aaaahyaaaa/lunwen-`
- `github.com/aaaahyaaaa/intent-router`

当前论文主线是：**CM-EGQA：面向中文医疗 RAG 的风险校准断言授权**。

## 访问状态

| 仓库 | 可见性 | 当前访问情况 | 已核验事实 |
|---|---|---|---|
| `medicalLLM` | 私有 | `gh api` 可读，当前权限为 `ADMIN`；如果要本地 clone，还需要配置 HTTPS git 凭据 | 默认分支 `main`；最近推送时间 `2026-06-19T15:05:54Z`；最新提交信息为 `Update intent router experiments`；顶层目录包括 `intent-router`、`jmir`、`medical-rag` |
| `lunwen-` | 公开 | 当前本地目录就是该仓库的 checkout | 默认分支 `main`；本地 `HEAD` 是 `a5e1952 Document paper note upload format`；本地已有 CM-EGQA pilot 代码与数据，远端基线还没有这些新增内容 |
| `intent-router` | 私有 | `gh api` 可读，当前权限为 `ADMIN`；如果要本地 clone，还需要配置 HTTPS git 凭据 | 默认分支 `main`；最近推送时间 `2026-05-11T14:13:37Z`；顶层目录包括 `configs`、`data`、`docs`、`prompts`、`reports`、`scripts` |

## 可复用信息

### `intent-router`

最适合作为当前方法的上游 **Risk & Intent Gate**。

可复用内容：

- 已有医学多意图标签体系，共 12 个一级标签：
  - 症状描述
  - 疾病诊断
  - 病因咨询
  - 检查检验
  - 检查结果解读
  - 治疗方案
  - 用药咨询
  - 风险并发症
  - 预后恢复
  - 生活方式与注意事项
  - 就医科室与流程
  - 其他
- 标注策略支持多标签、主标签，以及单问题最多 4 个标签。
- 已有流程：
  - 构造患者问题
  - 抽样 200-500 条问题做人工标注
  - 运行弱监督标注
  - 过滤弱标签
  - 训练 TF-IDF baseline
  - 抽样弱标签做人工复核
- 已有报告目录包括 `tfidf_baseline_intent_v0.1` 和 `tfidf_baseline_intent_v0.1_weak`。

迁移建议：

- 把 12 个意图标签作为 CM-EGQA 后续字段 `intent_labels` 的第一版来源。
- 用 `用药咨询`、`检查结果解读`、`就医科室与流程`、`风险并发症` 这些高风险意图来指导 100 条 pilot 扩容。
- 复用弱标签抽检流程，作为 CM-EGQA 标注质量控制模板。
- 后续可以把 `Q_sem` 接成断言授权前的输入质量分数，但不建议让它承担论文主创新。

### `medicalLLM`

最适合作为既有实验和 baseline 工程来源。

可复用内容：

- `intent-router/` 中有更新后的 `Q_sem` 与 RQ 实验说明：
  - `Q_sem` 由意图置信度、文本完整性、医学线索和路由可靠性组成。
  - 低质量输入评估覆盖缺失关键信息、多意图纠缠、术语歧义和错误医学前提。
  - RQ3 小型 RAG 代理实验显示，baseline direct RAG 的 `unsafe_direct_answer_rate` 为 `1.000`，`Q_sem v0.2` 路由后降到 `0.010`。
- `medical-rag/` 中有 GraphRAG、FAISS、RAG 脚手架：
  - `settings.yaml`
  - parquet 输入管线
  - OpenAI embedding/chat 配置
  - GraphRAG 配置中已启用 claim extraction
  - local/global search 设置
- `jmir/imcs21-main/` 可以作为医疗咨询任务参考，但不能直接当作 CM-EGQA 标签体系。

迁移建议：

- 把 `Q_sem` 定位为未来的输入质量门控模块。
- 把 `medical-rag/` 用作 vanilla RAG、GraphRAG 或 FAISS 检索 baseline 的工程参考。
- `jmir` 只用于医疗问诊风格和任务背景参考；CM-EGQA 仍需要重新标注 `gap_type`、`gold_action` 和 `not_authorized`。

### `lunwen-`

这是当前论文和实验的主工作区。

可复用内容：

- `medclaimauth/`：确定性的断言授权 pilot 代码。
- `data/cm_egqa_mini.jsonl`：10 条种子医疗 QA 样本。
- `data/evidence_corpus.jsonl`：10 条种子证据。
- `docs/ieee_bigdata_2026_roadmap.md`：投稿路线。
- `docs/cm_egqa_annotation_guidelines.md`：标注规范。
- `outputs/mini_experiment_report.md`：mini 实验结果，已包含 gap confusion。
- `outputs/tables/`：PPT 和论文可复用 CSV 表格。
- `outputs/cm_egqa_progress_report.pptx`：给导师汇报的 PPT 初稿。

迁移建议：

- 继续把本仓库作为主论文工作区。
- `intent-router` 和 `medicalLLM` 应作为上游数据、路由和 baseline 来源，而不是替换 CM-EGQA 主线。

## 推荐整合路线

1. 在后续 CM-EGQA 样本中增加可选字段 `intent_labels`。
2. 用高风险意图标签指导 100 条 pilot 扩容。
3. 先补确定性版本的 `llm_only`、`self_reflection_rag` 和 `source_trust_rag` baseline，再接入真实 LLM。
4. 后续把 `Q_sem` 接成输入质量分数：
   - 低 `Q_sem` 路由到 `clarify`
   - 高风险意图且缺关键患者信息时路由到 `clarify`
   - 已知危险前提路由到 `abstain`
5. 等 100 条 pilot 稳定后，再用 `medical-rag` 做更强检索 baseline。

## 需要用户接手

- 如果要完整本地 clone `medicalLLM` 和 `intent-router`，需要运行 `gh auth setup-git` 或提供已 clone 目录。
- 需要确认私有患者问题数据能否用于 CM-EGQA 采样。
- 在投稿或公开数据前，需要确认 license、脱敏和可发布边界。
- 需要决定 `Q_sem` 在汇报中是“已有相关工作”“后续整合模块”，还是最终方法的一部分。
