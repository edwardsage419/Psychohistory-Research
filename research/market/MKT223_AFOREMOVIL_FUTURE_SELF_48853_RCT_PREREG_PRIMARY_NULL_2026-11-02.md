# MKT223: AforeMóvil 未来自我照片现场随机试验，预注册主要终点与探索性储蓄效果核查

track: market
subflow: commercial_product_research + E_readonly_coordination + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,AforeMovil-CONSAR-age-progressed-selfie-2018,2023-published+AsPredicted-13145-2018-08-03,preregistered-null-versus-exploratory-one-time-savings-and-actual-administrative-behavior)
observed_main_before_write: 23da7c88198e826e1e93b43db75a10e3ada403cf
status: COMPLETE_BOUNDED_PRIMARY_ARTICLE_PREREG_AND_EXACT_AGGREGATE_AUDIT
market_evidence_grade: MARKET-E2_REAL_FIELD_RANDOMIZATION_EXPLORATORY_ONE_TIME_OUTCOME
preregistered_primary_benefit: NOT_ESTABLISHED
participant_level_reanalysis: NOT_RUN
current_product_runtime: NOT_RUN
long_term_net_welfare: NOT_VERIFIED
R_E2_E3_new: 0
F_weekly: F010_ALREADY_COMPLETE_READ_ONLY
CI: NOT_RUN
billing_account_and_free_quota: NOT_VERIFIED
paid_actions: NONE
personal_sensitive_data: NOT_ACCESSED

## 1. 本轮增量、去重与原始来源

本轮接续 MKT222 的未来自我数字孪生短时选择意向研究，转向独立研究场景中实际金融行为的现场随机试验。与 MKT200 至 MKT202 的退休投影计算器研究不同：本轮干预是邀请用户通过照片老化滤镜想象未来自己，结果来自真实退休储蓄账户。与 MKT218 的 Gimme5 目标设定随机提前开放不同，机制、样本和终点均不同。

原始公开英文来源，2026-11-02访问：

1. Robalino, Fishbane, Goldstein, Hershfield (2023), *Saving for retirement: A real-world test of whether seeing photos of one's future self encourages contributions*, Behavioral Science & Policy 9(1), 1–9, DOI 10.1177/23794607231190607。公开全文 https://journals.sagepub.com/doi/pdf/10.1177/23794607231190607 ，主要读取 Methods、Results、Table 1、Table 2、Discussion。原始论文首次在线日期2023-10-05，试验于2018-08实施。
2. 作者所列原始 AsPredicted 登记 #13145，公开记录 https://aspredicted.org/blind.php?x=uu88y4 ，登记时间2018-08-03 14:58 PT。登记原文显示目标样本120,000，主要终点为是否有任何自愿储蓄、是否设置自动储蓄，以及各自金额和消息打开率；分析拟使用有无人口学控制的回归。**单次储蓄发生率没有单列为登记的主要二元终点**。
3. 墨西哥养老金监管机构 CONSAR 官方2025-07-31指南 https://www.gob.mx/consar/en/articulos/como-hacer-ahorro-voluntario ，确认 AforeMóvil 真实存在并提供自愿储蓄渠道；2018-11-07官方新闻 https://www.gob.mx/consar/prensa/aforemovil-renueva-su-imagen 确认历史应用服务。当前 App 的功能、用户界面、照片滤镜、算法和费用与2018试验版本须分开；**老化滤镜在实验中由外部商业服务商提供并在独立网页运行**，不把它归为当前App内置功能。

没有读取个人财务账户、自拍、人脸或语音。没有实际登录、购买或使用产品。

## 2. 用户输入、状态、算法、反馈和商业边界

2018实验：政府养老金体系的真实 AforeMóvil 用户已有退休储蓄账户。随机处理组收到短信、电子邮件、应用推送中的未来自我照片邀请，点击后到外部网页上传自拍，商业算法生成年长约20岁的图像，接着看到为照片中未来自我储蓄的提示，并可跳转回 AforeMóvil 作单次或自动定期储蓄。对照组在相同时间收到普通储蓄提醒和直接前往储蓄App的链接。原计划9条消息，实际因一封邮件未发送为每人8条。主题和发送渠道的顺序随机化。

