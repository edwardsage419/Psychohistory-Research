# MKT224: 未来自我干预的独立现场研究与六个月结果边界

track: market
subflow: commercial_product_research + E_readonly_coordination + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,future-self-aging-intervention,Fintual-Chile-2024+Yeung-HongKong-2026+Stockdale-UK-2020,actual-investment-vs-self-reported-planning-and-subgroup-uncertainty)
observed_main_before_write: db926d20fd57a7dd0e84266247fbe25cbbd21129
status: COMPLETE_BOUNDED_PRIMARY_OPEN_ARTICLE_AND_OFFICIAL_ABSTRACT_REVIEW
market_evidence_grade: MARKET-E2_REAL_RANDOMIZED_EXPERIMENTS_WITH_DIFFERENT_ENDPOINTS
participant_level_reanalysis: NOT_RUN
product_runtime_and_algorithm: NOT_RUN
preregistration: NOT_VERIFIED
long_term_objective_savings_or_welfare: NOT_VERIFIED
R_E2_E3_new: 0
F_weekly: F010_ALREADY_COMPLETE_READ_ONLY
CI: NOT_RUN
billing_account_and_free_quota: NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NOT_ACCESSED

## 1. 选题及去重

接续MKT222未来自我对话的即时意向变化与MKT223墨西哥AforeMóvil 48,853人现场实验的预注册主要终点null。新目标是核查独立作者团队、真实投资平台行为、六个月随访和外部失败复现。以下三项研究互不等同，也未测试同一软件版本。没有把一篇论文的结果外推为另一款产品已证实有效。

本轮实际读取的免费英文或西班牙文来源，访问日期2026-11-02：

1. Kausel, Reyes, Larach, Chacón, Enei (2024), *Does enhancing the vividness in connection with the future self increase savings behavior? A field experiment*, Journal of Behavioral and Experimental Economics 110, 102204, DOI 10.1016/j.socec.2024.102204。大学官方摘要 https://www.ing.uc.cl/publicaciones/does-enhancing-the-vividness-in-connection-with-the-future-self-increase-savings-behavior-a-field-experiment/ 和作者所在学校新闻 https://comercial.usm.cl/noticias/conectandonos-con-el-yo-del-futuro/；RePEc论文记录 https://ideas.repec.org/a/eee/soceco/v110y2024ics2214804324000429.html 。正式论文统计全文未取得免费合法版本，未读取具体回归表或预注册，禁止虚构显著性数值。
2. Yeung, Chung, Chan, Lam, Lin (2026), *Activating and Strengthening Connection to Future Selves Boosts Retirement Preparation Among Middle-Aged Working Adults Over a 6-Month Period*, Journal of Applied Gerontology，2026-04-08在线，DOI 10.1177/07334648261441405。公开英文全文 https://journals.sagepub.com/doi/full/10.1177/07334648261441405 。实读Method、Table1、Table2、Results、Discussion、Limitations、Data Availability。
3. Stockdale & Sanders (2020), *Is future self-relevance necessary to increase saving for retirement? A replication study*, Journal of Applied Social Psychology 50(8), 456–463, DOI 10.1111/jasp.12673。公开英文全文 https://onlinelibrary.wiley.com/doi/10.1111/jasp.12673 。实读摘要与研究结果相关页面。
4. Fintual官方当前产品机制 https://fintual.cl/como-funciona/ ，当前费用说明 https://ayuda.fintual.cl/es/articles/3207275-cual-es-la-comision-de-fintual ，2026-07-30更新。研究用产品与现行功能须分开。

## 2. 真实商业平台：智利Fintual与2024年现场试验

2024年研究由智利大学学者和投资公司Fintual人员参与，研究对象是415名真实投资公司客户，随机三组：普通对照；文字提醒未来自我；文字提醒加数字年龄变化照片。官方大学摘要明确称未来自我干预提高退休储蓄意向，但意向变化只转化为**短期、幅度有限的实际投资金额变化**。2026年另一论文回顾称Kausel等的真实金额结果测于五日随访；由于2024年正式统计全文本轮未取得，五日细节标为跨论文转述，需原文核对。

