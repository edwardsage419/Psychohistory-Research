# original239 11-029 Cross Validation：原目录研究职责、R269有限E1及既有真人分组留出证据的逐项审查

track: R+B
subflow: R original239 itemwise scientific evidence review; B independent scope verification
run_date_utc: 2026-11-01
observed_main_before_write: 4d3cf7aa42a82045e33b10e946d4b2e2d5f6fa28
target_key: (R+B,original239-11-029/R269,2026-10-23-prescore-freeze,itemwise-primary-role-versus-empirical-evidence)
status: COMPLETE_BOUNDED_ITEMWISE_EVIDENCE_REVIEW / FORMAL_QUEUE_DISPOSITION_PENDING
queue_before: 154 (P0 27, P1 82, P2 45)
queue_net_closed: 0
new_E1_experiment: 0
new_E2_scoring: 0
new_E3_scoring: 0
new_CI: NOT_RUN
billing_checked: NOT_VERIFIED
output_path: research/validation/R269_11_029_ITEMWISE_ROLE_AND_E2_SCOPE_REVIEW_20261101T1745Z.md
commit_sha: see Git commit history of this file after publishing

## 一、原目录研究职责的直接核对

原始候选目录 `docs/MODEL_CANDIDATE_CATALOG_v0.1.json`，Git blob `f312a618223a0e96f1dcc99df49fe169d2ff50b3`，11-029 的原始字段为：name_en=`Cross Validation`、priority=`P0`、research_role=`独立数据上的预测比较`、review_status=`待逐项文献审查`、empirical_validity=`未知，取决于特定命题与研究情境`、first_hand_source_id=null。由此，方法上的独立样本预测比较是原目录提出的研究用途；一个人工群组泄漏反例本身尚未覆盖其经验检验要求。

