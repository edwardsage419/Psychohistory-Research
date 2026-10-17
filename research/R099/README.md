# R099：2024 PLOS 原作者96名真人、24个四人组、20轮完整组留出E2预测（正式有界结题）

**2026-10-17 · R099=CLOSED_BOUNDED · A01–A06全部限定PASS · PESEN v0.1 FROZEN。**

新原作者实验团队：Liu、Tsai、Chen、Cheng (2024), [*The signaling role of feedback in the repeated public goods game: Experimental evidence from the laboratory*](https://doi.org/10.1371/journal.pone.0299196), *PLOS ONE* 19(2):e0299196，[官方原始S1 Data CSV](https://doi.org/10.1371/journal.pone.0299196.s002)。原作者论文在独立8场实验室session招募96真人、每场12人、4场SF简化反馈/4场DF详细反馈、阶段二为固定四人组20轮，每轮代币20、贡献范围0–20。**论文报告8场次，但原CSV`subject,id,Period,group,DF,Contribution,OtherContri,Type`没有`session`列，所以本次实际来源只支持24个源四人组完整留出LOOG，而不是8场次LOSO。**

出版方完整第一手原CSV**43,467字节**，SHA256 **`75dc8ae8b63a6b3ea728df9acab9d27944b82ec4feb5c6055e26751ca9cc4a6e`**；无官方可独立核验MD5。PLOS网页发行了特定`plos-corpus-prod`签名对象，另冻[唯一PLOS签发原文件重定向协议](../../protocols/R099_PHASE_A2_OFFICIAL_PLOS_CORPUS_GOOGLE_STORAGE_SIGNED_CSV_REDIRECT_FREEZE_2026-10-17.md)，不保存签名令牌。先[Phase A源认证冻结](../../protocols/R099_LIU_TSAI_CHEN_CHENG_2024_PLOS_ORIGINAL_8SESSIONS_96HUMANS_20ROUND_4P_FEEDBACK_CSV_SOURCE_GATE_2026-10-17.md)，再[Phase B仅身份信息冻结](../../protocols/R099_PHASE_B_PLOS_1920_ROW_96_PERSON_24_ORIGINAL_GROUP_NONBEHAVIOR_ROSTER_FREEZE_2026-10-17.md)，[真实CI39027055517](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39027055517) 53synthetic+原作者全部96人、1920人轮、24真固定四人组×20轮真实来源一致性成功，严格不读取当时`Contribution`实际数值或`OtherContri`。

在行为得分前另冻[Phase C三模型源完整组留出合同](../../protocols/R099_PHASE_C_FIRST_PARTY_PLOS_24_TRUE_FIXED_4PERSON_GROUPS_20ROUND_LOOG_M0_M1_M2_PRESCORE_FREEZE_2026-10-17.md)：每组g从训练中整体留出全部4人20轮，目标t2..20 `Y(g,t)=sum_4 contribution_i,t/80`；M0=同反馈类其它**11个来源四人组**在同期t的均值；M1=留出g自身前轮组贡献占比；M2=固定0.5M0+0.5M1；每个真源组19目标、合计**456个真实组轮组均MSE**。不使用当期`OtherContri`或第一阶段`Type`，不假设能拆开自己的历史和其他三个伙伴的历史。

| 固定模型 | 实际456组轮均方误差（低越优） | 较M0增益 |
|---|---:|---:|
| M0其它源组同反馈类别同期基线 | 0.0243801993 | — |
| **M1本源组上一轮历史** | **0.0069520970** | **+0.0174281022** |
| M2固定半混合 | 0.0094260079 | +0.0149541913 |

**组间异质：M1在真实24组中22组正、2组负、0平；M2在24组中全部正。** 两个条件原始值匿名记A、B，每条件源12组、228个下一轮组目标，M1改善分别**+0.01853805**和**+0.01631815**，各11正1负；两组真实反例绝不删除。真实源`DF`两类别已确证，但本项目未核验原始类别码到论文SF/DF的精确含义，因此不随意写A就是SF。

[第一次整源原作者真人E2运行CI39027265753](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39027265753) **90synthetic全部PASS及456次真原组轮预测成功**；[第二次独立官方PLOS源CSV全文件重新下载、整源SHA再次核对、90synthetic及456源组轮逐字节精确复算并永久Git归档CI39027344527](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39027344527) **SUCCESS**；输出匿名JSON**7,098字节** SHA256 `91338505fac057c0dbc24f63430f7453f77cf824a1ccb40a737c047fc0449306`，Git blob `ef851d7a8bf46da2d8d85472135667ca8d2b15a0`。

正式成果：[原作者真人全部456组轮原匿名结果](R099_LIU_2024_PLOS_ORIGINAL_96_HUMAN_24_FOURPERSON_GROUP_456_LOOG_M012_E2_RESULTS.json) · [正式科学报告与两反例/独立性边界](R099_LIU_2024_ORIGINAL_PLOS_96_HUMAN_24_FOURPERSON_GROUP_456_TRUE_LOOG_E2_SCIENTIFIC_REPORT_2026-10-17.md) · [A01–A06有界机读验收](R099_FINAL_ACCEPTANCE_STATUS.json) · [原始来源身份/代码](r099_liu_2024_plos_official_original_S1_CSV_publisher_metadata_only.py) · [原作者真实group非行为身份审计](r099_phase_b_plos_2024_fixed4p_nonbehavior_group_roster_only.py) · [实际456个真groupLOOG模型源码](r099_plos_2024_24genuine_4person_groups_456_true_rounds_M012_LOOG_E2.py)，90项合成测试与工作流均完整入库。

**方法限界**：这是真人公开实验的**回顾性E2完整四人组留出**，不是8个实验室session的LOSO、不是日历未来预测、不是独立招募新被试的E3。论文有8个不重叠实验室session但数据中不能恢复它们；24组不等于24个独立实验；群体前轮均值混合所有参与者历史、不能证明单独同伴行为的额外预测增益，也不识别信号/互惠心理因果。本组四人连续贡献MSE不和R095/R096二人C/D的Brier数值相减。R095原8个session阴性、R096100轮FP和SP条件异质、R097 E0 / R098 E1数据可用性失败全部保留。

**R100 下一步：优先具有真实session与个体、对手过去行为可分别观测的另一研究团队真人数据，按真正独立session冻结模型与评分再检验R073关于两种历史各自新增预测信息的跨实验一致性；勿继续调整R099模型复杂度。**
