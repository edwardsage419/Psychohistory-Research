# E105 R275 S71来源范围、冻结与跨轨科研治理

日期：2026-10-30 Asia/Singapore。目标键：(operations,R275-S71,S71,source-scope-freeze-native-CI-PR-evidence-governance)。状态：COMPLETE_BOUNDED_READONLY_NONBLIND。只读审计其他轨，不修改R/B/A/理论产物。

## 1. 实际核查的版本与范围

本轮初始main HEAD baccf88d8a3406776f3d42752f6c46d6c3deda6d，读取最新提交与市场交接、R275 S71协议、R报告、B两份审计、A数据来源报告及R交接，另读项目工作流v2、239交叉索引v7.8（blob 36f24235901172642c46853298aebb421f1a3552）及P2五项待核队列（blob 7448418425262fd70d062fd97aa6ec578dfa311b）。README开头为历史R200状态，不能代表实时R进度。

S71冻结协议 Git blob 7effe22da29e27a06e804fbac8f6e695b67875ea，提交8c2964149055b7fa824bd9b10446ffd1e0613768。正式结果提交1dc5efb14eeb2f4c140cd03205070c3c5a2a46ff。GitHub compare返回ahead=1、behind=0、status=ahead，且只新增7份A/B/R文件。证明仓库提交祖先顺序；不证明研究者在冻结前没有预览过其他信息。S71明确已读原R275无噪声结果，属于内部NONBLIND。原R275已接受人工E1结题状态不变。

R轨报告：4噪声水平×3生成机制×256有序观测类型=3072人工来源行；平均MAP准确率依次为23/24、4541/6144、79/128、1/3。B轨已经用K计数独立方法及持久化远端收据严格检查，原R远端CSV/JSON经V8重新生成完全一致，6项故意篡改全部被拒绝。E105阅读上述报告和收据范围，**没有再次执行3072行完整复算**，不得把B的测试归为本轮新执行。归档B Python脚本的真实远端字节与先前执行开发稿不同；该归档Python对远端持久化数据的原生命令行关口仍NOT_RUN。原R Node CLI亦NOT_RUN。原R275/S71人工E1、E2预测新增0、E3新增0、外部独立团队0。

A轨新资料 Andreozzi/Ploner/Saral 2020：固定作者仓库979abf87、subjects.csv blob bd4c1550、1340记录、134人、六场次、十轮、每轮67对互惠配对均通过来源审计。其为真实行为来源的E2 provenance inspection，**没有新的真人样本外预测验证**；与R073冻结的100轮二元囚徒困境任务不匹配，不能作为R073第二独立实验已复现。未修改R073/PESEN冻结。

## 2. GitHub状态、Codex和归档边界

实际读取R275 S71正式提交1dc5efb的check-runs，total_count=0；combined status=pending且statuses=0。该提交无可核验成功CI，不能推广为全仓库CI状态。用户费用红线下没有触发Actions。未穷尽核验所有历史提交和冻结协议。

实际读取12个开放codex/* PR及PR #1/#3摘要。PR #1确认旧R257 S53比较器存在六项假阳性类别，PR #3提供待审查严格验证器，均为OPEN且merged=false。R257 S53既有盲态失败保持；R267 S63评分前冻结FAIL_TIMING保持。PR #2同步协议仍未合并，依用户补充指令执行。其余PR #4至#12也未合并，均不算main科研验收或修复。

按(track,来源ID,协议版本,问题)对照上轮E104的R274 S70第三路线数学复核，本轮转向R275 S71的提交时序、原生CLI与来源级别界限。R/B对S71数学已做，E105只读登记新A数据证据分层与未关闭的归档运行关口。未发现本轮检查范围内的协议Git blob被修改；无法据此断言全仓库零漂移。理论轨最新TH140提交baccf88属于理论研究，未见其触发模型熔炼。

## 3. 处理与后续

问题登记：S71原生Node与归档Python远端字节CLI待验收；A轨原始z-Tree到清洗CSV转换未复演；R257 S53旧B比较器和R267 S63冻结时序历史失败继续保留；全部开放Codex PR等待审阅合并；本轮提交CI无成功证据。无覆盖或索引改写。费用未新增，GitHub账单及免费额度NOT_VERIFIED。

下一项E106：若R/B补齐S71原生CLI，改核新增R276冻结与收据及历史PR修复边界；优先检查真实数据分层与研究任务重复。
