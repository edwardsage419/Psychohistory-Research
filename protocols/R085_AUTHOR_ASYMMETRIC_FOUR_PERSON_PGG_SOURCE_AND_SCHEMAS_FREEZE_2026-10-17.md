# R085 2025年不对称四人公共物品博弈：原作者Zenodo v2来源与架构资格门

日期：2026-10-17；本协议必须在R085任何真实四人数据内容下载、Schema或行为计算之前提交。性质为回顾性的原作者实验复算准备，不是原作者2025年实验前预注册。已有R047等不对称资源实验并不与本原作者样本等同，R083是第三方惩罚策略选择，R084因官方OSF HTTP503来源仍开放。

## A01研究问题与数据资格

研究题目：Wang, Xiaomin; Hilbe, Christian; Zhang, Boyu, *The dynamics of cooperation in asymmetric public goods games*，官方原作者Zenodo数据 v2, DOI https://doi.org/10.5281/zenodo.16918146, 固定原始发布记录 https://zenodo.org/records/16918146。研究要区分资源禀赋/生产率不对称下的四人合作轨迹与实现形式（阈值博弈 vs 线性博弈）。先**只验证来源和模式资格**，严禁在源结构未检验前编造行为分数。

原作者公开文档表明四人线性博弈包含三处理 FE/AI/MI，每处理两实验session、每session20轮，唯一真人 N=FE100, AI104, MI108。四人阈值博弈也为三处理、两session与20轮，唯一真人 N=FE76, AI100, MI100。数据说明强调**两session有相同真人但会重新分组，`GlobalPlayerID`在两session会改变**，所以不能当作不同真人或因行数翻倍推断N翻倍。本源不直接证明在不同实验形式之间同一真人出场，不得通过ID合并两种博弈。

独立官方两个二进制文件（每种研究一份，保留官方文件名，文件内容不可在项目仓库存放）：
* `LinearPGG_4P_ExperimentalData.mat`，原Zenodo v2网页记录**MD5 `42153952f8e6614d09c2d903fd97af62`**，约22.3kB。
* `ThresholdPGG_4P_ExperimentalData.mat`，原Zenodo v2网页记录**MD5 `6036f73c2f758ab3aeed6dcf4f74585b`**，约17.2kB。

## A02 Phase A准入，仅数据原本身份与MAT结构

通过官方记录ID 16918146的Zenodo metadata API确定两个文件名和官方 md5；官方API不可用时仅使用网页已经明确列出的官方固定记录files原始链接，例如 `https://zenodo.org/records/16918146/files/ThresholdPGG_4P_ExperimentalData.mat?download=1` 及线性同构URL。仅允许官方HTTPS主机 `zenodo.org` 与可信其文件后端（若重定向不能独立校验安全则直接拒绝）；不抓取来源不明转载文件。获取后必须严格比对**整文件MD5，及文件大小有界（1—200kB），并记录本地sha256**；任何一件不一致一票否决整个样本统一资格。本MD5仅用作官方身份比对，不当作现代加密真实性证明；配合官方原始发布页面、记录版本和额外重算sha256。

真实源文件只在GitHub Actions runner临时内存/目录存在；不公开个人 ID、轮行为、组号码、survey或原始 .mat，也不打印源码中的个人数据行。

使用scipy读取MAT并只输出**顶层变量名、类型、shape、公开实验条件标签计数、维数资格、解析失败类别**。如为.mat v7.3 HDF5则单独标记模式不适用并停止（不通过改造数据外形绕过冻结的严格类型关）。不得在 Phase A 计算原始贡献均值/相关/差异。若原始MAT的实际变量名或列布局与网页描述不同，必须**在看任何真人行为结果前**新提交R085 Phase B明确定义各变量的原始字段、角色、原作者participant/session/group及round唯一键、FE/AI/MI身份合同、每组四人×20轮、不同session真人ID不能直接等同、缺测策略和结果对比。

如Phase A通过并形成正式source收据，下一步以一个新单独冻结提交作为Phase B才可计算初末合作差、分组平均、双session分层、零假设及双文件跨博弈对比，必须始终区分“群组描述性条件差异”和随机因果。所有原始处理成功须包含FE/AI/MI且维度足够原网页假设，不能调整门槛迎合真实分数。

## E2可能结论与禁止结论

E0=出版元数据，E1=合成代码验证，E2=两份原始字节MD5核验后的真实运行、二次独立复验；必须严格区分。不得根据文件名直接声称拥有真人数据。内生/不确定处理分配、组内相互作用、两session重新分组与跨研究实验制度差异均使因果反事实资格尚未独立建立，不可宣称资源不对称导致合作下降或上升。网页原始摘要与实测数据需严格分开。

## 停止与移交

先执行至少15项synthetic来源HTTP和MAT元数据检查，单次真实Zenodo官方两文件下载，失败按错误类型保存；成功后用独立真正数据重新取回和完整MD5复验。来源未取得可以有界结题，但 E2 永远 OPEN。不向用户要求登录或手工转存；GitHub main每段提交后验证。统一验收A01–A06，PESEN v0.1 FROZEN。

R085_PHASE_A=PRE_REAL_SOURCE_FREEZE
R085_AUTHOR_ORIGINAL_HUMAN_E2=NOT_YET_ESTABLISHED
R085_CAUSAL_ASYMMETRY_OR_HISTORY=NOT_IDENTIFIED
