# R105：2024年新的重复公共资源困境实验来源认证

日期：2026-10-18。作者 Eladio Montero-Porras等（与本项目R096存在作者重合但属于不同实验、不同原数据），[Zenodo正式原数据 DOI 10.5281/zenodo.10818840](https://zenodo.org/records/10818840)。新的原始`data_long_format.csv`据公开描述为Prolific真人四人共用资源困境10轮长表，三种默认选项处理；论文设计数字控制组100、利他默认156、利己默认156，尚待本项目直接验证原人/组/轮身份。

在真正原文件和任何行为被读取前，[Phase A严格原Zenodo官方MD5与表头冻结](../../protocols/R105_PHASE_A_MONTERO_PORRAS_2024_DEFAULTS_CPR_ZENODO_ORIGINAL_LONG_CSV_MD5_HEADER_FREEZE_2026-10-18.md)，所用原出版方公开MD5 `a3afbb4e52179a0e1d8b1b533f076cc9`。首次实际来源真实被安全拒绝`R105_ORIGINAL_SOURCE_UNSAFE_OR_DUPLICATED_HEADER`；[保留首个真正源拒绝收据](R105_PHASE_A_LIVE_CI_FIRSTPARTY_2024_CPR_LONG_CSV_MD5_HEADER_RECEIPT.json)，不可删改。独立另冻[Phase A2真实原CSV表头字符类别诊断](../../protocols/R105_PHASE_A2_FIRSTPARTY_CPR_LONG_CSV_HEADER_CHAR_CLASSES_ONLY_FREEZE_2026-10-18.md)，[真正匿名源MD5诊断收据](R105_PHASE_A2_LIVE_CI_ORIGINAL_CSV_HEADER_CHARACTER_CLASSES_RECEIPT.json)已由GitHub Actions提交并再次读取验证：

* 官方已发表完整MD5：**匹配**，作者原CSV字节**1,131,426**；
* 本项目完整原文件SHA256 `a7d959361075ae88dc2fc4945b8a7ecd3c8fe3a234ff25dc53b28b9c2c5cdeae`；
* 原表头**37列**，其中**1列空白表头名称**、36列ASCII字母/下划线开头，其它36列无未允许的标点、0重复原列名，惟一源标点ASCII underscore；
* 该阶段**任何原始人提取行为、原人号、原组号均未应用解读**；当前原真人模型评分0。

因此，随后已在读取原CSV其它内容之前另冻[Phase A3唯一空白列名兼容](../../protocols/R105_PHASE_A3_ONLY_ONE_EMPTY_ORIGINAL_HEADER_FIELD_COMPATIBILITY_FREEZE_2026-10-18.md)，只允许1列无名称，另外36列保持原字符严格验收，报表以`__UNNAMED_ORIGINAL_SOURCE_COLUMN__`占位，绝不修改原文件字节或当作真实原作者列名。13项源synthetic及新真正原出版方审核工作流已提交，真实A3通过与否应**仅以[独立真实A3收据](R105_PHASE_A3_LIVE_CI_ORIGINAL_CPR_CSV_MD5_HEADER_ONE_UNNAMED_RECEIPT.json)为准**。截至此README定稿，如尚未形成实际收据，不可宣称A3严格源及源表头完整E1已验收。

R105源和以往R099/R104并非同一DOI。跨编号防重现已新增[全库来源DOI及资产登记](../SOURCE_PROVENANCE_DOI_DEDUP_REGISTRY_2026-10-18.json)，明确R099/R104完全同一原数据不能两次计数；相同多文件Zenodo记录还要区分具体实验、不能因为共用记录直接判为不同或相同参与者。

**当前科学证据：R105新的真实原文件MD5与SHA256已在A2直接取得；逐行原人/组/轮映射及同伴历史预测尚未做，真人E2=0，R073/PESEN v0.1 FROZEN。** 下阶段B仅在A3真正通过后先冻结非行为的source actor、group、round、treatment字段审计，不读取`player_contribution`或任何原提取值；随后新C必须另先冻**同等权重收缩安慰剂与伙伴身份负对照**，禁止同R102再度无法分离统计收缩与真实同伴历史信息。
