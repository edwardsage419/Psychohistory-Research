# MKT215：Wysa 两项随机试验的跨场景效果与参与依从性

track: market
subflow: 商业产品真实机制、真人效果与局限
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Wysa,2024-MacNeill-RCT+2026-Meinert-NHS-RCT,short-term-positive-vs-longer-null+engagement+version-drift)
baseline_main: f27af7dd07d87b787665a981b4eeaa3f5a76d2ff
status: COMPLETE_BOUNDED_PRIMARY_PUBLICATIONS_AND_OFFICIAL_POLICY
evidence_scope: MARKET-E2_TWO_DISTINCT_DIRECT_PRODUCT_RCTS
raw_data_reanalysis: NOT_RUN
production_algorithm_execution: NOT_RUN
real_personal_data: NOT_ACCESSED
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 选题与实际产品机制

MKT213 研究 Sleepio，MKT214 研究 juli。本轮转向 Wysa 两项不同研究团队的真人随机试验。2024 年加拿大研究使用修改版 Wysa 自动聊天应用，用户通过自由文本及脚本选项输入情绪和问题，接受 CBT、DBT、动机访谈相关练习、每周报告及提醒。研究版增加慢性病内容，移除付费人工治疗师选项。2026 年英国 NHS 研究使用论文所列 v0.1.4.0，患者填写 PHQ-9、GAD-7，使用自然语言对话、预设内容库和练习，部分信息进入医疗记录并可触发安全提醒。

当前 Wysa 全球隐私政策 v7.2.2 于 2026-10-16 修订，官方披露自有 AI 与第三方 LLM 组合、节点式决策树、临床编写的闭源护理内容库、输入输出安全门及每周衍生摘要。2026 年声明不能倒推为历史试验的生产算法。具体参数、个体推荐校准、真实用户决策改善、当前零售地区定价和生产版本的独立运行均 NOT_VERIFIED。未注册、购买或调用服务。

## 2024 年加拿大随机试验

MacNeill 等，JMIR Formative Research，2024-05-30，DOI 10.2196/50025，NCT04620668。招募关节炎或糖尿病成年人，79 人随机分配，68 人进入分析，两组各 34 人，4 周，对照为无应用干预。PHQ-9：Wysa 8.65 到 5.26，减少 3.39；对照 7.82 到 7.56，减少 0.26；描述性变化差为负 3.13 分，组别乘时间交互 F(2,128)=7.92，p<0.001。GAD-7：Wysa 7.44 到 4.74，减少 2.70；对照 6.09 到 6.56，增加 0.47；交互 F(2,128)=8.15，p<0.001。PSS-10 交互 p=0.16。均为自报量表，样本小，时长短，研究人员未对分组盲法，68 人分析集排除了退组及质量筛查者。论文披露无作者利益冲突，部分经费来自 New Brunswick Innovation Foundation。论文称原始数据位于 OSF，本轮未下载或处理个体资料。

## 2026 年英国 NHS 随机试验

Meinert 等，International Journal of Social Psychiatry，2026-03-05，DOI 10.1177/00207640251415507，NCT05533190、ISRCTN14644939。2022-12 至 2023-04 招募 NHS Talking Therapies 等候者。2161 人初筛，99 人同意，76 人随机，46 人完成 12 周随访，失访 30/76，约 39.5%。完整随访者 Wysa 30 人、对照 16 人，两组均可接受通常服务。原目标样本 480 人。论文报告研究登记早于招募，原始历史登记快照本轮未独立核对。

PHQ-9：Wysa 11.9 到 9.28，改善 2.62；对照 11.0 到 8.41，改善 2.59。基线调整 Wysa 组系数 0.2767，95% CI 负 2.8178 至 3.3711；加协变量和治疗次数后 0.2160，95% CI 负 3.3079 至 3.74。没有确认额外效果。GAD-7 和 EQ-5D-5L 也未确认组间优势。30 名完成随访的 Wysa 成员中 12 人完全没有使用应用，40% 仅针对这个随访子样本。四位访谈者报告聊天重复、深度有限、记忆不一致，访谈结果不能代表全部随机样本。原计划缺失值插补因样本量过小而取消。

研究由 NIHR/NHSX 资助，作者包括 Wysa 员工和顾问，学术作者保留编辑控制。个体数据因隐私未公开，生产代码为商业专有。非显著结果与宽置信区间无法证明真实效果等于零。

