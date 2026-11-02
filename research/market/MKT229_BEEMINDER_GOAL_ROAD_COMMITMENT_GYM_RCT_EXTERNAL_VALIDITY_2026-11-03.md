# MKT229：Beeminder 可核验目标轨道、经济承诺与独立现场试验的外推边界

track: market
subflow: commercial_product_research + E_daily_readonly + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-03 Asia/Singapore
target_key: (market,Beeminder,official-2026-API-pricing-privacy+Spika-2024-JHE-RCT+Bhattacharya-2015-NBER-RCT,product-specific-efficacy-vs-commitment-class-effect-and-deletion-charge-interaction)
observed_main_before_write: 8ea1b480e686cd431bbd01ce6e713a0da281265a
status: COMPLETE_BOUNDED_PRODUCT_PRIMARY_DOCUMENTATION_AND_INDEPENDENT_RCT_ABSTRACT_REVIEW
product_feature_evidence: MARKET-E1_OFFICIAL_IMPLEMENTATION_CONTRACT_DOCUMENTED
external_mechanism_evidence: MARKET-E2_OTHER_SYSTEMS_RANDOMIZED_HUMAN_BEHAVIOR
Beeminder_specific_causal_effect: NOT_VERIFIED
original_participant_data_reanalysis: NOT_RUN
product_account_or_API_execution: NOT_RUN
long_term_net_welfare: NOT_VERIFIED
new_R_E2_E3: 0
E_daily: E168_ALREADY_COMPLETE_2026-11-03_READONLY
F_weekly: F010_ALREADY_COMPLETE_2026-W45_READONLY
ci_status: NOT_RUN
billing_checked: GITHUB_ACCOUNT_BILLING_AND_ACTIONS_FREE_QUOTA_NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NOT_ACCESSED

## 1. 选题去重与范围

MKT225至MKT228聚焦个人财务追踪、参照框架与透支风险提醒；本轮转向现有个人目标管理产品 Beeminder 的另一种机制：可量化进度轨道、预先约定的经济后果、延迟生效的目标放松。独立随机试验检验的是同类承诺合同，研究对象并非 Beeminder 的付费用户。不能将独立研究的因果效应移植为该产品的已证效果。

本轮直接阅读 Beeminder 官网、API Reference、2026 年更新的价格与隐私/数据更正/删除帮助页；独立研究阅读 2024 年 Journal of Health Economics 论文的 PubMed 正式摘要、Lund University 机构摘要，以及 2015 年 NBER 21406 摘要。未取得 2024 年正式论文的完整回归表、预注册及原始个人级数据，未注册 Beeminder 账户。

## 2. 真实产品的输入、状态、算法、反馈

* 输入：用户设定可量化目标、单位、每日或每周目标速度；通过手动 datapoint、应用或第三方集成自动导入数据。官方举例有运动次数、体重、完成任务等。
* 状态表示：Bright Red Line 是随时间变化的分段线性目标轨道。官方 API 的 `road` 数组由 `[time, goal, rate]` 三元组构成，每段给出三者中的两个，第三个由前段终点求得；`roadall` 包含起点和终点。API 另公开 `curval`、`delta`、`safebuf`、`safebump`、`rah` 等状态量，可识别当前偏离、剩余安全天数及一周后约束。这里可核验的是文档描述的数据结构与接口，未独立运行生产计算服务。
* 目标修改：降低难度等改变受约一周 akrasia horizon 限制，防止在临近违约时立即改变承诺。该一周期限属于产品设计规则，官方早期说明承认其普适性经验基础有限，不能当作跨人群最优心理学常数。
* 反馈和经济后果：越过目标线可能触发 derailment 和金额扣款；官方列示阶梯 $0、$5、$10、$30、$90、$270、$810、$2430、$7290，用户可设置上限。用户可申诉非正当 derailment。实际算法对全部边界条件的处理、异常扣款率、长期用户净效用未独立验证。
* 导出：目标数据可通过 CSV、TSV 或 API 导出，Webhook 可推送新增数据；官方提醒 Webhook 失败可能静默发生，建议周期性重新抓取校验。这是有意义的产品可靠性风险，不能将单次 Webhook 成功视为数据完整性证明。
* 纠错：手工 datapoint 可编辑或删除；官方明确删除旧数据可能触发即时 derailment，自动导入数据在源端刷新时可能覆盖本地修改。目标数据纠错与真实扣款存在耦合，后续产品安全研究应分别验证原始数据真实性、费用争议及用户纠正权。

