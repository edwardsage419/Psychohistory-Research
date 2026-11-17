# R127 生产校验入口候选补丁的受限分支验收

日期：2026-11-17。项目 R 主线，original239 P0 / 05-003。**本文件记录候选分支真实执行，不构成生产启用授权或科学结题。**

## 实际起点与历史候选

新分支以 main `f1761b89af48bc38f70c04b1369ce76ecb6492e9` 为起点。原正式 R127 工作流仍有 33 行可能在 Python 优化模式下被略过的 `assert`，并尝试写入旧机器收据后执行 `git pull --rebase` 和 `git push origin HEAD:main`。现有 main 仍使用此旧工作流。

11 月 11 日 Codex A 已完成 `research/codex_a/r127_workflow_candidate/` 候选修复、受限本地 Git bare 模拟与负向控制；PR #43 仅归档其证据，原生产入口从未改变。之后 PR #47 通过真实 Python 3.11 GitHub CI 对旧候选及临时本地仓库执行完整验证，其运行标记为 `44030127836`。本轮**复用此候选**，没有重写科学模型或创建重复验收程序。

## 本轮真正完成的工作

确认当前 main 的三个旧文件字节仍与已审阅的候选补丁前置身份完全吻合，然后按来源身份依赖顺序在独立分支精确应用原三文件补丁：

| 文件 | 原 Git blob | 应用后 Git blob |
| --- | --- | --- |
| `.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml` | `4b22f653dc7516bb31ead23e45dcf7f62261d79d` | `d17cbee8750577a76ff386f5faebc3310adc3994` |
| `research/codex_a/r127_local_gates/gate.py` | `a06c3266541785886356baacbc520beb8cdfcb78` | `e57cd52eea4bc8a46e94a98c22facb9db8b703a5` |
| `research/codex_a/r127_local_gates/pins.json` | `09c4101737bee8c49daee38992b197ee1210de2c` | `9a390df6cdfce82d55f14bfebcc98cc91b045c72` |

三个后置 SHA 与旧 `candidate_manifest.json` 的历史 `after.git_blob` **逐字节相同**，均通过远端回读确认；不存在擅自改动旧补丁的数学阈值或源身份定义。

## 真实 GitHub CI 结果

[实际运行 44032032921](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44032032921)，对应候选补丁完全就位的提交 `7c4d991559d328709c94d3a1ce9f0d757f110f95`。

- `completed / success`，GitHub 标准 `ubuntu-24.04` 运行器和 Python 3.11。
- 正式命名的 R127 工作流从新独立分支实际启动，`Run authenticated original tests and explicit stage-two gates` **success**。
- 因当前触发分支不是 `refs/heads/main`，`Publish immutable run sidecar without changing historical receipt` 实际状态为 **skipped**。这是设计期望，绝不是该发布步骤已在 GitHub 实网成功的证据。
- 该候选校验步骤调用的是已归档的明确来源锁定 gate、60 项原 R127 测试、138 项严格字段核对与实际运行上下文。历史源身份、旧科研文件和冻结协议保持不变。
- 无直接 GitHub 生产推送；没有访问新的真实个人原始数据，也无 E2/E3 新预测评分。

## 生产部署前必须保留的准入限制

该候选 YAML 采用 `permissions: contents: write` 且仅在 `main` 运行发布步骤；如果未来获批合并，就会改变实际生产校验流程并**尝试**将新 run/attempt/job 命名的不可变侧车收据提交到 main。此事需要所有者**明确、独立批准**，而普通“继续”指令未包含生产准入批准。

现阶段尚未核实：

1. GitHub 真实 `contents: write`、分支保护及推送权限能否完成正式侧车写入。
2. 真实远端并发改动时的失败恢复及全自动重复触发行为。
3. 真实 GitHub job ID、尝试编号与外部证明身份如何进入长期证据档案。当前侧车将有数值 `run_id` 字符串和 `job_key`，`numeric_job_id=null`、`externally_attested=false`，不得宣称已独立认证 job ID。
4. 2026-10-24 第三方法原 CSV 漏写冻结 `exact_comparison_flag` 的历史协议格式偏差仍未得到正式科学裁定。

因此 PR 的正确状态为 `DRAFT_OWNER_PRODUCTION_APPROVAL_REQUIRED`。未经授权不能将此分支标记为 ready、合并或开放正式发布。若未来批准部署，先重新检查最新 main、冻结规范、GitHub 权限，再进行真正生产验证，且不得用成功 CI 自动升级科研等级。

## 本轮结论

**COMPLETE**：在独立 GitHub 分支精确应用旧候选补丁，三文件身份一致，真实同名工作流运行 success，来源校验步骤成功。

**NOT_RUN**：真实主分支 sidecar 发布、历史协议偏差正式追认、真人 E2 / 历史 E3、科学 P0 正式结题。

科研主线不变，R073、PESEN 及 R127 原科研收据与旧冻结协议未修改。费用：标准公有仓库免费 CI，没有新增付费服务或 API；账户账单本轮未核验。
