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


## 2026-10-18 正式跨模型负对照E2结题（优先于前文A3待验状态）

**[R105正式科学报告：真实同伴历史相对同权收缩阴性](R105_2024_412_REAL_HUMANS_103_GROUPS_3708_PEER_VS_SHRINK_E2_NEGATIVE_SCIENTIFIC_REPORT_2026-10-18.md) · [A01–A06机读最终验收](R105_FINAL_ACCEPTANCE_STATUS.json)**。原2024年真实Zenodo长CSV作者MD5/项目整文件SHA已正式通过[A3真正E1机器收据](R105_PHASE_A3_LIVE_CI_ORIGINAL_CPR_CSV_MD5_HEADER_ONE_UNNAMED_RECEIPT.json)。随后先冻[B仅原人／组／条件／轮验证](../../protocols/R105_PHASE_B_2024_CPR_ORIGINAL_PERSON_GROUP_TREATMENT_TEN_ROUND_ROSTER_ONLY_FREEZE_2026-10-18.md)，真实[身份审计](R105_PHASE_B_LIVE_CI_ORIGINAL_2024_CPR_PERSON_GROUP_ROUND_ROSTER_RECEIPT.json)认定412真原人、103个四人固定原组、10轮、4120真人轮、三匿名处理各100／156／156人、25／39／39组，**无原实验室独立session字段**。然后在读任何人提取数额前正式[预冻C同权收缩＋轮换外组对照](../../protocols/R105_PHASE_C_2024_CPR_TRUE_PEER_VS_EQUAL_SHRINKAGE_AND_ROTATED_DONOR_LOOG_PRESCORE_FREEZE_2026-10-18.md)，35项纯合成测试先通过后两次独立原作者完整官方CSV重新下载，真实3708个完全相同下一轮个人提取目标都逐一实算并逐字节复现。

| 模型（目标为原人提取/30） | 全部3708真原行为MSE |
|---|---:|
| M0 其它同处理组目标同期均值（回顾性） | 0.04822372 |
| M1 本人上一轮 | 0.06111471 |
| **M2 本人及其它组前轮均值各半（等收缩安慰剂）** | **0.04330681** |
| M3 本人及原组另外三位真伙伴上轮各半 | 0.04770729 |
| M4 本人及确定性轮换其它组前轮均值各半 | 0.04668966 |

关键原冻结比较：**M3相较M1仍为正`+0.01340741`（103组85正18负）；但M3相较同权的M2是`-0.00440048`（103组20正83负）**。三处理全部负（−0.003673、−0.004660、−0.004607）；前轮默认期、跨期第6轮、后段均负。相对轮换外组M4总体−0.00101763，方向53正50负。**首批明确同权负对照说明混入同伴前史改善私人单轮预测可由预测收缩解释，不能当作伙伴信息独有增益已证明**。也不意味着所有类型合作学习都不存在，比较严格限该组历史等权固定模型和单实验制度。

[真正原作者3708真人目标五模型匿名结果](R105_PHASE_C_ACTUAL_FIRSTPARTY_3708_PEER_VS_SHRINK_E2_OR_SOURCE_FAILURE.json) · [独立两次完整源重取逐字节SHA复演](R105_PHASE_C_DOUBLE_INDEPENDENT_ORIGINAL_E2_REPLAY_RECEIPT.json)：得分JSON **9,705 bytes**，SHA256 **`d35f4afb71033a4594e2326594754f9ac43ee1ae4c29492720581a81e6bba2e5`**，没有真实人物身份或单条原行为被公开。**R105=CLOSED_BOUNDED_E2_TRUE_PEER_NOT_ABOVE_EQUAL_SHRINKAGE、R073精准单对手复现=NO、E3日历前瞻=NO、PESEN v0.1 FROZEN。** 全部真人阴性均已归档、不可调参改为阳性。下阶段继续挑选与现有原实验来源DOI真正不同、优先真实独立实验session与完整合法伙伴行为的研究模型。
