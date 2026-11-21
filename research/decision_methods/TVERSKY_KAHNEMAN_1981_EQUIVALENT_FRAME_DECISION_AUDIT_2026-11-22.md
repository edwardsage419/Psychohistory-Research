# Tversky 与 Kahneman (1981)：等价框架与决策稳定性
实际研究日期：2026-11-22。原始论文：Amos Tversky, Daniel Kahneman (1981), The Framing of Decisions and the Psychology of Choice, Science 211:453–458, DOI https://doi.org/10.1126/science.7455683 。核查范围：出版方摘要、公开大学托管原文开头及问题1和问题2，未完成全文逐页审计。原文 https://www.csc2.ncsu.edu/faculty/mpsingh/local/Social/f25/wrap/readings/Tversky%2BKahneman-framing-1981.pdf 。

问题1：600人基线，A确定救200人，B有1/3概率救600人及2/3概率救0人，N=152，72%选A。问题2：C确定死亡400人，D有1/3概率无人死亡及2/3概率600人死亡，N=155，78%选D。A与C等价，B与D等价。两组样本不同，不能把组间比例差异当作同一人改变偏好的比例。实验为假设性选择，不构成现实医疗建议。

候选规则：自然语言分析中识别等价收益与损失表述，核对总人数、基线、时间窗、分母、条件概率与终点。底层计算和客观评分须对纯语言等价改写保持稳定。若表达方式可能影响理解，最多追问一项：“这两种说法描述同一结果，你希望重新确认选择吗？”保留用户原始选择及确认后的版本，权重只由用户确认修改。

六项合成验收反例（仅设计，未执行）：①救200人与死400人同基线却得到不同客观评分；②1/3救600人与1/3无人死亡被赋予不同概率；③一年存活与五年死亡强制互补；④两组受试者比例被解释为个体偏好转换率；⑤用户因生活质量确认改权重却被强制恢复；⑥把实验群体比例当成个人成功概率。均应判失败。

竞争解释：真实风险偏好、参照点、语言理解、价值判断、情景语义差异。Diederich、Wyszynski、Ritov (2023) 对亚洲疾病问题的扩展研究摘要报告时间压力、疾病类型、需求与概率等调节因素，https://www.cambridge.org/core/journals/judgment-and-decision-making/article/moderators-of-framing-effects-in-variations-of-the-asian-disease-problem-time-constraint-need-and-disease-type/7FE127D11A024B3EA8D1A8D18A244F7F ，只核查摘要，未复算。

去重：McNeil et al. (1982) 已覆盖治疗结果的生存与死亡表达，本项只核查1981年两组原始数字、跨受试者推断限制与计算不变性。Hsee (1996) 是联合和单独评价，研究问题不同。目录级去重完成，全库语义去重部分完成。

状态：原始文献定向核查、候选规则、反例设计及归档 COMPLETE；程序测试、数值复算、独立验证、科学验收 NOT_RUN。下一责任：模型轨负责等价改写的计算不变性；数据轨核查事件和分母；独立验收轨设计留出案例。零新增费用，无 CI，不改 R073、PESEN v0.1 或冻结协议。
