# MKT125 延迟反馈、选择性观察与总体校准不可识别反例

日期：2026-10-29 UTC。目标键：(market,MKT125,none,delayed-label-selection-identification)。基线 main HEAD `551f4a83ab33138857357e4dff2195c783481767`。状态：COMPLETE_BOUNDED_SYNTHETIC_E1。延续MKT124时间留出校准及弃权问题。本报告属于方法知识储备，未启动个人决策产品。

## 英文来源及证据区分

1. scikit-learn官方校准与数据泄漏文档 https://scikit-learn.org/stable/modules/calibration.html 及 https://scikit-learn.org/stable/common_pitfalls.html ，属于DOC_SUPPORTED，说明概率校准与测试信息隔离的机制。没有证明缺失标签可忽略。
2. Chen et al. (2022), Asymptotically Unbiased Estimation for Delayed Feedback Modeling via Label Correction, https://arxiv.org/abs/2202.06472 ，原始论文，讨论延迟转化标签和假阴性；该领域不同于人生决策，不能直接外推其效果。
3. Lechuga López et al. (2026), An Empirical Analysis of Calibration and Selective Prediction in Multimodal Clinical Condition Classification, https://arxiv.org/abs/2603.02719 ，原始实证研究，报告特定医疗多标签任务的选择性预测失败；不能当作个人决策效果的实证验证。
4. Beeminder官方暂停帮助 https://help.beeminder.com/article/98-can-i-put-my-goal-on-pause-for-a-little-bit 、退出目标 https://help.beeminder.com/article/44-how-do-i-quit-a-goal 、No-Excuses Mode https://help.beeminder.com/article/360-what-is-no-excuses-mode 。均属产品DOC_SUPPORTED，未独立验证承诺的行为因果收益或收费争议处理。

## 完整人工实验及精确结果

构造200条纯人工二元结果，两个预测组各100条。high组固定预测概率4/5，low组1/5。每组45条标签已到达、55条仍不可见；high可见15正30负，low可见30正15负。两个人工世界拥有完全相同的90条可见标签、110条缺失指示和预测概率。

世界A：high未到达45正10负，low未到达10正45负。世界B：high未到达0正55负，low未到达55正0负。

| 评价对象 | 可见样本Brier | 完整总体Brier | high真实正例率 | low真实正例率 |
| --- | ---: | ---: | ---: | ---: |
| 可见90条 | 11/25=0.44 | 未识别 | 1/3 | 2/3 |
| 人工世界A完整200条 | 11/25=0.44 | 7/25=0.28 | 3/5 | 2/5 |
| 人工世界B完整200条 | 11/25=0.44 | 11/20=0.55 | 3/20 | 17/20 |

同一可见数据与预测器对应0.28或0.55的总体风险。仅凭可见标签无法辨别这两个世界。仅利用缺失110条每条Brier介于1/25与16/25的结构，总体Brier可识别区间为[11/50,11/20]=[0.22,0.55]。这个界限针对本人工构造且未附加缺失机制假设。

假设知道真实世界每个预测组及结果类别的观察概率，人工oracle逆概率加权(IPW)在A得到7/25，在B得到11/20。A的观察概率分别为high正1/4、high负3/4、low正3/4、low负1/4；B则为high正1、high负6/17、low正6/17、low负1。错误地把全部记录观察率90/200当作常数，IPW仍给11/25。**oracle权重在实际部署中未知**，此人工恢复不能声称真实系统已解决延迟标签偏差。

使用Python标准库Fraction脚本 `research/market/mkt125_delayed_label_selection_20261029.py`，本轮本地原生命令行执行成功，全部内置断言通过；`python -m py_compile`成功。脚本SHA256 `090195e61b0c2380bf1ad3a3871e1fb9b2bb0d49837bde1822e0a121b055a70c`。没有运行scikit-learn或真实模型。归档后需再核Git blob及远端命令行版本身份。

## 产品机制及风险

Beeminder输入手工或集成进度，状态包含目标、承诺窗口、缓冲和失约事件。官方说明多数降低要求或暂停须提前七天，临时问题可联系支持，由其酌情处理。No-Excuses Mode是主动选择的更严格付费承诺，即使事故也不保证免除扣费，支持渠道仍可联系但不承诺取消。官网未公开足以本轮复算的用户长期效用、标签反馈缺失校正算法或公平性校准。费用模式与历史报价见MKT124，未在本轮购买或确认新价格。

候选控制：分别存储预测时点、标签预计成熟时点、实际收到时点、拒答/弃权原因、是否有人工反馈、用户撤销记录及承诺状态。评价需同时报告已收到标签覆盖率、延迟分层Brier、缺失标签风险界限和完整总体尚未识别状态。紧急安全停止须优先于惩罚性承诺，并记录申诉和人工复核；这只是未采用的安全设计，不预设唯一人生效用权重。

## 证据边界与下一步

MARKET E1人工数学反例。DOC_SUPPORTED产品机制及原始论文各自独立标注。真实个人数据0、真人E2新增0、历史E3新增0、外部独立复现0。缺失机制估计、反馈偏差真实规模、用户长期效果、费用敏感性和跨文化适用性均NOT_RUN。未注册收费服务、未支付、未触发GitHub Actions；账户整体免费额度及账单未独立核验。

下一项MKT126：在严格分离延迟标签成熟窗口和弃权策略的前提下，比较有已知随机审计概率与无随机审计时的总体风险识别；同时检查Beeminder争议申诉机制的官方边界。
