# R108 正式限定研究结题：2017原作者真MD5数据为6×300条件序列，不能作为个体真人对手历史E2复验

日期：2026-10-18。**`R108=CLOSED_E1_ORIGINAL_PUBLISHED_CONDITION_SERIES_NOT_ACTOR_DYAD_E2_ELIGIBLE`**。原英国莱斯特大学真人实验存在、官方文件真实完整、原CSV来源结构可以重复，但本次开放附件**不含经核验的逐个人—真实对手—实验场次身份键**。R108本身**没有计算任何真人次轮行为模型评分，E2=0，PESEN v0.1 / R073仍冻结**。

## 1. 作者研究与原始文件区分

Colman、Pulford、Krockow (2018), *Persistent cooperation and gender differences in repeated Prisoner's Dilemma games: Some things never change*, *Acta Psychologica* 187:1–8，[DOI 10.1016/j.actpsy.2018.04.014](https://doi.org/10.1016/j.actpsy.2018.04.014)。正式论文讨论两种收益结构版本与三种配对性别组合，在固定伙伴条件下连续**300轮**。大学[Figshare原作者数据](https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938)于2017年登记，页面另有实验说明PDF。**论文所陈述的真人实验设计成立，不等于这个公开CSV一定保存人级逐回合行动。** 不在项目仓库复制All Rights Reserved的原始文件或任何个体行。

真作者附件`Repeated Prisoner's Dilemma_raw data-data.csv`，官方file ID **18370526**，确切长度**36,526字节**、出版社发表全文**MD5 `7afc755c293dc261d696d1b3f9ba796a`**。原始文件从官方`ndownloader.figshare.com`经单个真正官方302委托到经A2零文件正文预审的`s3-eu-west-1.amazonaws.com`，两份独立获取逐字节一致，项目真正原CSV完整SHA256 **`e7dbb6ddc96cc5c65368be0d1918c3ebc7a83c14addd03ab44eeb07790575c18`**。官方MD5实算匹配、双源全SHA一致；[A4真原来源完整认证收据](R108_PHASE_A4_LIVE_CI_TRUE_PUBLISHER_MD5_DOUBLE_CSV_HEADER_CHARACTER_CLASS_SOURCE_E1.json)，真实GitHub Actions [run 39130128287](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39130128287)两个job成功。先前严格A1不许跨域来源的拒绝、A2只看委托主机、A3因非典型CSV表头和收据允许字段过窄的失败，都保留独立证据，未改历史文件证明内容。

## 2. 先冻B0仅原CSV形状：1804条每条五列

真正原CSV第一表头包含**5个字段、4个空列名、3个重复列名**。先冻[B0结构协议](../../protocols/R108_PHASE_B0_ORIGINAL_LEICESTER_CSV_ROW_WIDTH_NO_CELL_VALUE_PRESCORE_FREEZE_2026-10-18.md)，10项synthetic通过，[真实B0机器收据](R108_PHASE_B0_LIVE_CI_2017_UK_ORIGINAL_CSV_ANONYMOUS_ROW_WIDTH_STRUCTURE_ONLY.json)证实**1804条原逻辑数据行全部宽度5、无其它宽度，无隐含多列/重复不同宽度区块**，没有访问任何一列原个人值。

## 3. 先冻B1才检查匿名类型：不导出任何个人取值

为理解首行无效变量名，**在人类行为模型访问前**冻结[B1仅来源五列单元格语法类别协议](../../protocols/R108_PHASE_B1_ORIGINAL_2017_FIVE_COLUMN_CELL_SYNTAX_ANONYMOUS_CENSUS_PREMODEL_FREEZE_2026-10-18.md)。首次真实源任务尚未启动时，一个纯synthetic因测试fixture bytes/str格式差异安全失败，记录[首次B1 run 39130985079](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39130985079)；仅修复fixture并增补测试，没有改冻结分类或原MD5。第二次18项synthetic全部通过，GitHub Actions [B1 run 39131036887](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39131036887)成功，第一手[匿名B1真实分类收据](R108_PHASE_B1_LIVE_CI_ORIGINAL_2017_FIVE_COLUMN_ANONYMOUS_CELL_TOKEN_TYPE_CENSUS.json)。该程序**有限地读取原单元格以分类语法**，所以不再声称“没有接触任何源单元格”；没有输出原个人、行动、性别、收益、配对字段取值，也没有任何模型评分。