这个研究包含真实投资金额，优于仅在问卷里分配假想收入。其完整原始数据、三组样本分布、ITT估计值、置信区间、多重检验、预注册和长期行为保持均未独立核实。投资公司参与作者团队，不能认定完全没有利益关系；未发现证明现行Fintual产品仍部署年龄变化照片的官方材料。

Fintual现行官方产品可由用户输入投资期限、风险承受能力和目标，平台提供不同风险组合、基金投资、余额查看、追加投资和赎回，亦可模拟目标。推荐的具体算法权重、风险预测校准和真人长期决策改善没有公开独立验证。2026-07-30官方费用披露普通指定基金年费1.19%，APV类别0.49%；部分底层基金费用另有影响。研究阶段不注册账户、不投入资金、不购买服务。真实产品有投资市场风险、个人身份和财务隐私处理风险。

## 3. 2026年独立研究团队：235人六个月随访的结果范围

Yeung等在香港招募235名20至60岁在职成年人，平均43.2岁，60.4%女性，作者报告所有成功招募并入组者均完成全部测量，留存率100%。这不等于招募来源不存在选择偏差。三组随机分配为CS当前照片99人、FS年龄变化照片66人、FSW年龄变化照片加五日写作70人。照片使用AgingBooth，三组都进行引导想象；FSW组每天收到WhatsApp写作提醒。两周和六个月后以自报四领域退休准备活动量表追踪。没有接入真实退休账户或客观存款流水。

即时结果：年龄变化照片两组比CS报告更强未来自我连贯感，也报告更强负面情绪。未来自我连贯感估计边际均值CS=4.49，FS=5.48，FSW=5.17；负面情绪CS=3.23，FS=3.68，FSW=4.12。假想10,000港币分配任务的退休储蓄比例无显著组间差异。两周时四个领域均没有显著组间主效应或年龄交互。

六个月时，四领域的总体实验条件主效应均未确认。作者报告实验条件与年龄组在财务及心理退休规划上有交互：财务F=5.00，p=.03；心理F=5.91，p=.02。40岁以上FSW对照CS的财务规划自报均值2.17 vs 1.91，Cohen d=.45，95%CI[.05,.86]；心理规划1.58 vs 1.38，d=.43，95%CI[.02,.83]。将年龄阈值从40改45后，心理交互仍显著，财务交互报告p=.09，财务证据对年龄划分敏感。H1和H2未支持，H3/H4部分支持。

重要识别边界：缺少只有写作没有照片的第四组，因此不能隔离写作、照片和互动的独立因果贡献。自报行为不等于行政确认实际储蓄。参与者获得完成测量补贴，样本职业覆盖偏斜，基线未来自我连贯感未测。文章没有明确公开预注册及完整分析代码，数据需向通讯作者合理请求。当前研究并未证明真实六个月账户余额、净财富、健康福利或总体人生效用提高。

## 4. 统计报告口径待核：F检验自由度

2026论文描述三个实验条件乘两个年龄组的双因素ANCOVA，Table2和正文只报告F值与p值，没有明确交互检验分子及分母自由度。按常规三水平条件乘二水平年龄的**完整omnibus交互**，分子自由度应为2；作者的F=5.00,p=.03及F=5.91,p=.02更接近1自由度的预设对比。以N=235、六个单元及三个协变量粗估残差df=226，用公开F分布计算：
F=5.00：df(1,226) p约.0263，df(2,226) p约.00750。
F=5.91：df(1,226) p约.0158，df(2,226) p约.00315。
这只是检验口径一致性检查，未执行原作者ANCOVA或获得设计矩阵。若作者采用1df事前对比或其他模型，数值可有合理解释。**不据此宣布论文统计错误或撤销其结果**。下一次若有合法开放分析代码或预注册，应确认真实自由度、对比编码和多重检验族。检验多个领域、时间点和年龄切分的误报风险仍未闭合。

