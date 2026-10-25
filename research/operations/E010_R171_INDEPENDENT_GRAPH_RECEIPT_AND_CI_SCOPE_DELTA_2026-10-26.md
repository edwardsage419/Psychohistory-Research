# E010 R171 独立图遍历收据、冻结时间与 CI 证据范围增量只读审计

run_date: 2026-10-26 Asia/Singapore
track: operations
subflow: E incremental readonly
status: COMPLETE_BOUNDED_READONLY
preflight_main_head: f687682a4d910806eaaa3c3bdd7064a3134a8dfd
prior: E004 formal daily audit, E005 through E009, MKT041, F002
cost: ZERO_ACTIVE; account billing and free quota NOT_INDEPENDENTLY_VERIFIED
ci: NOT_TRIGGERED

## 1. 已读取对象及并发边界

直接读取 main HEAD、MKT040/MKT041、E004/E009、F002，R171 主协议冻结、主科学报告、主机器收据、B 独立协议冻结、B 独立审计及机器收据、A 轨 Cason 2026 数据来源门槛。检查 GitHub 提交祖先关系、R171 原始 summary.trees Git blob、主冻结协议 blob，以及三项指定提交关联的 Actions 记录。E010 仅追加独立运营审计文件，不修改 R/A/B/TH/C/D/F/market 及共享索引。未做全仓冻结文件和同名文件完整扫描。

## 2. 提交与冻结顺序

主 R171 协议冻结 13b9538f5c118378f7f9df0e8f496aeacb5ae88d；主科学报告 01b14fb848ed1b645d39212ead1d9a928f7d5c75。GitHub compare 冻结至报告 ahead=3、behind=0。

B 独立路线预执行协议冻结 b59aaa8f39abef461e8da313c45572f95376f509；B 最终审计 aa6fa072f0e33471348c96b477510312e9276737。B 冻结至 B 审计 ahead=3、behind=0。

**重要时间限定**：主科学报告提交 01b14fb8 是 B 协议冻结 b59aaa8f 的祖先，compare ahead=2、behind=0。因此 B 路线协议是在主研究结果已经归档之后才冻结，属于“B 自身执行前冻结”，不能称为“B 对主结果未知的事前独立预注册”。B 的独立性是代码/算法实现路径层面；共同数据及事先可见的主结果带来设计选择与比较范围的依赖。此顺序不违反当前 B 冻结文本要求，需在证据描述中如实限定。

主协议在其原提交和本轮 main 中的 blob SHA 均为 4c03ce2181aa3c0b49dd6b4ec58d0e75da7fccb6。R171 原始 research/R171/source/summary.trees 在主冻结提交和 main 中 blob SHA 均为 89139751991c9f5753d249baeb9230061db93a4d，文本长度 10954 字符。仅对这两个对象证明所查版本未变。

## 3. 两份实际机器收据的独立一致性检查

主收据 research/validation/R171_ROOT_QUARTET_EXACT_RECEIPT_2026-10-26.json，blob fa793f15af3f155f4c2530d75f5c6d4fea93f22b。
B 收据 research/evidence_audit/B_R171_ITERATIVE_GRAPH_EXACT_RECEIPT_2026-10-26.json，blob d2f35a3a67205a2918e54b27630079dbb1db9fe8。

本轮从远端读取两份 JSON，使用独立 Python 标准库对 9 个同义字段交叉核对，并复算 5 项组合关系，共 14 assertions，14 PASS、0 FAIL：

* tips=400，unordered pairs=79,800=400×399/2；
* quartet attempts=1024，skipped=16，valid=1008，resolved=951，unresolved=57；1024=16+1008 且 1008=951+57；
* root depth min=1,733,214，max=4,633,215 micro-millennia，range=2,900,001；
* B 独立记录 pair sum=590,570,691,634 micro-millennia，除以 79,800 再转换单位，mean=7.400635233508773 millennia，与 B 收据相符。

主程序记录全部 79,800 对 tip 距离在其重定根前后相等；B 独立程序记录独立图路径遍历 79,800 对并比较冻结原始九对和聚合摘要。B 主文称八项跨路线摘要核对通过，主收据没有存放全部 79,800 对的逐项距离向量，也没有相应跨路线逐项等式机器收据。**不得将摘要相符扩大表述为 B 与主程序逐项 79,800 对完全比对已归档。** 当前 B 预执行协议要求的聚合与选定对照有对应报告，故仅记录独立复核范围，不直接判定违反 B 验收条款。

两个负对照都报告实际执行：正边长+1 改变跨边 tip 距离，quartet 和+1 破坏四点等式。主程序首次科学计数法解析失败、B 首次标签状态检查失败均在报告中披露，之后更正程序再运行。无需将两条程序错误追溯成原协议变更。

