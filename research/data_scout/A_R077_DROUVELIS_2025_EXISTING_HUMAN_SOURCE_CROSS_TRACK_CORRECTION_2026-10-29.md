# A轨：Drouvelis与Pearce 2025 原始真人数据跨工作流登记纠正

日期：2026年10月29日 UTC。目标键：(A, Drouvelis Pearce 2025 cleandata.dta, R077 Rev002, 现有真实来源复用与时序风险边界)。本轮重新核对一手英文公开来源 https://zenodo.org/records/15462528 与项目现有 R077 一手数据审计、机器验收和实际源处理代码。

## 重要纠正

本日早前 A 轨报告 `A_DROUVELIS_PEARCE_2025_STATA_LAG_ORDER_AND_TWO_SOURCE_REPRO_GATE_2026-10-29.md` 记载本轮执行环境未成功下载 `cleandata.dta`，并将其标为 RAW_BINARY_UNREAD。该状态仅描述当时那次下载。**项目级原始文件验证和真人模型评分早在2026年10月17日由 R077 完成**，必须在A轨数据登记中关联既有证据，避免重复宣称尚无真实来源。

原作者 Zenodo v1 于2025年5月19日发布，页面列 `cleandata.dta`、三份 Stata 程序、作者 MD5 `4cce04ea68b7a0492c242b206efebe53`。R077 已独立核验原始二进制文件 1,514,315字节，SHA256 `1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985`，成功读取3620条本人真人二元行动，15个原实验 session、260个场次内身份槽、1810个双人互动轮次、1440个个人 game、1040个满足同一 Session/Subject/game 且 t、t−1、t−2 连续可见的预测事件。上述均为R077既有验证结果，本轮没有重新下载二进制或逐行重新执行。

R077原生代码 `research/R077/r077_fourth_real_human_source_only_e3.py` 明确按 `Session, Subject, game` 分组，在组内按 `practiceperiod` 排序，只有连续 t、t−1、t−2 都存在才生成历史行为特征，且历史对手行动来自上一轮实际反馈。R077原 Rev001 因130次组内配对变化及80个人局从第一轮缺失而拒绝，Rev002 在首次真人模型评分前另行冻结，旧失败记录仍保留。该程序与复制论文 `number 1.do` 中原 Proto 数据部分的 `sort id` 及行号滞后计算属于不同代码路径，不能将旧 Stata 风险直接认定为 R077 的实际错误。

## 数据登记

| 核验项 | 本轮结论 |
| --- | --- |
| 研究对象 | 已公开真人重复囚徒困境复制实验 |
| 原始文件身份 | R077 既有 SHA256/MD5/字节数已核验，本轮重读 R077 归档 |
| 行动与时间 | `left`, `otherleft`, `practiceperiod`，局内连续历史由R077代码显式处理 |
| 独立样本 | 15个原始 session；3620行不得当作3620个独立实验 |
| 冻结预测 | R077既有外部真人E3结构转移，R073固定参数，1040条可评分事件 |
| 原始许可 | Zenodo页面 Rights/License 栏未显示具体许可条款；继续限制原始文件再分发 |
| 全论文双来源复制 | 原 Proto `experimentaldata.dta` 仍另需获取；复制论文整体复现仍开放 |
| 本轮新预测 | E2=0、E3=0；历史 R077 证据保持原身份 |
| R073原双人100轮直接复验 | 不满足原长100轮同一结构；R077有单独冻结的适配合同 |

官方来源：https://zenodo.org/records/15462528 。项目既有证据：`research/R077/README.md`、`research/R077/R077_FINAL_ACCEPTANCE_STATUS.json`、`protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md`。本轮没有购买软件、数据或调用计费接口。
