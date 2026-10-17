# R087 冻结：原作者134真人10轮条件合作策略稳定性与行为变化

日期2026-10-17。本冻结在任何新的R087真人原始数据逐行评分前提交。2020年作者 Andreozzi/Ploner/Saral *Scientific Reports* 10:13610, DOI https://doi.org/10.1038/s41598-020-70681-z。原论文已经发表条件合作者向不合作者变化的结论，本研究为回顾性独立计算，不宣称E3新预测。

## 一手来源与实验边界
作者GitHub https://github.com/seyhunsaral/stabilitycondcoop 固定commit 979abf87b5d3cfb7aa8be13b81ef233076c3bb75。官方处理CSV data/csv/subjects.csv 长425701字节，Git blob bd4c1550002621bee7dfb50e0d15d317764d1ea9。作者原始处理代码 code/process_raw_data.R blob 522efd459f574ccaef3d9ce1dd2b086ffb70370e；作者主要复现分析 code/main.R blob 3b4f79ce3ddb2d144ea31ccbed26aa03396c9e3c。CSV由作者原始6个 z-Tree session文件经处理代码生成，数据目录也包含原始6份xls。第一份新评分只用作者生成并公开供复现的subjects.csv；其Git blob SHA1以Git标准blob头加原始bytes验证。该CSV真正的作者生成数据 E2并非独立新实验；原始session xls的重新处理一致性还须后续另行检查。

原论文宣称6 sessions、总134人，两个信息条件NoCondInfo 68人、CondInfo 66人，每人完整10个付费真实互动期，4个训练期不包含于处理CSV。如果每人没有恰好period1..10、同一session内subject唯一、恰好6 sessions、处理名称不等于原稿定义、同时同一subject_unq跨不同session或treatment重复或CSV有重复主键，立刻FAIL_CLOSED；不得删除缺测人、改变分母或补造其行为。若任一计分变量的单位/标签不符协议，记录具体源失败类别后另行冻结修正，禁止静默更换类别逻辑。

## 固定5种条件策略与可识别描述性指标
来源字段uc（主体非条件行动）、ccL、ccM、ccH（面对对手L=0、M=50、H=100三类选择的条件行动）、action（当期实际化行动），参见作者README精确字段定义。优先做原作者全部人按各人10期首次与末次的策略变化，策略类别按固定顺序：
D，若ccL=ccM=ccH=0（在任何对手行动下均贡献0）；
F，若ccL=ccM=ccH并且大于0（固定正贡献，无条件）；
C，若ccL≤ccM≤ccH并且ccH>ccL（单调正向条件合作者）；
O，其余全部策略（包括非单调和逆向、非零其他情形）。
只有0、50、100属于3-level条件行动的有效值；非数值、缺失或其他数字FAIL CLOSED，不作0插补。每期每人恰好一种类别。

主要冻结估计：第一与第10期各类别人数（134人、每处理分层）、首末类别4×4转移表，特别C→D与D→C方向计数；每人的策略响应振幅(ccH−ccL)第10期减第1期的等权均值；每人的实际化合作action第10期减第1期等权均值；当期不同处理所有10期逐期的4类别总体频数和平均uc、action、ccH−ccL；逐人10期是否始终同类的匿名人数。保留当期选择与动态策略不同，不能将真实action直接等同于uc或ccH；比率必须以人或人期标定，不能混淆。
竞争机制：M0 条件策略不变化；M1 条件策略向D长期迁移；M2 相反向C迁移。只比较可观察方向，不拟合个体RL或进行网络传播预测，不把2020年作者已提出的结论称原创。

次要作者级描述：NoCondInfo与CondInfo两个处理各三原始session，完整保留来源分组、首末分类与人均行动变动，原处理分配是否随机仍需作者方法独立审计；只描述分层，不赋予因果解释。可用session作为后续holdout而非本次现场拟合；此次不进行原始session外部预测宣称。若置信区间/显著检验未冻结，禁止事后挑选检验标准或形成E3结论。信念字段已知可用，但此研究暂不将belief变动作为因果解释或信息泄露特征。

## 来源、合成、隐私、复算
至少25个纯合成测试，覆盖身份唯一、period缺口/重复、六session、独立两处理、策略四分类边界与反例、负向条件选择、非法动作、全期分母、C→D/D→C、分类与行动差的区别、CSV SHA、个人身份不导出。程序仅发布匿名总体/处理级结果；不输出单人ID、来源单场个人决策、原始CSV、访谈问卷、R原始个体序列和联网地址。严格输出6个session是否达门而不含具体session值。

GitHub CI顺序：先纯合成全部PASS，后固定原始提交source CSV Git blob SHA与原始处理代码Git blob哈希，再运行134×10真人数据；首次匿名结果记录bytes/SHA256；之后独立再次下载及重新验证固定Git blob、整文件匿名结果字节严格一致，才自动归档。任何失败保留阴性，不以合成通过冒充实证。正式E2仍不能证明理念学、心理因果或长期历史演化。PESEN v0.1 FROZEN。

R087_PROTOCOL=FROZEN_BEFORE_NEW_REAL_R087_HUMAN_SCORES
R087_ORIGINAL_PAPER_ALREADY_PUBLISHED=YES
R087_ACTUAL_E2_SCORE=NOT_YET_RUN
