# R200 变点检测：永久改变、单期异常及短序列变点扫描误报

2026-10-21。原239目录P1/08-024 Change Point Detection。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_BERNOULLI_CHANGEPOINT**。

[计算前冻结协议](../../protocols/R200_CHANGEPOINT_36_WORLDS_11952_TRAINING_PRESCORE_FREEZE_2026-10-21.md)固定低/高/中三种Bernoulli事件率1/4、3/4、1/2，九个生成源/训练候选LOW、HIGH、MID、UP2、UP3、DOWN2、DOWN3、SPIKE2、SPIKE3，观察长度T4/5，m1/2条独立同真机制复制序列，共**36个人工来源世界、11952套完整有序训练组、712种完整去重拟合配置**。单条观测PMF由逐时点Bernoulli连乘与(当期概率/是否事件)分组频数幂两条Fraction来源逐状态完全一致，多复制训练候选likelihood用逐轨迹乘积与Counter指数双法一致。训练仅使用九固定候选的原可见似然，训练同分按LOW→HIGH→MID→UP2→UP3→DOWN2→DOWN3→SPIKE2→SPIKE3顺序；独立新复制序列的T+1事件用真来源成功率评价选中模型下一期二元Brier（直接Bernoulli未来积分与解析bias+variance两法Fraction完全一致）和math.log/70位Decimal双logloss。

**主要反例**：真UP2永久提升(1/4→3/4)与真SPIKE2只在t2异常，两者最初两次真实观测完全同分，但T+1正确真概率分别3/4与1/4。固定MID无变真空假设（每期1/2），事前报警统计量为四备择UP2/UP3/DOWN2/DOWN3的最大完整likelihood比MID、阈值LR≥4；T4、T5全原始数据准确扫描误报率分别**25%和12.5%**，只检验预定UP2单一备择的误报率分别6.25%和3.125%，阈值未经统一5%显著性校准。真实MID来源T5、m2训练自动选九候选后下一期Brier≈0.29181，而预固定正确MID预测为0.25；错误看到变点可损害独立预测。全部九源及36世界包含不利源均保留。完整九源×T4/5扫描来源共有**432条**源概率及备择准确LR/报警原始记录。

[正式科学报告](R200_SCIENTIFIC_REPORT_2026-10-21.md)、[36世界全部预测风险及18来源扫描报警JSON](R200_EXACT_RESULTS.json)、[11952人工有序原训练数据CSV](R200_ALL_11952_ORDERED_TRAINING_DATASETS.csv)、[712拟合完整源likelihood](R200_ALL_712_EXACT_CHANGEPONT_FIT_PROFILES.json)、[432精确扫描原始数据CSV](R200_ALL_432_SOURCE_WEIGHTED_SCAN_PROFILES.csv)、[最终机器验收](R200_FINAL_MACHINE_ACCEPTANCE.json)、[原生程序与39单测](r200_exact_bernoulli_changepoint.py)、[全部原协议/源码/结果七文件ZIP](R200_Exact_36_Bernoulli_ChangePoint_Worlds.zip)永久归档。[GitHub Actions39595142764](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39595142764) Python3.11、3.12各39项测试共78次及第三job完整11952原资料/712拟合/432扫描和ZIP SHA核验三个job全部success，[原数据提交f0832b24](https://github.com/edwardsage419/Psychohistory-Research/commit/f0832b24538347eb8ef493bcca444ed3dbd092bc)。

依据：[Page1954](https://doi.org/10.1093/biomet/41.1-2.100)、[Hinkley1970](https://doi.org/10.1093/biomet/57.1.1)。仅人工E1，不是实际人群变点或制度因果识别，E2/E3新增0，R073与PESEN v0.1冻结。下一 **R201 P1/08-025 Cox Proportional Hazards**；先全R，再分类和熔炼。
