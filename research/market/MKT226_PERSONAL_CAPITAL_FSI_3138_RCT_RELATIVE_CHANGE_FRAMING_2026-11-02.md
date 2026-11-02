# MKT226 Personal Capital 历史 FSI 随机现场试验：展示框架、相对增长口径与长期福利边界

track: market
subflow: commercial_product_research + E_readonly_coordination + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Personal-Capital-FSI,Levi-2015-UCLA-dissertation-2014-field-experiment,spending-growth-coefficient-versus-level-and-framing-heterogeneity)
observed_main_before_write: b0f773bfe5d9070a524c449193e3bc1526ecdc79
status: COMPLETE_BOUNDED_PRIMARY_FULLTEXT_AND_TABLE_REVIEW
market_evidence_grade: MARKET-E2_HISTORICAL_REAL_PLATFORM_RANDOMIZED_FIELD_EXPERIMENT
original_participant_data_reanalysis: NOT_RUN
historical_FSI_product_execution: NOT_RUN
current_Empower_FSI_feature_equivalence: NOT_VERIFIED
long_term_net_welfare: NOT_VERIFIED
new_R_E2_E3: 0
E_daily: E167_ALREADY_COMPLETE; THIS_RUN_INCREMENTAL_READ_ONLY
F_weekly: F010_ALREADY_COMPLETE; THIS_RUN_READ_ONLY
CI: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_ACTIONS_QUOTA_NOT_VERIFIED
paid_actions: NONE
personal_financial_data: NOT_ACCESSED

## 一、选题与来源边界

上一轮 MKT225 审阅秘鲁财务日记应用加人工访问及短信的组合随机试验。此轮换用不同的真实产品机制：金融账户自动聚合之后，单纯改变用户看到的财务参照框架，是否改变真实支出行为。目标区别在于无需每两周人工上门记录，且有多个随机展示条件对照。

一手全文：Yaron Levi (2015), *Information Architecture and Intertemporal Choice: A Randomized Field Experiment in the United States*, UCLA PhD dissertation，免费英文全文，https://escholarship.org/content/qt1kq722sn/qt1kq722sn_noSplash_4b8228869734cd0bdbf584eaea3ec87c.pdf 。另有2014年11月13日作者论文版本 https://www.runi.ac.il/media/llgb1aex/information-architecture-and-intertemporal-choice.pdf ，本轮未逐表核对该版本，不混合版本统计。二手机构摘要 https://cenfri.org/research-paper/information-architecture-and-intertemporal-choice-a-randomized-field-experiment-in-the-united-states/ ，只作为检索和对照，数值以2015年论文表格为准。

现行产品一手资料：Empower Personal Dashboard 官网 https://www.empower.com/tools 及旧 Personal Capital 品牌迁移说明 https://www.empower.com/empower-personal-wealth-transition 。访问日2026-11-02。旧版2014年FSI实验模块不能直接等同于2026年官网列出的退休规划、现金流与资产分析功能。

本轮实际阅读：论文实验设计第3节、数据第4节、结果第5节、结论第6节、Table 1至Table 3、Table 7至Table 8，以及相关脚注。原始用户级交易记录、预注册、代码、2014年原平台可运行版本均未取得。论文的回归、随机化、分组均衡、漏失和多重比较没有独立重估。

## 二、历史真实产品的输入、状态、算法、反馈

平台：2014年 Personal Capital 的账户聚合财务仪表盘。用户将银行账户、信用卡、贷款、退休和投资账户连接到服务，房产等非电子资产可手动补录。系统展示净资产、收支、投资组合。实验显示在用户登录后的 dashboard 顶部；部分移动端通过安全网页链接访问。历史样本曾经使用过 iPhone 应用，应用角标和每周提醒也影响参与度。

FSI (Financial Sustainability Index) 通过现有净资产、年龄、州、市场上报价的通胀保护终身年金，换算为从现在开始可负担的每月现金流。论文使用 Hueler Income Solutions 年金报价，作者说明采用男性报价网格覆盖35至85岁并跨州，来自多家保险公司。该指标是以当前净资产换算市场报价的参照，不是对未来工资、医疗、家庭支出或个人效用的完整预测。完整生产源码及实时定价数据未公开。

