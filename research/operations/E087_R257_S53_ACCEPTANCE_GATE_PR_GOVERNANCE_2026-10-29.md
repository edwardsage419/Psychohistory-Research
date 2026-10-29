# E087 R257 S53 协议验收关口与Codex PR只读治理审计

日期：2026-10-29 UTC。track=operations；subflow=E。状态 COMPLETE（有界只读治理审计），FULL_SCIENTIFIC_ACCEPTANCE=OPEN。基线 main 70b3e24481a50a072d7f86fa25f1eaf2f18dedae，本轮首次观察main=e2d82406bbefd0cfc371a8d89498f399f6ed1cd2，写前变更为 70b3e24481a50a072d7f86fa25f1eaf2f18dedae（TH122理论轨新增）。target_key=(operations,R257_S53,11a7300900888a3e668f462d7378f8683b35161a,protocol-order-and-PR-gate)。该项针对工程证据的接受资格，避开Codex PR #1已执行的6种变异反例复算。

## 实读范围与结果

已读 main 的 README、docs/PROJECT_WORKFLOW_REQUIREMENTS_V2_2026-10-24.md、docs/RESEARCH_SYNC_WORKFLOW_2026-10-15.md、original239 v7.8索引元信息、最近提交、R257 S53冻结协议、正式报告、B独立报告、B协议顺序偏差补充、B比较器Python原文、B机读收据及开放PR #1、#2的摘要和PR #1独立报告/results.json。PR #2的同步协议从其独立分支读取，仅作待审查协作文本。未执行R/B数学程序，也未重跑PR #1探针；本轮是已知结果基础上的非盲态静态审计。

冻结协议提交11a7300900888a3e668f462d7378f8683b35161a早于R/B正式结果。比较该提交至写前main，ahead=9、behind=0；变更列表未包含冻结协议路径。B协议补充明确 B_BLINDED_PRESCORE_ORDER_FAIL：B程序编写执行发生在查看R输出后。现有B脚本的compare循环直接遍历收据提供的worlds/perturbations，末尾检查n==72；脚本没有显式完整唯一世界与容量集合、delta身份、baseline_lambda、local_derivative、evidence的检查。由源代码可直接确认检查缺口，未对源代码执行本轮新变异测试。

开放PR #1（codex/engineering-audit-20261029）报告7项反例预期检查，其中6种无效收据被旧比较器错误接受，1种错误minimum被正确拒绝。PR #1新增4份专用审计文件，仍 OPEN / merged=false；严格检查器修复未归入main。PR #2（codex/workflow-sync-20261029）亦 OPEN / merged=false，协议文本仍仅在PR分支。PR存在不能当作main采纳或科学验收。

GitHub对R257正式结果提交b3425ef23ec9a63957a466659ad1a805c08a3566的workflow runs查询返回空数组；本轮未触发CI，CI_STATUS=NOT_RUN。既有B JSON仅记录72项比较与错误注入，不能单独传达盲态失败及完整性缺口。R257 S53当前保留：R内部精确人工计算E1；B内部非盲算法一致性；B盲态协议关口FAIL；完整预声明B验收OPEN；外部团队复现0、E2新增0、E3新增0。R073与PESEN v0.1冻结。

## 跨轨巡检与待办

最近主线R257 S53，理论TH122新增归档，A轨最近提交0fe5188dc0aa3a8ef0ae8345e6857727cddecae2为2025真人复制数据依赖及时间对齐检查；未读其完整原始数据，不能声称R073复验合格。latest original239 v7.8的blob 36f24235901172642c46853298aebb421f1a3552；仅导航元信息已读，239条逐项科研验收 NOT_RUN。market截至MKT117、privacy截至F008 Phase2，目标文件与新输出无同名冲突。开放R170跨语言收据、R248的486项跨运行时比较、R251/R252命令行核验、R254/R255原CSV来源审计、R256 Node CLI均沿用OPEN，未冒称本轮完成。

风险登记 E087-01：严格B比较器完整性门缺失；已有PR #1反例证据，待Codex独立实现与审查。E087-02：事前B盲态执行顺序失败，不能用后验程序修复追认。E087-03：主线索引/README存在历史时点快照，最新研究状态以提交链与相应证据为准。未修改其他轨、冻结协议、索引或PR。未执行收费API、云计算、Actions；账户账单与免费额度 UNKNOWN。

下一项 E088：在PR #1有新变化时审阅严格验证器对重复覆盖、metadata及python -O的回归；否则转向R256 Node CLI、R251/R252跨运行时缺口，避免重复Codex工作。
