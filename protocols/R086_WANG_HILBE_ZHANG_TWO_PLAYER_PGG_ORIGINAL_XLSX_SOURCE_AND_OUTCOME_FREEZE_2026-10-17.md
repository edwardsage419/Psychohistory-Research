# R086原作者两人不对称公共品实验：官方Excel源字节与条件性贡献轨迹冻结协议

2026-10-17。本冻结先于任何R086真人原始Excel行计算和文件实际下载。研究与已结题R085的四人MAT文件为**不同的独立原作者样本与文件**，原四人格式失败不允许被反向记作本二人研究的成功；R085负证据不删除。原作者 Wang, Xiaomin; Hilbe, Christian; Zhang, Boyu 于2025年发布数据 v2 [10.5281/zenodo.16918146](https://zenodo.org/records/16918146)。

## A01: 研究核心问题与未来竞争机制

两人不对称公共物品：资源禀赋不平等（EI）、产出生产率不平等（PI）、优势一致（AI）、优势错配（MI）是否对应与完全平等（FE）不同的真实合作选择、重复合作动态与伙伴响应。制度只是实验参数设计，并非人们自主选择制裁机构，因此不能把R083条件惩罚、R084内生SI/SFI或R085四人数据并入当前本人层面的行为风险集。

只有源文件成功后才取数。正式第一比较是**各处理×各角色初末贡献的同人同session原始单位差**，次级是同人在前后两session平均贡献差以及同一角色的合作与伙伴上轮贡献之间的关联（有明确时间索引后才可实现）。E2判定可为正、负或无明显改变：在某个处理两session均没有合格数据时，该格OPEN而不臆造0。跨处理对比需相同原始数值单位；若禀赋或生产率不同，贡献单位可能不可直接比较，必须根据作者账面endowment定义归一化并单独冻结以后才能比较。**绝不从跨处理描述差宣称实验随机因果**。

## A02：出版方原始数据完整性

Zenodo v2官方固定记录ID16918146，公布了两件不同于四人MAT的两人Excel：
(1) LinearPGG_ExperimentalData.xlsx，官方原文md5 = fc71d20de62c259629ceb56559d8a69e，约504.2kB，作者公开每处理FE114、EI110、PI110、AI106、MI110真人；
(2) ThresholdPGG_ExperimentalData.xlsx，官方md5 = c40171abb172da8e16b0839db98a2cf2，约217.4kB，FE110、EI118、PI112、AI104、MI110真人。
二原始实验的参与者不是当然相同人。将分别从官方 https://zenodo.org/records/16918146/files/<exact-name>?download=1 下载，严格整字节匹配**官方原发表MD5**，仅认Zenodo官方域名和官方固定record，限制1MB/件，并额外输出整文件SHA256以锁定具体字节。若缺文件、MD5差、解析失败任何一个源独立失败，其他源可独立记录来源通过，但全2源合同FAIL，不能将缺的一个替换为插补。

## A03：冻结源架构与读取资格（先纯结构、后真人行为）

原作者正式说明：每处理有两个sheet，Type 1/Type 2，单个focus participant对应四行（session1的两个参与者行为行+session2的两个行为行）。Type1本人在session1是Player1、session2变Player2；Type2反之。阈值实验每session20轮，对应C:V共20列。线性实验第1session22轮、第2session21轮；C:X共22列，第二session最后一轮可能空/占位。作者元数据某条说明误写Threshold session2为session1，但后文明确4行中后2为Session2；严禁把笔误解释为真实重复session1。每条焦点人的两行伙伴行为**不是额外真人**，不能把每四行直接统计为4个参与者或4倍独立观测。

Phase A应只输出文件byte、MD5、SHA256、workbook sheets和每个sheet行列维数、首行/末行的非空位置模式，**不输出任何单元格值、真人ID/姓名、行为行或pair标签**。若实际5×Type1/Type2十个sheet或各表的四行区块、预期人数无法复原，不能进入Phase B实际计算。每处理总人名册原始人数必须匹配元数据。首行是否有header、每个人第4行是否存在合计列需要Phase A观察后写独立Phase B冻结明确字段，任何“删掉异常行”的规则必须先于真实指标且记录。

## A04：正式E2评分前源资格保护

Phase B如能执行，需先冻结明确真实sheet准确names、participant block首行、ID或record键真实性、session分组完整性、Type角色取行顺序、C:V或C:X每列轮次、首末20/22/21的实际缺失、每组/每人统计权重及缺测处理，不能在看结果后更改对照。强制打印并保留总原始participant来源ID去重检查及每处理人数，未核验个体group匹配时不计算同伴条件回归。参与者跨session角色互换，不允许把Type1和Type2误判为不同人同时或删除其真实二session。

原始数据如果包含调查的规范公平答案，需与行为贡献分开，不能在未经规划情况下采纳事后 survey 作为预测特征来声称真实前瞻性。

## A05：计划验证与可见限制

至少20项纯synthetic身份、sheet、四行角色、轮次、缺测、权限测试；首次实际官方数据完整MD5、Excel版本openpyxl解析，仅源模式；成功则第二次独立下载与MD5并比对schema结果SHA和bytes后永久归档。若是真正本人、组、轮贡献E2，要独立Phase B真人评分后再次独立下载源复算，不能用“MD5通过但未计分”冒充真人E2。所有真人ID、逐人贡献数组、原始xlsx都不得上传至Git仓库。PESEN v0.1保持FROZEN。行政结题A01至A06基于当前真实证据，若来源不可访问则限定source gate结题并把E2 OPEN。

R086_FROZEN_BEFORE_NEW_SOURCE=YES
R086_SOURCE_E2_AND_HUMAN_BEHAVIOR_E2=UNESTABLISHED
R086_FOUR_PERSON_R085_FAILURE=INDEPENDENT_NOT_MODIFIED
