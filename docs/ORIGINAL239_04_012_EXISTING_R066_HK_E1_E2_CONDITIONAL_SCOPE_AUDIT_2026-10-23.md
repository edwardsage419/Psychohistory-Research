# 原始239候选04-012 HK模型：复用R066已验收的人工机制与条件性真实预测，不重复计算

日期2026-10-23 Asia/Taipei；性质：**已归档研究的来源/科学范围重归属审计**，不是新R模型、无新E1/E2样本。审计前冻结[科学范围协议](../protocols/ORIGINAL239_04_012_R066_HK_EXISTING_E1_E2_INTERNAL_SOURCE_REATTRIBUTION_FREEZE_2026-10-23.md)，commit [086175f2](https://github.com/edwardsage419/Psychohistory-Research/commit/086175f230fe05f2ec0979a8252b8150b7971a09)。

原始模型Hegselmann、Krause(2002), *Opinion Dynamics and Bounded Confidence: Models, Analysis and Simulation*, JASSS 5(3) art.2 [原著](https://www.jasss.org/5/3/2.html)。同一群体不同主体在上一轮意见距离不超过阈值epsilon时，同步取邻域平均；这个HK动态与Deffuant二人随机异步更新的源论文不是同一机制。R311只研究统一阈值置信**关系图**，不更新意见；两者不可相互伪装为新增HK结果。

## R066已有真实证据链的精确限定

[R066 原E1三机制结果](../research/R066/R066_E1_THREE_MODEL_RESULTS.json)与[完整初态模型源码](../research/R066/r066_three_opinion_models.py)已经在冻结初态[0,0.2,1]、epsilon0.25上计算**HK同步一轮[0.1,0.1,1]**，与DeGroot/FJ对照，旧[CI38845611874](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38845611874)25项synthetic测试成功。对应原文件Git blob SHA1分别为`45b9c737346a0b9e6b718f3bc1da43b3969f3e4c`和`34edc79e3bf1d7f886328089d37a196d4ab56317`。这是旧研究**E1，不新增本次实验**。

[R066 完整原结题状态](../research/R066/R066_FINAL_ACCEPTANCE_STATUS.json) = CLOSED_BOUNDED，证据E2_INTERNAL_CROSS_VILLAGE_CONDITIONAL_PREDICTION。真实Harvard Dataverse https://doi.org/10.7910/DVN/RAHSVM V1.0（Larson–Lewis 2026 16乌干达村庄），源家庭/问卷**2,125行**，基线和末次都完整**1,872行**。原作者R代码对比的4类家庭网络边**14,767条**，归并**8,659条**。有已观测干预即时态度的905条，输入并非严格干预前预测；缺基线或即时意见的网络节点按训练冻结规则局部均值填补。

[已封存的真实村庄留一预测](../research/R066/R066_E2_THREE_MODEL_LOVO_RESULTS.json)在每折用其他15村选择模型网格参数和公共漂移、评估剩下一村末次态度。GitHub [run38866210819](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38866210819) completed/success；主评价16村等权归一化意见MSE：Persistence+漂移**0.04227103404620483**，DeGroot **0.028614616600241692**，FJ **0.0266149141842743**，HK **0.0265478188648263**；按1,872配对家庭加权的MSE和MAE中FJ略低于HK。HK训练村16折均选`epsilon=0.5,steps=1`。**极关键的识别边界**：HK实现的是村内所有节点可通过意见阈值判断邻接，**没有使用真实家庭关系网络**；DeGroot/FJ使用真实家庭边，因此并非同一网络条件下公平比较；HK比FJ的村级MSE仅低0.0000670953，且没有已核查配对村级差异的不确定性区间，不能据此宣称HK理论、人际因果影响或网络拓扑优越性被证明。无新独立队列、历史E3不成立，完整作者R/igraph评估仍开放。

真正E2限定结论仅为：在这一份有来源核验的同一实验内、有干预即时意见参与输入、16村留一配置固定的**回顾性条件预测评分**存在；不是HK依照真实社会边传播的因果模型识别，更不是能外推到历史社会变迁的模型。

## 原始目录重归属

将原候选**04-012 Hegselmann Krause Model**单独指回原有研究**R066**，科学级别精确写为**旧E1 HK定量机制+旧E2内部条件评分、HK真实网络机制未识别**。保留原R066旧来源路径，R066正式结题及真实模型结果不变，本次不重新拟合/评估、不新增E1/E2、不读取家庭级隐私资料。原04-010 FJ已归属同一R066、但与HK算法原样分离。原04-011 R311的置信图关系和原04-013 Deffuant异步机制也严格保持独立。更新v2.8只更改04-012一行，主来源201→202，待核35→34（P1由8→7，P2维持27）。完整原239目录/科学验收未完成。R073/PESEN v0.1冻结。
