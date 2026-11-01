# R335 P0 生产收据优化模式错误接受与邻近R模型影响范围

日期：2026年11月1日 UTC。轨道：R主线及B科学验证。状态：PARTIAL_P0_REMEDIATION。证据：内部非盲态程序完整性复核，有限构造E1。无新S编号，无模型重拟合，无真人E2或历史E3。

## 1. 冻结身份与历史验收

原始R335三人群体公开一致性模型对应original239 03-013。冻结协议提交 `0c553f662ae723adadaba9c7f4ce325d8964032e`，原始源码Git blob `9c005079716fe38eb4cb6d99730884a55e2795a3`，384行CSV blob `f5987d4d9da8ef7532a3615b5f7fb6efbd4701cb`，128条件JSON blob `4ab8f69cbd483099dd2a1be28cb052e1e3bdb279`。

历史正式验收 `PASS_BOUNDED_E1_CONSTRUCTED_PUBLIC_UNANIMITY_ORACLE_ONLY`，历史CI运行 `40051490899` 报告Python 3.11、3.12及独立审计三个job成功。既有两项负例是常规执行条件下的归档结果。此轮保留原历史成功与有限E1范围，不追认历史CI曾运行优化模式。

本轮起始main HEAD：`133163d56db11c5f57c45679c704dfb99874e480`。original239 v7.8 blob `36f24235901172642c46853298aebb421f1a3552`；当前154项itemwise待核队列 blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`。两份文件未修改，待核净减少0项。Codex PR #1和#3在本轮读取时仍为OPEN_UNMERGED，R257 S53问题与本轮R335目标不同。

## 2. R主线P0反例：实际原生执行

直接从main读取原始R335源码，并在本地精确还原源码字节，Git blob一致。调用原源码的`render()`重建CSV及JSON，两份结果的Git blob均与main归档一致。随后仅在隔离临时目录运行原始`--test --audit`。所有破坏性变更仅作用于临时副本。

环境：CPython 3.13.5，标准库，无随机抽样，无网络或收费依赖。五种输入条件分别在普通模式与`python -O`优化模式下运行原始CLI和新独立检查器。原始与新检查器共20次子进程执行。

| 输入条件 | 原始普通 | 原始优化 | 新检查器普通 | 新检查器优化 |
| --- | --- | --- | --- | --- |
| 固定正确字节 | PASS | PASS | PASS | PASS |
| CSV决策标签篡改 | FAIL | **FALSE PASS** | FAIL | FAIL |
| JSON模式标识篡改 | FAIL | **FALSE PASS** | FAIL | FAIL |
| 两份收据同时缺失 | FAIL | **FALSE PASS** | FAIL | FAIL |
| 源码追加一个换行 | PASS | PASS | FAIL | FAIL |

三个优化模式错误接受案例中，原始CLI退出码0，仍输出`R335 PRODUCTION_REPLAY_PASS`，其五项unittest也报告OK。源码仅追加换行不会改变计算，原始CLI没有固定源码身份检查，两个模式均接受。原始正确字节没有发现数学不一致。

根因：`research/R335/r335_groupthink.py`的`audit()`使用Python `assert`进行全部持久化CSV和JSON身份校验。优化模式删除这些表达式；`test_byte_replay`调用相同的`audit()`，因此出现五项单测全部通过却未读取归档收据的条件性假阳性。

## 3. B轨独立补充检查

新增`research/evidence_audit/r335_strict_receipt_gate_20261101.py`。该程序不导入R335原始实现，以独立布尔枚举重建128个世界和384条记录，核对完整CSV、完整JSON、冻结汇总、JSON重复键及三个固定Git blob。所有失败采用显式异常，`python -O`不会移除检查。

新增`research/evidence_audit/test_r335_optimized_gate_20261101.py`。该回归程序从精确固定的原始源码生成测试夹具，执行上述五组正常和破坏性对照。它属于同团队非盲复算；新检查器的有限数学枚举不调用原模型。

本地普通与优化模式运行回归程序的完整输出相同。新检查器在10个条件和解释器模式组合中，正确样本2次通过，四种错误输入乘以两种模式共8次拒绝。独立计算的完整人工结果与归档完全一致。实际执行矩阵见`research/evidence_audit/B_R335_P0_OPTIMIZED_GATE_LOCAL_EXECUTION_2026-11-01.json`。

本轮B检查：COMPLETE，仅限上述原生CPython 3.13.5和E1收据。原始生产入口仍未接入严格检查器，整体P0关闭状态为PARTIAL。新程序在CPython 3.11与3.12的原生执行、跨团队盲态复现、原作者真人数据验证均为NOT_RUN。未发现历史归档真实遭到篡改的证据。

## 4. 同类风险的限定范围调查

逐个读取main中R333、R334、R335、R336、R337、R338、R339、R340八个生产Python源码的`audit()`，逐一核验Git blob及收据检查写法。八个脚本均存在以`assert`保护持久化字节检查的写法。R334已另行归档原生反例及独立严格检查器；R335在本轮完成原生反例和独立补充检查器。其余六个为：

| 模型 | 原始源码Git blob | 当前证据 |
| --- | --- | --- |
| R333 | `c28c82a6a18ababe8da14b0f48c846d940bf32b3` | STATIC_RISK |
| R336 | `bcbf7b40c1f8ba86d5478d57509a437b5ba0279f` | STATIC_RISK |
| R337 | `96e9e2be1b7d7ac0ac7b3cfcf05c7c81e938090d` | STATIC_RISK |
| R338 | `1ee4cff348278f208628358b626174fd5fcb5524` | STATIC_RISK |
| R339 | `ed769df49658f345e78859f2be733b5b43322791` | STATIC_RISK |
| R340 | `7bd287300825266be1a13fc12229b8c48b01e7` | STATIC_RISK |

对这六个脚本仅完成静态检查，尚未运行原生篡改反例，不能将它们记为已复现的错误接受。此处也不能推断其他R模型安全，扫描范围仅为上述八个源码。建议优先对六个脚本建立固定来源、实际负例、独立检查器及统一防回归验收，保留历史源码和CI事实。

## 5. A公开数据简查与去重

本轮查询公开真人百轮重复囚徒困境资料，复核Montero等人2022年固定及重新匹配对手的两组实验，作者论文确认100轮设计。官方Dryad DOI为`10.5061/dryad.37pvmcvmk`，目录包含`fix.csv`和`rand.csv`。经核对本仓库`research/coordination/r/20261029T124459Z-r267-s63-a-montero-b-primitive-handoff.md`，该来源已在R073关联研究和R267 A轨登记，官方Dryad字节等同性仍开放。故本轮只作去重和资格复查，不将其登记为第二独立队列，也未读取新的参与者原始记录。

R073冻结跨实验独立验证：NOT_RUN。新真人E2评分0，历史E3评分0。数据许可、完整身份与来源去重问题保持开放。A本轮状态：PARTIAL，未形成新的可评分独立数据集。

## 6. GitHub、CI、费用和后续验收

本轮只在R自有`research/evidence_audit/`和`research/validation/`新增独立文件，保留原始模型、冻结协议、正式验收状态、既有收据和original239队列。写入前核对main HEAD及目标路径不存在；提交后需回读实际commit、文件Git blob和CI情况。

本轮新代码原生执行已完成；本轮GitHub Actions没有启动。新提交CI为NOT_RUN。GitHub账单与免费runner额度未独立核验，未产生主动计费操作。代码运行通过仅证明有限人工收据完整性，科学等级保持E1，E2/E3及外部独立复现均未建立。

下一优先工作：在不修改历史冻结源码的前提下，对R333和R336至R340做逐项原生负例验证并评估统一安全验收入口。将R334与R335的独立检查器作为候选补充门槛，完成Python 3.11及3.12原生复验和代码审查后，再决定正式集成。之后继续original239 P0/P1 itemwise证据核查及R073独立数据复验。
