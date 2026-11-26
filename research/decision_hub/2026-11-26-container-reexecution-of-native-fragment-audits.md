# 固定原生片段审计的本轮容器再执行记录
2026-11-26。CONTAINER_REEXECUTED / NATIVE_FRAGMENT_ONLY / SYNTHETIC_FIXTURE / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
起点main d8bcfb878399e86ddd74d70126f5ec58769bc165；核对25近期提交、15开放PR、#63 head 734686980b19da9291bdd08b67d4e2519c011acf、v3.2及同步规程。交接关键词检索无结果，尚未确认最新交接路径。本轮检查历史报告实际执行记录时，未能从历史工具记录独立核实此前的Python运行陈述，因此以本轮真实执行建立可核查依据，不倒填历史执行时间或增加独立样本计数。
固定历史报告：
- 原生发布装配审计 0813c6fceba9094a54174fd9ece5977d2ebdcf25，核验补记 17ebc62ac77e694788fba0376a8ccf226c57f07c。
- 原生目标引述作用域审计 8fb6c4a7b4ad9d8251ea3137a998730a2e21f5e4。
本轮实际使用Linux容器Python 3.13.5 (GCC 14.2.0)，依据前轮已读取的固定自有源码转录以下片段，FNV1a去尾空白检查：
plugins.py blob 1777a1c4d5d32fac69df94f132fcc5a457fc231b 行81..93 e13247bb；
decision_registry.py blob b833a6d45d944f2f1b885ab1a409df28c390c233 行67..145 ff7b9046；
decision_hub.py blob a97de30f5241063862dbc0ce797c214cbc4d405f 行229..245 1e4a1521；
decision_knowledge_planning.py blob d32854c4909df858ee851634747234ed5dec657b 行8..末尾，4112字符，c2ae52aa。
四片段实际校验匹配。FNV仅为转录比对，不是原始文件密码学证明。执行两份历史报告的测试主体，各实际运行两次，使用本地转录片段读取而非原报告的完整文件参数包装；每项两次标准输出经cmp完全相同。实际结果：
```json
{"assembly":{"graphs":64,"releaseSelections":4096,"executionChecks":32768,"ineligibleMissing":22537,"ineligibleCandidates":16384,"called":26615,"controls":6},"goalDiscovery":{"checks":130,"nativeFalseDirectCandidates":70,"maskedFalseDirectCandidates":30,"nativeDirect":40,"maskedDirect":40,"unavailableControl":1}}
```
结果与两份旧报告对应计数一致。复算仍为相同合成结构、相同源码与夹具，真实Method/Context/Index、完整数学计算、全原生App、独立未见样本、真实用户及设备均未运行。前轮已给出完整可复算脚本及固定源码范围，本次不重复复制。历史报告不修改，实验状态自本轮真实容器运行起有直接证据，不能据此追认旧轮次运行或正式科学验收。未修改生产、PR、冻结、训练、部署、主动CI或费用。