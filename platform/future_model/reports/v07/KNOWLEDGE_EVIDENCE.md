# v0.7 B04 本地知识与事实更新边界

本地工程结果 `AVAILABLE`。以候选工作区 HEAD `6e44ecf50e9e8de0d8a3eb76766cd0d3bf44ab9c` 的原始文件为输入。固定 154 项清单 Git blob `6862d5a2cd3c7eb3f2da9a85d79c8b3386f2a102`，清单快照 `16986d537f3f974fe97e3865fd6f349f76846b0e`。发布政策 Git blob `319e9922bf2f05a66e69eaa504a76cd90ebee59a`。

| 复核 | 实测 |
| --- | ---: |
| 路径、原始字节数及重算 Git blob 与清单和 `git ls-tree -rl HEAD` 同时匹配 | 154/154 |
| 正文 UTF-8 可索引 | 154/154 |
| 缺失、变更、不可读、UTF-8 失败、正文空、未列和字节重复 | 各 0 |
| 已记录的语义重复补充 | 1 |
| 正文字节数、词项数、唯一词项数 | 697,064 / 132,483 / 29,755 |
| 关联原生方法的档案 | 26 |
| 历史方法来源边匹配 / 变更 | 37 / 1 |
| 已定位适用范围摘录 / 范围缺失 `UNKNOWN` | 132 / 22 |
| 档案自带日期（取文件名） | 154/154 |

逐文档报告 `/workspace/v07-B04-corpus-report.json` 含 154 条逐项路径、期望及实测 Git blob、SHA-256、字节数、索引状态、许可、关联方法、重复和历史变更。报告文件 SHA-256 为 `c8a8fa2e71564c88e52b6afb3eb7305e114a8977805fbbfbca01072c33510416`。固定清单注明 Arkes/Blumer 11-23 档案为 11-22 复审的补充，两份有不同原始字节。38 条历史来源边均有当前档案，其一 Buehler 1994 的 11-21 档案在 `timing_actions@1.0.0` 历史绑定为 `b611c66afbdeb862353dbad7330916afc57ac45e`，清单与当前工作区为 `e7e1002f00aab5bf782a5f2845fbfac2cb80969b`。运行原生注册表核对 15 项，14 项为 `MATCHED_REFERENCE_ONLY`，`timing_actions` 为 `REVIEW_REQUIRED`。

检索以第 28 轮中英文词项规则、BM25 k1=1.2、b=0.75 和正 IDF 为基础，增加 NFKC 宽度规范化。真实归档正文入索引，版本和大小不符即隔离。实际运行 `CERTAIN_PASS point-estimate midpoint`，C028 硬约束档案首位，分值 26.859。随机空词查询无命中。在同一工作区复跑第 28 轮 16 档案原型的 20 条开发问题，正文原词 Hit@3 为 9/16，有扩展词为 16/16，两个正文方案在 4 条范围外问题中均有 2 条返回结果。154 项现有检索的独立效果待验收。一次实测冷构建约 126 ms，两个指定查询分别重复 30 次的中位时间约 0.98 ms 与 2.00 ms。数据仅反映当次 Linux 环境。

引文记为项目档案。154 项项目笔记按已核验的公开档案政策标记 `NO_OPEN_LICENCE_DECLARED`，所引外部论文、数据和代码的使用许可仍需分别查验。搜索结果说明查询相关性和证据资格，档案只作 `RESEARCH_REFERENCE_ONLY`，不形成个人事实、估计、许可或数学执行授权。摘录为本地已有档案短文本，构建过程不下载或打包论文和数据，也不保存查询。

五条完整短句经第 67 轮的反向需求模式连接实际注册表，生成待确认范围、已确认底线、合格测量、先验可行性核查和后续方法自身的证据需求。C028、Pareto、权重敏感性和 C029 的开发调用均返回 `NEEDS_SCOPE`，时机方法返回 `REVIEW_REQUIRED`。否定用例 `我不需要判断方案是否违反底线` 返回空候选。搜索正文的正分只代表词项相关性。开放语义解析、外部语料科学准入、目标自动确认及独立效果验证待后续工程和验收。

外部事实更新提供独立的结构化隔离入口，验证由宿主配置的精确来源 URL、来源版本及许可、JSON 唯一字段、ISO 日期、有限小数、时间窗与载荷 SHA-256。外部正文、任意字段和内含命令不会进入索引或决策方法。合格格式的上传仍为 `UNVERIFIED_IMPORT` 和 `QUARANTINED`，陈旧为 `STALE`、缺载荷为 `OFFLINE_UNAVAILABLE`。当前零来源配置，连接器及外联未启用，实际联网更新 `NOT_IMPLEMENTED`。索引、正文查询及五种明确目标在 Python 拒绝所有 `socket.*` 审计事件时实际运行成功。

17 项针对性测试通过。用 `create_app` 与真实 FastAPI 请求处理验证 `POST /api/v7/decisions/knowledge` 无令牌为 401，认证后查询为 200、恰好返回请求的 1 项结果并带 `Cache-Control: no-store`。认证查询 `/api/v7/decisions/knowledge/discover` 返回 200 与 `NEEDS_SCOPE`，`GET /api/v7/decisions/knowledge/report` 返回 200 与 154 项计数。

## 复跑

在 `platform/future_model/` 执行，Python 为 3.12。

```bash
PYTHONPATH=src python -m psychohistory.decision_knowledge report > /tmp/psychohistory-v07-corpus-report.json
PYTHONPATH=src python -m psychohistory.decision_knowledge search 'CERTAIN_PASS point-estimate midpoint' --limit 5
PYTHONPATH=src python -m psychohistory.decision_knowledge discover '比较各目标的优势'
PYTHONPATH=src python -m psychohistory.decision_knowledge discover '比较现在行动和等待'
PYTHONPATH=src python -m pytest -q tests/test_decision_knowledge.py tests/test_decision_knowledge_updates.py
git ls-tree -rl HEAD -- ../../research/decision_methods
```

在仓库根目录执行，第 28 轮原型结果见 [复算记录](KNOWLEDGE_REFERENCE_REPLAY.json)。

```bash
node research/decision_hub/2026-11-24-content-method-retrieval/probe.js .
```
