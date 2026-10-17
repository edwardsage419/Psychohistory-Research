# R100 B0正式报告：已认证原始Excel的10工作表A/B身份列真实XML标签结构检查

2026-10-17。**B0=PASS_BOUNDED_SOURCE_STRUCTURE_ONLY**。E1第一手原始整文件认证仍有效，真实人物ID/原伙伴互证未执行，行为得分零。PESEN v0.1 FROZEN。

在之前[Phase B0源结构只读冻结](../../protocols/R100_PHASE_B0_AUTHENTICATED_XLSX_SHEET_COLUMN_A_B_STRUCTURE_ONLY_PRESCORE_FREEZE_2026-10-17.md)及[源A2重定向安全冻结](../../protocols/R100_PHASE_A2_OFFICIAL_ZENODO_XLSX_REDIRECT_PREFLIGHT_AND_AUDIT_RECEIPT_FREEZE_2026-10-17.md)之后，GitHub Actions 先运行20项A2+15项B0纯合成测试，再重新取得原Zenodo完整`ThresholdPGG_ExperimentalData.xlsx`官方MD5与固定内部SHA256，使用标准XML流解析计数A/B列单元格标签而**没有访问任何XML数值文本属性**。自动写回[真实匿名B0永久收据](R100_PHASE_B0_LIVE_CI_SOURCE_AB_TAG_RECEIPT.json)至[Git提交3a71b97ffa731b9f54c7ac571ce5b34d87305872](https://github.com/edwardsage419/Psychohistory-Research/commit/3a71b97ffa731b9f54c7ac571ce5b34d87305872)。本项目重新读取了这份收据。过程不打印原个人/伙伴编号、数据sheet原始名称或C:Z贡献/问卷。

| 匿名sheet区间 | 每个工作表实际XML行标签 | 每个工作表A列标签 | 每个工作表B列标签 |
|---|---:|---:|---:|
| 1、2 | 221 | 221 | 221 |
| 3、4 | 237 | 237 | 237 |
| 5、6 | 225 | 225 | 225 |
| 7、8 | 209 | 209 | 209 |
| 9、10 | 221 | 221 | 221 |

十张表共有**2,226个实际XML行节点**，每张从结构上出现1行表头后的**候选数据行**共2,216，恰好与出版说明五处理总人数554×每人四行相匹配。**上述2,216是结构层面的推断，不代表从A源ID确认了554名不同真人。** 每行原标识是否真的非空、每个人究竟四行、两个stage是否完成换伴、每组的人是否重复、C:V的实际20轮贡献是否有效，都留给下一级源字段审计，不能由XML cell标签数量证明。

源文件整字节217,396，官方MD5 `c40171abb172da8e16b0839db98a2cf2`，真实SHA256 `825b1cd3226aeca7a19d76d9594f655114b12059648f9ca03b3291c3cf9ab200` 再次与冻结值相等。B0的Python结构检查从底层XML逐节点扫描，而XML解析器不可避免临时持有文本；代码没有读取或公布任何单元格的实际字符串、数字和20轮动作，故**零应用层值访问**这一表述精确，不能夸张为原始压缩字节从未进入进程内存。

**验收边界**：B0身份列结构 PASS；B1实际身份证据 = PENDING；B2唯一配对去重 = PENDING；C行为模型评分 E2 = NOT_ESTABLISHED；原Session1与Session2绝非独立招募实验室场次；R073完整个人+对手历史模型的独立严格复现 = NOT_ESTABLISHED。下一步必须遵照Phase B匿名人簇和配对互证冻结，仅以A/B实值（绝不以行为值）建立原伙伴的互指记录，失败即安全阻断，不按表格四行倍增独立样本。