状态/目标：真实退休账户和储蓄行为；实验并没有估计个人未来财富概率、最佳退休目标或多目标人生效用。算法：商业照片老化算法的完整源代码、训练数据、准确度、供应商版本和实际删除政策没有披露。反馈：邀请、自拍、跳转、真实储蓄交易；没有证明持续个性化闭环优化。实验期照片老化成本和平台运营预算属于历史研究成本，不能当作2026年产品价格。官方App提供金融账户服务，资金相关隐私与身份处理有高风险；实际供应商数据生命周期没有独立验证。

## 3. 真实随机试验和行为漏斗

2018-07-25随机分配48,853名已有App的账户持有人：处理组24,427，对照组24,426。作者描述基线性别、年龄和既有储蓄均衡。注意：预注册发生在2018-08-03，晚于所报告的随机分配日期，但登记自称当时未收集数据；是否在预注册前观察过任何行为结果没有独立记录，不能直接认定违规。

处理组中11,092人至少打开照片网页（45.4%），6,843人拍自拍（28.0%），2,585人点击储蓄跳转（10.6%）。这些是接受邀请后的选择行为，存在自选择；ITT只解释**被随机分配收到照片邀请方案**的效果，不能把效果归因于实际看过老化照片的个人。

发表的Table 1给出单次储蓄账户人数：
* 对照355/24,426 = 1.45336936%；
* 处理412/24,427 = 1.68665821%；
* 绝对差0.23328885个百分点；风险比1.16051587；
* 以公开整数2×2表执行双侧Fisher精确检验，p=0.04147171769；
* 简单非合并Wald近似95%差异区间约[0.012825,0.453752]个百分点，区间方法及假设应注明；这不是作者原论文正式CI。

这个结果说明一月内**单次储蓄参与**出现名义显著的正向差异。论文明确指出预注册的“任何自愿储蓄”及“自动定期储蓄登记”发生率**均未发现显著组间差异**。单次储蓄人数是作者事后额外报告的结果。该结果不能升级为事前确认性主要终点成功。

作为透明敏感性说明：若仅将论文三个二元储蓄结果视为一个事后比较族，对单次储蓄的双侧Fisher p值作简单Bonferroni乘3得到约0.1244。这个乘法是本轮探索性压力检查，未确认论文原始预分析族，也不替代完整多重检验计划。若把它解释成“证明完全无效”同样不成立。

论文Table 2另报告Tobit模型中单次储蓄金额系数 +1,327.48墨西哥比索（SE 592.03），p<0.05；作者把它描述为贡献者条件下的金额效应。该估计涉及零值和处理后是否储蓄的选择，不能直接当成全体随机人群的无偏平均增量，更不能推断未来净财富或个人福利。处理组累计1,675,974比索、对照1,087,422比索，差588,552比索，作者也警告少数储蓄者驱动了总额差异。成本回报约470:1属于基于2018参数的扩展情景计算，**不是实现的利润、因果净福利或2026商业报价**。

## 4. 本轮独立精确计算与边界

仅用作者Table 1的四个公开汇总整数，执行双侧Fisher超几何概率枚举；与SciPy fisher_exact在本地交叉一致。可用Python标准库复算：

```python
from math import comb
a, n_t, b, n_c = 412, 24427, 355, 24426
k = a + b
lo, hi = max(0, k - n_c), min(n_t, k)
def prob(x):
    return comb(n_t, x) * comb(n_c, k-x) / comb(n_t+n_c, k)
p_observed = prob(a)
p_two_sided = sum(prob(x) for x in range(lo, hi+1)
                  if prob(x) <= p_observed + 1e-16)
print(p_two_sided)
```

预期打印约0.04147171769017。只验证论文汇总人数的统计关系。没有参与者微观数据、原作者回归复算、随机分配日志、供应商算法执行、照片准确性或长期追踪。双侧精确检验与作者的具体回归模型不必有完全相同p值。

