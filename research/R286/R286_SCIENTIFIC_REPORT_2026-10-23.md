# R286 正式科学报告：Temporal Difference Learning（原239目录P0/02-002）补缺

日期2026-10-23 Asia/Taipei。本研究是原239目录中**02-002 Temporal Difference Learning（P0）**的明确补缺R项目，不添加第240个原候选。前置证据审计：[早期全部74份ZIP实际二进制和文本来源检索](../../docs/ORIGINAL_239_P0_EARLY_74_ZIP_CONTENT_SCAN_RESULTS.json)显示旧知识包确有TD学习简式、文献索引和初步研读卡，R063则关注原作者特定模仿学习机制；此前仍未有一个独立标准TD(0)对完整人工未来行为来源进行机制和数学风险验收的主R。

## 一手论文、定义、适用范围

Richard S. Sutton (1988), *Learning to Predict by the Methods of Temporal Differences*, Machine Learning 3:9–44, https://doi.org/10.1007/BF00115009。Sutton & Barto (2018), *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press ISBN 9780262039246，第六章TD prediction；原出版方介绍 https://mitpress.ublish.com/book/reinforcement-learning-an-introduction-2 。TD(0)公式`V(S_t) ← V(S_t)+α[R_(t+1)+γV(S_(t+1))−V(S_t)]`，以一步bootstrap替代完整回报的等待。本文独立构建一个短链原理实验，只复核TD时间顺序和有限未来评分，并不称复现Sutton的1988年具体任务或神经心理机制。

## 事前冻结、完整来源与原模型

[先行冻结协议](../../protocols/R286_TD0_TWO_STATE_5_EPISODE_3_POLICY_576_ORDERED_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，独立冻结Git提交[d055e148](https://github.com/edwardsage419/Psychohistory-Research/commit/d055e14831565571ca9e953d311b55e7eed9ef42)。唯一状态轨迹每回合 A→B（奖励0）→Terminal（奖励Y∈{0,1}），折扣γ=1，固定学习率α=1/2，V(A)=V(B)=0初值。三个人工真p=1/4,1/2,3/4，各有前五个独立训练奖励bit及第六个独立**未来**留出bit；每真p完整64个有序六bit原source，准确质量p^K(1−p)^(6−K)。三个竞争算法共**9人工world、576个带模型标识原source类型**。每模型同p复用相同真实原空间，绝非576个独立受试。

**TD0_ONLINE_CORRECT**严格先更新A的旧状态bootstrap（因此只能用更新前的V(B)），再看到当回合最终奖励并更新B。**MC_COMPLETE_RETURN**等整回合结束后以实际完整回报Y更新A及B。**B_THEN_A_UPDATED_BOOTSTRAP**人为先更新B再让A读新B，属于另一种执行次序的算法，不是标准在线TD(0)，但没有接触未来Y6，不能误叫“留出泄漏”。

## 全部精确结果与两条完全独立数学路线

路线A对每个六bit原source实际调用五次指定更新算法，保存五个训练时点的A/B精确Fraction值以及未碰过的第六奖励评分`(Y6−V5(A))²`，原质量加权求9world未来Brier。路线B不使用算法逐期模拟、甚至无需枚举64个来源：直接根据五次训练奖励Y1..Y5的线性系数c推导V5(A)=Σc_j Y_j，利用独立伯努利二阶矩得到`E[(Y6−V5(A))²]=p(1−p)+p²(1−Σc)²+p(1−p)Σc²`。两路逐原source预测和九项风险全部严格有理相等，第三GitHub CI另行无导入源码从CSV重放576源。

|冻结真实p|标准在线TD0：未来Brier|完整回报MC：未来Brier|先B后A更新：未来Brier|
|---|---:|---:|---:|
|1/4|57/256=0.22265625|1/4=0.25|3643/16384≈0.22235107|
|1/2|155/512≈0.30273438|683/2048≈0.33349609|2445/8192≈0.29846191|
|3/4|123/512≈0.24023438|513/2048≈0.25048828|3741/16384≈0.22833252|

这证明在**这一条两状态短链、固定α=1/2及训练五回合**的有限实验中，正确在线TD0比该MC基线有较小平均未来Brier；但反向错序模型数值甚至可以更小，故不能用“哪个得分低”证明“哪个才是真正TD(0)”。真正区分是信息时间：第一训练回合Y1=1时，TD0 的V1(A)=0，MC为1/2，反向次序为1/4。TD0学习依赖被观察过程先后位置，最后第五个奖励对当前A状态没有即时贡献。这些结果不允许推广成所有环境、所有训练时间或真人社会学习中TD0必优的经验规律。

## 运行证据、真实边界及下一审计

[模型源码与93个真实单元测试](r286_exact_td0_learning.py) · [全部576原六bit训练/留出来源CSV](R286_ALL_576_ORIGINAL_TD0_SIXBIT_FUTURE_SOURCES.csv) · [九世界完全精确结果JSON](R286_EXACT_TD0_RESULTS.json) · [原CSV/JSON SHA256收据](R286_MACHINE_RECEIPT.json)。

[GitHub Actions run39909168454](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39909168454)三job均completed/success，Python3.11及3.12各**93个真实unittest**合计186通过；第三完全独立逐CSV验真、每源位序和A/B五步状态重算、二项解析风险对账及源CSV/JSON SHA检查成功，机器人将全部原数据永久归档main提交[cdf9c6ee](https://github.com/edwardsage419/Psychohistory-Research/commit/cdf9c6ee74630e5ed1fddd26dc25e069b485281c)。

源CSV SHA256 `9e7bf07e8ab61d58185496076c4e1d1256b1f215c2340b4c1e1fae653bc297e1`；结果JSON SHA256 `7512e3a097d993727c1a56dc61d65f333be4d1245f3eb198a1472f0874349eec`。

**实际新证据是有限人工数学E1，不是历史TD人类反应预测、不是作者原数据拟合、不是延时多试验自动加强R063/R073结论**。新增真人E2=0、真实历史E3=0，R073及PESEN v0.1保持冻结。原02-002目录只可标`NEW_DIRECT_BOUNDED_E1_R286`，不能称通用机制被实验证实。
