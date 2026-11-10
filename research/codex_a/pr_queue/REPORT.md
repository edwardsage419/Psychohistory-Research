> 最新20项快照与main兼容验证见 [final_sync_20261110/REPORT.md](final_sync_20261110/REPORT.md)；本文件保留17项历史清点。

# 开放 PR 工程队列刷新与可复用 Git 审计

track: Codex A engineering
subflow: PR inventory refresh and adoption commands
run_date: 2026-11-10 Asia/Shanghai
observed_main: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611
status: COMPLETE_FOR_PINNED_17_PR_SNAPSHOT
ci_status: 无新 dispatch；快照各 PR 检查项为空，不是 CI PASS
billing_checked: 无付费 API、订阅、资源、依赖安装或 CI；免费额度 NOT_VERIFIED

## 完成内容

在现有 PR #14 专用分支 codex-a/pr-integration-audit 中增加本包，不再新建清点 PR。保留原 12 PR 历史报告/清单；此处是新的固定17项快照。读取最新 main、开放 PR #1–#17 的 head/草稿/服务端状态、增量路径，以及新增 #13/#15/#16/#17 的报告和调用边界。现有 R/B 科研文件、其他 PR、冻结协议、R073/PESEN 均未修改。

新增 audit_queue.py：离线读取 `gh pr list` 的保存快照，验证字段、唯一正整数 PR 号、完整 SHA、main base、本地 fetched PR ref 对应 head；全部 head 校验完成后才生成合并结果。Git 操作使用捕获的一次 main SHA 和固定 PR SHA，记录每项 merge base、落后提交数、所有改动路径、Python/JS 字节的 Git blob/SHA256、main 合并模拟及完整两两矩阵。删除的代码文件明确记为 D/null，不读取不存在的 blob。Git 路径用 NUL 分隔解析，重命名按删除/新增处理。

脚本不会联网、checkout、修改工作树/refs 或实际合并分支；merge-tree --write-tree 会向 Git 对象库写入模拟对象。输出仅 stdout，不写成功文件。失败返回 BLOCKED/exit 1；冲突本身是可报告的审计发现，不伪装为程序失败或合并批准。

## 固定清点结果

- 17 个广告 head 与本地 fetched ref 全部一致。
- 17 次 main 合并模拟 exit 0。
- 136 对两两模拟 exit 0；增量文件路径无重叠。
- API 快照中 #1–#17 全为 Draft/MERGEABLE/CLEAN，statusCheckRollup=[]。
- 这些是快照时点事实，不保证完成本提交后远端状态仍相同。特别是本次正在更新 #14：快照保存其此前 head 24ee68ab，不可能自引用尚未创建的本提交 SHA。

完整 head、Git 身份和各次结果在 evidence/inventory.json；输入快照在 open-prs.json，其 SHA256 被审计输出及 execution.json 绑定。脚本只能证明所给列表被完整分析，不能自行证明输入列表包含所有开放 PR。两两文本可合并不证明整个队列顺序整合成功，尚未执行全队列合并后的联合测试。

## 可采用顺序与避免重复

机器可读建议在 adoption_plan.json；可直接运行的固定版本命令在 ADOPTION.md。

P0 联审 #1/#3/#15（反例、数学门、来源组合）；P1 联审 #7/#5 及 #8/#9/#17；#13/#16 为独立场次/评分变异门。P2 #4/#6/#10/#11/#12 保持各目标的原生重放边界；#2 走治理审阅；#14 是工程支撑，不是科学结题。

关键区分：#15 依赖 #3 的固定程序字节，#17 依赖 #8/#9 的固定程序字节，不要求先合并它们。#9 默认 fixture 来自 #8，但也可由原 B stdout 重新生成。#13/#16 重跑的部分 R073/R077 基线重叠，不能把重复执行当作新独立科学证据。没有将相似的哈希/重放骨架当作目标重复，未抽大型通用框架。

## 实际执行与工程修复

新审计器先写9项测试：不检查快照的骨架实际 8 failures/1 error，exit 1，red.log 保留。实现后增加删除代码场景，复现 git show 不存在 blob 的错误；修复为显式 D 记录后，最终10项在普通/-O 各通过。测试实际构造临时 Git 分支冲突，同时确认审计前后 HEAD 和工作树不变；还覆盖重复 PR、bool PR号、过时 head、缺字段、空快照、其他 base、缺ref及CLI重复JSON键。不是镜像断言或零测试通过。

命令：

```bash
python3 -B -m unittest discover -s research/codex_a/pr_queue -v
python3 -B -O -m unittest discover -s research/codex_a/pr_queue -v
python3 -B research/codex_a/pr_queue/audit_queue.py . research/codex_a/pr_queue/evidence/open-prs.json
```

运行审计前必须显式刷新 `origin/main` 和 `refs/remotes/pr/N`，再保存所需 API 字段；脚本自身不 fetch。完整快照捕获命令是：

```bash
git fetch origin main '+refs/pull/*/head:refs/remotes/pr/*'
gh pr list --repo edwardsage419/Psychohistory-Research --state open --limit 100 --json number,title,url,isDraft,headRefOid,baseRefName,headRefName,mergeable,mergeStateStatus,statusCheckRollup
```

本次 API 返回17项，低于limit，无分页截断推断；未来达到limit时需确认分页，不可直接声称清点完整。

按 ADOPTION.md 固定字节导出的 S53 和 R170 候选组合本轮均 exit 0，命令与输出原样保存；不是运行主干已采用入口。此前 #15/#17 的全部测试不重复计数，本轮两候选调用只跑普通模式。#13/#16 完整变异矩阵本轮 NOT_RUN；不把报告阅读说成执行。

内部独立上下文工程审阅实际跑10项普通/-O，未发现重要问题；建议补充“两两不代表全队列顺序整合”的边界，已落实到代码输出和文档。原始历史日志里的 unittest 行尾空格保留，不为通过空白检查改写证据；代码/Markdown/JSON检查单独执行。

## 剩余工作

保持所有 PR 未合并；owner/reviewer 的采用决定、全队列顺序整合、原生产 caller 绑定、Python3.11、全仓库测试、CI免费额度、正式科学验收仍开放。S53 盲态 FAIL、R170 witness 排序 NOT_ESTABLISHED、科学 PARTIAL 不变；无新增真人 E2、历史 E3 或外部团队复现。

下一有界项应从真实尚未解决的执行或采用障碍中选择；先刷新 main/PR，避免继续为已验证的相同快照制造重复报告。
