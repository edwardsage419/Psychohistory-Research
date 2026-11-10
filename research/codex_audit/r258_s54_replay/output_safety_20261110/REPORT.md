# PR5 R258 S54 输出别名覆盖修复

track: Codex A engineering
subflow: existing-PR replay output-write safety
run_date: 2026-11-10 Asia/Shanghai
base_pr5: ab9c45ebef3882c5caa7f9d105d6b4755ce6e1cc
status: COMPLETE_BOUNDED_LOCAL_FIX；远端交付以本提交及本轮回读为准
ci_status: NOT_DISPATCHED
billing_checked: 无新增费用、依赖安装、订阅、资源或 CI；免费额度 NOT_VERIFIED

## 根因与复用

刷新 main、18个开放 PR 与 #4 review（空）。#18 是 Codex B 的 R077精确Brier平局补充，与本包不同，已读取范围而不重复其数值核。本轮针对 #5 中与 #4 相同的 write_text 日志覆盖路径。

仅在临时副本中运行5类真实 CLI 回归：stdout symlink、stderr symlink、stdout hardlink、execution.json alias、dangling stdout symlink。旧版本12项总测试中新增5项全部失败，包含把副本归档收据截断为空；raw red.log 保留。没有对真实历史来源做变异，不推断历史收据曾被篡改。

直接复用 #4 已审阅的 lstat/nlink 预检与同目录临时文件/replace 写入函数，来源固定提交9ba7e2ad24a0936e7893e9721e1c806e29053286；仅将错误检查函数名 check 适配为 require，并为R258枚举本身8个运行标签。保持各PR独立可运行，不引入跨PR运行导入或新的通用框架。

全部16个 stdout/stderr 路径及 execution.json 在 mkdir、撤销旧成功收据和启动子进程之前预检。已有目标只允许单链接普通文件；symlink（含悬空）、hardlink和非普通文件拒绝。日志及最终收据均通过 atomic_output 发布，写前再检查。原有临时沙箱 emit 和刻意篡改副本的写入保留，没有改变数学比较或归档检查算法。

不安全别名拒绝时原路径保持，可能保留先前 COMPLETE 内容；消费者必须以本次退出码和新收据身份为准，不能把旧文件当作本次成功。安全普通输出的重用/旧成功失效行为保持。输出父目录仍需稳定，各并发运行用不同目录；此补丁不是全文件系统并发锁，也不保证重用目录永久保存历史日志。

## 实际验证

- 12项（原7+新5）普通与-O均通过，共24次成功执行；包括直接执行测试文件覆盖全部12项。没有使用提前退出的 unittest.main，只有底部入口。
- 原有正例真实执行 native82、R8、B7，共97项原程序测试；归档crossroute3456比较、27 world/initial覆盖和原负例检查保持。原生--emit仅在副本运行，3份生成文件字节一致；历史门忽略持久收据的已知边界仍披露，没有将其修复或科学升级。
- 最终完整replay exit0，9份输入前后SHA256相同，Git blobs与最后抓取main相同。原始命令、版本、code/source hashes、输出清单、完整replay收据在 evidence。
- 独立上下文内部审阅者重跑12项普通/-O，无重要或次要发现，确认8标签全覆盖、剩余直接写只作用于临时负例副本。

-O说明：测试和新增保护在优化解释器下验证；原runner内部子命令保留其原有-B启动选项，不宣称97个历史测试的所有进程都使用-O。本轮使用完整Git检出执行；原runner静态字段 full_repository_checkout=False 保持历史内容，未用它当作本机环境探测或成功条件。

```bash
python3 -B -m unittest discover -s research/codex_audit/r258_s54_replay -v
python3 -B -O research/codex_audit/r258_s54_replay/test_replay.py -v
python3 -B research/codex_audit/r258_s54_replay/run_audit.py . --output /tmp/new-r258-safe-audit
```

输出目录须新建或使用允许覆盖的安全普通文件；不要指向归档证据目录。完整来源hash和实际路径见evidence/execution.json，而非用此示例路径追认执行。

## 交付与剩余

本地专用分支 codex-a/r258-output-safety，目标普通快进更新现有 https://github.com/edwardsage419/Psychohistory-Research/pull/5 ，不新建重复PR，不合并/关闭/强推。保留旧报告、红绿日志和历史提交；本包仅改Codex自有runner/test并新增本日期证据，不改R/B原程序、冻结协议、原CSV/JSON、R073/PESEN或科研结论。远端同步须先核对#5 head未并发变化，实际commit/PR状态以最终回读为准。

NONBLIND_INTERNAL_ARTIFICIAL_E1；新E2/E3/外部团队复现0。输出安全不是预测有效性验证。全仓库/Python3.11/CI未运行，owner采用和科学验收仍开放。静态检查还看到#6/#7/#8的直接日志写入；未开展对应动态别名实验，不能把本次PASS推广到它们。#17在独立临时快照中使用固定#8代码，本轮未改变其依赖pin。
