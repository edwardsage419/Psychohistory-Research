# R093：Pereda 2019大型真人公共品实验（100人至1000人）个体历史预测E2（正式结题）

**2026-10-17：R093=CLOSED_BOUNDED；源真实原作者已发表2019人类实验，完全留出原来源参与者的记录行为下一轮预测E2；A01–A06全部严格限界PASS。不得误认为R089–R091完整群体留出复验、纯自主手动贡献因果E3。PESEN v0.1=FROZEN。**

[Pereda et al. (2019), *Large scale and information effects on cooperation in public good games*](https://doi.org/10.1038/s41598-019-50964-w)，六次2017年真实14天在线公共品原始实验，原作者[Zenodo固定v1 2590686](https://zenodo.org/records/2590686)完整CSV `2017A2ECOCOOPANSA01ONL0000ESPMAD.csv` **612196字节**，发布方MD5 `626c61c2c18a114a5b92a7d2b7e46558`，全原件SHA256 `4eb3380a5eacdef5466709b343af391b27b48a35b5b82f355a4d85d5172644bc`，两次重新读源及MAC/源SHA独立完整复算确认。

**真实原作者来源范围**：CSV 21195行，其中83行无法归到合法实验+参与者+轮次（4关键字段全缺失，已独立审计、未伪造ID），有效 **1508个实验内来源人编号×14期=21112个源人物轮**；其中`player_alive=1`实际17736次，前后两轮同时在场且原始贡献是整数0..10的合格预测目标共**16365次**。没有目标的人137；1371人至少1次合格目标。作者论文完成者1159**不是**该数据所有原始ID的分母。六次来源大型组实验：PGG100 100个来源原人、PGG1000 1004人，PGG_H/PGG_H2/PGG_HM/PGG_HM2各101人；各实验只有一个大型公共品互动群组，**不能使用六人/四人多个组的leave-one-group-out协议**。团队亦与R090有Antonioni、Sánchez作者重叠，仍属不同实验与真正不同真人来源。

全部实读贡献之前先后冻结[Phase A原始MD5及结构](../../protocols/R093_PEREDA_2019_LARGE_GROUP_14DAY_FIRST_PARTY_CSV_SOURCE_GATE_FREEZE_2026-10-17.md)、[Phase B真实83个缺失身份/源处理码元数据审计](../../protocols/R093_PHASE_B_PUBLISHED_2019_SOURCE_MISSING_PARTICIPANTS_TREATMENT_LABELS_PRE_BEHAVIOR_2026-10-17.md)、[Phase C全部16,365人轮预测模型/缺失淘汰及限界](../../protocols/R093_PHASE_C_PEREDA_2019_1508_HUMAN_14ROUND_INDIVIDUAL_HOLDOUT_M012_BEHAVIOR_FREEZE_2026-10-17.md)。所有科学负例按时间留存：[初始真实来源缺失人ID拒绝CI39017561811](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017561811)、[工作流纯调度job ID语法失败CI39017697592](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017697592)、[独立官方原件安全元数据及43 synthetic通过CI39017733091](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017733091)、[原始模型首次synthetic 3人退出致仅余1个基线训练主体反例CI39018023442](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39018023442)。后面只修合成环境四人/组保留至少2他人，**不修改冻结的科学真实评分合同**。

固定个体完整留出：M0=同实验其他仍在场的人当轮平均贡献/10（全14期不使用留出个人参与均值训练）；M1=待预测个人前一轮原记录贡献/10；M2=固定0.5M0+0.5M1。平方误差越小越好：
 
| 来源实验 | 真实原人轮预测目标数 | M1相对M0配对改善 | M2相对M0改善 |
|---|---:|---:|---:|
| PGG100 | 1159 | +0.03734512 | +0.04254134 |
| PGG1000 | 10767 | +0.03270560 | +0.04091604 |
| PGG_H | 1231 | +0.03275314 | +0.05009477 |
| PGG_H2 | 1023 | +0.03615769 | +0.05213379 |
| PGG_HM | 1124 | +0.03085465 | +0.03863128 |
| PGG_HM2 | 1061 | +0.04029105 | +0.05301605 |
| 全部 | **16365** | **+0.03361821** | **+0.04305038** |

全部池化M0均方误差 **0.10670834**、M1 **0.07309013**、M2 **0.06365796**；按六个源实验各赋相同权重，M1也改善 **+0.03501787**，M2改善 **+0.04622221**。六条件全正，但个体异质**788人M1较好，583人更差，137人无合格相邻轮**，不能宣布每个人都存在强烈自我行为惯性。

**最大科学限制**：论文明确在真人忘记当轮时系统代填行为80%复制上轮、20%上/下1，源仅`player_alive`在场标记，无法区分具体记录中哪些为系统代填。故**过去选择M1明显较强，可能部分源于机器机械复制上轮**；不得将模型准确率当作纯人类学习/心理记忆因果，或宣称全16365均为真人主动逐次选择。M0能看其他人同轮记录，也不是日历实时预测；原始独立公共品组最多6个而非16365个独立实验。不能与R089/R090/R091的**完整群体**留出预测结果合并为一个效应。

[首次真实162? 实际**16365**条有效目标+82项纯合成CI39018076790](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39018076790)、[第二次独立原CSV完整MD5/SHA、82项合成与整个匿名结果字节完整一致、永久Git归档CI39018148784](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39018148784)均SUCCESS。[9625字节六组匿名原始来源E2汇总](R093_PEREDA_2019_1508_PARTICIPANTS_16365_PERSON_HISTORY_HELDOUT_E2_RESULTS.json)，SHA256 `b432375714d2393187a6baf52057d4b2c2cda22435da966b67f61e07c3581105`，Git blob `86ed893856927af4d4bb6151145f30e4f86ad0b2`；[正式科研限界报告](R093_PEREDA_2019_LARGE_GROUP_1508_REAL_PEOPLE_INDIVIDUAL_HISTORY_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[机读A01–A06验收](R093_FINAL_ACCEPTANCE_STATUS.json)及[实际首方来源个体预测程序](r093_original_pereda_1508participant_14round_ownhistory_individual_holdout_E2.py)与其82项纯合成测试都归档。

**R093=CLOSED_BOUNDED；实证证据是连续登记参与者“记录行为”个体自历史预测信息阳性，未识别纯心理记忆、不能完成群体模型跨实验复验；PESEN v0.1持续FROZEN。** 后续R094最重要的是独立找到有来源标识的人工/自动行为选择及与R089定义更一致的原始二元投资数据，而不是在当前自动复制混杂的原资料上进一步优化模型。
