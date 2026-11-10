# PR11 原生重放输出别名保护扩展

track: Codex A engineering
run_date: 2026-11-10 Asia/Shanghai
base_pr_head: c1ee936c33aa9ca35d16b76fbe264b897f62c968
status: COMPLETE_BOUNDED_LOCAL_FIX；远端以本提交和回读为准
ci_status: NOT_DISPATCHED
billing_checked: 无付费API、依赖安装、资源/订阅购买或CI；免费额度未核实

## 精确问题范围

原runner已经检查日志/结果是否别名到登记的PINS输入或检查代码，这部分有效，正向保留控制在旧版也通过。问题是指向来源目录内**未登记文件**的日志链接仍被跟随，违反“只写输出/临时文件”的边界。

仅在临时副本中复制真实PINS文件，另创建人为来源说明文件（不是历史科研数据）。stdout/stderr symlink、stdout hardlink、execution.json alias和悬空stdout alias负例对旧版失败，发生说明文件覆盖/截断或新增来源目录文件。旧红测为18方法6失败（含DP结果别名），raw red.log保留。没有真实研究文件被变异，也不据此声称原数值结果或历史收据遭篡改。

## 修复与复用

保留旧protected-input/code别名检查。复用#4已审阅的lstat/nlink预检与同目录临时文件replace，直接使用现有targets列表，避免重复枚举漂移。新增检查在mkdir、旧成功撤销、原始输入字节身份检查及子进程之前。所有现有目标只允许单链接普通文件，拒绝symlink（含悬空）、hardlink和非普通文件。

日志/最终execution收据/DP_full_receipt.json统一原子发布。为保持#12原byte日志合同，临时流为wb：字符串仅UTF8编码，bytes不解码、不规范化、不改换行；相同helper用于本组3个独立runner，无跨PR运行导入。数学/状态/收据验证、原程序、数据、冻结协议都不改；剩余直接写只作用于私有临时负例文件。

不安全别名拒绝时保留原路径，可能留下旧COMPLETE内容；消费者必须检查本次退出码和新收据身份。安全普通文件覆盖/旧成功失效逻辑保持；输出父目录仍需稳定，并发用独立目录，建议新目录保存各轮证据。无父目录并发锁或永久日志保留保证。

## 实际验证

- 18项局部方法普通/-O各通过，共36次成功执行。包含旧oracle测试、5种别名、登记输入保护仍有效、完整原生重放及**整个副本来源树**字节保持。另含DP文件别名拒绝。
- 完整原生runner独立再执行exit0。S66原5条正例CLI、192尾概率/27报警及3种表示控制保持；DP_full_receipt.json也受保护，写出后与归档逐字节相等。
- 3份真实输入前后SHA256不变，Git blob与最后抓取main一致。实际argv/cwd、stdout/stderr、代码/来源哈希、输出清单和原完整收据见evidence/execution.json与replay-execution.json。
- 内部独立上下文审阅重跑全部两模式，无发现；确认全部11标签及DP文件/execution覆盖、原件保持及数学代码不变。不是外部科研团队复现。

```bash
python3 -B -m unittest discover -s research/codex_audit/r270_s66_native -v
python3 -B -O -m unittest discover -s research/codex_audit/r270_s66_native -v
python3 -B research/codex_audit/r270_s66_native/run_native.py . --output /tmp/new-pr11-safe-run
```

只使用新建/明确允许覆盖的稳定输出目录，不指向历史归档。优化模式覆盖局部测试/runner；历史子进程保留原调用参数，不宣称全部后代都-O。原完整模型单测、全仓库、Python3.11及CI本轮NOT_RUN。

## 交付边界

快进更新现有 https://github.com/edwardsage419/Psychohistory-Research/pull/11 ，分支codex/r270-s66-native-replay-20261029；核对原head后推送，不新建重复PR，不合并/关闭/强推。旧报告/日志/提交保留，新的源码身份由本增量Git提交及evidence绑定。来源只读，R073/PESEN、科学结论和验收不改；NONBLIND内部人工E1，新E2/E3/外部团队复现0。

这次只重跑受影响3个模块。PR14之前20候选/460执行矩阵属于其记录的旧固定heads，不把它追认到本次新代码；本组新局部证据单列。main实际采用仍需用户明确范围/顺序；CI费用未确认，不触发。
