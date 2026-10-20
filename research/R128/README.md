# R128：猎鹿博弈——信任门槛、群体成员依赖与重复囚徒困境转换

日期：2026-10-20（Asia/Taipei），原239模型目录候选 **P1 05-004 Stag Hunt Game**。

**科研结题状态**：CLOSED_BOUNDED_ORIGINAL_SKYRMS_2004_STAG_HUNT_GROUP_BELIEFS_REPEATED_PD。
**限定学习状态**：LEARNING_COMPLETE_BOUNDED_SKYRMS_2004_STAG_HUNT_GROUP_TRUST_CORRELATION_AND_REPEATED_PD。
**本轮没有原作者真人行为逐行数据、新的个体独立预测E2分数为0**，R073和PESEN v0.1保持冻结；先完成全部R系列候选逐项学习、后统一分类、最终才熔炼。

## 一手正式来源与真正读到的层级

- Rousseau (1755), *Discours sur l'origine et les fondements de l'inégalité parmi les hommes*，[日内瓦大学所托原法语全文](https://athena.unige.ch/athena/rousseau/rousseau-discours-sur-l-inegalite.html)和[原初版文字转录](https://www.rousseauonline.ch/Text/discours-sur-l-origine-et-les-fondemens-de-l-inegalite-parmi-les-hommes.php)：原始有猎鹿与野兔的集体行动叙事，**并没有赋现代猎鹿收益4/3/0或现代博弈论Nash定理**。
- Brian Skyrms (2004), *The Stag Hunt and the Evolution of Social Structure*, Cambridge University Press，[出版社官方开放第1章完整13页原刊PDF](https://assets.cambridge.org/052182/6519/sample/0521826519ws.pdf)。实际阅读全文，特别可视截图复核其原印刷**p3、p5、p10–12**：原游戏猎鹿/猎兔收益4/0/3，继续概率0.6的囚徒困境变Trigger/Foole协调游戏，猎鹿群体频率的75%理论吸引域边界。**不是已经核读全书其他章**。
- Battalio、Samuelson、Van Huyck (2001), *Optimization Incentives and Coordination Failure in Laboratory Stag Hunt Games*, Econometrica 69(3):749–764，DOI [10.1111/1468-0262.00212](https://doi.org/10.1111/1468-0262.00212)：已核出版社书目与作者公开摘要对“优化收益差”的主张，**未下载处理2001年原参与者逐行实验、完整表格或模型拟合**；该文不构成本轮新真人E2。此前R127已研究Van Huyck1990最低努力与一般2×2风险占优，本期优先原2004正式数值、相关行动与折现策略变换，非重复R127作业。

## 第一项——原书二人信任门槛（真正原作者印刷收益）

两人可选猎鹿S或猎兔H。原书p3明确：双方选鹿各4，某个人独自选鹿0，选兔始终获得3。两个严格纯Nash是(S,S)和(H,H)，(S,S)的共同收益更高但受到别人可能失约的风险。若相信对方选鹿概率q，选鹿期望4q，选兔期望3，故**q=3/4是信念无差门槛**；高于75%才愿选择鹿。这是对给定支付结构的条件性最佳反应，不是测定真实人类有75%信任时必然会做什么。

## 第二项——增加人数与行动相关性，不是一个问题

为考察跨尺度风险，本项目新定义n=2..8人**必须所有人都选鹿才合作成功**的全员参与模型，鹿成功获得4、否则参加鹿者0、兔行动者始终3。**这不是2004作者实测群体制度的原函数**。

若其他n−1人独立且均以p行动鹿，则成功概率为p^(n−1)，本人鹿收益4p^(n−1)，因此需要p^(n−1)>3/4。若每个人的边际合作主观概率p=4/5：
- 只需另1人（二人组）时，鹿期望4×4/5=**16/5=3.2**，鹿胜兔的3；
- 需要另外2人（三人组）时，鹿期望4×(4/5)²=**64/25=2.56**，兔3反胜鹿。
这是对**同边际+独立**的敏感性分析，不是人数变大必然减少现实合作的实证命题。

更重要的是：保持n3的另外两名同伴各自边际合作概率全为**4/5**，不同联合信念可使行动抉择直接**反转**：
- 独立行动，两人均鹿概率16/25，鹿期望64/25小于3 → **兔**；
- 完全正相关，两人均鹿概率4/5，鹿期望16/5大于3 → **鹿**；
- 两人尽量错开的合法分布，均鹿概率3/5，鹿期望12/5小于3 → **兔**。

三者都是严格给出SS/SH/HS/HH四格的**本项目纯合成联合分布**，每人的边际概率都完全一样。在没有独立性证据时，不能从各人边际乘出整个群体的合作概率。该可识别性风险对将来跨群体心理史学建模具有形式化价值，但**没有产生可直接用于历史预测的新真人数据**。

## 第三项——原书印刷的“未来阴影”精确重建

Skyrms第1章p5在数学上从行收益单期PD [[2,0],[3,1]]出发，只允许两种无限重复策略：
1. **Trigger**：开始合作，对方任何背叛后下一轮起永远背叛；
2. **Foole**：每轮始终背叛。

当每轮继续概率/折现因子δ=3/5，书中原印刷的行收益表：

| 本人 / 对手 | Trigger | Foole |
|---|---:|---:|
| Trigger | **5** | **3/2** |
| Foole | **9/2** | **5/2** |

由每轮C/D行动路径独立推导无限期总收益通式TT=2/(1−δ)、TF=δ/(1−δ)、FT=3+δ/(1−δ)、FF=1/(1−δ)，δ=3/5时严格还原原刊所有四格。进一步在δ=0、1/4、1/2、3/5、2/3、3/4、9/10七种折现因子、四种策略配对和五种显式截断轮次T=1,2,4,7,12下，**140个完整组合**逐轮执行有限收益并加上精确几何余尾项，和闭式无限收益完全相等。这比仅背诵原数字增加了可运行的机制审计，**但不是2004作者实验级模型验证**。

仅在这两个跨期策略限制下：δ>1/2才同时存在两个严格对角均衡，δ=1/2时Trigger共同采用不严格（不能称严格双Nash）；δ>1/2时对手选Trigger的信念无差门槛q=(1−δ)/δ。原示例δ=3/5时q=2/3，(F,F)更风险占优而(T,T)共同收益更大；δ=2/3风险并列，δ>2/3时(T,T)反为风险占优。不要将此范围推广到所有无限重复PD策略或现实社会机制设计。

## 第四项——群体频率动力学的原书边界

原书p10–12用连续适应/replicator直觉讨论猎鹿群体人口占比x的吸引域，当个体随机配对且群体合作份额等于匹配信念时，鹿预期4x、兔预期3，收益差符号由4x−3确定，临界比例x=3/4。**相同数学分数不能绕开抽样与共同信念假设，直接把x（人口真实比例）当个人心理信任q**。

为验证这一点，本项目另写**明确不是Skyrms原连续演化方程**的离散收益比例更新：x_next=x×4x/(x×4x+(1−x)×3)，精确有理数在0、3/4、1时不动，x<3/4时下降（如1/2→2/5），x>3/4时上升（如4/5→64/79）。这些是纯数学演算，没有拟合人口实际时间序列，也未建立现实制度影响群体吸引域的因果效应。

## 真实GitHub CI与复算路径

[GitHub Actions 运行39350466421](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39350466421) **completed success：70项单元测试全部通过，0失败；完整n2..8×6边际合作概率的42组合、1,524种其他伙伴的完整行动轮廓概率核查、三类同边际不同关联反例以及140个有限折现＋无限余项核验均成功**。CI已提交原始源码、测试、科学报告三文件的SHA256和机器收据，[独立GitHub回读确认](R128_PHASE_A_SKYRMS_70_TEST_1524_GROUP_140_DISCOUNT_CI_ACCEPTANCE.json)。

- [计算前冻结协议](../../protocols/R128_SKYRMS_2004_STAG_HUNT_GROUP_BELIEFS_REPEATED_PD_FREEZE_2026-10-20.md)
- [一手原书全文样章核阅及原创数学反例的科研报告](R128_SKYRMS_2004_ORIGINAL_STAG_TRUST_GROUP_CORRELATION_AND_SHADOW_FUTURE_SCIENTIFIC_REPORT_2026-10-20.md)
- [Python Fraction精确主程序](r128_skyrms2004_stag_hunt_exact.py)
- [70项真正单元测试](test_r128_skyrms2004_stag_hunt_exact.py)
- [机器原有SHA和真实验收数据](R128_PHASE_A_SKYRMS_70_TEST_1524_GROUP_140_DISCOUNT_CI_ACCEPTANCE.json)
- [正式有界研究和学习结题状态](R128_FINAL_ACCEPTANCE_STATUS.json)

复算指令：PYTHONPATH=research/R128 python -m unittest -v research/R128/test_r128_skyrms2004_stag_hunt_exact.py。

**科学界线：已完成的是一手理论数值、完全合成概率与折现的独立复算。没有直接读取2001原始人类参与者数据，没有任何新的真人E2独立预测、历史E3外部概率评分或自主新跨层模型。** 此阶段只允许有界结束R128模型学习；其他尚未完成的R模型继续按先前既定目录逐项进行，全部完成后才整理分类、然后熔炼。