## 4. 科学证据、CI、数据来源和历史阻塞

R171 这次分析使用既有已推断的 Gray et al. 2009 Phlorest 树，重定根不改变未定根 pair metric、四点等式及非严格超度量性质属于给定树上的描述性数学。状态为 PASS_BOUNDED_INTERNAL_E1_SOURCE_DESCRIPTIVE；新增合格真人 E2=0、独立历史预测 E3=0、外部研究者独立复现=0。不能把公开历史来源树的内部一致性当作对历史演化预测的独立检验。

直接查询 GitHub Actions REST 的 head_sha：主冻结 13b9538f、主报告 01b14fb8、B 最终审计 aa6fa072，分别 total_count=0。仅能说明这些指定提交没有返回关联 workflow runs；本轮未触发 CI，不能将 commit 存在解释为 CI 通过。

A 轨新增 Cason 等 2026 Dryad 真人间接互惠实验来源，公开 README 有 donor/recipient、round、session、cohort、person ID 等字段，原始 CSV 字节与逐行完整性尚未核验；其机制与 R073 冻结双人同步二元博弈不同，不能无协议改变地作为 R073 独立复验。R170 独立 Python 对主 JS 全状态质量逐项比较的 E009-01 缺口仍开放。R136 历史冻结负对照失败及原始 CSV 字节问题保持。原始239项中154项逐项证据审计待办为 E004 既有索引读取数，本轮未重新统计。

## 5. 只读问题登记

E010-01 MEDIUM OPEN：B 协议冻结晚于主结果，所有“独立”措辞须限定为执行实现独立，不应宣称对主结果盲法预注册。
E010-02 MEDIUM OPEN：主/B 79,800 对逐项跨路线相等未有远端全量比较收据；当前报告仅支持汇总一致及各自内部计算。若原轨未来声称更强验收，应提供逐项比较或稳定哈希与反例检查。
E010-03 MEDIUM OPEN：三项指定提交 CI total_count=0，远端新算法 CI 未证实。
E010-04 HIGH OPEN：R170 E009 跨语言全状态比较证据缺口。
E010-05 HIGH OPEN：R136 原冻结负对照失败、纠正性新协议成功与原始 CSV 字节未完全核验，应并列保留。
E010-06 HIGH OPEN：original239 154 项逐项审计仍待处理，未在本轮全仓巡检。
E010-07 MEDIUM OPEN：A 轨 Cason CSV 原始字节、授权及 session/cohort 切分门槛未闭合；不得升级 E2。
E010-08 MEDIUM OPEN：本轮仅抽查最新研究及两个冻结对象，不能声称全项目零冲突或全部冻结协议无漂移。

## 6. F、本轮费用与下一步

F：2026-W44 的 F002 已完成，本轮仅把 Exist Insights 的派生文本权限与 created/target_date 生命周期加入未来候选风险池；没有重复立项 F003，没有接入真实敏感数据或开发个人决策产品。

主动新增费用为零；仅已有 ChatGPT 与免费公开 GitHub、英文官方资料及本地标准库计算。没有购买产品/论文、注册收费服务、调用计费 API、启动 CI、租云服务器或 GPU。GitHub 账户总账单及免费额度未独立核验。

下一项 E：追踪 R172 是否存在新冻结与执行证据；优先检查 R170 的全状态跨语言补验、R136 CSV 和 original239 待办。坚持完成全部 R 系列后再系统分类，最后模型熔炼。

## 7. 直接读取的仓库来源

1. https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R171_ROOT_INVARIANCE_ULTRAMETRIC_FOUR_POINT_THIRD_METHOD_FREEZE_2026-10-26.md
2. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R171_ROOT_QUARTET_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
3. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R171_ROOT_QUARTET_EXACT_RECEIPT_2026-10-26.json
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R171_ITERATIVE_PARSER_GRAPH_WALK_PRESCORE_FREEZE_2026-10-26.md
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R171_ITERATIVE_GRAPH_INDEPENDENT_SCIENTIFIC_AUDIT_2026-10-26.md
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R171_ITERATIVE_GRAPH_EXACT_RECEIPT_2026-10-26.json
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/CASON_RIEDL_SCHRAM_ULE_2026_CRSU_100_ROUND_INDIRECT_RECIPROCITY_SOURCE_GATE_2026-10-26.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E009_R170_FROZEN_CROSS_ROUTE_STATE_COMPARISON_EVIDENCE_GAP_2026-10-26.md
9. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT041_EXIST_INSIGHTS_SINGLE_ATTRIBUTE_SCOPE_RENDERED_TEXT_AND_TIME_FILTER_2026-10-26.md