七组随机条件包括：对照组，FSI含历史支出对比曲线，数值人为提高20%的Inflated FSI含对比曲线，Partial FSI只给指数而不提供历史支出曲线，退休开始的FSI无对比曲线，采用投资框架命名的LAI含曲线，退休开始的LAI无曲线。各组仍可看到常规仪表盘，实验版本中某些组替换了仪表盘上的原现金流区域。研究同时改变框架与界面局部内容，不能完全解释为只更换一个文字标签。

用户并没有收到自动执行的消费限制或转账命令。反馈机制是动态金融状态和支出参照线，以及部分设备的提醒。论文没有公布真实个人价值函数、最优人生权重或可验证的个人因果预测校准。

## 三、随机试验规模与真实测量

实验启动于2014年3月17日，七组共3138名用户。入选限制：年龄超过35岁、尚未退休、使用产品至少四个月、最近三个月至少登录一次、此前用过iPhone应用、至少连接一个非手工账户、平均月收入和月支出均在1000至500000美元之间、净资产5000至2000万美元。论文Table 3显示对照组458人，FSI组422人。全样本平均年龄约44.6岁，平均净资产约112.8万美元，基线平均月收入约27623美元、月支出约21418美元。这是高度选择的高净资产平台用户群。

主要观察窗为实验前三个月和之后四个月。收入、支出来自平台聚合交易记录，较纯自报行为更直接，但并不等于审计完整的所有外部账户、现金支出或独立银行数据。没有用户级原始交易重算，也没有长期净财富、主观福利、机会成本或干预结束后的反转测量。

## 四、Table 7 直接核对：10.7% headline 的重要分母解释

论文的支出因变量定义为 (后四个月平均月支出 减 前三个月平均月支出) / 前三个月平均月支出。对照组该相对变化的均值为 +0.211，FSI对照回归系数为负0.107，t为负2.51，论文标记双星。由相同线性回归均值口径得到FSI组的估计变化约 +0.104。

因此，10.7% 的作者摘要表述对应的是两组**相对基线支出变化率之间约10.7个百分点的差异**。不可将其改写为FSI用户在实验前后绝对月支出下降10.7%，也不可把该系数当成相对于实验后对照组支出水平的严格百分比。对照组同期支出平均增长约21.1%，FSI组估计增长约10.4%。作者指出季节性低基线可能推动两组共同增长，随机对照识别组间差异。

Table 7同列还报告 Inflated FSI 相对对照组负0.098，t负2.34；Partial FSI负0.001，t负0.02；Retirement FSI负0.003，t负0.07；LAI负0.015，t负0.34；Retirement LAI负0.004，t负0.09。与FSI组直接比较时，Inflated FSI差异仅 +0.009，t为0.21；Partial FSI +0.106，t为2.49。该组对照支持明确显示支出参照线的重要性，但六个处理组与多种结果的多重检验及预先分析计划尚未核查。

Table 8：FSI相对对照组储蓄变化系数 +0.007，t=2.96；此处储蓄定义为收入减支出，变化量**除以实验启动时净资产**。该0.007不是储蓄率提高0.7个百分点，也不能当作月净财富增长0.7%。FSI储蓄改善的二元指标系数 +0.078，t=2.37。论文没有确认全部资金流入和债务及长期福利净效果。

论文第5.5节报告支出差异主要来自较大且不频繁的交易；对水电、按揭、汽油、餐饮和杂货的类别分析未确认显著效果。具体类别自动归类有误差，五笔最大交易和支出波动属于探索性分解。

## 五、可迁移的候选问题与局限