真正原1804行前**4行为非统一数值的注释/空行结构**；后面来源值全是数值类型。原始五列前三槽主要正整数；第四槽有**1762个0与1之间小数**、38个数字1；第五槽有**1727个小数**、64个0、6个1及少量其它整数/文本。来源具体变量名不由这些类别反向臆造。

## 4. 先冻B2真来源确认六个连续300轮条件序列

随后独立冻结[B2只检查六个连续300轮区块的数值结构和来源资格](../../protocols/R108_PHASE_B2_REAL_2017_ORIGINAL_1800_SIX_BY_300_BLOCK_CONDITION_CENSUS_PRESCORE_FREEZE_2026-10-18.md)，12项synthetic成功，真正原源[run 39131372988](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39131372988)通过。[B2官方MD5约束的匿名数据结构机器收据](R108_PHASE_B2_LIVE_CI_TRUE_2017_ORIGINAL_SIX_300_BLOCK_CONDITION_SOURCE_ELIGIBILITY.json)证明：

| 原始真实结构，不含来源个人值 | 已证结果 |
|---|---:|
| CSV非数值前言/结构行 | 4 |
| 随后可解析的数值数据行 | **1800** |
| 以第一槽位的数值判断逐段完全从1到300 | **6段全部是** |
| 每段数值行数 | **300** |
| 第二槽位匿名不同数值编码总数 | **2** |
| 第三槽位匿名不同数值编码总数 | **3** |
| 六段内部第二/三槽位编码稳定 | **全部是** |
| 六个第二×第三编码组合是否各自不同 | **全部不同，2×3组合齐全** |
| 第四槽数值0到1开区间 | **1762 / 1800** |
| 第五槽数值0到1开区间 | **1621 / 1800** |
| 第五槽大于1 | **109 / 1800** |
| 真个体与对手唯一身份、实验室场次字段获认证 | **均未建立** |
| 本项目实际真人次轮模型评分 | **0** |

该结构与论文“2种收益博弈 ×3种性别组合 ×300轮”的设计描述**高度一致**。但尚无足以独立确认源码本的字段名称，因此第二、三槽位只能称为**两个和三个未知含义的来源条件编码**，不能肯定哪槽是收益制度/性别，更不能当成原真人ID或六次独立采集。末两槽大多是连续小数，不可直接解释为某位真人逐轮0/1行动。若误将6个条件块分别设成6位真人或6个实验室session，属于不可接受的伪复验。

## 5. 统一科学验收：本来源E1真、真人机制E2零、无伪阴性

- **A01 PASS_E1**：作者、真实英国长重复博弈、2017出版社数据源、发表完整MD5与原文件SHA逐字确认。
- **A02 PASS_E1_SOURCE_LAYOUT**：真实1804五字段CSV行、4行前言及6×300连续块、二元×三元条件编码匿名审计可重复。
- **A03 BLOCKED_PERSON_OPPONENT_KEYS**：本作者公开CSV未独立建立逐个人、同一真实对手及可完整留出实验session键，因此不能通过R073/R106个体历史预测合同。
- **A04 PASS_TRANSPARENT_NEGATIVE**：从最早strict来源跳转、A3 header阻断、B1合成fixture错误至B2真实独立实验任务成功，所有来源合格/不合格关口独立保留。
- **A05 NOT_RUN_E2**：没有任何有效个体原真实行动预测评分，不声称模型效果正负，不对实验合作率或性别差异产生新实证结论，不以B2列的小数冒充个体二元选择。
- **A06 PASS_ARCHIVE**：正式原出处、冻结协议、程序、synthetics、机器证据、科学报告和验收索引提交GitHub主分支并核验。

结论 **`R108=CLOSED_E1_ORIGINAL_PUBLISHED_CONDITION_SERIES_NOT_ACTOR_DYAD_E2_ELIGIBLE`**、**`REAL_ACTOR_LEVEL_FORECASTS=0`**、**`NO_CAUSAL_CLAIM`**、**`R073/PESEN_v0.1=FROZEN`**。下一研究R109优先作者公开的真人**逐人×逐对手×场次×回合**文件；若是真人可改配博弈，原作者的“退出/惩罚/缺席轮次”要分别编码和审计，先冻同权普通收缩及匹配行动分布的安慰剂，再接触真人目标。不得再继续在这份六条汇总式时间序列上优化预测模型冒充微观心理机制。
