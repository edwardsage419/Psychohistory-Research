# Codex A：12 个草稿 PR 整合审计与跨 PR 回归

- track: Codex A engineering
- subflow: PR integration and reproduction
- run_date: 2026-11-10（北京时间；执行记录由本轮生成）
- observed_head: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611
- status: COMPLETE_BOUNDED_LOCAL_AUDIT；远端 PR 创建待权限验证，科学验收不变
- evidence_scope: NONBLIND internal engineering; new E2/E3/external-team replication = 0
- ci_status: UNKNOWN（GitHub API 403）；本轮未 dispatch CI
- billing_checked: 无新增购买、付费接口、计算资源或订阅；账户免费额度 NOT_VERIFIED
- commit_sha: 本目录由其所属 Git 提交标识，不写入自引用 SHA

## 范围和执行方案

按用户授权连续推进。先读取 main、最近提交、公开 PR 列表、全部 PR 的增量、报告、代码与来源清单，并读取同步规范、v2 工作流、E162/E126 既有治理记录、S53 冻结及 R170 排序条款。独立目录 /workspace/codex-a/repo，分支 codex-a/pr-integration-audit；原 /workspace/Psychohistory-Research 未写入。未更改环境草稿或发布环境。

采用现有验证器加跨 PR 契约测试，避免新建竞争性数学验证框架。完成顺序：全量清点和冲突模拟 → 固定 PR 快照复测 → 当前 main 加 PR 新增文件复测 → 两组依赖的跨 PR 检验 → 证据归档与专用分支交付。

## 全量清点及建议整合次序

所有链接位于 https://github.com/edwardsage419/Psychohistory-Research/pull/N 。2026-11-10 公开列表含 #1–#12，均 Draft；12 个页面 HTTP 200，Git pull refs 完整读取。不得将 pull refs 存在单独用作 OPEN 证明。API GraphQL Forbidden，REST CONNECT 403，故 review threads、精确服务端 mergeability、branch protection 和 CI 检查结论 UNKNOWN。

| PR | 固定 head 前缀 | 落后 main 提交数 | 功能 / 依赖 | 实测测试数（每模式） | 建议 |
|---|---|---:|---|---:|---|
| #1 | 8196dede | 1309 | S53 旧比较器六类假阳性，#3 的缺陷证据 | 无 unittest；7 探针期望通过 | P0，与 #3 联审，保留失败历史 |
| #2 | 2600c3d7 | 1308 | 三轨同步文档，无运行时代码 | N/A | 单独治理审阅；不能替代现行用户指令 |
| #3 | 97d5f74d | 1306 | S53 严格 KKT 收据检查；不导入 #1 | 32 | P0，数学门可复测；来源门仍 NOT_RUN |
| #4 | 039e7d26 | 1296 | S52 Node/Python 重放及写入安全 | 2 | P2 独立候选 |
| #5 | ab9c45eb | 1295 | S54 持久收据与原归档重放 | 7 | P1，先于普通重放整合 |
| #6 | 6b17d869 | 1285 | R251/R252 持久收据完整比较 | 7 | P2 独立候选 |
| #7 | dee83459 | 1217 | S44 覆盖和 486 字段比较 | 8 | P1，拒绝重复/漏项有直接价值 |
| #8 | fd0d2c65 | 1119 | R170 288 状态分布及 B 全文归档 | 10 | P1，与 #9 联审，不能独自宣称身份强制门 |
| #9 | 89a64ecd | 1112 | R170 四来源及 B 全文的字节身份门 | 11 | P1，默认 fixture 依赖 #8，或另生成 B stdout |
| #10 | 9ed78489 | 1112 | S67 Node 原生重放、独立 DP | 8 | P2 独立候选 |
| #11 | c1ee936c | 1111 | S66 原生重放、前缀 DP | 10 | P2 独立候选 |
| #12 | 95c1754e | 1106 | S62 原生重放和完整 CSV 重建 | 8 | P2 独立候选 |

建议评审次序：#1/#3 → #7/#5 → #8/#9 → #4/#6/#10/#11/#12；#2 走单独治理审阅。此为本地工程建议，不是自动合并批准。各组无须因排序而等待其他无关组完成。

## 依赖、冲突、重复能力与历史一致性

`evidence/inventory.json` 保存全 SHA、merge base、全部增量路径、每 PR 的 main 合并模拟和 66 对 PR 的模拟。`git merge-tree --write-tree --name-only` 全部 exit 0；没有 PR 增量路径重叠，也没有与当前 main 的目标路径碰撞。模拟只写专用仓库的 Git 对象，不合并分支或修改工作树。不代表 GitHub 必须允许合并或科学验收通过。

