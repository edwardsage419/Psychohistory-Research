# MKT216：stickK 2015 年随机默认期限试验全文核对与福利识别边界

track: market
subflow: 真实产品机制、随机试验及长期决策效果
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,stickK,2015-NBER-w21406-full-text,randomized-default-ITT-exposure-time-post-contract-proxy-welfare)
observed_main_before_write: 5742fa93bbb05b5f167008b83000bad92893a3e4
status: COMPLETE_PRIMARY_FULLTEXT_BOUNDED
evidence_scope: MARKET-E2_DIRECT_PLATFORM_RANDOMIZED_DEFAULT_TRIAL
prior_work_dedup: MKT193 cited abstract; MKT196 audited distinct 2010 619-person RCT and 2013 retrospective contracts; MKT204 audited Beeminder and a different negative RCT. This file adds original 2015 PDF group counts, analysis denominators, ITT/TOT and post-contract limitations. No new Beeminder RCT claimed.
production_runtime: NOT_RUN
individual_data_reanalysis: NOT_RUN
randomized_registration_history: BLOCKED_403
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NOT_ACCESSED

## 研究对象及实际可确认产品机制

stickK 允许用户设定目标、起止日期、每周目标频率、可选金钱损失、referee 与 supporters；连续目标每周报告，可自行报告成功，也可邀请 referee 核对。当前官方 FAQ 表示创建合同免费，选择财务押金可能导致真实扣款，未成功报告或逾期报告有不同扣款规则。生产行为和历史 2010 至 2012 版本未实际运行，不能把当前条款倒推至历史试验。产品未公开可独立校准的长期人生福利预测器。

与 Beeminder 的连续量化红线及安全缓冲不同，stickK 的核心状态为合同期限、每周报告、成功标记和可选金钱损失。两者的自选目标及报告机制均可能使合同完成率与客观目标结果、长期净福利发生分离。当前研究没有注册、填写卡片、购买产品或使用第三方收费接口。

## 原始随机试验设计及样本口径

Bhattacharya J, Garber AM, Goldhaber-Fiebert JD. Nudges in Exercise Commitment Contracts: A Randomized Trial. NBER Working Paper 21406, July 2015, DOI 10.3386/w21406。直接阅读原始免费 PDF 第 1 至 8 页及表 1、表 2，另读理论部分第 11 至 13 页。工作论文明确声明未经过期刊同行评审。

研究涉及 2010 年 10 月至 2012 年 4 月的 stickK 运动合同。随机显示的默认期限为 8、12、20 周，参与者可修改。随机单位是合同，重复合同可再次随机。初始创建合同的 8,809 名用户按默认期限分组分别为 2,952、2,981、2,876。签署合同人数分别为 2,157、2,212、2,110，总计 6,479，约占发起者的 73.55%。论文称随机化组可观察人口特征基本平衡。

签署者选择的平均合同期限分别为 12.5、14.0、18.8 周，表 2 的期限组间检验 p<0.0001。每周目标锻炼频率约 4 次，押金采用比例约 22.7%，referee 使用约 31%；这些其他合同特征的组间差异在表 2 没有达到 p<0.05。财务押金是自选变量，不能从默认期限随机化中识别押金本身的因果效果。

## 合同内成功周数：ITT 与 TOT 分开

论文在有足够观察窗口的签约合同子集中评估合同内成功周数，n=3,397。按随机分配的默认期限作 ITT：
8 周默认组平均成功 3.2 周，95% CI 2.9 至 3.5；
12 周默认组 3.4 周，95% CI 2.9 至 4.0；
20 周默认组 4.3 周，95% CI 3.8 至 4.9。
20 周默认相对 8 周默认的描述性均值差为 1.1 个成功周。论文说明仅 20 周默认相对短期组的效果达到 p=0.05 显著门槛。此差值不是独立测量的实际运动总时长。

论文另以随机默认期限作为合同期限工具变量，使用两阶段估计的 TOT 结果：短于 11 周合同组成功 3.3 周，95% CI 1.3 至 4.5；11 至 18 周合同组 2.0 周，95% CI 负 0.1 至 4.4；大于 18 周合同组 6.0 周，95% CI 4.5 至 7.6。此估计依赖工具变量识别假设，不能作为实际随机分配到三种合同长度的直接实验均值。中间组的非单调估计与宽区间也不支持通用的“越长越好”。

关键测量限制：成功周数由平台合同报告及可选 referee 产生，论文没有使用独立加速度计等客观运动测量。不同默认期限诱导不同实际合同长度，累计成功周数还受暴露机会影响。不能从 1.1 周差值推断相同时间窗口内的成功率、长期习惯或健康结果改善。

## 合同结束后：继续签约是代理指标

论文明确表示无法观察初始合同结束后的实际锻炼。只能观察用户是否在 stickK 再次签署合同。30 天后续样本 n=4,085，90 天后续样本 n=3,448。ITT 估计：
8 周默认组在 30 天内再签约 2.8%，90 天内 4.3%；
12 周默认组 30 天内 2.8%，90 天内 3.9%；
20 周默认组 30 天内 4.5%，90 天内 5.8%。
20 周与 8 周默认组 90 天再签约的描述性差为 1.5 个百分点。论文报告该组比较达到 p<0.03。

再次签约可以表示持续自我约束需求、对平台的依赖或持续运动兴趣，无法唯一识别长期独立习惯。没有再签约者可能继续运动，已经再签约者也可能仍然没有运动。观察到的合同后代理指标不能升级为客观运动维持、临床健康或个人长期福利改善。

