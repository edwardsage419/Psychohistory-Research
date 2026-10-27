# A轨：Burton-Chellew与West 2021公开社会困境数据，237项汇总研究与原始真人实验分离登记

日期：2026-10-27（Asia/Singapore）。状态：PRIMARY_DRYAD_METADATA_VERIFIED / VERSION_AND_CC0_POLICY_VERIFIED / ARCHIVE_BYTES_BLOCKED / ORIGINAL_EXPERIMENT_SCHEMA_UNKNOWN / R073_DIRECT_COMPATIBILITY_NO。仅登记公开资料；本轮未新增真人E2评分。

## 一手英文来源及独立性

原论文：Burton-Chellew, M. N. & West, S. A. (2021), *Payoff-based learning best explains the rate of decline in cooperation across 237 public-goods games*, Nature Human Behaviour, DOI 10.1038/s41562-021-01107-7。
原始归档：https://datadryad.org/dataset/doi:10.5061/dryad.fn2z34tsv ，DOI 10.5061/dryad.fn2z34tsv。Dryad页面明确显示2021-04-29首发、2021-05-03更新，当前显示三个ZIP文件：
A_Simulation_analyses.zip 29.31 MB，属于人工模拟，E1候选；
B_Black_box_experiment.zip 873.68 KB，页面说明为牛津CESS真人参与者的z-Tree实验原始软件输出，属于潜在E2来源；
C_Comparative_regressions_meta_data.zip 2.54 MB，237项已发表公共物品博弈的跨论文比较元数据，属于研究汇总资料，不能自动作为237个独立可评分真人场次，更不能当作237条独立历史E3事件。
三部分在来源、观测单位与独立性上严格分离，禁止将模拟、单项真人实验和跨论文聚合统计拼接为同一原始人类行为面板。

## 实际核验与许可

实际读取Dryad归档页面的作者、论文、发布日期、版本、三项文件名称与大小、Methods及Usage Notes。Methods明确说明B文件由CESS真人实验的z-Tree输出构成；C文件跨论文抽取的是每轮平均贡献百分比，部分来自图形数字化，故C不是完整逐人行动记录。Usage Notes明确有三类ZIP及各自Read_Me。

实际读取Dryad官方说明：https://datadryad.org/mission 和 https://datadryad.org/help/submission_steps/files 。Dryad对平台发布的数据采用CC0许可规则；需以该归档的具体文件归属、README及可能附带的非数据软件许可进一步核对，当前可登记平台层面的CC0政策，不能凭平台说明推定所有ZIP内第三方代码许可。

尝试直接访问更新版B和C的Dryad下载端点，返回HTTP 403，未取得ZIP原始字节、文件内目录、CSV列名、行数、逐人ID、真实轮次、实验分组、独立场次或数据字节哈希。2021首版与更新版B文件大小存在小幅差异，不应混合版本。没有登录、付费或尝试绕过访问控制。

## 复现资格与价值排序

B原始真人实验：价值中高，优先尝试免费公开下载及Read_Me，核实参与者ID、session、round、真实行为、同伴配对、处理、缺失及时间顺序。原始实验是否与R074/R075/R077的参与者或论文样本重叠仍未知，不能仅凭作者不同认定完全独立。公开归档本身不证明每人轨迹足以开展逐轮预测。

C的237项元研究：适合长期制度或群体合作趋势、研究设计异质性与测量来源审计，必须先识别每项论文、实验组、时间序列单位、样本重复和图形数字化误差。它不满足R073同一实验逐轮双方行动的冻结评分定义。

A模拟：只能进入E1，不能计入E2/E3。

R073原冻结为双人二元囚徒困境、同处理场次留出、100轮及七模型。公共物品博弈的多人贡献与收益结构不兼容。当前R073原协议直接评分资格=NO；如未来取得B数据，只能另行冻结对应的真人E2新协议，R073与PESEN v0.1保持原样。

## 去重与既有证据读时纠错

重新核对R073、R074、R075、R077正式验收JSON，确认项目已经归档四个不同原始真人实验，其中R074、R075、R077是与R073不同的三项原作者实验。R074、R075为新实验内部场次留出并在该实验训练场次拟合，R077为使用R073来源参数、目标1040条记录无标签拟合的跨研究预测。R076复用既有实验，不计第五项。旧报告中的“仍缺第二个独立真人实验”不能作为当前项目全局事实。旧E3标签属于当时“外部实验”口径，当前E3专指真实历史社会演化证据。此次没有重新运行其真人评分。

## 结果、阻塞与费用

本轮新增：一套明确版本的公开数据候选；已核实平台许可政策、文件分类、来源时间与研究单位风险。原始ZIP逐行核验=0；新增E2预测=0；新增E3历史预测=0；外部研究团队复现=0。下一步在免费可用时读取B的Read_Me与z-Tree数据、C的研究ID和每轮平均贡献数据，做去重和许可核验。无私人数据、付费账号、收费API、GitHub Actions或GPU租赁。主动新增费用0，实际账单未独立核验。
