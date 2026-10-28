# A轨：Toledo、Ávila、Green 2025 真人对确定性程序TFT的40次重复囚徒困境来源门槛

日期：2026-10-28。结论：`PUBLIC_ARTICLE_VERIFIED / NEW_DISTINCT_HUMAN_STUDY_CANDIDATE / RAW_BEHAVIOR_REQUEST_ONLY / R073_DIRECT_INELIGIBLE`。本条独立登记，不作为新增正式E2预测或R073外部验证。

## 本轮实际核验的英文一手来源
原研究 Toledo, Ávila & Green (2025), *Undiscounted costs and socially discounted benefits modulate cooperation in one-shot and iterated prisoner's dilemma games*, *Journal of the Experimental Analysis of Behavior* 124(2), e70046，DOI 10.1002/jeab.70046，2025-09-07在线发表。正式全文 https://onlinelibrary.wiley.com/doi/full/10.1002/jeab.70046 ，PMC开放全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC12415503/ 。

全文Method、Session 3与Data Availability已实际核对。初始Session 1有129人，Session 2完成126人，Session 3完成111人。111人来自前面会话的同一队列，跨会话不能当成独立研究样本。Session 3随机分为五种收益矩阵条件，人数分别25、20、24、20、22，总和111；每人完成一场40试次的实验。由此按论文完整完成的描述可推导111×40=4440个预期真人决策槽，**尚未取得原始数据，不将4440声称为实际逐行验证记录数**。

每轮人类选择X或Y，屏幕显示双方选择及收益。对手是预先编程的确定性tit-for-tat：首轮Y合作，从第二轮起严格复制参与者上一轮行动。五组收益矩阵分别为1-2-4-5、1-2-8-9、1-2-12-13、1-3-5-7、1-4-5-8。轮次单位是同一人对固定程序的1至40次决策，独立单位至少需要按人聚类。不存在可识别的第二名真人对手；程序生成的对手历史是参与者自身历史的确定性函数，不能当作独立真人社会学习信号。

论文Data Availability Statement明确数据需向通讯作者合理请求取得。本轮未联系作者、未注册账户、未访问私人参与者数据、未购买服务。公开全文中未提供可核验的逐轮原始CSV下载、字段码本或文件级再分发授权，故 `RAW_BYTES=NOT_ACQUIRED`、`FIELD_SCHEMA=UNKNOWN`、`SUBJECT_ID=NOT_ROW_VERIFIED`、`SESSION_ID=NOT_ROW_VERIFIED`、`TRIAL_CONTINUITY=NOT_ROW_VERIFIED`、`MISSINGNESS=UNKNOWN`、`LICENSE=UNVERIFIED`。伦理审批及匿名性描述不能代替数据授权。

## 复现准备与适配
研究问题有价值：可在未来独立协议下考察人类对确定性TFT反馈的适应、收益矩阵影响、40次学习动态及三会话样本流失。若未来公开数据可合法取得，先核验五条件的完整人号、每人40试次、原始动作语义、程序TFT逐轮一致性、试次缺失及样本选择，再预先冻结按人分组的基线、时间切分与校准方案。

R073冻结目标是100轮双人真人重复囚徒困境及其固定评分协议。本实验40轮且对手为确定性程序，`R073_DIRECT_TRANSFER=NO`，不能拼接不同参与者、扩展到100轮、把程序对手当真人，亦不能据论文聚合合作率给R073模型打分。与R073/R074/R075/R077原研究作者及实验设计不同，论文层面初步属于不同研究；未完成所有既有A轨来源ID的完整跨库去重，故 `FIFTH_INDEPENDENT_ELIGIBLE_STUDY=NOT_ESTABLISHED`。

新增E2=0，新增E3=0，新增费用0。来源仅英文期刊及PMC原文。下一优先寻找可直接公开获取逐人×真人对手×场次×轮次×双方行动的合法数据。
