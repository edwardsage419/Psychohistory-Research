# PR4 R256 S52 输出别名覆盖修复

track: Codex A engineering
subflow: existing-PR output-write safety
run_date: 2026-11-10 Asia/Shanghai
base_pr4: 039e7d262eaa3d9b20f1a279a61055aab08d4746
last_fetched_main: e5f2baa7f6b13b1a2bf95f48ed49571f732e7611
status: COMPLETE_LOCAL_FIX / REMOTE_SYNC_BLOCKED
ci_status: NOT_DISPATCHED；当前在线 CI 无法读取
billing_checked: 无付费 API、资源、订阅、依赖安装或 CI；免费额度未核实

## 根因与实际复现

开始时刷新 main、17 个开放 PR，并读取 #14/#15/#17 的 review API，均为空，没有待处理的新审阅反馈。沿实际使用边界检查 #4，发现 run() 使用 write_text 写已有 stdout/stderr 路径；文件若为符号链接或硬链接，会跟随别名截断/覆盖目标。仅使用临时来源副本进行五类回归：stdout symlink、stderr symlink、stdout hardlink、execution.json alias、dangling stdout symlink。旧版本7项总测试中5项失败；证据 red.log 保留。stdout 别名把副本收据截断为0字节；没有对真实仓库来源做变异，也不暗示历史科研收据已被篡改。

## 修复

只修改原 Codex 自有 run_audit.py 与 test_replay_safety.py：

1. 列出全部固定日志及结果名，使用 lstat 在 mkdir、旧成功收据撤销、任何子进程之前预检。已有目标必须为单链接普通文件；symlink（含悬空）、多链接文件及其他类型拒绝并返回非零，原别名不移除。
2. 日志、python_expected.json 和最终 execution.json 统一用同目录临时文件写入后原子替换。写入前再次检查目标；替换本身不跟随目标文件 symlink，避免直接截断别名目标。
3. 保留安全的普通输出文件覆盖及旧成功收据失效逻辑。**不安全别名拒绝时以保护输入为先，可能保留先前已有的 COMPLETE 内容；调用者必须检查本次退出码和新收据身份，不能读取旧文件冒充本次成功。**
4. 不提供输出父目录并发修改锁，仍要求各并发运行使用独立且稳定的输出目录；原有普通输出重用会替换先前日志，应优先新目录保存历史证据。本补丁不是全文件系统并发安全保证。

没有修改任何 R/B 科研程序、冻结协议、原始 CSV/JSON、历史科学结论、R073 或 PESEN。原 PR4 报告、日志和初始提交保留，新增此日期补充，不重写旧证据。

## 测试与独立审阅

- 7 个方法（原2+新5）普通及 -O 均通过，14次成功执行，不是14个科研命题。
- 正例仍真正运行原82项原生 unittest、4条归档 Node CLI、两条 clean sandbox 控制、两条负例 CLI、独立 Python精确风险比较；source tree/bytes 不变。
- 审阅者独立重跑 discovery 两模式全部7项，未发现生产保护问题；发现测试文件较早的 unittest.main() 会在直接执行时仅跑原2项。已实际复现 exit0/只跑2项（direct-entrypoint-red.log），移除提前入口，底部只保留一个入口；最终直接执行普通/-O 都跑7项并通过。
- 最终真实完整 replay exit0。七份历史输入前后 SHA256 相等，Git blob 与最后抓取的 main 全相同。code hash、source hash、版本、实际命令、子进程退出码、输出清单与 replay receipt 见 evidence。未把原生子进程都宣称为 -O：固定 runner 的历史子命令保留原启动选项。

命令（仓库根）：

```bash
python3 -B -m unittest discover -s research/codex_audit/r256_s52_replay -v
python3 -B -O -m unittest discover -s research/codex_audit/r256_s52_replay -v
python3 -B research/codex_audit/r256_s52_replay/test_replay_safety.py -v
python3 -B -O research/codex_audit/r256_s52_replay/test_replay_safety.py -v
# 选择新的、稳定且不含预置别名的输出目录：
python3 -B research/codex_audit/r256_s52_replay/run_audit.py . --output /tmp/new-r256-safe-audit
```

## 交付与阻塞

本地专用分支 codex-a/r256-output-safety 从原 #4 head 建立，目标是普通快进更新现有 #4，保留 PR，不新增重复 PR，不合并/关闭。远端目标分支最后已知为 codex/r256-s52-cli-replay-20261029。

同步前 Git read 开始返回 `could not read Username for 'https://github.com': No such device or address`；独立 GitHub REST branch/PR read 同时返回 HTTP401 `Bad credentials`。环境状态 observations_current=true/network enforced/failure=null，进程 GH_TOKEN PRESENT、GITHUB_TOKEN ABSENT（只检查存在性，没有打印值）。说明现有 API 认证被拒绝；不能因变量存在就声称凭据有效，也不能由此确定过期原因。已停止受影响远端操作，未尝试 push、索取聊天令牌、提取代理凭据或更改凭据配置。

需在连接/环境设置恢复 GitHub 授权后，先重新读取 main 和 #4 当前 head。只有确认没有并发改动，才能快进同步本地增量。当前未声称远端 PR 已包含此修复，现有 #4 的实时合并/CI状态也无法重验。

工程边界：NONBLIND_INTERNAL_ARTIFICIAL_E1；新E2/E3/外部团队复现均0。此修复保护重放输出写入，不提升数学结论或预测有效性。Python3.11/全仓库测试未运行；没有 CI dispatch。剩余是认证恢复和远端交付，不再扩写同一审计报告替代同步。
