# E106 R276 S72原生复验与Andreozzi 2020滞后列来源风险治理

日期：2026-10-30 Asia/Singapore。目标键：(operations,R276-S72+Andreozzi2020,S72+author979abf87,native-closure-and-published-lag-misalignment)。状态：COMPLETE_BOUNDED_READONLY_NONBLIND。只读核验R/B/A/理论和Codex元数据，不修改其他轨文件或索引。

## 1. 实际核验

本轮初始main HEAD bb561b92a891338c8d6ce54becd2642de2d33573；已读最近八个提交及其文件、开放的12个Codex PR摘要、E105、F008 phase21、R276 S72正式报告、B轨最新原生验收补充、R轨短交接、A轨Andreozzi来源审计、作者原始R清洗源码。README顶部仍是历史R200，不能用作实时HEAD进度。最近TH141只属理论轨，未见启动模型熔炼。MKT137研究与本审计分开归档。

R276 S72冻结提交8e3eb673efa5daeddf1c5defe03ae205a2aa9429，结果报告提交207bbb51a327f759d3e2bc0d523917899484679d。GitHub compare status=ahead、ahead_by=5、behind_by=0，新增5份来源/结果文件。证明Git提交祖先顺序，不证明未看过冻结前全部结果；S72明确已知先前m2=11/16，故为NONBLIND探索性E1。原R276结题不改变。

B轨新增B_R276_S72_NATIVE_R_PYTHON_BYTE_REPLAY_ADDENDUM_2026-10-30.md：归档原R Python blob e4742d63d3356a1ded01fad78dc3efbb119cf8f7，本地执行--output-dir、--check、--selftest，8项测试PASS；重新生成1533行CSV与JSON的Git blob分别为08dbd0c57ea2f18749d05fe953b2ed907de9cbdd、51eb669c9150b6c90ac81c3ab8cf5f91030f9d0b，与远端原件逐字节一致。本轮E轨读取B轨实际执行报告并核对冻结祖先关系，**没有重复运行原生Python**。此前E105登记的R275 S71原生关口仍需按自身版本独立核验，S72关闭不能代替S71。没有独立外部团队复现或真实预测提升。

## 2. 真实数据来源的新重大风险

A轨固定作者来源：seyhunsaral/stabilitycondcoop commit 979abf87b5d3cfb7aa8be13b81ef233076c3bb75，code/process_raw_data.R Git blob 522efd459f574ccaef3d9ce1dd2b086ffb70370e。E轨本轮再次直接读取该作者源码，确认第269行对opp_cond_class_wide_o生成lag1，第275行却以replace(opp_cond_class_wide_o,period==1,NA)覆盖lag1。后式对第2至第10期保留的是**当前期**数值。

A轨已读取原发布subjects.csv全部1340条，逐人按十期比较1206条可计算滞后：发布lag字段与当前期一致1206/1206，与真正上一期一致393/1206，差异813/1206。另一个opp_cond_type_lag1负控制1206/1206正确。E轨本轮确认源码语义及A报告数据口径，**未亲自重新解析1340条原CSV或执行原作者R/zTree全流程**。这是明确的数据测量与预处理风险，须阻止将该字段直接作为滞后对手行为特征输入任何未来预测复验。应从原始时序按subject、period重新构造并保留原列供差异审计；A轨拥有原研究路径，E轨只登记问题，不修改其结果。

Andreozzi是10轮不同任务的真人数据来源，不能称R073第二个100轮二元囚徒困境外部复现；目前只有E2数据来源/测量审计，没有新增E2样本外预测或E3。若后续使用该数据，先核查来源身份、清洗逻辑、许可及预先冻结的目标和评分。

## 3. Codex、CI、费用和协作

开放PR仍12个，包括#1 R257 S53旧B比较器假阳性反例、#3严格数学检查器、#10 R271 S67原生验收、#12 R266 S62原生验收；这些均为待审查PR，不能计作main合并修复。R257 S53原盲态失败和R267 S63评分前冻结时序失败继续保留。没有从本轮查询证明全部历史冻结blob未漂移、全部CI通过或全部PR被完整复验。没有触发Actions，账单/免费额度NOT_VERIFIED。没有发现本轮已读R/B/A/理论轨文件被本轨覆盖。

本轮E的实际增量：S72原生归档关口由旧NOT_RUN更新为B轨可追溯PASS；独立重读作者源码确认813条发布滞后字段错位风险。下一E107优先核验A轨原生全CSV负控制及R277新冻结/PR合并状态，避免重复S72的已完成审计。