## 福利模型、真实效果与外推限制

作者的四期跨期效用模型引入当前偏好、习惯资本折旧和时间不一致，50,000 组参数随机抽样用于理论比较静态，固定折现率参数。该部分是理论模拟，不是从 8,809 名用户的真实福利观测中识别出的效用分布。模型显示在部分参数条件下，更强的承诺诱导即使增加锻炼也可能降低未来自我效用。模型中的正负福利效应不能当作已测量的真实用户净福利。

主要识别边界：随机默认期限对合同选择和平台记录成功周数有实证支持；金钱押金、referee、长期运动、健康结果、退出后的自主性、整体人生福利没有被本试验独立随机识别。自选使用者外推有限。原始个体数据与历史 AEA RCT 登记页面本轮未读取，登记页访问 403，无法证明研究开始前预注册；不对预注册状态作肯定判断。

研究报告对产品广告声称的“3 倍成功率”不给独立验证。对于 Beeminder，只能将本试验列为相邻产品机制的 MARKET-E2；Beeminder 本身的随机真实用户因果效果仍 NOT_VERIFIED。

## E 当日只读治理与 F 本周状态

2026-11-02 已有 E167 实质治理报告，Git blob 按原文件只读。新 R272 报告 R272_P0_ARCHIVE_PREIMAGE_MASKING_AUDIT_20261102T0447Z.md，Git blob 47635ab8fdc56bfa5adc0e8e441e2946d61e273c，指出生产工作流 push.paths 不覆盖三份归档输入和候选验证器，且 --emit 先重写归档、后验证，可能掩盖原有归档字节损坏。已执行人工负例，真实历史 CI 错误接受未观察到，生产 P0 继续 OPEN；该发现由 R/B 主责，E 不重复制造验证器。R333 至 R340 组合验收强制调用仍为 0/8，完整原生执行 NOT_RUN。R073 与 PESEN v0.1 冻结保持。

原239队列 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，交叉索引 blob 36f24235901172642c46853298aebb421f1a3552，与此前一致。最近已审队列 154 项，P0 27、P1 82、P2 45；本轮没有正式逐项结题，文件级净减少 0。2026-11-02 主线最近理论交接 TH208 Powell 作者稿有 10 项人工算术断言，C010/D003 完成，不能升级 R E2/E3。

本轮查询 12 个开放 Codex PR，均 Draft、merged_at=null，未自动合并。PR #3 head 97d5f74df5d84916917db943156120f08144f445，相对观察 main 5742fa93bbb05b5f167008b83000bad92893a3e4，main 独有 1144 提交、PR 独有 1 提交。来源身份和历史盲态顺序问题继续开放，mergeable 标志不代表科学验收完成。

F010 在 2026-W45 已完成一次高价值专题。本轮只读补充：Beeminder 官方删除说明显示长期用户须联系支持并确认删除；已删除账户的付款历史和支持邮件仍可能保留，备份短期残留，论坛账户需分别删除。其本意为承诺退出摩擦，但对于未来个人决策系统涉及紧急退出和真正数据撤销的安全设计值得研究。只记录厂商政策，不开展个人数据处理或删除实测；不新增 F 编号。

## 免费英文原始来源及核验范围

1. 2015 NBER 原始全文 https://www.nber.org/system/files/working_papers/w21406/w21406.pdf ；DOI https://doi.org/10.3386/w21406 ；本轮直接读论文研究设计、结果、表 1 和表 2、理论与福利模型。
2. 2015 NBER 论文入口及登记链接 https://www.nber.org/papers/w21406 ；登记 https://www.socialscienceregistry.org/trials/784 访问 403。
3. stickK 当前官方合同 FAQ https://new.stickk.com/faq/commitment/Commitment%2BContracts ；财务 FAQ https://new.stickk.com/faq/financial/Commitment%2BContracts ；报告 FAQ https://new.stickk.com/faq/reporting/Commitment%2BContracts 。
4. Beeminder 当前官方 API https://api.beeminder.com/ ；价格 https://help.beeminder.com/article/19-how-much-does-beeminder-cost ；账户删除 https://help.beeminder.com/article/48-how-do-i-delete-my-account 。
5. 仓库既有去重文件 research/market/MKT193_BEEMINDER_COMMITMENT_OUTCOMES_WELFARE_2026-11-01.md；research/market/MKT196_STICKK_DIRECT_OUTCOMES_VERIFICATION_2026-11-01.md；research/market/MKT204_BEEMINDER_ROAD_AKRASIA_DIRECT_SURVEY_NEGATIVE_RCT_2026-11-02.md。
6. E/F/R 原有审计 research/operations/E167_R269_ORIGINAL239_P0_SCOPE_AND_OPEN_PR_GOVERNANCE_2026-11-02.md；research/privacy_safety/F010_VALUES_AI_HUMAN_OVERRIDE_DATA_LIFECYCLE_2026-W45.md；research/validation/R272_P0_ARCHIVE_PREIMAGE_MASKING_AUDIT_20261102T0447Z.md。

next_action: 商业主线转向独立客观结果和明确长期净福利的非同类产品试验；如继续 stickK，优先原始注册历史、独立运动测量或退出后客观随访。E 只读追踪 R272 归档预映像先验验证与触发覆盖、R333 至 R340 原生强制接入、PR #3 科学验收。F 本周只读。无需创建状态性提交、启动 Actions 或增加任何费用。