最新交叉索引 `docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.8_2026-10-25.json`，Git blob `36f24235901172642c46853298aebb421f1a3552`，仍将 R269 作为 `PROVISIONAL_PRIMARY_README_LINK`，`manual_primary_mapping_and_acceptance_review=PENDING`，并将 R073、R105、R106列为旧有分组或场次留出相关证据。实际队列 `docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv`，Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`，11-029仍为P0待核。

## 二、R269来源、冻结先后与历史CI核实

R269在2026-10-23提交冻结协议，commit `1ba86be0a35b77c0d5e5f6a72bb102ba08c48795`，协议 Git blob `5c34e78a4a846786049a83348437c08eb82454a7`。GitHub compare 确认源码提交 `0d77cc29b047b1a9e9a5d9a1251352f2509b027c` 是冻结提交的后继，ahead_by=1、behind_by=0。原始人工 CSV 与 JSON 归档提交 `23b88012cc4811666aa47d51e16f2df3d79e9760` 在源码提交之后。

历史 GitHub Actions run 39902238505 于2026-10-23T04:47:54Z启动，status=completed、conclusion=success，运行 HEAD `7e763a3bb8a1105c93f4f1e1ab96862def321afd`。实际从GitHub API读取三项 job，Python 3.11、Python 3.12 和 independent-source-audit-and-archive 均 success；各自对应的测试或重建步骤也标记success。需准确保留：该 CI 的 HEAD 是归档提交 `23b88012...` 的祖先，机器人随后在同一工作流中提交生成的 CSV/JSON；不能声称该CI以最终归档commit为起点执行。冻结顺序与三作业成功均得到 GitHub 历史记录支持。本轮没有下载CI原始日志、重跑三作业或执行新真实数据评分。

2026-11-01既有R/B完整字节审计已在不同运行路线复算576个人工来源配置、13824预测和13824损失，CSV blob `20b33f85a9408655cfbd7bdbfc1de15ec534571e`，JSON blob `4947ccb7a53de1343216e1b69773d0a5c4ea1f29`。本轮只核查其范围和历史身份，不重复执行该数学复算。R269的正式状态 `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_GROUP_CROSS_VALIDATION` 保持有效。

## 三、原始英文文献与方法适配

直接核对 Roberts et al. (2017) 的期刊原文元数据和摘要，DOI `10.1111/ecog.02881`，其主题是依赖性数据中普通交叉验证低估预测误差，以及与时间、空间、层级和系统发育结构相匹配的验证策略。原文页面：https://nsojournals.onlinelibrary.wiley.com/doi/abs/10.1111/ecog.02881 。

核对 Arlot & Celisse (2010) 的作者公开预印本摘要，DOI `10.1214/09-SS054`，强调不同交叉验证策略的风险估计与模型选择性质。作者预印本：https://arxiv.org/abs/0907.4728 。

R269的六个独立潜在群组、每组两条完全重复观测、LOOR与LOGO分割，以及组记忆器的0对1/4 Brier反例，与结构依赖和目标外推单位的理论问题一致。该有限构造由项目自行定义，未复现两篇综述的原始经验样本。其比较同时改变训练行数11与10，不能把所有差距单独归因于泄漏。

## 四、原目录经验研究职责的既有相关证据

R073正式状态Git blob `4dcd30a7b47cc0f81ff186541d791474a3e2e0e9`，来源Montero-Porras等2022年原作者投稿版CSV，12个完整实验场次留出，188名真人、18424项条件预测目标，预定Brier比较，GitHub Actions run 38931506064 completed/success。这属于既有真人E2，训练来自其它同处理场次，支持场次留出在实际预测比较中的可操作性。其冻结模型仍未跨实验原样复现。

R105正式状态Git blob `2f1857d328d2efedd56601022cd86b2f37499fc6`，103个固定四人组整组留出、3708个真人下一轮目标，真实伙伴模型相对同权收缩对照为阴性，提供应保留的竞争基线结果。R105缺少独立原实验室session字段，不能把103组说成103场独立招募实验。

R106正式状态Git blob `ad7b328a7a2fb7a3a5aa2cd9eb33fd4bd7dc68ad`，独立2025英国实验260名真人、26个原场次留出、2022个合法下一轮预测目标，Brier真实对手历史模型优于同权收缩对照，GitHub Actions run 39127386064 completed/success。R106的任务、来源、冻结模型与R073不同，不能升级为R073精确冻结模型的第二实验复制。

三项历史证据与R269的人工E1相互补充，属于不同研究ID、不同冻结协议与不同实验任务。R269自身新增真人E2=0、历史E3=0；本轮新增评分=0。仅从这些关联不能推导某个通用CV方案在所有真人领域更优，亦不能自动改变original239正式队列。

## 五、逐项科研裁定与后续条件

1. `R269_PRIMARY_MAPPING = SUPPORTED_FOR_BOUNDED_METHOD_E1`：R269的原目录编号、冻结研究、方法来源、真实历史CI及有限数学结果均有直接证据。
2. `ORIGINAL239_11_029_EMPIRICAL_ROLE = PARTIALLY_SUPPORTED_BY_DISTINCT_EXISTING_R073_R105_R106_E2`：已有真实分组/场次留出比较，三者的研究目标、来源和证据等级必须分别保留；本轮未逐条重算三套真人行为。
3. `ORIGINAL239_11_029_FORMAL_ITEMWISE_CLOSURE = PENDING`：需由正式itemwise判定明确接受何种有限范围，以及是否要求原目录的“独立数据”与R269同一冻结模型绑定。若要求同模型独立数据，现有R269 E1尚未达到。
4. `ORIGINAL239_QUEUE_CHANGE = 0`：不改写共享 docs 索引/队列，不把本报告等同于正式队列验收，不静默扩大历史R269的证据等级。
5. 保持R333至R340原检查器的强制验收入口P0开放；其合成复合候选尚未完成完整仓库原生执行和生产强制绑定。R257 S53 PR #1/#3继续作为未合并证据独立处理。

实际检索范围：仓库原始目录、v7.8索引、154项CSV队列、R269冻结协议/源程序/原CI与提交关系、R073/R105/R106正式状态、两篇英文原始出版/预印本元数据。未检索收费资料，未下载真人原始个人数据，未触发CI。环境为GitHub连接器只读API和公开网页，随机种子不适用。实际账户费用及GitHub免费余额未独立核验。下一最优先科研任务仍是R333至R340真实完整仓库的复合验收与独立篡改负例，随后处理原239的正式逐项裁定。
