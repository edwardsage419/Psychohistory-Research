# MKT174 ProjectionLab 蒙特卡洛精度与模型失配校准边界

日期：2026-10-31 UTC。目标键：(market,ProjectionLab,official_docs_2026-10-31,structural_misspecification_vs_monte_carlo_precision)。基线 main ede7008d04d715fe1e7d1eb70fd828e098f3253f。继承 MKT172 抽样机制、MKT173 跨资产依赖反例，新增概率模型失配与抽样误差的明确区分。没有登录、注册、购买、使用真实个人数据。

## 公开英文资料实际核对

ProjectionLab 官方：
* https://projectionlab.com/monte-carlo 明示历史回测、自定义概率分布、逐试验查看收益次序、由用户调整成功分类。这些是产品公开功能描述，非独立代码审计。
* https://projectionlab.com/help/plan-vs-chance-of-success ，2026-08-18，Plan 为固定增长假设，Chance of Success 使用历史或随机试验改变收益、股息和通胀，其他页面继续使用固定Plan假设。
* https://projectionlab.com/help/model-investment-growth ，2023-01-22，账户可用不同增长率，随机模拟另有历史或自定义分布配置。
* https://projectionlab.com/pricing ，本轮访问：Basic $0/year，Premium $129/year，Pro $549/year。免费仅限阅读公开文档，没有开通账户。
* https://projectionlab.com/security ，2026-08-12，官方声明使用Google Cloud/Firebase、TLS和静态加密，允许不绑定金融账户；SOC 2 aligned 属厂商陈述，云服务商认证不能视为产品自身通过审计。

独立文献：Cooley, Hubbard, Walz (2003), A Comparative Analysis of Retirement Portfolio Success Rates，https://doi.org/10.61190/fsr.v12i2.4759 ，期刊摘要指出 Monte Carlo 与重叠历史窗口法在部分条件下结果差异显著。该论文比较方法类别，并未独立验证 ProjectionLab。论文正文和原始数据未逐行复算。

输入：余额、收入支出、里程碑、增长假设、历史或自定义回报分布。状态：年度现金流、资产、情景及收益路径。算法：官方文档支持多试验历史或随机情景与成功分类；真实联合分布、相关性估计、历史窗口选择及模型校准细节 UNKNOWN。目标和反馈：用户改变方案与成功标准，查看失败试验和计划敏感性。解释性：单次试验路径可审阅；因果识别与样本外校准未获独立证据。隐私权限：官方云端及不必绑定金融账户；实际访问控制和删除可靠性未独立审计。费用：Basic 公开免费，其余付费，本轮零购买。

## 实际可复算人工反例

程序 research/market/mkt174_mc_structural_misspecification_20261031.js，已在V8环境执行PASS。假设两个二元冲击变量，每个变量向下概率均为1/2。模型A假设独立，四种组合等权；人工真世界B为完全共同冲击，仅(下,下)及(上,上)等权。两模型的单变量边际分布一致，联合失败事件“两者同时向下”的概率分别为1/4与1/2。

错误独立模型预测q=1/4，人工真概率p=1/2，结构误差为1/4。以人工真分布计算常数概率预测的期望Brier：错误模型5/16，人工oracle 1/4，差1/16。该精确结果来自两个有限支持集合的直接枚举。

固定种子174的演示性伪随机抽样，模型A在n=20、200、2000、20000时分别观察到4、44、513、5060次共同向下；共同冲击世界分别9、88、986、10008次。独立模型n=2000时基于其自身q=1/4的正态近似95%抽样区间约[0.2310,0.2690]，与人工真值1/2明显不一致。此区间只描述固定模型内部的Monte Carlo抽样误差，不能作为现实覆盖率保证。伪随机实现用于可复现教学，未作随机数质量检验。

## 证据等级、局限与候选储备

官方功能及定价为DOCUMENTED_VENDOR，独立学术摘要为INDEPENDENT_METHOD_COMPARISON，人工精确枚举为INTERNAL_SYNTHETIC_E1。未运行ProjectionLab产品，未确认其内部联合采样方法，未对任何真实金融或人生结果作校准。E2=0，E3=0。

候选研究要求：分别报告模型内抽样不确定性、结构假设风险和样本外校准；保留联合分布、共振冲击、模型版本、随机种子、失败定义与外部验证窗口；预先冻结评分，保留多目标与未知偏好，不设置单一人生效用权重。未来先做公开数据的滚动时间外测，再考虑产品设计。无收费API、云GPU、付费数据、GitHub Actions，账单/免费额度未独立核验。
