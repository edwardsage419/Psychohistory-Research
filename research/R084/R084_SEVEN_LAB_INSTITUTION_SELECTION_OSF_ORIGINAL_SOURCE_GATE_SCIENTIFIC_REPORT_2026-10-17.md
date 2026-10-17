# R084 正式科学报告：2023年七实验室内生制度选择原作者OSF访问资格失败的有界来源审计

日期：2026-10-17。**R084 来源门范围限定结题，`CLOSED_BOUNDED`；原始真人实验的科学实证复算 E2 = `OPEN/NOT_ESTABLISHED`。** 正式题目：Lo Iacono 等（2023）七实验室惩罚制度竞争的已发表证据与原作者数据可取性审计。冻结协议：`protocols/R084_MULTILAB_INSTITUTIONAL_SELECTION_SOURCE_GATE_FREEZE_2026-10-17.md`，于任何原作者OSF元数据真实请求之前提交 commit `43dd26ecaad1160ea33015c795751a3630302e76`。PESEN v0.1继续FROZEN。

## A01：为什么进行这个研究

从R083（同一人被假定他人会不会惩罚时的策略偏好）转入更高一级的内生制度选择研究。原论文 Lo Iacono, Przepiorka, Buskens, Corten, van Assen, van de Rijt (2023), *The competitive advantage of sanctioning institutions revisited: A multilab replication*, *PNAS Nexus* 2(5), pgad091，DOI https://doi.org/10.1093/pnasnexus/pgad091，PMC10153419，明确报告：
- 7个欧洲实验室，单实验室12个12人组，总 **1008人84组**，每人实验设计 **30轮**；
- 每轮本人先选择参加含惩罚/奖励的制度 SI 还是无制裁制度 SFI，再向公共品贡献；加入SI者可进行付费奖励/惩罚；
- 原作者**在实验前**固定三项联合成功标准：1A末轮至少75%参与者选择SI、超过一半组有SI多数；1B SI成员在末轮贡献高于SFI；1C SI成员末轮利润高于SFI，后二者以组为单位并采用双侧Wilcoxon配对检验；
- 原论文报告**五个实验室满足全部准则**，Oxford和Warsaw未全部满足。Oxford末轮加入SI仅63.9%，Oxford及Warsaw中SI的利润优势未达到上述统计标准。

这均是**2023年原作者已发表结果**，并非本次R084用真实真人逐行数据重新计算的结果。2026-10-17初始研究阶段设定为验证原作者原始数据OSF接口资格，原数据不合法可取时正式E2结果不输出。

## A02：官方一手路径和独立公共索引

原论文Data Availability官方OSF节点 https://osf.io/tyxfm/?view_only=604fe6ace95d4e52b89ec8556c4fb304 。论文Introduction的另一出版链接有不同view-only授权令牌（不在CI终端输出这两个令牌）。在另一条**OSF本身公开的元数据** [Trove Index Card](https://share.osf.io/trove/index-card/eccbea3d-0a61-4584-92c5-2dec9dd84f6f)中，确认元数据登记的原作者 Sergio Lo Iacono，名为 `Replication Data` 的component ID `r7y9n`，以及文档 `Utrecht_sbj.csv` 的原始文件ID `fjyg3`、版本1和公开指称的SHA256
`f85367e8fff52c29384e51b48baa2b4efed4014c2ef08c00c9ec4549e6d65f3d`。

**这个哈希来自OSF搜索索引，未由R084下载对应文件并以真实字节计算。** 本次并未实读全部7实验室对应原始表文件列表、原始程序、列名、文件行数、每组人数或任意参与者的行动记录；因此不能给出原始E2来源通过的表述。

## A03：安全纯合成测试、真实访问尝试及第二次独立结果

[元数据巡检程序](r084_original_osf_7lab_metadata_source_gate.py)以 HTTPS官方OSF API仅检查固定project id `tyxfm`、原作者component id `r7y9n`、原始Utrecht源文件id `fjyg3`，在原论文**两个不同的公开view-only链接下**各查询对应3个具体资源及2个目录，共计每次**10个官方元数据请求**。连接HTTPS主机白名单和大小上限，不下载原始真人文件，不泄露可访问者能力串。此前[26项合成协议和安全单测](test_r084_original_osf_7lab_metadata_source_gate.py)验证源身份、sha源字段校验、防泄露、错误状态、目录及JSON类型，不使用真实真人源行。

