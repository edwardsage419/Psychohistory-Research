# MKT173 ProjectionLab 多资产相关性与提款尾部风险

UTC 2026-10-31T10:20Z。目标键 (market,ProjectionLab,official_docs_2026-10-31,cross_asset_dependence_tail_risk)。基线main 1ce20374c049bc0643008622dbd802abc0444b40。承接MKT172抽样方法比较，新增跨资产依赖结构反例。仅研究公开英文官方资料与本地人工数据。

## 实际读取的官方证据
ProjectionLab 2026-08-18官方帮助将Plan固定增长与Chance of Success多路径区分；官方Monte Carlo页面称可使用历史数据、定制概率分布并逐路径查看收益序列；2026-10-01官方科普介绍收益次序风险；2026-08-12安全页面称云端使用Google Cloud/Firebase、传输及静态加密，可不关联金融账户。官方2026-10-31访问的定价页：Basic $0/year，Premium $129/year，Pro $549/year。未注册、未付款、未导入私人数据。
https://projectionlab.com/help/plan-vs-chance-of-success
https://projectionlab.com/monte-carlo
https://projectionlab.com/financial-terms/monte-carlo-simulation
https://projectionlab.com/security
https://projectionlab.com/pricing

文档支持的输入为账户余额、收入、支出、资产配置、增长假设、历史或自定义收益；状态为逐年资产现金流及情景轨迹；输出为成功率、试验路径和可配置成功类别；用户通过修改计划与假设反馈迭代。公开资料未足以核验实际跨资产相关性采样算法、默认联合分布或现实概率校准，均记UNKNOWN。用户可导出JSON及删除计划，见 https://projectionlab.com/help/data-security 。云端数据存储及SOC2 aligned是官方声明，不等同于独立认证或本轮安全审计。

## 新增可复算人工反例
程序 research/market/mkt173_cross_asset_correlation_tail_20261031.py。两种情景均为两资产各50%配置、每资产每年收益±40%各占一半、初始资本100、每年开始提款30、随后按两资产等权组合收益增长，连续两年独立等权宏观冲击，年初再平衡。唯一改变同一年两资产收益相关方向，完全正相关(+1)或完全负相关(-1)。两种情景的每资产边际收益均值0及方差4/25完全相同，平均终值均40。

正相关四个等权终值为36/5、84/5、204/5、476/5；负相关四个等权终值均40。预设终值至少35为成功，正相关2/4，负相关4/4；最差四分位终值分别36/5与40。全数使用Fraction精确有理数，普通Python 3.13.5与python -O各实际PASS；显式ValueError校验，避免优化模式忽略assert。远端脚本blob需另核验。

## 证据分级与方法边界
MARKET官方文档支持输入/输出与商业模式，厂商宣传与现实有效性分离；本实验INTERNAL_SYNTHETIC_E1，只证明指定依赖结构对尾部结果敏感。两个极端相关场景、两年时长、任意提款/成功阈值均为人工选择，不是ProjectionLab内部实现或市场收益预测。未做独立产品运行、历史校准、用户效用测量、真人E2或历史E3。不能用2/4或4/4作为现实人生成功概率。

候选知识储备：保存资产与外部变量联合分布、相关性/共同冲击、提款时点、再平衡、尾部失败路径、目标阈值与敏感性；在模型熔炼前不采纳固定人生效用权重。

状态 COMPLETE_BOUNDED_E1；无新增费用，实际账单/免费额度NOT_VERIFIED。下一MKT174可调查官方Monte Carlo的自定义联合分布支持边界与第三方独立校准研究。
