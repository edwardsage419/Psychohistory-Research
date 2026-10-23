# 心理史学 R251–R253：李雅普诺夫稳定性、精确Shannon信息、有限四人信息级联 — 原R有界E1正式研究索引

日期2026-10-23（Asia/Taipei），对应原239候选模型目录的**11-011 Lyapunov Stability（P2）、11-012 Entropy and Information Theory（P1）、11-013 Information Cascade（P1）**。每项仅采用人工冻结数学机制与完整可再生外生来源，不含新真人E2/历史E3。三个研究包各自先行独立冻结、原生Python、独立代数/理论路线、两版CI、归档job与原source/SHA机器人永久推送main，然后形成科学报告、机读正式验收。继续所有原R先做完后再统一分类、最后熔炼；不提前转入个人决策软件。R073/PESEN v0.1冻结。

## R251（11-011）离散李雅普诺夫稳定性

[九world及完整原source协议](../protocols/R251_LYAPUNOV_9_RATIONAL_MAP_WORLDS_405_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整405人工来源及源码](../research/R251/README.md) · [科学报告](../research/R251/R251_SCIENTIFIC_REPORT_2026-10-23.md) · [正式验收](../research/R251/R251_FINAL_ACCEPTANCE_STATUS.json) · [成功CI run39894992871](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39894992871)。

九有理系数离散映射，每world9初值×5时点，共**405完整初值—时间原结构来源点**，每source设计质量1/45。直接状态递推及初值导数链式规则 vs 独立有理多项式符号复合/形式微分逐项一致；V=x²严格下降可证明若干局部或全局吸引，V在恒等和符号翻转中不变只能证明稳定、不意味着渐近吸引。CUBIC_LOCAL_INWARD与CUBIC_OUTWARD在零固定点乘子同为+1，却分别证明严格局部吸引与不稳定。中心化Logistic r3的V=x²在小正偏差处**单步反而上升**，仍能以`f²(x)=x[1−x²(18+27x)]`和`0<|x|≤1/12`两步严格收缩证明局部渐近吸引。因此区分“某候选函数单步充分条件失败”和“系统真实不稳定”，不能从有限四步样本独立推断无限时性质。最终CI三job success，Python3.11/3.12各84真实测试、**168合格执行**，完整405来源与SHA机器人提交[4fdebd05](https://github.com/edwardsage419/Psychohistory-Research/commit/4fdebd05aac54718b48a7b925f8993fd9647ddba)。

## R252（11-012）Shannon信息与条件互信息

[九world协议事前冻结](../protocols/R252_ENTROPY_9_SIXBIT_WORLDS_576_ORIGINAL_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整576原六bit来源、程序/机器凭证](../research/R252/README.md) · [科学报告](../research/R252/R252_SCIENTIFIC_REPORT_2026-10-23.md) · [正式验收及失败推送保留](../research/R252/R252_FINAL_ACCEPTANCE_STATUS.json) · [最终成功CI run39895279784](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895279784)。

九个人工三观测变量world，各6bit独立公平、每world64原source，共**576完整人工类型**。原source积分完整(X,Y,Z)联合 vs 独立显式列表16可能观察模式（按机制实际支持）全部精确Fraction一致。H/I/I(X;Y|Z)全部以**有理系数和log₂素数**的线性组合保存，非有理值如`(3/4)log₂3−1>0`没有被不当取整或仅靠小数误差“证明”。XOR世界I(X;Y)=0却I(X;Y|Z)=1bit；collider AND下无条件独立，给定其AND后条件I=(3/4)log₂3−1；直接复制X→Y vs隐藏共同原因A→X,A→Y在每完整source上的全部(X,Y,Z)观察逐项相同、全部H/I统计同值，但人工do(X翻转)的Y反事实逐source不同。原[CI run39895196152](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895196152)两个模型版本和第三数学审计通过却因并发main文档提交，机器人git push非快进被拒，故真实**overall failure不能计合格归档**。仅增强有界fetch/rebase/push重试后[最终run39895279784](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895279784)三job success、Python3.11/3.12各85测试共**170次通过**，原576source/JSON/SHA机器人提交[a63c75a0](https://github.com/edwardsage419/Psychohistory-Research/commit/a63c75a047dee455382f5983c70a4c9935e6182a)。数学信息量≠真实认知理解或因果证据。

## R253（11-013）四人Bayesian信息级联及竞争生成机制

[九world完整事前冻结与BHW来源](../protocols/R253_INFORMATION_CASCADE_9_WORLDS_4608_NINEBIT_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [九world完整4608原九bit来源和源码](../research/R253/README.md) · [完整科学报告](../research/R253/R253_SCIENTIFIC_REPORT_2026-10-23.md) · [正式验收](../research/R253/R253_FINAL_ACCEPTANCE_STATUS.json) · [成功CI run39895572949](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895572949)。

Bikhchandani–Hirshleifer–Welch (1992)二元四人级联思路之**有限人工具象化**：每world一公平状态bit θ和四对独立fair二bit信号R，每world512全原source，九world合计**4608完整结构人工来源**。第一原source模拟四人私人信号/公开四步行动 vs 独立θ×16私人信号组合的理论似然乘积分布完全Fraction一致。q=3/4且同收益、先后公开前人行动、后验平手取私人信号：第1/2人各跟随私人信号；若第1/2人行动同向，后两人跟随这一共同选择而不再将自己私人信号更新给公众；人工触发概率5/8，一致条件下准确率9/10，第3/4人无条件准确率27/32，第3人公开选择与私人信号冲突概率3/16。私讯号独立不利用社会信息的对照四人准确率3/4。模仿首个行动和四人共享同一外生信号在相同全source观察四步动作逐项同值，但人工do(Y1翻转)时第二人的行动响应不同；硬编码同向追随策略或报告器模拟贝叶斯级联则与真正明示Bayes策略产生逐source一致公开历史，而个体实际推理/私下行动机制不同。仅可计算人工条件反例，**未证明任何真人实际作了Bayesian推理、出现社会级联或存在历史传播因果**。最终CI三个job全部success，Python3.11/3.12各85单测、**170次实际通过**，全4608来源/JSON/SHA机器人永久归档[4079aad0](https://github.com/edwardsage419/Psychohistory-Research/commit/4079aad0efa6225d718c2d564bc158c6f9077433)。

## 统一验收与下一步

这一轮 **3个独立原目录模型、27个预评分冻结人工world、405+576+4608=5589个完整人工结构原来源类型**；两个Python版本实际单测**168+170+170=508次通过**，最终三个GitHub Actions runs合计9个job success，并有全部原CSV+完整结果JSON+独立SHA机读收据在main长期归档，另有每项完整科研报告和有界正式状态。一个明确失败run和修复记录保留在R252档案，不冒称一切初次就成功。

**新真人E2=0、真实历史E3=0，原R073及PESEN v0.1冻结。** 完整人工来源类型不是独立人类样本、实测历史资料、真实因果识别或经验预测，也不因为CI绿色而晋级E2/E3。原239目录下一项已确认 **11-014 Spectral Methods（P2），拟R254**；仍遵守用户指定的先完成所有R→统一归纳分类→最后熔炼。