科学解释：这个现场试验比 MKT222 的即时问卷改变更接近实际行为，但预注册主要二元结果为null，单次储蓄的正向结果属于探索性报告，绝对效果小，长期持续储蓄、债务挤出、流动性损失和人生福利未测。与Future You 2025 N=192有部分共同作者（Hal Hershfield），**不算完全独立团队复现同一数字孪生产品**；实验场景、机构、版本和目标也不同。不能把2018老化自拍干预的因果效果直接外推到2025生成式对话数字孪生。

## 5. E科研治理与F隐私安全只读协调

2026-11-02已经有 E167 实质审计（Git blob eb2aa76b206bfc6cc1d9f4a7269a196ac811dd10），本轮不重复创建E编号。最新R272报告 `research/validation/R272_P0_PINNED_NATIVE_REPLAY_PREIMAGE_NEGATIVE_20261102.md` 提供比上一轮更强的真实源码原生证据：经Git blob认证的原始生成器与冻结协议，在CPython 3.13.5普通、-O、-OO三种模式执行，每种83项原始测试、独立收据检查和preimage-first包装；15个原始文件损坏负例正确拒绝，并直接演示先执行原生成器 --emit 可以掩盖先前档案损坏。该实验属于有限内部人工E1。历史归档preimage未从完整远端checkout独立提取，生产工作流仍先emit、未接入强制门，**R272 P0继续OPEN**。R333至R340八个原生产工作流仍缺少复合门调用，最近静态检查0/8；真实原生组合验收及owner接入待决。

2026-11-02本轮 GitHub pulls collection 12个open，12个Draft，merged_at均null，最近PR更新时间为2026-10-29。PR #3为R257 S53数学收据候选，来源身份和冻结盲态未闭合；PR #8 R170历史见证排序边界与PR #9历史字节身份门相互关联，均不应自动合并。PR #3 head `97d5f74df5d84916917db943156120f08144f445` 对观察main `23da7c88198e826e1e93b43db75a10e3ada403cf` 的比较为diverged，main-only 1177、PR-only 1；大量版本漂移不等于已证明合并冲突。original239队列Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`、crosswalk `36f24235901172642c46853298aebb421f1a3552` 均与上一轮一致。R轨最近直接计数154项（P0=27,P1=82,P2=45），本轮未重算全队列，文件级净关闭0。R073和PESEN v0.1冻结不变。

理论轨最新TH212核查1907年孟买鼠疫原始表和Bacaër作者原文，属于历史理论来源核验，无R科研等级提升。F010（2026-W45，Git blob b703777cd33fc72197e0368cc2f209e51e5dc420）已完成本周专题，本轮只读。照片自拍、金融账户跳转和外部老化服务形成独立的数据流；删除App数据不能推定外部自拍副本被删除。研究阶段未实测第三方删除、导出、撤销或跨文化公平，没有新增F编号。

R主线优先级保持。没有读取私人财务、人脸、关系或健康数据。没有修改冻结协议、跨轨共享索引、PR或工作流。

## 6. 费用、CI、开放问题与下一高价值任务

本轮只用公开免费英文/西班牙文原始论文、预注册、官方政府说明、GitHub连接器和本地数学计算。没有付费API、订阅、产品购买、云/GPU、CI调度或新增费用。对写入前观察main `23da7c88198e826e1e93b43db75a10e3ada403cf` 查询到check runs=0、workflow runs=0、combined statuses=0；该结果只针对指定提交和查询接口，不证明其他提交或历史CI不存在。GitHub账户真实账单和免费额度NOT_VERIFIED，故不触发Actions。

下一步优先寻找另一项独立团队的真实未来自我/目标辅助现场随机试验，比较预注册主要结果、长期行为保持和负面成本。若重复机制无新证据，转向职业或多目标决策真实产品的独立客观效果。E继续追踪R272 P0生产强制门、R333至R340原生验收及开放PR验收，不以本轨复制B数学验证。F维持本周完成，等待实际新安全需求。