1. 信息呈现与真实状态数值应分离。相同财务内容若没有明确的支出参照曲线，用户可能无法将其转化为行动。未来评价应分别随机比较纯信息、明确参照、提醒及执行反馈，避免把不同处理捆绑后归因于某一种算法。
2. 将净资产换算成可持续月现金流是有用的跨时间尺度表示方法，但它依赖年金市场、性别和地区报价以及样本财富分布。市场报价不是不含假设的个人真实可持续消费上限。将一个展示值当作人生唯一正确目标存在误导风险。
3. 该试验中人为将指数提高20%仍出现相近的支出组间差异，表明呈现和参照效应可能大于精确数值差异。不能据此推断误报20%是可接受的产品做法；任何未来展示应披露计算假设、校准误差和情景范围。
4. 观察到的支出增速下降不等于生活质量提高。研究没有直接测量必要消费被推迟、负债偿还、健康和关系成本，不能从支出减少推出整体人生福利改善。
5. 现行 Empower 官网确认 Personal Dashboard 的账户连接、自动交易分类、退休情景、资产、预算、储蓄与债务工具免费；另有收费顾问服务。官网未证明2014年实验FSI曲线当前仍可使用。算法细节、实际隐私删除、跨文化表现及长期真实用户效果仍 UNKNOWN。

证据等级 MARKET-E2：只限2014年历史平台随机试验中由作者论文报告的四个月组间支出及派生储蓄效果。没有第三方原始数据复算，不能声称独立E3或当前产品效果。R系列E1/E2/E3不受影响。

## 六、E只读治理与F本周状态

E：2026-11-02 已有 E167 实质审计，Git blob eb2aa76b206bfc6cc1d9f4a7269a196ac811dd10。本轮重读R272报告 R272_P0_EARLY_SUCCESS_BYPASS_IDENTITY_AUDIT_20261102T1444Z.md，Git blob a87be829d9aec0548dac59ed609a5ee90cdf877b：候选工作流中可插入提前成功退出，旧结构检查器在重构夹具中错误接受3/3，严格身份检查拒绝3/3；真实生产调用仍未采用候选，完整checkout与真实Actions false-green测试未运行。R272 P0保持OPEN，R/B已登记，E不重复错误注入或发出重复P0通知。

本轮逐一读取八份 R333至R340 原始生产YAML，均未包含既有 composite acceptance 入口的直接调用，静态强制接入覆盖 0/8。该事实不能代表已实际执行CI。开放Codex PR重新查询为12个，全部Draft，未合并。PR #3数学严格门属于R257 S53，来源身份与历史盲态尚未闭合，head 97d5f74df5d84916917db943156120f08144f445；比较至写入前 main 返回 diverged，main独有1191提交、PR独有1提交。PR #8/#9均为R170，仍需处理历史收据及身份依赖，均未合并。比较结果不证明合并冲突。

original239 待核队列 Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，交叉索引 Git blob 36f24235901172642c46853298aebb421f1a3552，与E167一致，文件级待办净变化0。154项、P0 27、P1 82、P2 45来自已登记并由R272报告重数的同一版本，不自动提升为最新已完成逐项审计。理论TH213交接记录描述性原始历史材料，不能提升R历史E3。R073及PESEN v0.1保持冻结。

F：2026-W45 的F010（Git blob b703777cd33fc72197e0368cc2f209e51e5dc420）已完成本周专题，本轮只读。此实验额外提示财务基准线在样本性别、财富和市场报价不适配时可能影响重要选择。当前研究不采集个人健康、财务或关系数据，不开展真实删除测试或安全部署，不新增F编号。

## 七、CI、费用与下一任务

写入前已核main HEAD并检查目标路径不存在，提交后必须回读文件Git blob及commit。CI只读查询，主动触发 NOT_RUN；账户计费与Actions剩余额度 NOT_VERIFIED；新增付费操作0。

下一商业任务优先检索独立团队对个人账户聚合软件的客观支出和长期净福利复现，或2026年Levi与Benartzi《Mind the App》正式论文与公开数据。其研究设计若为错峰推出加自选安装，应与本轮随机FSI分开登记，不混为随机试验。E下一次重点看R272真正强制调用与R333至R340生产YAML变化；F本周已完成，仅新证据再增量。