## 3. 2026 年商业和隐私边界

2026-11-02 UTC 访问的官方价格页：Core $0/月，Infinibee $8/月，Bee Plus $16/月，Beemium $81/月，均为页面展示的月付价格；帮助页（2026-03-06 更新）称免费可有三个活跃目标，注册目标需提供付款方式，违约可产生真实扣款。Beemium 可将某些目标的 pledge cap 设为 $0。免费研究范围内未开户、未付款、未启用 API。

官方隐私帮助页说明新目标默认“图表公开、具体 datapoint 私密”；公众若知道目标链接可以查看图表，需主动设置目标私密。官方删除帮助页（2026 年更新）称无活跃目标或新账户可直接删除，长期活跃账户通常须联系支持并确认；删除后仍可能保留支付处理方的历史金额/日期及支持邮件，备份可能短暂存在。上述为厂商政策陈述，未独立验证实际删除范围、备份周期或跨服务副本。

由此得到 F 相关现实风险：公开图表可泄露进度和目标类型；纠正数据可能改变扣款；退出和删除程序引入人为摩擦。将“停止扣款”“撤销数据同步”“归档目标”“删除账户”“清理备份和支付记录”分别记录为不同状态。F010 本周已完成，故本轮仅在市场报告补充证据，不新增 F 编号。

## 4. 独立现场随机试验与识别范围

**Spika、Wickström Östervall、Gerdtham、Wengström（2024），Journal of Health Economics 98:102943，DOI 10.1016/j.jhealeco.2024.102943。** PubMed 和 Lund 机构记录确认在瑞典斯德哥尔摩一家健身房对 1,629 名会员开展随机实验，比较提供软性（无经济惩罚）和硬性（有经济激励/惩罚）承诺合同与对照条件。正式摘要报告，相对于对照组，提供硬合同的月到访次数提高 21%，提供软合同提高 8%；硬合同还提高达到合同目标的概率。2023 年工作论文机构摘要进一步报告，基线运动最少者效果较大。

这两个百分比是**相对对照组的到访次数变化**，不能当作到访概率增加 21 或 8 个百分点；也不能把 21%-8%=13% 当成未经检验的硬合同相对软合同显著因果差异。研究随机的是“被提供的合同”条件，合同实际接受者存在自选，不能直接从总体提供效应推断所有愿意付费的 Beeminder 用户的平均效果。正式论文的表格、置信区间、组别人数、预注册、多重比较和长期福利本轮均未独立核验。

**Bhattacharya、Garber、Goldhaber-Fiebert（2015），NBER Working Paper 21406，DOI 10.3386/w21406。** NBER 原始摘要描述对 4,000 余名寻求运动承诺的参与者随机推动选择 20 周或 8 周合同；较长合同提示使参与者更可能选择长期合同、达到自设运动目标，并在合同结束后再次报名。这是不同场景下对承诺期限选择的随机证据，随机化维度为期限提示，不能当作罚金效应或 Beeminder 直接复现。

**证据分级必须分开**：
* Beeminder 官方功能、API、价格、隐私声明：MARKET-E1（公开技术/政策描述），生产服务独立执行 NOT_RUN。
* 2024 年瑞典健身房和 2015 年 NBER：MARKET-E2（其他承诺合同机制的人类随机试验，摘要范围），完整原始数据重算 NOT_RUN。
* Beeminder 本身改善目标达成率、个人长期福利、避免冲动或跨文化公平：NOT_VERIFIED。
* 任何 R 系列真人独立预测 E2 或历史 E3：本轮均无新增。

## 5. 研究价值与可证伪问题

与 MKT227/228 的自动监测、低摩擦提醒相比，Beeminder 通过用户预先设定目标和经济后果影响行动。下一步有价值的实验应把单纯记录、提醒、延迟修改、软承诺、真实罚金五类处理拆开随机比较，优先采用客观行动数据，另测净费用、压力、退出、错误扣款及其他目标被挤出的机会成本。目标完成率提升仍可能伴随负面福利；系统无法凭进度曲线决定目标本身是否值得坚持。

尤其需要独立验证“用户在重大情境变化后是否仍能及时退出”。一周锁定与账户删除摩擦可能帮助某些用户克服短期冲动，也可能在疾病、失业、家庭冲突等情境增加损失。研究阶段不收集真实敏感资料，不开展个人产品开发。

## 6. E 当日只读核对