- [第一次原作者OSF元数据来源实跑 GitHub Actions 39001728447](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001728447)：纯合成26项PASS，尝试实际OSF元数据请求，**10/10次均 HTTP 503**，可解析的官方JSON元数据 =0；来源审计程序执行success仅代表**失败收据按协议生成**，不代表原始来源成功。
- [第二次独立重跑 39001798435](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001798435)：26项合成PASS，**第二次10/10元数据请求仍HTTP503**，得到完全同样的**4,185字节安全失败JSON**，对第一次摘要 **SHA256 `3ebccaca8f6b631afeaa927aeadc677d896b8aa358ab498c3309c2542028e1ac`** 逐字节一致；永久归档[完整匿名原始API响应状态收据](R084_2023_SEVEN_LAB_ORIGINAL_OSF_OFFICIAL_SOURCE_GATE_FAIL_CLOSED_E0_RESULTS.json)，Git blob `25bb98cbefaa034fdd00a5b6f60c2e67b242ce6e`。
- 两次访问分别处在本次GitHub runner运行环境下；不能从两次503推断OSF对所有人、所有时间永久不可用，也不能把经过公开搜索Trove看到的条目等同于人类数据内容读取。

实际下载的原始真人数据文件 **0**；读取人类行 **0**；原作者效应的实算 **0**；真实E2检验案例 **0**。1008、84、30、5/7 都只来自作者原文，不是这个程序的真人实验重算。

## A04：拒绝静默修复数据来源资格

从官方OSF来源到原始代码/数据本体的资格门并未闭合：缺真实原始文件每件内容sha、文件字段/ID的身份含义、每轮记录完整性、真正参与者因子、末轮SFI是否为0人的计分、真实组级Wilcoxon算法和缺失分组处理。直接用作者刊出的Table 2数字建立一份伪造「程序真人结果」属于科研证据造假；本研究没有这样做。

两次HTTP503没有被解释成422空数据、文件内容不存在或样本为0。即使以后OSF恢复，也须重新冻结后续E2代码中每个字段的操作定义并真实从原始原作者字节计算。未将数据替换为模拟实验或从二手图表逆推个人记录。失败证据留存，没有将失败状态改写成成功。

## A05：真实制度迁移不能被误读为外生因果

SI/SFI每一轮由本人内生选择，之前收益/贡献信息可能影响下一轮身份迁移。单轮机构均值的SI>SFI即便正确，也混合了自选择、组内成员组成差异、历史信息与可执行奖惩机制，不是已识别的“随机分配到有惩罚机构所造成的纯制度干预效应”。

原2023论文的7实验室5个通过是作者层级的实验复验，并非R084现场新招募实验的E3。Oxford/Warsaw部分关口未通过必须保留。不能自动把R083个体条件性惩罚偏好、R071仿真处罚净收益与本原作者制度迁移作跨样本参数共享或者拟合同一观测单位。**本轮A05只代表没有把这些概念混淆，不代表当期真实制度模型被验证**。

## A06：统一验收与下一阶段处理

本研究**限定范围**是在首次真正原始来源E2复算前执行一个可重放、公开失败条件的元数据来源门。形式验收：A01问题及限定范围PASS；A02论文与OSF目录入口通过发表来源和公开元数据索引校验、**实际官方API源目录/文件SHA字节OPEN**；A03合成26项和两次失败访问源审计PASS，**真实真人E2计算 OPEN**；A04负结果登记PASS；A05推断边界PASS；A06提交正式报告、协议、源码、合成测试、二次CI及独立一致永久归档PASS。行政档案状态 `CLOSED_BOUNDED`（**仅元数据来源失败有界审计**），科研资格 `REAL_HUMAN_E2=BLOCKED_BY_OFFICIAL_OSF_SOURCE_503`，`E3=NOT_ESTABLISHED`。

若未来恢复访问，不应无限复刷HTTP503。先核对原作者2023分析代码和1008人×30轮包含的lab/group/actor/round键、实际SI/SFI制度选择、参与者最终贡献与净收益定义，再单独冻结后续源资格与真实复验评分规则。优先探索其他**独立研究机构/模型家族的可取得的原作者数据**，切勿依赖OSF源为整个心理史学研究主线阻断。PESEN v0.1继续冻结。

R084_SCOPE=CLOSED_BOUNDED_SOURCE_GATE
R084_REAL_HUMAN_E2=OPEN_OFFICIAL_OSF_SOURCE_503
R084_7_LAB_FIVE_REPLICATIONS=PUBLISHED_AUTHOR_CLAIM_NOT_OWN_RERUN
R084_INSTITUTIONAL_CAUSALITY=NOT_IDENTIFIED
PESEN_v0.1=FROZEN