#1→#3 是证据依赖，非代码依赖：跨 PR 测试实际证明旧比较器接受六个非法收据，而 #3 全部拒绝。真实 main 收据通过 #3，但返回盲态 FAIL、完整科学验收 PARTIAL、来源认证 NOT_RUN。

#8→#9 是默认测试数据依赖：#9 默认从 #8 的目录读取 B_full_receipt.json，不导入 #8 代码。#9 文档提供原 B stdout 替代生成方法。本轮跨 PR 测试以固定 #8 全文加当前 main 四个来源通过 #9，并拒绝等语义重新序列化和来源尾部新增字节。#8 runner 的身份布尔披露没有被本轮改成硬失败，使用时必须同时调用 #9；首字典序反例的排序资格仍未确定，不改冻结解释。

#4/#5/#6/#7/#10/#11/#12 复用相似的临时目录、哈希、重放和失败撤销模式，但目标输入与数学证据不同，不是重复证明同一结果。#10/#11 都用 DP，分别处理窗口命中与后验预测前缀统计，不能互换。暂不抽公共框架，避免破坏已有固定来源。main 上 R334 strict gate 为另一对象，不将其视为 #3 已采用或替代品。

递归解析 11 份来源清单（#2 无 source_manifest）：197 条带 path + blob pin 的记录全部与当前 main 一致，详细 Git blob 和 SHA256 在 source_drift.json。计数含跨 PR 重复引用，不是 197 个独立源文件；未把无 pin 的文字记录计入。这支持这些已记录字节未漂移，不认证作者、运行时间或盲态。较旧基线的其他新增 main 研究不是 PR 输入变化；不要为“更新基线”改写历史 observed_head 或执行日志。

## 实际验证

Python 3.12.14，Node v24.22.1，标准库，无新增依赖安装。

1. 精确 PR head 快照：#3–#12 共 103 项现有 unittest，普通和 `-O` 各执行一次，206 次全部成功。
2. 当前 main 加全部互不重叠 PR 增量的独立目录 /workspace/codex-a/current：同样 103 项 × 两模式，206 次全部成功。合成目录不含 .git，不伪称是 GitHub 已合并分支。
3. 本目录新增 5 项跨 PR 契约测试，普通和 `-O` 各通过，合计 10 次。六类 S53 反例位于一个测试的六个 subTest，不冒充六个测试函数。缺少固定 Git 对象会直接报错，不 skip。
4. #1 原探针在当前整合副本实际 exit 0：六假阳性和一个正确拒绝控制均符合历史描述。成功复现缺陷不是旧验证器安全通过。
5. #10–#12 原生 runner 在当前整合副本均 exit 0：S67 13584 行/27 世界及元数据漏检重现；S66 192 tails/27 alarms 与完整字节重建；S62 5328 来源行/180 指标字段及完整 CSV 字节重建。具体原始 CLI、输出 hash、控制结果在 execution 证据中。

重放命令模板（每个目标目录见 inventory 的 code 路径及 suites 的完整 command/cwd）：

```bash
python3 -B -m unittest discover -s research/codex_audit/r257_s53_validator -v
python3 -B -O -m unittest discover -s research/codex_audit/r257_s53_validator -v
python3 -B research/codex_audit/r271_s67_native/run_native.py . --output /tmp/unique-s67-output
python3 -B -m unittest discover -s research/codex_a/pr_integration_20261110 -v
python3 -B -O -m unittest discover -s research/codex_a/pr_integration_20261110 -v
```

新增跨 PR 测试从 Git 对象读取固定 head，先具备对象：`git fetch origin refs/pull/3/head refs/pull/8/head refs/pull/9/head`。无需把这些 PR 合并进 main 即可执行。输入 main 本轮固定 SHA，后续变化必须另做版本复核，不能悄悄替换 pin。

## 问题登记及未完成队列

- API-403：GitHub API 不可用，CI/评审/保护规则未知。Git 读和网页读可用不能推出 API 写权限。
- S53-SOURCE：#3 明示 source_authentication NOT_RUN。本轮记录来源身份，但未把来源门接入其生产 CLI；下一包优先做显式附加的来源认证包装和篡改回归，不改历史科学收据。
- R170-COMPOSITION：#8/#9 仍需操作者同时调用；可做独立组合入口，保留首反例排序 PARTIAL，不选择新的历史 witness。
- PR2-GOVERNANCE：无代码测试，文档沿用与最新规范/用户要求的协调需人工评审。
- FULL-SCIENCE：全仓库测试、Python 3.11、外部团队复现、真人 E2/历史 E3 未运行。没有把单测成功升级为科研预测有效。
- CI：未核实免费额度，不触发 Actions。读取所有 workflow 发现没有 pull_request / workflow_run / schedule/create 触发，push 为目标路径过滤，本轮新增路径不匹配；提交仍加 [skip ci]。服务端最终状态因 API 403 不能验证。