2026-11-03 已有 E168 实质治理报告，blob 6f47d589c072b148b732ac3f279d40352ca680c5，故不重复建立 E 编号。最新 R/B 增量 R272_P0_UNPROTECTED_MAIN_TRIGGER_AND_FREEZE_COMPAT_AUDIT_20261102T1740Z.md，blob d59d20ac98966b0ebe6e6f725fea2610d5240249，基于当时真实 GitHub API 快照报告 main 未受保护、required checks 为空、rulesets 为空；生产工作流仅覆盖六个关键样本路径中的 2/6，候选覆盖 6/6，但候选只有一个 job，与冻结协议三 job 口径仍需审查。该证据属于 R/B 已登记的生产 P0 增量，E 只读引用，不重复实施测试或修改分支保护。

本轮直接回读生产 YAML blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d，仍有 `contents: write`、原生成器先 `--emit`、自动提交推送路径，单入口未采纳。12 个 Codex PR #1 至 #12 逐一读回均 open、Draft、merged=false；PR #3 对本轮 main 的 compare 为 diverged，main 独有 1205 提交，PR 独有 1 提交；PR #8/#9 历史收据身份依赖仍需审查，均不具备本轮自动合并授权。待核 CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f、crosswalk blob 36f24235901172642c46853298aebb421f1a3552 均未变，R/B 最新完整解析为 154 项、P0 27、P1 82、P2 45；本轮文件级净减少 0。R333 至 R340 组合验收上次静态证据为 0/8，本轮未重新逐份读取或执行。R073 与 PESEN v0.1 保持冻结。

最新理论轨交接 TH216 仅有理论/方法学增量，C011 当日、D003 本周已完成；不提升 R 科研证据。F010（blob b703777cd33fc72197e0368cc2f209e51e5dc420）2026-W45 已完成，只有只读新案例，无新 F 专题。

## 7. CI、费用、归档和后续

本轮仅使用免费公开英文资料和 GitHub 连接器只读查询，不调用商业产品收费接口，不建立付费账户，不触发 Actions。写入前 main HEAD 与目标路径已检查，目标路径不存在；提交后应独立核验 commit SHA、文件 blob 与远端 HEAD。此前 HEAD 8ea1b480e686cd431bbd01ce6e713a0da281265a 的 combined statuses 和 PR-triggered workflow runs 均为 0 项，这些接口不穷尽所有 CI 触发类型。GitHub 账单与免费额度 NOT_VERIFIED，故主动 CI NOT_RUN。

下一高价值任务：获取 2024 年健身房 RCT 合法免费完整统计表和预注册，核对软/硬合同直接比较、退出/不利事件与长期效果；如无法取得则研究另一个可核验目标偏离产品，避免围绕罚金机制持续增加编号。E 优先跟踪 R272 真实强制验收、main 分支保护和写权限审查；F 本周保持只读。

## 8. 本轮直接使用的英文公开来源

* Beeminder 产品机制：https://www.beeminder.com/overview
* Beeminder API 文档：https://api.beeminder.com/
* 目标轨道与一周期限：https://blog.beeminder.com/dial/
* 2026 定价：https://www.beeminder.com/premium
* 2026-03-06 免费目标/违约说明：https://help.beeminder.com/article/19-how-much-does-beeminder-cost
* 经济承诺阶梯：https://help.beeminder.com/article/20-how-much-do-i-pledge-on-my-goals
* 2026-09-24 数据导出与 Webhook：https://help.beeminder.com/article/41-can-i-export-my-data
* 2026-09-22 数据更正与误扣风险：https://help.beeminder.com/article/39-how-do-i-fix-incorrect-data
* 默认公开图表：https://help.beeminder.com/article/102-privacy
* 账户删除与历史付款保留：https://help.beeminder.com/article/48-how-do-i-delete-my-account
* Spika 等 2024 正式论文 PubMed：https://pubmed.ncbi.nlm.nih.gov/39571470/
* Lund University 2023 工作论文机构摘要：https://www.lusem.lu.se/ulf-gerdtham/publication/fdf4c5f0-dfee-4bea-ba81-565c5145852b
* Bhattacharya 等 2015 NBER 原始摘要：https://www.nber.org/papers/w21406
* 仓库内已审阅的 R/B 审计：research/validation/R272_P0_UNPROTECTED_MAIN_TRIGGER_AND_FREEZE_COMPAT_AUDIT_20261102T1740Z.md