## 5. 2020年英国独立复现的反向证据

Stockdale和Sanders使用219名参与者，在金融产品网页及假想金额分配任务中尝试复现葡萄牙研究的未来自我相关性调节机制。结果没有复现原先声称的调节作用。该研究是独立研究团队对**相关理论机制**的复现，既未测试Fintual、AforeMóvil或MIT Future You，也没有测量真实账户储蓄。保留null结果有助于防止将未来自我想象视为普适有效干预。

## 6. 对市场有效性与F风险的判断

当前跨研究层次：MIT Future You MKT222仅即时选择问卷；AforeMóvil MKT223真实单次储蓄的探索性名义显著且预注册主要二元终点null；Fintual相关2024试验有短期实际投资金额方向性证据，但完整统计表本轮不可得；香港2026试验有六个月自报规划的年龄子组差异，总体主效应null；英国2020相关机制独立复现null。干预、版本、文化和终点不同，**禁止合并成一个普适因果效应或当作同一产品外部复现**。

MARKET-E2仅表示存在直接随机试验；本轮证据对实际长期客观收益的支持仍为UNKNOWN。用户输入照片、未来目标、财务信息或写作日记会产生不同的数据生命周期，尤其年龄变化图像可能引发负面情绪及年龄刻板印象。未来应先验证自愿选择、拒绝与延后、消极情绪监测、照片第三方删除、真正客观结果和跨文化测量等问题。本轮仅F010已完成专题的案例补充，F没有新增编号，个人敏感资料及真实安全测试均NOT_RUN。

## 7. E只读治理、Codex PR与费用

本地2026-11-02已有E167正式审计，未重复创建E编号。写入前最新main为db926d20fd57a7dd0e84266247fbe25cbbd21129，最新理论轨TH212交接仅对1908温度实验和1912地理分母作有界原文审阅，未产生R新等级。R272最新R/B报告research/validation/R272_P0_UNADOPTED_MANDATORY_CALLER_PROPOSAL_AND_10_MUTATIONS_20261102T1245Z.md：候选YAML位于research/validation，尚未放入.github/workflows；局部静态守卫10/10变异拒绝，但生产原workflow仍先--emit、包含assert、可写回main，P0 OPEN。候选在本轨没有运行，也未触发CI。R333至R340八个工作流组合强制门仍未有已接入证据，原生完整仓库组合验收NOT_RUN。

本轮直接读取pulls collection为12个open，全部Draft、未合并，最近PR更新仍为2026-10-29。PR #3 R257 S53来源身份和历史盲态门未闭合；相对当前main比较为diverged，main-only 1184、PR-only 1，文件统计截断为300条，不能由此判定真实合并冲突。PR #8与#9关于R170历史收据字节身份与见证排序存在逻辑依赖，均不具备自动合并授权。

原239待核CSV Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，交叉索引blob 36f24235901172642c46853298aebb421f1a3552。直接逐行读取CSV共154项，P0=27、P1=82、P2=45；与前轮blob一致，文件级净关闭0。R073、PESEN v0.1继续冻结，E没有重复B数学复算或跨轨文件修改。

本轮只使用公开免费英文/西班牙文原始资料、GitHub连接器和轻量公开统计量计算；没有购买付费论文或产品，没有新增费用，没有读取个人敏感资料，没有创建或触发Actions。写入前main的check runs和workflow runs查询均为0；账户实际计费与免费额度NOT_VERIFIED。GitHub写入后须另行远端回读核验commit/blob与当前CI，不将文件存在等同于科学验收。

next_action: 优先取得Kausel2024合法免费统计全文或预注册，核查真实投资金额的ITT与五日时间窗；同时核实Yeung2026交互自由度及多重检验。若不能取得新原始材料，转向非未来自我类真实长期决策产品，避免继续同题编号。E优先等待R272生产强制门的真实验收，F本周只读。
