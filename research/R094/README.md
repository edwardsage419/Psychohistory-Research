# R094：2015年Nishi二元网络公共品真人实验（Zhu2026次级发表来源），个人历史预测随财富可见性反转

日期2026-10-17。**R094=CLOSED_BOUNDED，真正的2015年原始真人互动实验，但实际使用经过2026年Zhu第二研究者整理、发表于Zenodo的次级CSV；回顾性E2真实数据计分完成、A01–A06有界PASS。** 未获取原始80个实验场次的身份，故不是严格session级复验。PESEN v0.1 FROZEN。

**原实验**：Nishi, Shirado, Rand & Christakis, [*Inequality and visibility of wealth in experimental social networks*](https://doi.org/10.1038/nature15392), *Nature* (2015)，1,462名真人、原论文80场次×10轮网络博弈，原行动二元合作或背叛，伙伴边可重连；**2026次级整理者** Zeyu Zhu, [*Decision time is associated with future cooperation and social rewiring decisions in network public goods games*](https://doi.org/10.1371/journal.pone.0347919), *PLOS ONE*。[Zenodo固定v1 19544006](https://zenodo.org/records/19544006) 复现包`individual_data.csv`，720,707字节，出版社MD5 **`85db2536b5be1cd50266900e61590d5a`**，完整来源SHA256 **`b37fa71434dd46249a0e7f43f9b9e798b1d3cafcffea3c80bc6997b99b6dd0a5`**，两次独立实跑完整认证。

前读贡献严格分阶段[Phase A来源认证](../../protocols/R094_ZHU_2026_NISHI_2015_BINARY_NETWORK_PGG_SECONDARY_CURATED_ZENODO_CSV_SOURCE_PRE_OUTCOME_FREEZE_2026-10-17.md)、[Phase B源ID/轮次/可见性元数据](../../protocols/R094_PHASE_B_ZHU_2026_NISHI_BINARY_NETWORK_NODE_ROUND_VISIBILITY_METADATA_FREEZE_2026-10-17.md)：发现14,620个源人物轮=1,462人×10轮、真实可见0/1的726/736真人，每个人标识与visibility在十期都稳定，没有真实原场次`session_id`；不得根据2015论文80场次声称完整留出实验场次已经执行。 [真实源场次资格CI39019371936](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019371936)通过。

在读真实二元合作值之前冻结[Phase C全人留出、三模型完全固定](../../protocols/R094_PHASE_C_NISHI_ZHU_BINARY_NETWORK_1462_PARTICIPANT_LOO_M012_PRESCORE_FREEZE_2026-10-17.md)：个体上一轮和当前有合法`decision=0/1`方评分；由原14,620行检验出原论文报告一致的**13,560次有记录的二元选择**、源1,060条无选择，形成**12,110次合格下一轮二元Brier目标**。M0=相同财富可见性、同目标轮的**其它**来源人选择均值（跨未知原实验场次），M1=本人的上一轮二元选择，M2=固定各半，全部无需拟合参数；绝不用已派生`decision_lead`未来信息。M0利用其它来源人在目标时刻的记录，因此是横向全人留出，**不是日历真正向前预测**，不等同R089六人全组留出。

| 正式原始二元Brier（低优） | 有效原人下一轮目标 | M0其它同visibility同轮 | M1自己上一轮 | M2各半 | M1改善M0 |
|---|---:|---:|---:|---:|---:|
| 财富不可见0 |5,910|0.201629795|**0.153299492**|**0.127710972**|**+0.048330303**|
| 财富可见1 |6,200|**0.241771654**|0.265483871|**0.192801301**|**−0.023712217**|
| **全部** |**12,110**|0.222181366|0.210734930|**0.161035500**|+0.011446436|

**R094最有价值的负证据**：在`visibility=1`下，上一轮自己行动的M1**不如**对照M0；`visibility=0`下M1明显优于M0。固定M2在两层都优于M0。原1,462个不同参与者里，M1按本人有效连续轮数均值表现**856人较好、558人较差、48人无合格相邻轮**；不将来源明显的两层反向平均抹掉。

测试和原作者真实来源成绩严格独立：首次小synthetic因缺失一个peer导致别人训练样本不够而[CI39019608534](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019608534)失败；只修synthetic训练组大小后80测试PASS，但真实文件程序审计有`KeyError`，按安全程序先[冻结C2异常类](../../protocols/R094_PHASE_C2_FIRST_TRUE_BINARY_MODEL_SOURCE_EXCEPTION_CLASS_ONLY_2026-10-17.md)、再[冻结C3源码行定位](../../protocols/R094_PHASE_C3_SAFE_KEYERROR_CODE_LOCATION_BEFORE_REACCESS_2026-10-17.md)，成功定位Phase B来源码本统计键拼写不一致，**只更正来源字段的固定键，没有改模型和选择准入**。原拒绝[CI39019647183](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019647183)到[CI39019903763](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019903763)均完整保留。

[首次真正实时原作者整理后的二元合作成绩CI39019950466](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019950466)、[第二次全部80synthetic+官方同一原始Zenodo720707字节MD5/SHA重新下载及3685字节结果完全一致永久归档CI39020029476](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39020029476)均成功，源结果完整SHA256 **`2b68edc1efc87cf63df4eb915c09e19ac5fc5696bcbdd54874601393718045f0`**、Git blob `eea544b6b61d1f0658284456c760862b646a9edd`。[全部可核验匿名实证结果](R094_ZHU_NISHI_2015_BINARY_NETWORK_1462_ACTORS_12110_INDIVIDUAL_HOLDOUT_E2_RESULTS.json)、[正式科学报告](R094_NISHI_2015_BINARY_NETWORK_ZHU_2026_SECONDARY_1462_PERSON_HISTORY_E2_SCIENTIFIC_REPORT_2026-10-17.md)、[A01–A06科学验收](R094_FINAL_ACCEPTANCE_STATUS.json)、[真实数值全复算原生Python](r094_zhu_nishi_2015_1462_binary_network_participant_holdout_E2.py)、[38纯binary synthetic](test_r094_zhu_nishi_2015_1462_binary_network_participant_holdout_E2.py)、前两阶段42项source/隐私synthetic、自动工作流全部入GitHub。

**局限严格保留**：来源是2026次级整理的2015真人原实验资料，不是原版Breadboard完整日志；丢失80session身份及四种禀赋初态，不能做跨session外部LOSO或聚类因果/标准误；`decision_time`列存在不证明逐次全为人类手动决定。对比R089“六人二元global投资”、R090六人连续贡献含自动行为阴性、R091四人贡献阳性、R093大型群体个体贡献自动填补疑问，不得建立万能惯性参数或长历史动力结论。

**R094=CLOSED_BOUNDED，真实个人二元选择历史预测信息随可见性条件反转，M2固定混合两层为正；正式E3及留出真实80场次未成立；PESEN v0.1冻结。** R095优先寻找完整保留session-ID的其他独立多人二元实验，不再以个人标识编造实验场次。
