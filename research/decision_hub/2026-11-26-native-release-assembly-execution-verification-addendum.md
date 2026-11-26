# 原生发布装配审计执行核验补记
2026-11-26。REPRODUCED_IN_CONTAINER / NATIVE_SOURCE_FRAGMENTS / SYNTHETIC_FIXTURE / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
原报告 research/decision_hub/2026-11-26-native-release-assembly-and-missing-dependency-fragment-audit.md，blob 0813c6fceba9094a54174fd9ece5977d2ebdcf25，commit 856ae2abaed5baa2391cd3e73c14d806b43c7c45。本轮核对当前main、25近期提交、15开放PR、#63固定head 734686980b19da9291bdd08b67d4e2519c011acf、v3.2及同步规程。旧报告所载数值与执行记录在本轮开始时未能从工具记录核实，不能仅凭报告自述计为已执行。为消除该证据缺口，本轮实际在Linux容器用Python 3.13.5 (GCC 14.2.0) 转录固定三个自有源片段（旧报告中的行范围和FNV），执行旧报告给出的测试主体两次。三片段FNV e13247bb、ff7b9046、1e4a1521 实测均匹配；两次实际输出完全一致：
```json
{"graphs":64,"releaseSelections":4096,"executionChecks":32768,"ineligibleMissing":22537,"ineligibleCandidates":16384,"called":26615,"controls":6}
```
数值与原报告一致，自本补记实际运行起可认定上述有限片段实验已复算，不倒填早期执行时间或计为新增独立样本。使用原报告已声明的Method、Context、entry、run_method等合成夹具，执行真实Registry/DecisionRegistry及hub循环片段；不是完整原生、独立验收或科学有效性。原报告文件读取包装未执行，本轮使用本地转录片段并核对FNV；非完整字节密码学验证。旧报告保持不变。未修改生产、PR、训练、部署、主动CI、冻结、证据等级或费用。唯一交接尝试路径404，未确认最新交接。