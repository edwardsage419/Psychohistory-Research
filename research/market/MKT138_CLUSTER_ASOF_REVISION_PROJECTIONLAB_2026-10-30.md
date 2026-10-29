# MKT138 群组共享标签、选择性修订与 ProjectionLab 双视图预测机制

日期：2026-10-30 Asia/Singapore。目标键：(market,MKT138,none,cluster-shared-missing-asof-revision-ProjectionLab-plan-vs-monte-carlo)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。只作方法与商业知识储备，R系列先行，个人决策产品开发暂缓。

## 1. 事先固定的有限人工数据

四个群组A1、B1、A2、B2，群组人数依次为1、2、3、4；组别分别为A、B、A、B。每群组所有记录共享一个二元标签，固定预测概率分别为1/4、3/4、3/4、1/4。总记录数10，真正独立的人工标签变量至多4个。预测在所有时点固定，禁止使用未来修订结果修改历史预测。

标签事件：A1在时点2首次见到0；B1在时点3见到1，在时点7修订为0；A2在时点9首次见到1；B2一直未知。仅在cutoff以前的事件可见。对每个cutoff，按未知群组共享标签逐一枚举所有0/1完成方式，不赋予任何完成方式概率，不假定缺失随机。

按人数加权Brier = sum(n_g*(p_g-y_g)^2)/sum(n_g)。同时计算等群组加权Brier，以及A组人数加权Brier减B组人数加权Brier。

| 截止时点 | 已知群组/全部 | 已知记录Brier | 全体人数加权Brier可行界 | 等群组Brier可行界 | A减B风险差可行界 |
| --- | --- | --- | --- | --- | --- |
| 4 | 2/4 | 1/16 | [1/16,33/80] | [1/16,5/16] | [-1/3,3/8] |
| 8 | 2/4 | 19/48 | [13/80,41/80] | [3/16,7/16] | [-1/2,5/24] |
| 10 | 3/4 | 11/48 | [13/80,29/80] | [3/16,5/16] | [-1/2,-1/6] |

时点4、8的未知群组完成方式各4种；时点10为2种。若错误地把未知群组内每条记录的标签当作独立自由变量，组合数会被扩成128、128、16。组合数只是有限可能性数量，不能当成概率或样本量。

时点4至8，B1的迟到标签修订令已知记录Brier从1/16升至19/48；时点10新看到低损失A2后又降至11/48。模型预测完全没有改变。直到时点10，A组Brier低于B组才在本人工设定下对全部可能完成方式成立，前两个时点均不能确定组间风险排序。区间是**确定性部分识别可行界**，不是95%置信区间，不能推导群组公平或因果效应。

程序：research/market/mkt138_cluster_asof_revision_exact_20261030.js。远端拟归档源码在隔离V8实际运行，18项正向断言、6项异常输入拒绝PASS。原生Node.js CLI、GitHub Actions、真人数据验证均NOT_RUN。证据等级人工E1；新增E2预测0、E3为0、外部团队复现0。

## 2. ProjectionLab 2026年英文官方资料机制深读

官方2026-08-18帮助文章：https://projectionlab.com/help/plan-vs-chance-of-success （CDN同文：https://cdn.projectionlab.com/help/plan-vs-chance-of-success）。
官方蒙特卡洛方法说明：https://projectionlab.com/financial-terms/monte-carlo-simulation 。
官方价格：https://projectionlab.com/pricing 。
官方安全页面（更新2026-08-12）：https://projectionlab.com/security 。
官方隐私政策（更新2026-08-07）：https://projectionlab.com/privacy-policy 。
自托管维护政策（2025-03-06）：https://projectionlab.com/blog/update-on-self-hosting 。

* 输入：用户填入资产、收入、支出、投资组合、税务及生活事件时间线；无需连接银行。状态是跨年度账户余额、现金流、投资配置、目标与假设；没有证据支持真实人生多目标效用被唯一优化。
* 机制：Plan页基于输入和每年固定增长率展示单条确定性路径；Chance of Success在同一基础计划上使用历史或随机市场收益、通胀等反复模拟，报告组合在模拟期限内存续的试验频率。官方明确其他页面仍以Plan固定路径为依据。固定路径与随机情景可能得出不同数字，不能把模拟成功比例直接解释为已校准的个人未来发生概率。
* 反馈与解释：允许修改假设、比较方案、查看失败路径与财务目标；高级比较模式在Premium层。官方文章的示例20,000次模拟及成功率是说明性情景，不能当作产品对真实个人长期结果的独立回测。
* 权限与隐私：保存的规划数据位于账户云端，Google Cloud Firestore存储，传输及静态加密；有JSON导出、账户删除、MFA。官方仅称安全控制“SOC 2 aligned”，不能改写为产品取得独立SOC 2认证。活动系统删除后备份按固定周期过期，公开安全页未给出具体备份最长期限。2025年起自托管版本不再获新功能，原有部署的修复支持截至2025-12-31。
* 费用：官网当前Basic $0/年，Premium $129/年，Pro $549/年。只读资料审查，未注册、购买、使用付费试用或连接个人财务数据。
* 证据：产品机制、价格和数据处理边界由2026年官方文档支持；其长期个人决策改善、模拟概率校准、云端安全有效性与优化算法独立验证均NOT_VERIFIED。营销声称和研究证据分别保存。

## 3. 后续

候选字段：cluster_id、person_id、prediction_at、label_first_seen_at、label_revision_at、label_asof_cutoff、missing_cluster_count、group_definition_version、risk_bounds、rank_abstain、simulation_assumption_version。未来须把情景模拟成功频率与真实外部预测校准分开显示。下一MKT139优先比较群组层选择概率与延迟修订的可识别性，不新增人生效用权重。

零新增收费操作、云服务或敏感数据；GitHub实际账单及免费额度未独立核验。R073/PESEN v0.1冻结。
