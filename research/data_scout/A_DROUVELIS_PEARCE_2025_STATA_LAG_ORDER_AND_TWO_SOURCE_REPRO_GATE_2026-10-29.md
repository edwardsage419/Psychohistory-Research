# A轨：Drouvelis与Pearce 2025公开复制脚本的时序滞后与双来源依赖核验

日期：2026年10月29日。原先来源登记 `A_DROUVELIS_PEARCE_2025_ZENODO_REPLICATION_SOURCE_GATE_2026-10-29.md` 保留，本文件仅记录新增可直接检查的程序证据。来源为作者Zenodo英文归档 https://zenodo.org/records/15462528 ，公开Stata脚本 https://zenodo.org/records/15462528/files/number%201.do?download=1 ，DOI `10.5281/zenodo.15462528`。本轮实际读取公开脚本全文，并尝试取得 `cleandata.dta` 二进制文件，当前环境下载失败，未能执行原始数据逐行审计。

## 新增发现1：完整复制依赖两套原始数据

脚本第40至42行载入原Proto等人研究的 `experimentaldata.dta`，第243至246行另载入复制实验的 `cleandata.dta`。Zenodo归档的四个公开文件包含后者及三个Stata脚本，归档描述明确要求另行下载原研究的数据。故当前Zenodo四文件无法单独完成两研究的合并复算。来源依赖状态 `TWO_STUDY_SOURCE_DEPENDENCY_CONFIRMED`。必须分别取得两研究原始文件并校验许可与来源，才能声明完整复制。

## 新增发现2：原研究滞后字段需要逐行时间顺序验证

脚本第46行先执行 `sort id`，第62至63行以 `partnerchoice[n-1]` 生成 `partnerchoice2`，条件仅为 `period!=1`。可见程序在这一段未明确按 `id round period` 排序。若同一id的记录在输入文件中未按博弈场次和轮次排序，`n-1` 可能取到错误上一行。当前没有原始 `experimentaldata.dta`，无法确定实际发生了多少错误，也不能断言论文结果存在泄漏。核验要求：先按 `id, round, period` 或真实完整场次键独立重建前一轮对手行动；仅当同一参与者、同一独立场次且轮次连续时赋值；与作者 `partnerchoice2` 逐行比较并报告不一致数量。

复制研究部分第263至265行注释区分 `p2otherleft` 的上一轮行动和 `otherleft` 的当轮行动；第281至294行由 `Session Group Period` 构建匹配键并读取邻行的配对特征。这些字段是否正确映射到固定对手、场次与时间，只能在取得 `cleandata.dta` 后核实。任何包含当轮对手行动的预测特征都必须在预测时点可用，否则会构成目标时点信息泄漏。

## 复现准备登记

| 检查项 | 现状 |
| --- | --- |
| 研究类型 | 真人重复囚徒困境复制实验，论文和作者程序可核验 |
| 时间单位 | 程序使用 `period`、`round`、`practiceperiod`、`game`；真实逐场长度待原始数据核验 |
| 行动字段 | 原研究 `choice` 与 `partnerchoice`；复制研究 `left` 与 `otherleft` |
| 身份与独立场次 | `id/session` 及 `ID/Session/Group/Period`；配对唯一性和跨场次重置待核 |
| 文件可获得性 | 公开页面和文本脚本已读；二进制 `cleandata.dta` 当前环境下载失败；原 `experimentaldata.dta` 未取得 |
| 许可 | Zenodo页面License栏目没有明确可见的文件级许可，暂不再分发原始数据 |
| 直接R073复验 | NO；冻结的双人100轮独立场次要求未满足 |
| 当前结论 | `PAPER_AND_STATA_SCRIPT_VERIFIED; RAW_BINARY_UNREAD; TEMPORAL_LAG_ALIGNMENT_UNVERIFIED` |

原脚本使用Stata软件及外部原始数据。可用Python标准库或免费开源读取工具在合法取得文件后复算，不购买Stata、不注册付费账户。当前不生成E2预测，不将论文外部复制当作本项目R073外部独立复现。新增E2=0，E3=0。下一步先验证二进制文件合法可获得性，再检查时间排序和配对身份；若无法取得，维持明确阻塞。
