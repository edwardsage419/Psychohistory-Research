# Stiglitz与Weiss（1981）：信贷配给中的逆向选择、激励效应及均衡边界

track: theory
run_date: 2026-11-07 (Asia/Shanghai)
target_key: (theory,StiglitzWeiss1981,AER71-3,screening-incentive-credit-rationing)
prewrite_main_head: c5dc93af8515973fbb3a8edd5369a7525eb3b49b
source: Joseph E. Stiglitz and Andrew Weiss (1981), Credit Rationing in Markets with Imperfect Information, American Economic Review 71(3):393–410.
stable_link: https://www.jstor.org/stable/1802787
open_university_scan: https://www.econ.puc-rio.br/mgarcia/Macro%20II%20-%20Mestrado/StiglitzWeiss1981.pdf
source_type: university-hosted scan of original journal, original text examined through extracted page text; image-level equation verification NOT_RUN
reading_scope: printed pp.393,395–399,408–410; remaining pp.400–407 not systematically reviewed
status: PRIMARY_SPECIFIED_PAGES_READ; CONDITIONAL_THEORY_NOTE; NO_EMPIRICAL_VALIDATION

## 直接阅读范围和理论命题

原刊p393区分两个可能同时存在的渠道：利率提高改变申请人风险组成（adverse selection），也改变已获贷者的项目选择（incentive effect）。这两者均可使银行预期回报与贷款利率不单调，不能把信贷配给全部归因于风险类型的静态筛选。

原刊pp395–397的限定：银行无法辨识项目风险，项目具有相同均值、风险以mean-preserving spread排序；借款人与贷款人风险中性，固定项目规模、有限责任，抵押C固定。借款人收益为 max[R−B(1+r),−C]，银行收益为 min[R+C,B(1+r)]。前者关于R凸，后者凹。因此在同均值且均值保持扩散的风险排序下，借款人更偏好高风险，银行预期回报更低。该比较是模型条件结果，不适用于所有现实借贷合同。

原刊p397定理4：离散风险类型退出借款池可导致银行预期收益曲线出现跳跃。p397–398定理5：当银行平均回报曲线具有内部峰值时，存在某些资金供给函数使竞争均衡出现配给。定理是存在性结论，不能读成所有信贷市场必然配给。原刊pp398–399定理6还允许多个局部峰值及两个贷款利率并存，不能强制单一利率解释。

原刊p398推论1在其图4指定均衡条件下指出，资金供给增加时，存在配给的区间内贷款利率可以保持不变而超额需求减少。该比较静态依赖曲线和市场结构。

原刊pp408–410讨论抵押、股权、非线性合约及动态激励，承认扩展合约集合可能改变结果。作者主张某些扩展条件下仍可能配给，不能据此认为所有合约设计都无法改善配置。

## 独立代数机制核查（非原著完整复算）

设两种项目同均值：安全项目确定产出2；风险项目以各1/2概率产出0或4。借款本金B=1，抵押C=0，承诺偿还额J=1+r且0<J<2。
安全项目借款人净收益为2−J，银行回收J。
风险项目借款人预期净收益为(4−J)/2，银行预期回收J/2。
风险项目相对安全项目的借款人净收益差为(J/2)，随利率增加；银行对风险项目的回收比安全项目少J/2。
这一合成例子仅证明有限责任下风险偏好和银行风险敞口的方向，未证明借款人申请选择、市场出清或信贷配给均衡。若安全项目的参与约束或资金成本不满足，例子不能直接形成贷款市场均衡。

## 竞争解释和识别

与Akerlof1970的商品质量选择、Spence1973的有成本教育信号比较：这里贷款利率本身同时影响筛选与借款后行动。信贷配给还可能由监管利率上限、资本监管、银行流动性、抵押法律、违约执行、关系借贷、宏观冲击或市场势力产生。观察到拒贷和高风险借款人并不能识别原文的两条渠道。

最低限度候选可观测量：申请与拒绝记录、贷款报价及接受情况、申请人事前风险代理、抵押和贷款规模、获贷后项目选择、违约与损失、银行资金成本、同期信贷供给变化。未获贷者的反事实违约率无法直接观察，贷款定价、筛选和项目选择同时内生。若只用获贷样本回归违约对利率，存在严重选择偏差。需要能够区分报价对申请池和对已获贷者行动影响的外生变化，且须审计排除限制与溢出效应。

层级：个人的风险与项目选择，组织的贷款筛选，制度的契约与监管，宏观历史的资金供给冲击。原著为理论存在性证明，非跨国历史或真人预测验证。

## 研究状态与后续

与本日Akerlof1970和Spence1973记录属于不同原著、不同核心问题；本条仅局部比较，不进行统一分类、模型熔炼或产品开发。
C013 2026-11-07已有合格研究，D003 2026-11-02已完成本周专题，均不重复编号。
R073、PESEN v0.1及R E1/E2/E3、MARKET证据分级保持冻结/隔离。
原著指定页文本阅读COMPLETE；独立合成代数核查COMPLETE；公式影像复核NOT_RUN；原著完整模型复算NOT_RUN；真人与历史因果检验NOT_RUN；CI NOT_RUN。新增收费服务0，实际账户计费NOT_VERIFIED。
下一步审读原著pp400–407，逐式核对风险偏好与项目选择的充分条件；优先补足其他弱覆盖学科，不因相邻细节重复创建TH编号。
