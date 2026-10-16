# R072 真人实验增量：PLOS S8 与 Table 1 八组真实「请求数×任何回应」联合统计完全一致

日期：2026-10-16。**证据范围：原始真人数据、但仅为事后探索性、不带实验身份标签的聚合计数复核；不是R072信誉评判模型的真人 E2 校准，不是对服务历史因果效应的独立复现。**

## 来源与修订前可知信息

本阶段使用已取得并来源固定的 [van Apeldoorn & Schram (2016), *Indirect Reciprocity; A Field Experiment*, PLOS ONE DOI 10.1371/journal.pone.0152076](https://doi.org/10.1371/journal.pone.0152076)，尤其是 [作者 Table 1](https://doi.org/10.1371/journal.pone.0152076.t001)。正式 S8 原作者原始文件 DOI `10.1371/journal.pone.0152076.s008`，38,647字节，**SHA256 `5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b`**，每次从 PLOS 指定原出版入口签名委托链加载。

此轮前 [REV-004 原始行域](R072_E2_PLOS_S8_ANONYMOUS_COLUMN_DOMAINS_REV004.json) 已知198个非表头物理行，第1列189个numeric＋9个text，第2列189个numeric＋9个空，第2列在候选189行只有0/1两码（0=100、1=89）；[REV-005](R072_E2_PLOS_S8_ANONYMOUS_PROFILE_BLOCK_PARITY_REV005.json) 已知第一列八个匿名组的请求数量严格等于作者Table3的八组多集 19×4、25、28、30×2。由于作者原文 Table1 同时公开总回应**89**，本轮**不可能**在未观测回应总数前独立预注册0/1意义。它只能算**根据已发现的材料提出的事后确认细化核验**，应拒绝任何“事前证伪性独立E2结果”的误称。

研究者在看到每组真实回应数前提交 [REV-007 单独冻结协议](../../protocols/R072_E2_S8_REV007_PUBLISHED_GROUP_RESPONSE_CHECKSUM_2026-10-16.md)，commit `69ed08a2edab7669c0d3981c2cd891ee9b0029e0`。只按前两个 OOXML 数值列提取此前固定的189个匿名候选行，第一列作为**未知意义组代码**，第二列暂按数值1代表**候选有回复**计算；对每个匿名组形成 `(group_size, coded_ones)`，仅输出**不带原始代码、不给任何真实身份的计数对多集**，再与作者在发表时已经公开的八个 `(requests, responses)` 对严格排序比较。**不得**尝试其它字段、取反、移除行、按 p值或显著性倒推组的服务历史身份；若有不匹配也必须保留。

## 真正成功的来源级复核

[GitHub Actions 初次真实运行 38928749514](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38928749514) SUCCESS，**16项**虚构模拟边界测试 PASS，且真实由PLOS原 S8 SHA固定 Excel 独立计算全部八组配对：

| 组规模（匿名，顺序已去标识） | 本源第二列数值1数量 | 作者Table1已发表任何回复数 |
|---:|---:|---:|
| 19 | 9 | 9 |
| 19 | 10 | 10 |
| 19 | 11 | 11 |
| 19 | 12 | 12 |
| 25 | 11 | 11 |
| 28 | 14 | 14 |
| 30 | 6 | 6 |
| 30 | 16 | 16 |
| **189** | **89** | **89** |

`STRONG_EIGHT_PAIRED_MULTISET_MATCH=TRUE`。这比只有 `189个请求 / 89个数值1` 的**弱总数匹配**更强，因为8个不同组的总体大小与`1`数量同时完全相同。作为主动负对照，若倒转二元码，聚合数为 **100** 而不是作者发表的**89**；人工虚构的测试即使保持189请求/89回复总数，仅改变两个组之间的回复配置，也会导致八个`(group_size, responses)`联合多集**明确失败**，说明程序没有只检查总数。

按作者 Table 1 明确定义，`respond` 是“收到任意回应”；`yes` 是直接愿意提供服务；`maybe` 为尚保留提供服务可能性。**本项目仅检验了与作者`respond`数量多集相同的一个二元列候选**，并没有把它当作独立证实的作者原字段定义；`yes`及`maybe`的原始编码、总数和任何组间差异尚未重算。没有做真人的个体模型拟合或参数优化。

[永久原始匿名工件归档 Actions 38928909389](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38928909389) 再次执行16测试并重算原S8，检查精确匿名结果 SHA256 `3cd8a9baa0b881942e8c394ae7d547f419a6ea2348dab1b5bb3aa5c543b1f09a`，原1,816字节JSON永久存入 [R072_E2_PLOS_S8_ANONYMOUS_TABLE1_PAIR_CHECKSUM_REV007.json](R072_E2_PLOS_S8_ANONYMOUS_TABLE1_PAIR_CHECKSUM_REV007.json)。程序 [r072_plos_s8_table1_group_checksum_rev007.py](r072_plos_s8_table1_group_checksum_rev007.py)、[16项测试](test_r072_plos_s8_table1_group_checksum_rev007.py)和执行流水线入Git；原真人XLSX、具体编码、个体资料均未写入任何Git commit。

## 对作者变量含义和实验科学主张的限制

即使八个 `(n,#ones)` 计数对逐一匹配论文，**不可以**据此确定8个匿名数值组代码中的哪些是 serving、哪些是 neutral。所有八个 `(n,response)` 配对在作者表里恰好不同，因此确实能**通过已经发表的回应结局和组规模**“猜出”每个来源组代码对应哪个原文性别×国家×服务历史类别；**但这会使用结果去定义处理组**，再以该映射检验“服务历史是否提高回应率”会发生根本性的数据泄漏和循环论证，故本研究禁止该做法。

尚缺**独立于回应结果的处理身份**：例如原作者发布的代码字典，把S8第一列原始数值直接绑定至八个档案，或源文件明确标注的原始实验派发记录。来源后段九行虽带`service/neutral/yes/maybe/no`说明关键词，当前 [REV-006 匿名字典扫描](R072_E2_PLOS_S8_ANONYMOUS_FOOTER_LEGEND_REV006.json) **未确认数字代码↔身份含义的一对一映射**。不能仅凭论文 Table 3的 `96 serving / 93 neutral` 将组依据总人数重新分配，因为多组人数19、30存在多个可交换的标签，且“恰好匹配”不证明真实实验中的服务历史身份。

真实性分级：
- **E2来源级** 原 PLOS数据真实可用、哈希固定、完整结构/小组数量真实计算，PASS；
- **E2公开描述性聚合** 八组规模×第二列数值1的计数多集，与文章作者公开 Table1 **完全一致**，这是有限且**探索性**的共同证据；
- **E2实验处理身份** S8数值代码↔serving/neutral和国家×性别 `NOT_RECOVERED`；
- **E2作者原始回应编码** 二元列1是“收到回应”目前只有高度相符的**候选证据**而非原始codebook明确确认；
- **E2因果推断/心理机制** 尚未使用作者身份与完整响应测量定义，`NOT_ESTABLISHED`，**不把本文作者发表的处理效应说成本项目已经复现**；
- **R072 IMAGE / SIMPLE_STANDING / STERN_JUDGING** 三种动态信誉判断规范并非此现场实验随机操纵的变量，更没有对应数据，`NOT_TESTED`。
- **E3独立研究总体** `OPEN`；PESEN v0.1 `FROZEN`。

此结果给未来项目的实证模型设立可重放**数据来源/汇总计数校验标准**。没有外部原作者代码本时，限定完成这一阶段并独立保留 E2 处理识别的上游阻塞，比靠结果倒猜“哪种身份解释有利于论文主张”更符合本项目研究可复现与可证伪的要求。
