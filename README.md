# 论文资料整理

这个仓库用于存放论文检索、追踪和阶段性整理材料。

## CM-EGQA / Claim Authorization Pilot

当前新增了一个面向 IEEE BigData 2026 主会目标的最小实验闭环：

- `data/cm_egqa_mini.jsonl`：中文医疗 QA 小样本。
- `data/evidence_corpus.jsonl`：小型医学证据库。
- `medclaimauth/`：断言级证据授权实验代码，当前包含 7 个确定性对照方法。
- `outputs/mini_experiment_report.md`：可复现实验报告。
- `outputs/dataset_validation.md`：数据质量门禁报告。
- `outputs/case_studies.md`：论文 case-study 候选。
- `outputs/tables/`：论文和 PPT 可复用 CSV 表格。
- `outputs/cm_egqa_progress_report.pptx`：给导师汇报的 PPT 初稿。
- `docs/ieee_bigdata_2026_roadmap.md`：BigData 2026 投稿路线。
- `docs/cm_egqa_annotation_guidelines.md`：CM-EGQA 标注规范。
- `docs/source_repo_audit.md`：截图中三个 GitHub 仓库的可迁移信息审计。

运行测试：

```bash
python3 -m unittest \
  tests/test_claim_authorization.py \
  tests/test_run_experiment_cli.py \
  tests/test_dataset_validation.py \
  tests/test_case_studies.py \
  tests/test_export_tables.py
```

复现实验：

```bash
python3 -m medclaimauth.run_experiment \
  --samples data/cm_egqa_mini.jsonl \
  --evidence data/evidence_corpus.jsonl \
  --output-json outputs/mini_experiment_report.json \
  --output-md outputs/mini_experiment_report.md
```

验证数据集：

```bash
python3 -m medclaimauth.validate_dataset \
  --samples data/cm_egqa_mini.jsonl \
  --output-json outputs/dataset_validation.json \
  --output-md outputs/dataset_validation.md
```

导出论文 case studies：

```bash
python3 -m medclaimauth.export_case_studies \
  --samples data/cm_egqa_mini.jsonl \
  --evidence data/evidence_corpus.jsonl \
  --output-json outputs/case_studies.json \
  --output-md outputs/case_studies.md
```

导出论文/PPT 表格：

```bash
python3 -m medclaimauth.export_tables \
  --report-json outputs/mini_experiment_report.json \
  --output-dir outputs/tables
```

## 目录结构

- `意图识别治理幻觉/论文检索/`
  - 按日期保存“意图识别治理幻觉”方向的论文检索笔记。
- `医疗大模型幻觉论文追踪/季度整理/`
  - 保存按季度或主题整理后的医疗大模型幻觉论文追踪材料。
- `医疗大模型幻觉论文追踪/历史记录/`
  - 保存早期检索、追踪和自动化生成的历史笔记。
- `医疗大模型幻觉论文追踪/自动化记录/`
  - 保存自动化任务相关记录。

## 收纳规则

- 新增日常检索笔记时，优先放入对应主题下的 `论文检索` 或 `历史记录` 目录。
- 已经提炼成阶段性主题总结的材料，放入对应主题下的 `季度整理` 目录。
- 根目录只保留入口说明文件，避免后续继续堆散文件。

## 后续上传格式

新增文件时，先在本地放入对应目录，再提交到 Git。

### 日常论文检索

- 目录：`意图识别治理幻觉/论文检索/`
- 文件名：`YYYY-MM-DD-意图识别治理幻觉-论文检索.md`
- 示例：`2026-06-20-意图识别治理幻觉-论文检索.md`

### 医疗大模型幻觉追踪

- 阶段性整理放入：`医疗大模型幻觉论文追踪/季度整理/`
- 历史检索记录放入：`医疗大模型幻觉论文追踪/历史记录/`
- 自动化任务记录放入：`医疗大模型幻觉论文追踪/自动化记录/`

### 上传命令

```bash
git status
git add .
git commit -m "Add paper notes"
git push
```
