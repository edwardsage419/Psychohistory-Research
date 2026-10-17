# R083：协调惩罚偏好的原作者真人配对比较（E2）

2026-10-17 新模型家族：社会规范实施机制中的**条件性惩罚协调偏好**。本轮与R071的纯数学处罚制度模型以及R080至R082的动态网络机器人实验分别存档；不把一个跨个体规范、独立平台操纵或社会变迁因果机制冒充已证实。

## 原作者独立来源

Molleman et al. (2019), *People prefer coordinated punishment in cooperative interactions*, *Nature Human Behaviour*, DOI https://doi.org/10.1038/s41562-019-0707-2。作者数据、Stata代码与说明由作者在 [LucasMolleman/NHB_CoordinatedPunishment](https://github.com/LucasMolleman/NHB_CoordinatedPunishment) 公开。锁定原始上传提交 `42cba97300910988b7b7386379fa32492d35d8aa`，真实Stata数据的Git blob `7989855cadae3dc70b83dd29bab572a1bc0d30fb`，作者分析代码Git blob `981ca799943b97e9b6216053135e86db806eb0b5`。只核验这些原始内容，不在当前仓库存任何真人逐行选择、身份、原始二进制记录或可识别的个人轨迹。

## 评分前冻结与研究设计

[正式评分前协议](../../protocols/R083_COORDINATED_PUNISHMENT_ORIGINAL_HUMAN_PAIRED_MAIN_REPLICATION_FREEZE_2026-10-17.md) 提交 `2f9e6ddfb56bc1a83cd3c6484ca7efe307ae6ac0` 发生于任何R083真人原始数据评分之前。需精确通过原始作者Stata文件和.do源码 Git blob、原作者 `rerun` 主实验/复验队列、原作者 `punisher==1` 选择、参与者身份唯一键和两个0/1条件性策略选择的完整来源资格。唯一主评价为同一人的 `conditional_other_pun` 与 `conditional_other_nopun` 配对差，分别在主/复验队列报告四格表及两方向反例。原始 `unconditional_punishment` 做三个固定描述分层，不能依据结果更换样本或阈值。

[严格来源程序](r083_author_sha_coordinated_punishment_replication.py)、[35项纯合成检查](test_r083_author_sha_coordinated_punishment_replication.py) 与[首次真实作者GitHub Actions](../../.github/workflows/r083-author-original-coordinated-punishment-E2.yml)作为主研究产物。真实数据必须另行独立完整重取、重算、与第一次匿名结果文件逐字节一致且Git永久归档，方可认为E2数值已被独立核证。

这是作者已发表2019年结论的**回顾性独立数据复算**，并不构成原实验前预注册或新E3。即便两队列方向一致，也只是在原始策略问题中观察到条件性偏好，不能识别真实惩罚制度对人的因果影响、规范因果扩散、合作净收益或历史制度演化。PESEN v0.1保持冻结。


## 2026-10-17 原始真人数据 E2 真实复算与有界结题

正式状态 **R083=CLOSED_BOUNDED**，六项验收 A01至A06 均 PASS。主实验及作者标记的复验实验同在2019年原始Stata数据中，**4,320名原始记录行对应 `punisher==1` 资格队列共2,880条有效配对**，所有来源字节与作者固定Git blob严格一致。[首次原始真人实跑39001261509](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001261509)与[第二次独立原始Stata重新下载、35项纯合成与匿名结果逐字节归档39001352142](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39001352142)均 success。

原作者主实验 1,336 条配对，其他人不惩罚时自身选择惩罚11.0778%，其他人惩罚时15.4940%，配对差**+0.044162**（n01=134, n10=75，双侧精确 p=0.0000542）；复验队列1,544条配对，分别12.1114%和14.8964%，差**+0.027850**（n01=115, n10=72，p=0.002049）。新来源检验方向两队列正，符合此前已冻方向门。但是原本无条件愿意惩罚者中主实验差**−0.019737**（p=0.795），复验差**+0.030172**（p=0.520），**反向和不显著结果都保留**，不能声称所有心理类型均稳定协调惩罚。

[完整来源、两队列四格和分层负面证据科学报告](R083_REAL_AUTHOR_COORDINATED_PUNISHMENT_MAIN_REPLICATION_SCIENTIFIC_REPORT_2026-10-17.md) · [作者SHA全字节匿名结果](R083_ORIGINAL_HUMAN_COORDINATED_PUNISHMENT_MAIN_REPLICATION_E2_RESULTS.json) · [六项正式机读验收](R083_FINAL_ACCEPTANCE_STATUS.json)。匿名结果 **6,019字节**，SHA256 `a75638fbb3619667a077e1fa640bc1b3ca97dce062b2538c779eeac053e216ae`，Git blob `9065d45f7ab4a78097d73c15094aa41c33424a67`，第二次独立原始数据重算逐字节核验后永久Git归档。原始个人行为行和Stata原始文件没有写入本项目仓库。

这是**已发表论文的回顾性 E2 原始计算**，只测试同一真人在两种假想第三方惩罚状态下的条件选择，不独立识别他人真实惩罚行动、实际机构处罚、群体惩罚网络、制度演化与长期历史效果。原作者 `rerun` 是主/复验队列标记，程序未另行独立确认两组真实招募名单完全不重合；因此不将其声称为新E3。PESEN v0.1 保持冻结。
