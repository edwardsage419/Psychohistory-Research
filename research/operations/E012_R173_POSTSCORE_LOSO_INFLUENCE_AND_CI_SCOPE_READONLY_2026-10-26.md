# E012 R173 评分后补充诊断、原始预测账本与 CI 边界增量只读审计

审计日期：2026-10-26（Asia/Singapore）
轨道：operations，E增量审计
状态：COMPLETE_BOUNDED_READONLY_RECOMPUTATION
preflight_main_head: 7e9789aec2a38b28b9345bf42d0fdc419ebb4a08
此前已完成当日正式E004日检，E011已检查R172；本次聚焦最新R173，不重复建立全量日检
科研证据：R173原始研究为真实民族志资料的有限E1观察性预测关联；本次独立复算为内部E1审计，新增E2=0，新增独立E3=0
费用：仅GitHub连接器公开资料只读、内部算术及本文件归档；无购买、收费API、云计算或主动CI；新增主动费用0；整体账单未核验

## 1. 最新 HEAD、轨道和并发检查

读取main最新HEAD、market至MKT043、operations至E011、privacy_safety至F002，以及最新15条提交。最近研究变化为R173的2026-10-26追加评分后诊断，最新TH046理论轨提交和此前R172审计。R系列原始主线仍有大量归档目录，本次未全量枚举其验收状态。F002是本周2026-W44已完成专题，不重复立项。只新增本E012文件，不修改R、B、A、TH、F、market任何现存产物或索引。

R173新诊断协议冻结提交 f34d77e53f11f59608609bdd28946f5dec356391；主报告及B轨复核在下一提交 cf82f02b04b14bc8fd459328db6ed36dd4bea6d7。GitHub compare确认后一提交相对冻结 ahead=1, behind=0。冻结文件在冻结提交与当前main的Git blob均为18f798ae6d320586a1a0d252e2338f53498e96db。原预测CSV的Git blob为453c118c64fc5ce0073f7be4c474efbfb1d8b695，当前读取匹配协议所列。原始R173的2026-10-21评分在本次冻结前已公开，所以这是postscore诊断，不能改称原始预评分预注册。B独立脚本与主追加报告同一提交，独立性限定为计算路径，不是事先盲法复验。

## 2. 独立读取2899行预测并逐行复算

通过GitHub直接取得原始2899行CSV，UTF8文本984702字符，表头包含sample、society_id、EA005农业分组、EA006婚姻类别、两种逐行log loss与14个模型概率。独立JavaScript代码逐行计算各模型观测类别自然对数损失及七分类Brier，检查概率正值、归一、社会ID组内唯一和分组汇总，复算剔除单一农业类别及婚姻类别后的平均配对log loss差。

检查结果：2899行全部参与，4组记录数与机器收据一致，重复社会ID计数0，非法概率或类别计数0，概率归一最大误差3.3306690738754696e-16，逐行重算log loss对归档最大绝对差8.881784197001252e-16。四组平均Brier与log loss差和主机器收据在当前浮点汇总精度下一致。按行执行三类结构条件并对四组执行指标/计数核对，共8717个条件评价，发现不一致0。该数量是本次审计程序评价次数，不是原研究新增的独立实验或样本。

| 样本 | 行数 | M0减M1平均log loss | M0减M1平均Brier | 剔除农业类别翻转 | 剔除婚姻类别翻转 |
| --- | ---: | ---: | ---: | --- | --- |
| SCCS_186 | 186 | 0.014241271629136 | 0.021789704443504 | 8 | 1、2 |
| EA_1271 | 1271 | 0.038951268384616 | 0.026313343773678 | 无 | 无 |
| SCCS_COMPLETE_SOURCE_YEARS | 183 | 0.028396023760567 | 0.025679968755812 | 无 | 1 |
| EA_COMPLETE_SOURCE_YEARS | 1259 | 0.037813960396372 | 0.026416113318039 | 无 | 无 |

