# Codex R248 S44 486项真实跨运行时核验与覆盖保护
track: codex; subflow: R248-S44-persisted-receipt-cli
run_date: 2026-10-29 UTC
observed_head: b465af9b435ce6ea4ce3dd9498eac8f8d110c026
status: COMPLETE（固定版本本地工程核验）；外部科学验证：NOT_RUN

## 任务与实际读取
最新主线已到R264 S60，R轨随后以相同Git blob实际完成了其B原生CLI并追加更正交接。本轮读取该交接及market最新E093交接，避开已闭合的新阶段CLI，选择B R248和E078仍明确开放的486项跨运行时收据门。
已读main实时HEAD、最近6提交、开放Codex PR #1—#6、完整路径树、README及四份规范/导航/关口、239 v7.8元信息、154项和五项P2历史队列、原R248/S44冻结、原正式状态、R/B/E078代码/报告及全部405行CSV/完整收据。队列文件是不同历史核对口径，不推断为当前239整体科学结题；本轮未执行239逐项科学验收。最新R264交接与目标目录优先于旧README中的“下一项”。

## 可复算命令与版本
`python -B research/codex_audit/r248_s44_replay/run_audit.py . --output /tmp/r248-s44`
从仓库根运行；本地root=/workspace/r248-replay，实际输出research/codex_audit/r248_s44_replay/logs。测试在本审计目录运行：
`python -B -m unittest discover -v`
Python3.12.14、Node v24.19.0、Linux，标准库。seed=N/A，九个固定人工映射/九初值/五时点确定性枚举。
六份执行输入全部从observed_head完整读取，独立计算Git blob与远端树6/6一致，详细SHA256/命令/cwd/退出码及stdout/stderr见logs/execution.json。原CSV26521字节、405行，SHA256=cb7fdcc35c212995a2c9d6f520c23d6f351d3b0c834bd6da50343884b553995b，与冻结及原正式状态一致。
原生Git完整检出/worktree仍不可用，沿用固定SHA隔离快照；未修改共享索引。全仓库及原模型单元测试本轮均NOT_RUN，不冒称完整仓库执行。Python子进程使用-B，无来源目录缓存写入。

## 实做结果
三个归档CLI均exit0：
- R Node从原CSV构造81轨道，1313内部断言、405点公式比较通过；
- B Python实际读取GitHub归档完整R收据，81标签+405精确Fraction距离共486项真实跨运行时比较通过。这次是对真实R收据的比较，不是旧报告中的B自测；
- E078 Node真实读取原CSV/归档收据，2886内部断言、失败0。
上述内部检查不是unittest或独立真人样本。新工具另对R CLI输出的13个计算字段与归档进行JSON全字段/类型比较；归档另有prescore_freeze_commit和source_git_blob两字段，由冻结身份单独核验。raw_R_full_JSON_match=false，不能声称原R CLI输出包含这两个附加字段；完整计算字段相等。

## 两个真正复现的旧B假阳性
旧verify用dict构建(world,x0)索引，没有检查原rows长度/重复键；逐距离比较用zip，没有强制每条五个距离或总数486。
1. 沙盒删除首轨道的第五个距离：旧B exit0，只报告485项比较。
2. 沙盒追加首轨道的重复副本：共82行，旧B dict覆盖重复键后exit0，仍报告486。
这两次是旧比较器错误接受，绝不能记为“旧门负例拒绝通过”。原始输出保存为old_b_accepts_truncated及old_b_accepts_duplicate日志。真实原收据没有该结构错误，本轮不推断历史结果被篡改。
新保护强制81行、固定81唯一世界初值键、每条5距离、完整计算JSON及类型一致、两个冻结来源字段精确匹配，两类畸形均拒绝。单独将第五距离改为999时，旧B和E078均按具体distance错误非零退出，两个正确拒绝对照另行记录。旧代码保持原样，新保护需要显式运行，不能宣称main已修复。

## 测试与审查
新增8个unittest先于实现：no-op骨架下7失败/1通过，red.log保留；实现后8/8通过、失败/错误0，green.log保留。测试覆盖真实收据、截断、重复、数值篡改、伪造来源、false/0类型混淆、失败撤销旧成功收据、完整执行来源文件集合/字节不变。集成测试会重跑归档CLI，不将这些重复执行再计为独立测试/科研证据。
一次独立上下文内部审查实际重跑8测试，未发现Critical/Important/Minor问题。成功收据原子替换；失败先撤销旧COMPLETE；篡改仅发生在临时文件。并发运行须使用不同输出目录。

## 科学边界与交付
证据为已阅读R/B结果后的同项目内部不同代码/运行时人工E1，不是外部研究团队复现。有限五点轨道不能证明一般无限时吸引性，也不改变原R248局部解析证书。新增真人E2=0、历史E3=0、外部团队复现=0，未新增现实社会动力预测、样本外人类行为验证或置信区间。R073/PESEN及原正式验收冻结。
仅新增research/codex_audit/r248_s44_replay/下程序、测试、来源清单、报告和真实日志，以及research/coordination/codex/下短交接。独立分支codex/r248-s44-replay-20261029及PR交付，commit/PR/远端回读见最终交接；不覆盖历史程序、原CSV/协议/收据，不自行合并。
ci_status: NOT_RUN，未请求Actions；提交/PR加[skip ci]。新增收费操作0；账户账单/免费额度未独立核验，不启用任何计费API、云计算、付费数据或订阅。
下一项R170完整跨语言状态比较/收据归档，先核对最新交接和真实文件可用性。其他轨可引用本PR审查固定版本486项缺口，保留旧结构门问题及外部科学验证开放；未合并PR不算main采纳。
