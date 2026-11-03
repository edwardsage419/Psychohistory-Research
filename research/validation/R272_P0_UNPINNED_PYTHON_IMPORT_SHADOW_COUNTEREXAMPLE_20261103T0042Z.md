# R272 P0：单入口候选的未固定 Python 导入路径反例

UTC 日期：2026-11-03。Track：R/B。审查起始 main：`0a90fc891b721142670edb43a1be2164d8259d48`。目标键：(R/B, R272, 2026-10-23 prescore freeze, candidate single-entrypoint Python import integrity)。状态：COMPLETE（有界合成反例）；PARTIAL（真实完整仓库及生产验收）；生产 P0 仍 OPEN。

## 一、固定证据

* 候选入口：`research/validation/r272_single_entrypoint_failclosed_20261102.py`，Git blob `f33e4e7e544560d65342a899606311d169e4d122`。
* 候选调用者：`research/validation/r272_single_entrypoint_caller_candidate_20261103.yml`，Git blob `a84b3d13d7d6bc8da45dc523454d7804520ca79c`。仍在 research/validation，未成为正式工作流。
* 生产工作流：`.github/workflows/r272-exact-train-test-oos-e1.yml`，Git blob `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`。原有 P0 风险未关闭。
* 冻结协议：`protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md`，Git blob `9fbdb0078a58c4a9c0a548643227e30da5731119`。
* original239 v7.8 crosswalk，Git blob `36f24235901172642c46853298aebb421f1a3552`；实际待核队列 Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`，154项：P0 27、P1 82、P2 45。正式净关闭0。
* 开放 Codex PR 检索：12项，#1、#3仍开放。没有改动任何 PR。

## 二、反例与实际执行

候选入口在校验任何文件前先执行 `import argparse, hashlib, io, json, ...`。普通 Python 脚本的所在目录可参与模块解析。候选的固定 `BLOBS` 集合和 ZIP SHA256 未覆盖额外的 `research/validation/json.py`。候选工作流的 `push` 和 `pull_request` 路径列表也未覆盖这一额外文件。

新增独立复现程序：`research/validation/r272_shadow_import_audit_20261103.py`，Git blob `bef93e291f1c298c880d37225f47b4bd0b6d2f95`。它只在临时目录写入与候选完全相同的导入前缀和一个合成 `json.py`。合成模块在被导入时打印 `FORGED_R272_PASS_FROM_UNPINNED_JSON_MODULE`，然后以退出码0提前结束。镜像入口在正常路径必然以17退出。没有更改真实仓库或科研数据。

本地执行：`/usr/bin/python3 -I -S /mnt/data/r272_shadow_import_audit_20261103.py`，CPython 3.13.5，Linux，标准库，无随机数。结果：

| 执行 | 观察 | 判定 |
| --- | --- | --- |
| 普通 Python 启动镜像入口 | 未进入验收，退出0，打印伪造成功标志 | 反例成立 |
| Python -O | 同上 | 反例成立 |
| Python -OO | 同上 | 反例成立 |
| Python -I -S | 镜像入口退出17，无伪造成功标志 | 正确拒绝 |

合计3/3个未隔离模式被提前成功退出，1/1个隔离控制拒绝。当前容器默认 Python 带有预加载 hook，故测试使用系统 `/usr/bin/python3` 的干净启动路径，并明确记录这一环境差异。

这是**基于真实候选导入语句的合成执行反例**。本轮未将候选完整原始文件放入临时目录执行，程序的可选 `--source` 参数保留了在真实检出中复测原文件的路径。也未运行真实 83 项测试、历史归档或 ZIP checker，未启动 CI。该反例证明候选存在导入路径信任假设，不能单凭当前单入口自测断言执行控制已完整封闭。它没有证明历史 CI 已经被攻击。

## 三、影响与修复验收

风险条件：如果不受身份约束的同目录模块或 `PYTHONPATH` 可影响候选解释器的模块解析，候选入口在第一项文件身份检查之前即可被改变执行流程。即使固定源文件及归档字节完全正确，仍可输出成功退出码。候选工作流当前仅列举特定 validation 文件路径，新增的模块可能不触发它；且仓库强制状态检查仍未形成已证实的生产保护。

建议修复先在可信环境验证 `python -I -S` 启动候选入口及其全部子进程的兼容性；清理 `PYTHONPATH` 等环境输入，固定完整运行时与被允许的导入依赖。必要时将 Python 源与所有辅助文件放在经审查的只读目录，避免同目录额外文件进入解释器路径。候选工作流应覆盖所有影响执行的源路径，维护者另行评估强制检查与冻结协议的三 job 要求。任何修复都须保留历史失败记录，重新运行本反例和完整原生验收，不可只让结构测试通过。

## 四、A 数据与其他科研边界

A 只读简查了 Drouvelis/Pearce 2025 Zenodo v1，`https://zenodo.org/records/15462528`。页面仍列有 `cleandata.dta`（MD5 `4cce04ea68b7a0492c242b206efebe53`），但 License 栏未给出可核实的具体许可；该来源已对应既有 R077，不登记为新独立实验。另见 Cason 等2026 Dryad 数据 `https://datadryad.org/dataset/doi:10.5061/dryad.mcvdnckd6`，本轮仅候选页面侦察，未核对真人配对、时间字段或 R073 适配。新合格数据集0；新E2/E3评分0。

B 证据等级：内部非盲、合成 E1 工程反例。未做真实模型预测、外部团队独立复现。R257 S53历史盲态失败、R333至R340复合验收问题维持开放。R073及PESEN v0.1继续冻结。模型分类、熔炼、产品开发未启动。

## 五、GitHub、费用及下一步

本轮仅新增本审计的复现程序和报告。脚本远端 blob 与本地 `git hash-object` 一致；提交及报告的最终远端身份以回读结果为准。Actions：NOT_RUN；账户账单与 Actions 免费额度：NOT_VERIFIED。没有新增付费调用、数据购买或 CI 调度。

下一步优先由独立审阅者在可信完整仓库以 `--source` 模式复验真实候选入口，再实施隔离启动与完整原生验收。修复必须先关闭导入路径反例，随后解决原有预像与正式工作流强制执行缺口。
