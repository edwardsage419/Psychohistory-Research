# R074：第二独立真人重复博弈来源初审结果与 E3 资格阻塞

日期：2026-10-17。状态：`R074_SOURCE_SCHEMA_AUDIT=PASS`；`R073_INDEPENDENT_EXTERNAL_E3=BLOCKED_SESSION_MAPPING`；`PESEN_v0.1=FROZEN`。

## 先冻结、再检查的执行证据

[R074 冻结协议](../../protocols/R074_SECOND_INDEPENDENT_HUMAN_IPD_SOURCE_GATE_2026-10-17.md) 先于外部任何模型评分提交：Git commit `eb28cef57d90323dce518cbd6f29dcd16eecabe6`。随后在 [GitHub Actions run 38934819236](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38934819236) 成功从固定 Git commit 下载两个第三方公开数据文件，逐文件校验 Git blob SHA1 和精确字节数，在执行环境内用 R 读取真实数据字段和局内轮次。工作流 `audit-two-independent-published-datasets-no-model-fitting` 结论 **success**，其成功只证明来源字节/字段审计跑通，**不等于 E3 实验预测成功**。

第一版 CI run 38934473974 与第二版 run 38934647044 曾失败。第二版日志定位到 FRD2012 实际字段顺序与文档叙述顺序不一致；修正为按字段名集合匹配，仍保留两个 Git blob 强校验和重复观测失败封闭规则；成功重跑 commit `ea76a26ec6651bb3efc9ee727c34c987f1d639f3`。历史失败不得抹去。

## 两个真正来源的有限审计

| 对象 | Dal Bó & Fréchette 2011 | Fudenberg, Rand & Dreber 2012 |
|---|---|---|
| 论文 DOI | 10.1257/aer.101.1.411 | 10.1257/aer.102.2.720 |
| 一手复现开放目录 | 10.3886/E112401V1 | 10.3886/E112512V1 |
| 当前已执行的可核验证据文件 | cran/stratEst DF2011.rda | cran/stratEst FRD2012.rda |
| 来源 commit | a6373b23d80dc816a63f18f973d372c9e8421914 | 同左 |
| Git blob SHA1 | 52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0 | 6b196ca1624081850b41dc2084c762257d59dd8f |
| 原始字节长度 | 3298 | 26923 |
| 逐轮选择记录数 | 7358 | 13126 |
| 匿名不同参与者数量（按 treatment + id） | 266 | 384 |
| 参与者 × supergame 数 | 2604 | 1536 |
| 同一局内前两轮连续的第3轮及以后候选评分事件 | 3248 | 10054 |
| 二级整理文件中的真正实验 session 字段 | **没有** | **没有** |
| R073同一实验场次整场留出 | **当前不可验证** | **当前不可验证** |

上述是**对两个已固定第三方整理文件的实际匿名审计**，并非作者一手原始行的等价复核；可评分事件数量是具有连续两轮数据的结构性计数，**没有任何真实人类模型预测或模型误差评分**。不能把 participant、supergame、日期分块推断出的组伪装成真正 session。FRD2012 含实施噪声，intent、realized 与历史所见行动的一致性仍需原始作者代码/字典核验。

本次审计没有把任何 ID、CSV/RData 原始行、个人决策序列、具体场次成绩提交到Git。Actions 工件只含匿名汇总 TSV，原始 RData 在 CI runner 临时读取后删除。

## 科学门与下一入口

G1（独立作者、论文、第二数据线索）达到 **候选来源已确认**；原始作者字节、第三方加工过程等价尚待证。G2（同局两轮历史结构）达到 **候选事件可数**；特别是2012实际行动与历史行动含义未独立恢复。G3（外部原生实验 session 的跨组隔离）为 **BLOCKED**。若强行把 2604/1536 个 supergame 当独立场次会允许同一人在训练与测试两边出现，构成伪复验。禁止以这种拆分推导肯定结果。

优先：恢复 Dal Bó 与 Fréchette 原作者 openICPSR 的 `dal_bo_2010a_data.dta` 或 `dal_bo_2010a_data.txt`，验证 `session`、`clientid`、`round` 与当轮双边动作的含义及每轮观察完整性。原作者 Stata 分析脚本存在以 session 为变量的操作，表明继续寻找原始完整数据有实际价值，但不能据此断言原数据已被审读。备选：恢复 Fudenberg 等原作者2012数据和噪声操作字典；另一项有公开16个实验场次、360个互不跨 session 受试者的 Kamei (2024) 研究 (DOI 10.1111/ecca.12539)，目前逐轮原始数据访问性尚未验证，不能直接转入评分。

**R073原始18424次个人测试、七模型及既有负结果保持完整不变。** 任何第二实验的完整外部评分必须在真正 session 映射与观测含义明确后，维持模型和评分规则冻结实施，并将不同试验的实际轮数与处理结构如实登记。

`R074=SOURCE_GATE_COMPLETED_BOUNDED`
`R073_E3=BLOCKED_SESSION_MAPPING`
`EXTERNAL_PREDICTION_RUN=NONE`
`PESEN_v0.1=FROZEN`
