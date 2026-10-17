# R103 正式限定结题：2016真实双人博弈原始E1通过，但对手身份来源互证不满足预冻95%门槛

日期：2026-10-17。**R103=CLOSED_E1_DYADIC_SOURCE_ROSTER_NOT_ESTABLISHED，E1原出版方完整MD5/SHA认证通过，真人行为E2评分0，PESEN v0.1保持冻结。** 该结论是当前本项目预冻结来源身份合同的资格受限，不代表原作者数据错误、实验作弊或双人社会学习模型效果阴性。

## 第一手完整来源的真实已证事实

Poncela-Casasnovas等（2016），*Humans display a reduced set of consistent behavioral phenotypes in dyadic games*，Science Advances，论文DOI 10.1126/sciadv.1600451，正式[Zenodo原作者数据记录](https://zenodo.org/records/1127154)，DOI 10.5281/zenodo.1127154。作者资料说明45次实际实验副本、参与者来自不同副本、每次通常13至18回合；这些宣称**尚不能据本次资格阻断前的数据处理程序独立核实人数与配对结构**，不能冒充本项目已验收的45个来源独立留出场次。该作者团队与R102在Ángel Sánchez上有合作作者重叠，但数据采集与设计独立。

真实GitHub Actions下载原CSV `drbrain_decisions.csv`，原文件**319,528字节**，公开官方**MD5 `712e3a4ae905af3e004b4a31a38b250d`完全匹配**，项目完整SHA256 `c63b99ba7554908e54393eb9f8267a98de1a3d9bdd123a77f60f2b2122236013`，九列，物理数据行**8477**，与公开代码说明中的`User_ID`、`Experiment_number`、`Round_number`、`S`、`T`、`Game`、`Action`、`Opponent_ID`、`Opponent_Action`九项一致。[最初真实源E1收据](R103_PHASE_A_LIVE_CI_ORIGINAL_DYADIC_CSV_MD5_HEADER_RECEIPT.json)、[A正式科学记录](R103_PHASE_A_AUTHENTIC_2016_DYADIC_FIRSTPARTY_E1_SCIENTIFIC_REPORT_2026-10-17.md)。

## 人物伙伴互指验证的全部真实否定证据

1. 先于行为数据冻结[初次B真实人物与同轮对手正整数ID、双方互指及95%资格](../../protocols/R103_PHASE_B_2016_DYADIC_45_EXPERIMENT_SOURCE_PERSON_OPPONENT_ROUND_RECIPROCITY_PRESCORE_FREEZE_2026-10-17.md)。首次真正B执行被来源`Game`名称格式超出严格字符类阻断：`R103_B_ORIGINAL_GAME_CODE_UNSAFE`。保留[初次真正失败收据](R103_PHASE_B_LIVE_CI_ORIGINAL_DYADIC_RECIPROCAL_ROSTER_RECEIPT.json)。
2. 另预冻并运行[B1仅Game公开文本元数据字符类诊断](../../protocols/R103_PHASE_B1_ORIGINAL_GAME_LABEL_CHAR_CLASS_ONLY_PRESCORE_FAILURE_DIAGNOSTIC_FREEZE_2026-10-17.md)，真实源九种不同`Game`编码中额外仅含ASCII英文撇号（39）、连字符（45）、斜杠（47）。代码只输出标点Unicode十进制与匿名长度等价类，没有输出任何人行动或人号。[B1真实脱敏收据](R103_PHASE_B1_LIVE_CI_GAME_LABEL_CLASS_DIAGNOSTIC_RECEIPT.json)。
3. 独立预冻[B2只扩展Game公开文字字符许可](../../protocols/R103_PHASE_B2_EXACT_SOURCE_GAME_APOSTROPHE_SLASH_ONLY_COMPATIBILITY_FREEZE_2026-10-17.md)再执行真正原B，遭`R103_B_ORIGINAL_SELF_OPPONENT_NOT_DYAD`安全阻断。源存在**至少一条User_ID=Opponent_ID**，不能将其自动解释为两位独立真人；[B2真正失败收据](R103_PHASE_B2_LIVE_CI_ORIGINAL_DYADIC_RECIPROCAL_ROSTER_RECEIPT.json)保留。
4. 别立[B3先冻自指源行作为原来源非合格双人记录计数](../../protocols/R103_PHASE_B3_SELF_OPPONENT_SOURCE_ROW_AS_INELIGIBLE_PAIR_COUNT_PREBEHAVIOR_FREEZE_2026-10-17.md)，不再因自指本身退出，而仍要求其它原ID为正整数、双向同轮互指、全部8477源行中至少95%有合格互指、至少30独立source实验。实际执行又遭`R103_B_ORIGINAL_PERSON_EXPERIMENT_ROUND_NOT_POSITIVE_DECIMAL`，保留[真正B3失败收据](R103_PHASE_B3_LIVE_CI_ORIGINAL_DYADIC_RECIPROCITY_WITH_SELF_ROW_COUNTS.json)。
5. 按预先声明的止损规则，另冻[最后一次B4仅四个人物/实验/轮/对手ID语法匿名分类](../../protocols/R103_PHASE_B4_FINAL_ORIGINAL_ID_NUMERIC_SYNTAX_CLASS_DIAGNOSTIC_FREEZE_2026-10-17.md)。**真实第一手B4机器收据**[R103 B4](R103_PHASE_B4_LIVE_CI_NONBEHAVIOR_ID_SYNTAX_CLASS_RECEIPT.json)证实：`Experiment_number`、`User_ID`、`Round_number`三个字段每列8477行**全部为ASCII正整数**，但`Opponent_ID`仅**7876**为ASCII正整数，另有**601行**属于其它可打印ASCII文字，非零、非简单负整数、非十进制小数、非空、非`NA`/NAN/NULL文字。所有分类是**匿名总量**，未输出任何原编号或源单行文字。原`Action`和`Opponent_Action`行为值整个R103均保持0次应用读取。

真正异常`Opponent_ID`文本的语义在原作者公开代码说明中没有建立可核验的人号映射，不得仅凭类别猜测其为计算机、无法匹配或实验设计特殊角色。未来如有原作者正式字面码本可另案复核；本项目此次**不允许多次盲改特殊码本直至得分为正**。

## 明确证据上限与源合同的不可通过证明

**现已先验决定原始对手ID必须是来源ASCII正整数，且全部8477个来源人物轮中至少95%能建立真正同轮双向独立个人的互指。** 当前真实来源只有7876个正整数`Opponent_ID`，因此即使7876条都能形成合法互指，其占全集的比例上限为 **7876/8477≈92.91%**，仍**严格低于预冻95%**。还未计入其它可能不互指、残缺或自指的源行，真实可配对上限只会进一步减少。所以无需打开人类行为值即可证明当前来源资格条件无法达成。

科学解释仅限本项目固定编码/覆盖合同，**不能推断原作者原始45次实验没有真实两两博弈，也不能据此认为其他更宽松或作者自带的实验标识编码不可使用**。当前事实只是**本项目在不能证实601种文字编码真正含义下不能给出合法严格的双人社会历史全实验留出**。

## 统一验收与下一方向

* A01 第一手不同实验来源、完整官方MD5/来源SHA：**PASS_E1**。
* A02 固定9字段、8477源物理行及出版方论文来源：**PASS_E1_BOUNDED**。
* A03 原人/对手/场次真实互指及95%覆盖：**BLOCKED_SOURCE_IDENTITY**，已用实际601个非正整数源记录证实上限不足。
* A04 全部B/B1/B2/B3/B4正负收据、事前冻结协议和合成测试原位保留：**PASS**。
* A05 行为`Action`/`Opponent_Action`逐条内容应用读取**0**，原人模型得分0，无假阳性/假阴性因果宣称：**PASS**。
* A06 研究可复核代码、机器哈希、正式科学记录和总项目索引归档：**PASS**。

**`R103=CLOSED_E1_DYADIC_SOURCE_ROSTER_NOT_ESTABLISHED`；`STRICT_95PCT_SAME_ROUND_RECIPROCITY_POSSIBLE=NO`；`REAL_HUMAN_SCORE_COUNT=0`；`PESEN_v0.1=FROZEN`。** 下一阶段R104直接搜寻又一独立原作者发布的易完整认证、原人/伙伴/轮/场次明示且没有无法独立映射特殊人号的大规模真人实验。最优先是在**独立新来源第一次真人行为读取前冻结等收缩安慰剂和真实伙伴特异性负对照**；不要在R102既有阳性资料上不断调整模型拿来算证实。
