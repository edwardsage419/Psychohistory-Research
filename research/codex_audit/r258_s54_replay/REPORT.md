# Codex R258 S54 归档程序原样执行与持久化收据核验
track: codex; subflow: R258-S54-archived-replay
run_date: 2026-10-29 UTC
observed_head: 116385b06abb500ab91dd546b9b57141f6ed3ee3
status: COMPLETE（固定版本的本地工程复算）；外部科学验证：NOT_RUN

## 任务和避重
先读main实时HEAD、最近8提交、开放Codex PR #1—#4、完整路径树、五份必读项目文件、original239 v7.8元信息及154项待核队列。历史README/导航不替代最新提交。已读原R258/S54冻结、原正式验收/机器收据/结果、R/B程序/报告/收据和E088/最新market交接。
E088已在隔离JavaScript环境核查原1728行CSV，明确留下“原样CLI尚未运行”和其独立50152检查执行器未归档两个开放项。本轮选择前者，附加原生生成器字节再现，不重写其独立JS执行器，也不将本轮再生成当作已归档E088方法。全部原始来源/协议/程序/收据保留。

## 实际执行与身份
Python3.12.14，Linux，标准库，无随机抽样（seed=N/A）。九份执行输入全部从observed_head通过连接器取全字节，实际Git blob独立重算与远端树全等，见source_manifest.json和logs/execution.json。
原CSV134900字节、1728行，SHA256 0af44af9bc97bd2cd8035e8437a58d420ac172cb6657eae969a50968f8be0f54。完整检出/worktree仍不可用，采用固定SHA隔离来源快照；全仓库测试NOT_RUN。没有规避原生Git网络策略或覆盖共享工作树。

从仓库根执行：
`python -B research/codex_audit/r258_s54_replay/run_audit.py . --output /tmp/r258-s54`
本地真实root=/workspace/s54-replay，实际输出目录research/codex_audit/r258_s54_replay/logs。全部子进程命令/cwd/退出码及stdout/stderr已存档，使用-B防止向来源目录写字节码。不同并发进程须用不同输出目录。启动时撤销旧成功收据，成功后原子替换，失败不能残留旧COMPLETE。
从本目录执行 `python -B -m unittest discover -v` 验证新增工具。

## 真实结果
1. 原R258 --test为82/82；S54 R --test为8/8；S54 B --test为7/7，合计97个归档unittest，失败/错误0。
2. 原归档跨路线检查器直接执行，输出3456逐政策期望比较、27世界初态对、四个内置负例拒绝，status=PASS。这些是程序检查，不是3456个unittest。
3. S54 R --emit与远端正式收据全部JSON字段、值、类型及列表顺序一致；比较忽略对象键顺序/排版，不声称S54文本格式逐字节相等。B --emit的完整27行与正式收据一致。
4. 原R258 --emit只在临时副本执行，生成的原1728行CSV、原结果JSON、原机器收据三文件均与归档逐字节相等。该项是同一原生代码的确定性再生成，不是外部独立科学复现。原CSV/结果SHA与正式状态一致。
5. 新工具四个篡改控制均被拒绝：gap、重复世界初态、E1改E3、零改布尔false（Python普通相等可能混淆，使用JSON类型严格比较）。原归档收据未被改动。

新增7项unittest先于实现编写：no-op骨架下6失败/1通过，red.log保留；实现后7/7通过，green.log保留。涵盖真实归档、最优并列数、证据标签、类型、重复键、失败撤销旧成功收据、整套执行来源文件/字节不变。集成测试内部会重跑归档97测试，不将重复次数再计为新测试或独立样本。本轮为97个归档测试加7个新测试，均真实运行。

## 新发现：算法比较与持久化收据验收不同
原crossroute_gate的main现场调用R.receipt()/B.results()，没有读取R258_S54_COARSE_OBSERVATION_EXACT_RECEIPT文件。因此本轮把沙盒内该归档收据gap_A改为999后，原检查器仍输出与原先相同PASS；原文件的篡改不在它的输入范围。
这不证明真实归档已被篡改，也不否定3456算法比较。它限定了“严格检查器”的覆盖：现场两算法结果相等不能自动证明已落盘收据相等。
本轮新工具另将原样R CLI的完整JSON与固定归档比较，能拒绝该篡改；真实归档比较通过。corrupted_persisted_receipt_rejected_by_new_replay=true，archived_gate_ignores_persisted_receipt=true。日志gate_with_corrupted_archive.stdout保留实际旧门通过证据；不将此表述成旧门拒绝成功。
原source_method字段“未读原CSV”是当时计算路线说明，本轮不静默改写该历史字段；本轮读取/重算证据以新日志为准。

## 审查与证据边界
一次独立上下文内部代码审查重跑7项新增测试全部通过；未发现Critical/Important问题。Minor deferred：工具校验归档检查器的计数和退出码，未单独强制其status字符串必须PASS；本次原样输出已实际观察PASS且文件固定哈希，故不影响当前证据。若将来接纳变化后的检查器，应增加状态字段约束。本轮不扩大为任意不可信输入的通用验收服务。
此为已经阅读原结果后的内部非盲态、有限人工E1复算；不追认或改变原B代码先行/部分盲态资格，不是外部研究团队复现。E2/E3新增0，外部团队复现0，现实控制干预/样本外人类预测均NOT_RUN。原R258验收及R073/PESEN冻结不变。
E088独立JS执行器的文件归档仍未由本轮完成；不能把原生代码再生成替代它的独立第三路线方法。

## 同步、交付、费用和下一项
仅新增research/codex_audit/r258_s54_replay/及Codex短交接。分支codex/r258-s54-archived-replay-20261029，以独立PR审阅，commit/PR/远端回读身份见最终交接，不自动合并、不修改main研究结果。
ci_status: NOT_RUN，不请求Actions，提交/PR加[skip ci]。新增收费操作0；账单和免费额度未独立核验，没有启用云/API计算/订阅或收费数据。
下一轨可引用本PR核对固定版本CLI开放项；保留CI、外部科学有效性与E088执行器归档开放。Codex下一候选为R251/R252完整收据CLI或R248跨运行时486比较，先查最新交接避免与R/B/E轨重复。
