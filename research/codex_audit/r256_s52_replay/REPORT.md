# Codex R256 S52 归档命令行与跨运行时复算
track: codex; subflow: archived-cli-replay; run_date: 2026-10-29 UTC
observed_head: 51c408124fadffa4f5f15c7ccafa5f198b636e0c
status: COMPLETE（本轮有界执行审计）；完整R输出JSON同一性：PARTIAL

## 选题和实际读取
先读main最新HEAD、最近8提交、开放PR #1/#2/#3、完整路径树、五份必读项目文件、original239 v7.8元信息和154项待核队列、R256原冻结/S52冻结、原正式验收和程序、S52程序/收据/补充、更正记录以及E086。E086和补充报告明确“隔离V8函数已执行，归档Node CLI仍待验证”，因此本轮补命令行和跨运行时证据，不重写原有数学结论。239项逐条科学验收NOT_RUN。
最新R轨交接20261029T034326Z明确已读Codex PR #3，R主线推进R258 S54，未重复实现检查器。提交前main并发新增TH123（acf61773c4f172d9c586084e842b33998268b674），仅理论文件/索引及交接变更，未触及执行来源或Codex目标。已读theory短交接20261029T041516Z，明确列出PR #1/#2/#3及未合并状态。加上market/R已有交接，可确认三轨均已有实际同步采用记录，不宣称未来零遗漏或零重复。交付以该最新main为父提交保留理论变更。没有修改任务频率或新建任务。

## 来源、版本与运行
通过连接器从observed_head固定SHA获取七份执行输入，全部实际Git blob与远端树相等；SHA256/Git blob详见logs/execution.json及source_manifest.json。CSV真实全字节598348，4608行、44列，SHA256=8be5360465497321c15bffc554c7088fad48bcef71847e43e2ee2f714ed5119b。归档CSV不复制到本PR，由仓库原路径读取。原CSV、冻结协议、程序、收据和历史报告均不修改。
环境Python3.12.14、Node v24.19.0、Linux；仅标准库。seed=N/A，完整有限枚举。无完整Git clone/worktree，沿用已诊断的原生Git代理失败，用固定SHA来源快照；不伪称完整检出，也未运行全仓库测试（NOT_RUN）。

在仓库根目录执行：
`python research/codex_audit/r256_s52_replay/run_audit.py . --output /tmp/r256-s52-audit`
在本审计目录执行：
`python -m unittest discover -v`
本地真实root=/workspace/r256-replay，实际输出目录research/codex_audit/r256_s52_replay/logs。脚本记录每条原生命令、cwd、退出码和stdout/stderr。并发审计进程必须使用不同输出目录。

## 实际结果
- 原生R256 Python --test：82真实unittest通过，失败/错误0。
- 四个归档Node CLI原样执行exit=0：R重建、B条件U动态规划、原CSV完整重放、E086第三路线。两个沙盒干净对照也通过。
- 原CSV重放真实比较202752字段、18432格守恒；SHA与原正式收据一致。E086脚本输出60605项内部检查、失败0。这些为脚本内部检查，不能计成unittest。
- Python调用原冻结队列生成器，在每个信息分组直接累计两种标签的平方误差（Fraction），不导入两份JS算法。相较R与B，各144字段（45风险、45组数、45混合组数、9事件数）精确一致，合计288次字段比较。属于已知结果后的跨语言复算，不是新数据或外部团队复现。
- 实际负例4项：E086对risk=999在risk断言退出、原CSV单字节变动在SHA256断言退出；Python比较器分别拒绝错误风险和重复world。两项CLI负例不仅检查非零退出，还核对具体诊断，并先跑同沙盒干净对照。全部被拒绝。

## 发现的收据边界与首次失败
首次脚本要求R输出与归档JSON完全相等，实际exit=1，见first_failure.json。逐字段诊断后确认仅归档多出四个附加验证声明：
negative_injection=PASS；independent_dp_exact_comparison=PASS；comparison_fields=144；future_label_leakage_risk=0_ILLEGAL。
R compute()并不生成这些字段，故不能声称“全部JSON由R CLI重现”。本轮显式保留r_json_matches_archive=false，r_computation_fields_match_archive=true，并列出archive_only_attestations；原归档保留不动。前3个声明涉及的风险比较/错误检测有本轮新执行证据，但执行方式不追认原历史操作；第四个泄漏负例不在本轮重跑范围。现未发现计算字段或数值矛盾。

## 工程审查及修复证据
一次独立上下文内部代码审查发现：
1. Important：复用输出目录失败可能留下旧COMPLETE收据。先写回归，实际失败；修复为启动时撤销旧execution.json，成功后同目录原子替换。
2. Minor：负例只看非零退出。已补具体risk/hash诊断及两个干净沙盒对照，避免依赖/路径故障被算作拒绝成功。
3. Minor：import原生模块默认写__pycache__，违背来源只读意图。先写全来源字节/文件集合不变回归，实际失败；设置dont_write_bytecode后干净沙盒全量执行，来源目录无新增/更改。
两项新增回归最初2失败，修复后2/2通过，原始safety_red.log及safety_green.log保留。补充修复后完整重跑审计exit=0，结果如上。审查者不是外部科学团队。没有剩余审查阻断项。
本轮脚本只是可重复执行的工程审计器，不是面向任意不可信JSON的通用验收服务。历史原生程序测试及本轮回归分列，不把重复执行数或字段数混成科学样本量。

## 交付、费用和下一步
output_paths: research/codex_audit/r256_s52_replay/下程序、回归、来源清单、报告、初始失败和原始日志；research/coordination/codex/下唯一短交接。
分支codex/r256-s52-cli-replay-20261029，以PR交付；最终commit/PR及远端回读身份见本轮最终交接。仅新增专用路径，不覆盖其他轨或main。写前复核HEAD和目标路径；不自行合并。
ci_status: NOT_RUN，不请求Actions，提交/PR加[skip ci]；历史CI不代替本轮运行。新增收费操作0，未核验账户账单/免费额度，不启用云计算/订阅/付费数据。
evidence_scope: 非盲态、同项目内部、有限人工E1。E2/E3新增0、外部研究团队复现0；不改变R073/PESEN冻结，不宣称经验样本外/现实排队预测或完整一般排队理论验证。
next_action: 其他轨可引用本PR将这些固定版本的本地Node CLI执行缺口标为已核验（待审查），保留CI及外部验证开放；Codex下一项可选R258 S54归档程序原样执行/原CSV核验，先查实时队列避免与B轨重复。
