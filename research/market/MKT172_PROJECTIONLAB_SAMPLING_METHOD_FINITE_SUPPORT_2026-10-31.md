# MKT172 ProjectionLab 抽样方法与有限支持集审查

UTC 2026-10-31T09:18Z。目标键 (market,ProjectionLab,official_docs_2026-10-31,sampling_method_support)。已读MKT171、官方英文方法帮助及历史更新。本轮仅研究公开机制与人工E1，无账户注册、购买、敏感数据或付费API。

## 官方文档证据
ProjectionLab 2025-04-11官方帮助明确：Chance of Success中Random Start Years及Random-Restart可增加随机试验，最多2000次；Historical, No Looping为固定历史序列，重复试验没有新增路径，因而不可调整次数。2023-02-22官方v3.5.1更新明确随机种子可保存相同收益路径。2026-08-18帮助说明Plan页固定增长单路径，Chance of Success使用历史或随机市场收益、股息及通胀；其他页面继续使用Plan假设。2026-10-01官方教育文章说明成功率是模型条件下的模拟频率，依赖输入分布及收益顺序。

输入：资产、债务、收入、支出、增长、通胀、里程碑和提款。状态：基线及计划变体、逐年现金流、成功/失败路径。算法：固定历史序列、随机起点或随机抽样，具体内部实现未审计。目标：财务可持续性与情景风险。反馈：调整计划并对照历史进展。解释性：可查看试验路径、成功阈值、种子。隐私：官方称可手工录入且无需连接银行账户，服务器权限与安全未独立审计。费用沿用MKT171官方定价Basic免费、Premium年129美元、Pro年549美元；本轮未购买。

英文官方来源：
https://projectionlab.com/help/increase-trials-in-chance-of-success
https://projectionlab.com/blog/monte-carlo-redesign
https://projectionlab.com/help/plan-vs-chance-of-success
https://projectionlab.com/blog/getting-started-with-projectionlab
https://projectionlab.com/financial-terms/monte-carlo-simulation

## 可复算人工E1
Python 3.13.5 Fraction：人工历史收益库[-1/2,0,1/2,1]，资产100，两期每年先收益后提款40，各期余额非负视为成功。三种研究者构造的类比方法：固定不循环连续历史窗口3条成功2条，2/3；循环起点连续窗口4条成功3条，3/4；独立有放回两期抽样16条成功11条，11/16。固定种子172的IID前20条成功16条(4/5)，前2000条成功1383条(1383/2000)。两次相同种子序列全等。收益顺序(-1/2,1)终值-20，反序(1,-1/2)终值40。原生Python九项人工断言PASS。程序 research/market/mkt172_sampling_methods_20261031.py。

推论：历史样本、重采样支持、时间相关性及成功阈值必须记录；重复固定路径不会创造独立证据；增加试验次数无法修复分布失配或真实决策效用偏误。以上方法仅为人工类比，不代表ProjectionLab实际抽样代码或外部校准。官方功能属文档证据，独立验证仍OPEN；新增E2=0/E3=0，零新增费用。下一项MKT173研究尾部依赖、相关性和成功率区间。