所有输出位于本专用目录；原有 PR、R073、PESEN v0.1、冻结协议、原始数据、历史结果均未修改。没有自动合并、关闭、强推、删除证据或修改 main。此为有界第一轮完成，不声称后台自动持续执行。

## 内部工程审阅

按 requesting-code-review 技能进行独立上下文只读审阅；审阅者实际重跑新增 5 测试两模式，并独立核对 197 条来源的 blob/SHA256，无 Important 发现。Minor：网页 OPEN/DRAFT 证据缺离线摘录；已补 evidence/web_status_excerpts.json，含 12 页面可见文字摘录及原 HTML SHA256。此为内部工程代码审阅，不是外部科研复现或正式科学验收。

## 远端交付回执

实现提交 `2c9efe0aff8dbe7e6d70560b23fd64de8fcfcb26` 已推送并经 `git ls-remote` + `git fetch` 回读确认，专用分支 `codex-a/pr-integration-audit`。测试文件 Git blob `8133c091b80f06df1af8e04bd334b7ec821544a8`，SHA256 `3a80e41308413c3d0ccda16a298d10823e1ab846340ec77ff6ba9d180cf0614b`。main 仍为本轮固定 SHA。

尝试 `gh pr create --draft --base main --head codex-a/pr-integration-audit ... --body-file /workspace/codex-a/pr-body.md`，exit 1，精确错误：`Post "https://api.github.com/graphql": Forbidden`。未创建新 PR，未将失败记作同步成功；分支推送成功与 PR 创建失败分别记录。API 写操作停止，不重复索取或提取凭证。可从 https://github.com/edwardsage419/Psychohistory-Research/pull/new/codex-a/pr-integration-audit 创建草稿 PR（这是创建入口，不是已存在的 PR）。现有 #1–#12 未修改；所有成果仍 OPEN_BRANCH_UNMERGED，不属于 main 已采用成果。CI 在线实际状态仍 UNKNOWN，本轮没有 dispatch。

## 后续授权后的 API 阻塞定位

用户授权继续后，重新确认 main 和工程分支 SHA 未变。`gh pr list --head codex-a/pr-integration-audit` 仍报 GraphQL Forbidden。进一步只读 HEAD 请求 `https://api.github.com/repos/edwardsage419/Psychohistory-Research/pulls` 返回代理 CONNECT 403（envoy），请求未到达 GitHub；当前 enforced 网络白名单无 api.github.com。故先前 API-403 不能解释为已确认 GitHub 账号写权限不足。网页创建入口返回登录页，当前无已认证网页会话。

已通过环境配置工具仅保存新增允许域名 api.github.com 的草稿，保留 package_managers 预设，不添加秘密或改写安装/启动说明。草稿状态 saved，requires_publish=true；保存本身不应用运行时网络，未发布环境。须由用户在环境设置审阅、保存并按平台要求发布后，重新读取生效状态、请求 API，再验证是否还有身份/写权限阻塞。未重复创建 PR、未触发 CI；本轮新增代码不变。

## 网络生效后的 PR 交付确认

用户发布新环境后继续授权。本轮确认环境 observations_current=true、network_policy.state=enforced，api.github.com 已在有效白名单。专用分支和 main SHA 与此前一致，查询该 head 的全部状态 PR 为空，随后成功创建草稿 PR：https://github.com/edwardsage419/Psychohistory-Research/pull/14 。回读确认 OPEN、isDraft=true、base=main、head=54c7ad68314f3129d93861a08053373940188a3b、MERGEABLE/CLEAN。此次状态读取取代此前“当前 API 不可用”的运行时阻塞，但不改写历史失败记录。

现在 API 可读取 #1–#12：全部仍为 OPEN DRAFT，服务端 MERGEABLE/CLEAN，statusCheckRollup=[]。#14 同样无检查项；按工程分支查询 Actions runs 返回 []。这些空记录不是 CI PASS，不证明免费额度或保护规则已满足；没有触发任何 CI。

另观察到并行主体 Codex B 新建 #13（R074/R075 session-isolation，head 91aa5ec254bc4dc561e78b908bda77d6477e1746）。已读取说明，验证对象与本轮两组契约测试不同；它在最初 12 PR 冻结清点之外，未纳入本轮 66 对冲突矩阵或测试计数，后续工程队列应加入 #13 联动检查，不重复其 donor/heldout 验证器。未修改、合并或关闭 #13。

本次仅补充实际远端状态证据，无实现改动或科研结果变化。完整 API 状态存于 evidence/live_pr_status_after_network_update.json；该文件是读取时快照，后续状态变化需重新读取。
