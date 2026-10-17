# R084 来源门冻结：2023 七实验室内生选择惩罚制度实验

日期：2026-10-17。状态：在任何 R084 原作者原始数据复算、文件实际下载或新指标计算前冻结。性质：回顾性的来源资格审计，不冒称对2023年实验重新预注册。R083已结题，PESEN v0.1保持 FROZEN。

## 1. 已知论文事实及新研究问题

Lo Iacono et al. (2023), *The competitive advantage of sanctioning institutions revisited: A multilab replication*, PNAS Nexus 2(5), pgad091; DOI https://doi.org/10.1093/pnasnexus/pgad091，PMCID PMC10153419。作者已发表七个欧洲实验室、每实验室12组×12人，共84组1008人；每人每组30轮选择无惩罚制度 SFI 与含奖惩的 SI，再选择公共品贡献。七个实验室里有五个满足全部原文预注册成功条件，Oxford/Warsaw两个不全部满足；这些**2023年既有论文事实**在此次冻结前已知。原作者在论文“Data availability”链接 OSF https://osf.io/tyxfm/?view_only=604fe6ace95d4e52b89ec8556c4fb304；正文曾给出不同的访问令牌 view_only=5f560d5d570241eaa460b094aed074b4。令牌来自发表的文章，但不能在CI公开记录或输出其内容。

研究新问题是：作者真正的原始实验按人、组、实验室、轮次拆分的文件，能否取得并固定其源字节和变量资格，支持以后独立复算内生制度选择、组级收益/贡献比较？R083的“假定他人实施惩罚时自己的惩罚选择”与这里的真实制度选择不共享参与者或条件干预合同。严禁直接把二者当作一个因果模型。

## 2. 已经找到的原作者元数据线索，尚非真实数据读取

官方 OSF 公共搜索元数据索引 https://share.osf.io/trove/index-card/eccbea3d-0a61-4584-92c5-2dec9dd84f6f（检索日期2026-10-17）列出作者 Sergio Lo Iacono 的原始 OSF component https://osf.io/r7y9n （标题 Replication Data）、文件名 Utrecht_sbj.csv、文件ID https://osf.io/fjyg3、文件版本1、数据量大约0.143 MB及元数据声明 SHA256 f85367e8fff52c29384e51b48baa2b4efed4014c2ef08c00c9ec4549e6d65f3d。仅是OSF indexed metadata；未下载内容，绝不报告这个CSV包含多少行、数据资格或数据结果。该 checksum 只是明确可核验的来源线索。

## 3. 冻结 Phase A 的有限来源任务

首选原作者论文官方 OSF Node tyxfm、其直接关联的 component r7y9n 和原始文件 fjyg3，限定两种论文公开的 view_only 令牌。程序依序检索官方 OSF v2 nodes/{id}、nodes/{id}/files，必要时用官方 file IDs 自身的 v2 files/{id}。允许安全地重试超时、429，不能降低来源域名或转到第三方数据镜像。严格 HTTPS 主机仅 osf.io、api.osf.io、files.osf.io、share.osf.io；任何未经官方来源响应证实的目标URL不可作为原始数据。

若官方元数据真能提供上述 Utrecht 文件的稳定下载链接，Phase A仍**不读取真人原始决策行**；只公开文件 ID、名字、大小、版本、发布方给定sha256是否存在及OSF可达性。只有后续独立先冻结字段映射/完整1008人7实验室84组30轮合同后才计算原始真人数字。

输出安全机读来源收据：OSF node/component/file三个资源的HTTP状态码、是否为JSON、ID及checksum身份匹配、文件目录是否可枚举、文件个数、可信原发布方sha256及是否找到按实验室拆分的可判定数据格式；所有网络异常经归类输出无身份证明/访问令牌/响应原文/真人记录。若访问 blocked/401/403/404，则如实 SOURCE_BLOCKED，禁止静默换源；响应类型是captcha/HTML不能当原始OSF数据。发布作者原论文的7×12×12×30与已发表5/7并标记 PUBLISHED_ONLY_NOT_RECOMPUTED。

## 4. 完整原始E2复验的后续资格门（此阶段不执行）

原研究预定义的三联合成功准则：1A 每实验室最后一轮多于半数（12中至少7）组多数选SI，且最后一轮至少75%的参与者选SI；1B SI贡献高于SFI且依原作者组单位使用双侧Wilcoxon配对检验p<0.05；1C 组级SI净收益高于SFI且相同检验。以来源原分析代码确认组差的配对定义与最后一轮空SFI的处理，不自行把1008名个体当独立84组。冻结未来检查原始人/实验室/组/轮ID唯一性、30轮每个组12人名册资格、20MU贡献单位、净收益奖励惩罚开支、无SFI样本时不造零；只在真正得到源样本和代码、先固定结果比较后才能宣布 E2。

科学推断限制：参与者每轮自主选择 SI/SFI，按实际所加入组比较贡献与利润存在内生选择；不能从两组观测均值宣称随机因果。7个实验室存在5对2的复验异质性；未经组级Wilcoxon重算不得宣称本轮复验成功。R083没有联合来源个体ID，不能声称个体态度转为制度选择的机制已被证明。

## 5. 验收与停止

本来源门实行有界检索：最多两篇论文公开令牌、3个OSF ID和各自官方source metadata接口；每个HTTP请求设固定超时和响应上限；元数据正常访问也不包含真人原始下载。事先运行 >=15 个合成安全/JSON元数据解析单测。第一次真实来源巡检和第二次独立运行均记录不含人的来源收据；输出明确 ACCESSIBLE_METADATA 或 SOURCE_BLOCKED，外部网络失败不得伪装为完整成功。只有取得原作者真正原始字节、冻结分析、通过数据及代码一致性后才可能 E2；此阶段只做 E0-E1来源审计，公开论文事实与OSF公开元数据索引各别标注。审计本身按A01-A06提交正式档案，真实E2 A03必须保持 OPEN。若后续实际来源闭合失败，研究结题为 CLOSED_BOUNDED_SOURCE_GATE 或 BLOCKED（如来源审计自身无法执行）；避免为旧数据源无限停滞，优先开启其他新模型家族。

R084_PHASE_A_ONLY=SOURCE_ELIGIBILITY
R084_HUMAN_REAL_DATA_E2=NOT_YET_ESTABLISHED
R084_ORIGINAL_2023_REPLICATION_FIVE_OF_SEVEN=PUBLISHED_AUTHOR_ASSERTION
R084_INTERVENTION_CAUSALITY=NOT_IDENTIFIED
PESEN_v0.1=FROZEN
