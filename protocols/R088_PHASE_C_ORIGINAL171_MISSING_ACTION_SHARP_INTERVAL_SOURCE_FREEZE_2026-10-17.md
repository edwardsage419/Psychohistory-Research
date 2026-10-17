# R088 Phase C：171原作者六人群体缺失行动下全球合作比例与阈值的锐界实证协议冻结

2026-10-17。本协议在任何 R088 Phase C 真人全球合作率/群体达标率实算之前提交。不得追溯改写Phase A：初次来源评分run39011042473中35synthetic全过，真人 `R088_HUMAN_ORIGINAL_ACTION_NULL_OR_UNEXPECTED` 来源失败；Phase B冻结后的源编码安全审计 run39011243425 合计52synthetic全过，**20,520** 个原作者人-轮机会中 `EXACT=20,456`，`EMPTY_MISSING=64`，其它不明类别=0，三处理缺失为 GlobalOnly 19、Balanced 26、GlobalBoost 19，第一轮缺失29、末轮缺失0。Phase B是来源编码分析，未执行真实群体达标和合作率评分；本协议延续原源身份与组构成不变，在看任何新E2群体结果前固定锐界算法与竞争方向门。2026已发表原论文结果事先公开，不冒称前瞻预注册。

## 原作者来源与参与宇宙不可变

同一GitHub原作者 `chasmani/PUBLIC_social_identity_and_cooperation`，同一固定commit `8ce2c0cac4784485232aa96295f48ff147290b05`，同一作者完整组CSV `analysis/data/data_full_groups.csv` 的Git blob `f902865203bdb465a505869b593eca432831b2fa` / 2,270,643字节；校验 `analysis/analysis_exclusions.R` blob `5d7f6e65523df55a1f05bd69f48d60b9306783a9` 及 `analysis/analysis_cooperation_rates.R` blob `60793d82709a7807e86ceddd772fe2847733a6e2`。唯一目标 **171组×6人×20轮**，三处理各57组；每组六人恰有两个三人subgroup，group_id仅内存，不存唯一组特征组合。原始各轮行动合法值为 `global/local/other/self`，GlobOnly条件合法 `global/self`；来源`None`、空文本、只含空格视为 missing interval，其他未知或非映射token依旧FAIL CLOSED（不容忍未来不明字节）。不得剔除一名演员或丢弃已审原群体。必须独立验证全部64空值和每处理分布是这份不可变作者数据的真实一致性；否则STOP并保留第一次审计差异，不默默改变主体。

## 冻结的缺失锐界计数规则：无任何插补和推断

每一group、每一20轮从6名原始人员的每期实际观察记录数分别算 `g=observed global`, `l=observed local`, `o=observed other`, `s=observed self`, `m=missing`，`g+l+o+s+m=6`。**未知行动可以取当期该处理任何被允许行动，但不认为观察值的类别可改**。

- Group global investment count `G∈[g,g+m]` (integer inclusive). 每group×round合作率 `[g/6,(g+m)/6]`；每条件×round或完整20轮按57个等权完整六人组求均值区间，并发布准确分母6×57、6×57×20，不使用`g/(6-m)`当主分数。
- Global threshold `G≥4`：`certain_yes=1(g≥4)`，`possible_yes=1(g+m≥4)`。每条件×round `[sum certain/57,sum possible/57]`，全20轮同样用1140 group-round分母。记录`certain_yes`、`possible_yes`差额（受缺失影响的不确定群体轮）。
- 对每group `G_20-G_1` 的范围为 `[g20-(g1+m1), (g20+m20)-g1]`，除6后对所有57个group等权取平均；公布**保证增加人数** `lower>0`，**保证减少人数** `upper<0`，**可能有增/减的组数** `upper>0`/`lower<0`，保证完全相等 `lower==upper==0` 以及来源不确定跨方向的组数。**不允许**强行把不能判符号的归为“零变化”；本次不计算p值或聚类显著性。
- 不同处理的20轮平均全球率差 `X−Y` 的锐界为 `[lower_X−upper_Y,upper_X−lower_Y]`，仅固定三种 pair: GlobalOnly-Balanced、GlobalBoost-Balanced、GlobalBoost-GlobalOnly。若区间下界大于0则无论缺失如何这份完整组观测都支持正方向（**并不代表随机分配的因果效应**）；如果跨0则方向无法由来源识别。严禁为了想得到正结果调整missing或分母。
- 为明确"other"与"local"的多层效应，global组数与缺失是重点；另外已观察`local+other`比例可给 `[(l+o)/6,(l+o+m)/6]`，自留率 `[s/6,(s+m)/6]`，GlobalOnly局部率上下界均零（不可选择）。此为描述性资源配置并非已经识别实际两个小组如何满足阈值；**不计算局部阈值**。

## 缺失处理敏感性与已发表研究边界

这些interval在每个缺失行为可为global与非global时在代数上可达到极值（只对合法处理组合而定），是**完整组行为变量的极值包络**，非统计置信区间、非预测概率、非MAR假设/多重插补。原研究条件分配与完成样本筛选可能使原作者full-groups样本不代表所有曾招募者；组内6人重复20轮有强依赖，不能将20520槽当20520独立RCT单元。即使实验随机分配条件，当前只报告三条件筛选后样本中的观测差异及其锐界，不宣称population ATE、身份认同因果、长时段制度演化。
  
## 验收
独立新增>=20 synthetic tests验证单六人组已观察数+missing=6、2×3 subgroup、阈值4、group first-last上下界/不确定组、两处理对比锐界、globalonly本地不能投入、字段恶意标签拒绝、64 missing源完整性、20轮57组条件宇宙、禁止所有人/组ID。首次真实程序须复取三份原作者Git固定blob后才能计分，运行失败须无真实outcome输出。第二次原始完整重新取回、所有synthetic复跑、匿名宏结果byte size+SHA256严格匹配后永久归档main。原始逐人数据/群组ID/问卷都不写仓库。A01–A06 E2因果边界正式报告，PESEN v0.1保持FROZEN。

R088_PHASE_C_BEFORE_ACTUAL_INTERVAL_SCORES=FROZEN
R088_PREVIOUS_PHASE_A_REAL_SCORE=FAIL_RETAINED
R088_PHASE_B_SOURCE_MISSING=64_OF_20520
R088_PHASE_C_REAL_GROUP_E2=NOT_YET_SCORED