SCCS_186总体配对log loss改善总和为2.6488765230193394，农业代码8的13个社会贡献正向总和4.893478717348007，超过总体净改善。剔除该代码后剩余173社会的平均改善变为负0.012974579157969176。此现象直接从原逐社会账本重新计算，说明主样本的微弱优势对少数类别敏感，仍未控制语言家族或地理相关性。

四个样本存在来源与社会重叠，不能视为四次独立跨文化复现。原SCCS_186的配对社会重抽样95%区间为[-0.0643892219,0.0882251598]，跨零。原EA总体区间虽为正，仍未校正共同祖先、空间扩散、观察者与来源年代。B轨独立重建2899行、40586概率的声明已读取其收据；本次E没有重新执行B脚本的全部训练折计数重建，不能把B的40586项核验计作本次E的独立完成。

## 3. 原始CI与新增CI分离

直接读取GitHub Actions原始运行39549084819，status=completed，conclusion=success，event=push，head_sha=0f635a7143256654958d3da0e66fff472775a424。它对应2026-10-21原始R173流程的既有CI证据，不能移用为2026-10-26第三方法通过CI的证据。

针对新增第三方法报告提交cf82f02b04b14bc8fd459328db6ed36dd4bea6d7，直接查询Actions head_sha，total_count=0。新增诊断CI状态为NOT_VERIFIED；本轮不启动任何CI。不能因报告存在或commit成功推断算法经过远端自动化验收。

## 4. 治理风险及后续登记

E012-01 HIGH OPEN：SCCS主样本的弱正向关联对农业类别8敏感，剔除后方向翻转；禁止推广为普遍跨文化预测机制。

E012-02 HIGH OPEN：民族志资料存在语言亲缘、空间扩散和历史观察时间不一致；留一社会预测无法解决非独立来源，E1观察性关联不能升级为独立E3。

E012-03 MEDIUM OPEN：新增第三方法为原始评分后的补充诊断；B复核与主报告同提交，不具备独立预冻结盲法性质。

E012-04 MEDIUM OPEN：原始R173 CI确有成功记录，新增第三方法对应SHA查询无运行，必须分别报告。

E012-05 HIGH OPEN：E009 R170完整跨路线状态概率复核证据缺口、R136原冻结负对照失败与原始CSV字节问题继续开放。本次未独立重查这三项的最新原始文件，不能宣称已关闭。

E012-06 MEDIUM OPEN：original239中154项逐项证据审计待办沿用E004既有计数，本轮没有重新计数。全仓同名文件冲突、全部冻结协议和全部研究轨CI仍未普查，不得声称零遗漏。

F：2026-W44 F002已完成授权撤销及派生数据生命周期；本轮只记录“错误的统计成功归因及群体样本不独立”供未来解释和申诉专题，未接入敏感个人数据，未开发个人产品。

下一次E优先检查最新R174及其冻结与独立复核收据，另行跟进R170与R136缺口；R主线完成后统一归纳分类，最后熔炼。

## 5. GitHub固定来源

1. https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R173_PREDICTION_LEDGER_BRIER_INFLUENCE_POSTHOC_DIAGNOSTIC_FREEZE_2026-10-26.md
2. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R173/R173_REAL_EA_SCCS_LOSO_HELDOUT_PREDICTIONS.csv
3. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R173_POSTSCORE_BRIER_INFLUENCE_RECEIPT_2026-10-26.json
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R173_POSTSCORE_BRIER_INFLUENCE_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R173_INDEPENDENT_RECONSTRUCTION_RECEIPT_2026-10-26.json
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R173_INDEPENDENT_RECONSTRUCTION_SCIENTIFIC_AUDIT_2026-10-26.md
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R173/R173_SCIENTIFIC_REPORT_2026-10-21.md
8. https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39549084819
9. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E011_R172_COUNTRY_CLUSTER_RETROSPECTIVE_E3_AND_INDEPENDENT_BOOTSTRAP_CHECK_2026-10-26.md