## 跨试验判断及商业证据等级

两项均为 MARKET-E2 的直接产品随机试验，研究团队、样本、对照、时长及软件版本不同，不能直接合并或宣称严格独立复现。2024 年支持研究版在慢性病人群 4 周自报抑郁及焦虑改善；2026 年 NHS 场景在通常服务之外没有确认 12 周增量效果，且招募不足、失访及使用率限制估计。没有直接测量长期客观行为、独立决策质量、长期整体福利或推荐算法单独贡献。历史结果不证明当前 LLM 混合版本的效果。

## F010 对照及 E 只读治理

F010 在本地 2026-W45 已 COMPLETE。本轮仅核对 Wysa 2026-10-16 隐私政策：Reset my data 可删除对话及设置，机构 Medical Assistant 和 Co-pilot 记录存在明确删除例外；研究退出、衍生数据及第三方 LLM 处理有单独条件。均为厂商政策声明，实际删除与第三方副本未测试。没有新增 F 编号或读取个人敏感资料。

E167 已在本地 2026-11-02 完成实质审计。新 R272 2026-11-02T03:42Z 报告确认候选收据验证器普通、-O、-OO 三种模式各拒绝 8/8 附加变异；完整可信 checkout 受 DNS 阻塞，原生产工作流强制调用 0/1，P0 OPEN。R333 至 R340 八份工作流对组合入口的强制调用 0/8，push.paths 覆盖 0/8，完整原生组合执行 NOT_RUN，P0 OPEN。R257 S53 PR #1/#3 仍需来源身份和历史盲态审查。

当前 GitHub pulls 实际返回 12 个 open PR，全部 Draft、merged_at=null。PR #3 head 97d5f74df5d84916917db943156120f08144f445，相对观察 main 落后 1140 个 main 独有提交，PR 独有 1 个。original239 队列 Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，交叉索引 blob 36f24235901172642c46853298aebb421f1a3552 均未变化；最近 R 主线逐行统计 154 项，P0 27、P1 82、P2 45，文件级净减少 0。理论 TH208 已交接，C010/D003 已完成。R073 与 PESEN v0.1 冻结保持。

观察 HEAD f27af7dd07d87b787665a981b4eeaa3f5a76d2ff 的 check-runs=0、combined statuses=0、PR-triggered runs=0，其他事件类型和历史 CI 未穷尽。没有主动触发 Actions、收费服务或读取个人敏感数据；实际 GitHub 账单与剩余额度 NOT_VERIFIED。

## 直接阅读的免费英文原始来源

1. 2024 RCT：https://pmc.ncbi.nlm.nih.gov/articles/PMC11176869/ ，DOI https://doi.org/10.2196/50025 。
2. 2026 NHS RCT：https://pmc.ncbi.nlm.nih.gov/articles/PMC13569919/ ，DOI https://doi.org/10.1177/00207640251415507 。
3. Wysa 官方隐私政策 v7.2.2：https://legal.wysa.io/privacy-policy 。
4. Wysa 官方 FAQ：https://www.wysa.com/faq 。
5. 登记入口：https://clinicaltrials.gov/study/NCT04620668 和 https://clinicaltrials.gov/study/NCT05533190 。历史版本 NOT_VERIFIED。
6. 仓库只读：research/operations/E167_R269_ORIGINAL239_P0_SCOPE_AND_OPEN_PR_GOVERNANCE_2026-11-02.md；research/privacy_safety/F010_VALUES_AI_HUMAN_OVERRIDE_DATA_LIFECYCLE_2026-W45.md；research/validation/R272_P0_ARCHIVED_TRIPLET_AND_MANDATORY_CALLER_AUDIT_20261102T0342Z.md；research/validation/R333_R340_P0_EIGHT_WORKFLOW_CALLER_REACHABILITY_AUDIT_2026-11-02.md；docs/ORIGINAL_239_PENDING_154_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-25.csv。

next_action: 优先核对 Wysa 2024 OSF 数据许可与可复算聚合结果、2026 原始预注册历史及依从性敏感性；如缺新证据，转向客观长期结果更充分的真实决策辅助产品。E 跟踪 R272 完整原生及强制接入、R333 至 R340 原生组合及 caller。F010 本周只读，不增编号。
