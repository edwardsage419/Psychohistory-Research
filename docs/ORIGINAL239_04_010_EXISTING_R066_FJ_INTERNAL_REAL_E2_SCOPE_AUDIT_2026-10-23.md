# 心理史学：原候选04-010 Friedkin–Johnsen既有R066真人村庄留出证据逐项归属审计

日期2026-10-23 Asia/Taipei。性质：在已经完成的R066既有档案里核查可用证据并重新归属；**不是新的R311研究、没有重复执行或新增E1/E2、并非跨实验外部复验**。[事先冻结本次归属协议](../protocols/ORIGINAL239_04_010_EXISTING_R066_FRIEDKIN_JOHNSEN_E2_SOURCE_REATTRIBUTION_FREEZE_2026-10-23.md)提交[05764e0c](https://github.com/edwardsage419/Psychohistory-Research/commit/05764e0c19edc0fcf2daf6e805f540ccbfcee266)。

## 原作者模型对应的已经存在的科研证据

Friedkin & Johnsen(1990) *Social influence and opinions*, DOI https://doi.org/10.1080/0022250X.1990.9990069。原候选04-010 FJ意见固守／易感性机制，在[R066原正式结题状态](../research/R066/R066_FINAL_ACCEPTANCE_STATUS.json)已有直接研究：25个E1源模型测试和R/Python精确的作者真实家庭网络两核心边程序核验，后者全16个村庄四类家庭关系的14,767条类型边无差异。原先v2.5仅把04-010记为PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY，漏列已经符合对应研究主题的R066作为主来源。

更重要的[R066真实村庄数据留出报告](../research/R066/R066_E2_THREE_MODEL_LOVO_AUDIT.md)：Larson–Lewis 2026 DOI 10.1017/nws.2026.10038；来源哈佛Dataverse DOI 10.7910/DVN/RAHSVM V1.0 CC0，已经得到作者实录2,125行、16村、1,872条基线与末次完整家庭态度测量。作者核心R家庭网络关系结果与Python逐边一致，真实[CI38865507356](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38865507356)成功；[整村留出协议提交85b8abb3](https://github.com/edwardsage419/Psychohistory-Research/commit/85b8abb398f2e4cc060b6e4b36dc6880893455a1)早于该阶段真实结果产生，[CI38866210819](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38866210819)真实两个job成功。留出16折，每折只用其余15村选网格参数与公共漂移，测试村末次值在选参/预测时不用。但预测起点部分使用干预后即时态度，其余使用基线，不应宣传成干预前跨社会预测。

已归档[原真实16村模型评分JSON](../research/R066/R066_E2_THREE_MODEL_LOVO_RESULTS.json)主要指标为各村等权规范化态度MSE：
- Persistence+训练村漂移 **0.04227103404620483**；
- DeGroot+训练村漂移 **0.028614616600241692**；
- **FJ+训练村漂移 0.0266149141842743**；
- HK+训练村漂移 **0.0265478188648263**。

FJ次要家庭行加权MSE **0.02822275983149589**、MAE **0.12901516753537692**；折内仅在训练村选择的FJ参数全部是α=0.75，其中k=2三折、k=4十三折。HK宏观MSE仅比FJ低0.000067095319448左右，但HK是**每个村全村任意状态足够接近者可交互**，并不使用FJ所用的真实家庭网络。两者不同信息集和参数族结构，使任何简单的“HK模型机制已经在人类中优于FJ”的结论都不成立；对16折差值的配对置信区间未完成，原文全部igraph统计也未完全重跑。

R066 E2结论只支持**该一组现场研究的回顾性16村内部条件性预测**，不是因果辨识社会影响；两轮调查、实验干预、村级一般漂移与结构选择可能造成评分改善。本项目**没有**把研究外独立人群留出作为E3完成、没有跨尺度历史事件预测，没有新受访对象行添加。

## 归属边界

只把04-010 FJ主R来源改为**已有R066**，保留该候选原先旧有限范围R066来源字段。R066原本E1/E2档案、负结果和全部冻结协议均保持字节未改；04-012 HK和04-011 Bounded Confidence尚未重新审核，不能因为同一R066比较过HK就偷渡新主R链接。R309 SIR、R310 voter、R307 minority、R308 efficacy、R072 REV008声誉真人处理编码未识别及R073/PESEN v0.1冻结状态全部保留。

原239目录v2.6更新以后只是候选到既有R研究的**来源完备性提升**：主R199→200，待核37→36（P1 10→9，P2维持27）。若机读逐项来源审计未完成，不能宣称归属正式验收，更不能把本次算作又完成了一项新的独立真人E2研究。
