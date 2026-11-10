# PR7 R248/S44 输出别名覆盖修复

track: Codex A engineering
subflow: existing-PR replay output-write safety
run_date: 2026-11-10 Asia/Shanghai
base_pr_head: dee83459afc1f558fbe97ad6d70518fc8da4f52b
status: COMPLETE_BOUNDED_LOCAL_FIX；远端状态以本提交及本轮回读为准
ci_status: NOT_DISPATCHED
billing_checked: 无新增付费API、资源、订阅、依赖安装或CI；免费额度NOT_VERIFIED

## 实际缺陷与修复

刷新main及18个开放PR，读取对应固定head源码。在独立目录/分支中，复制本runner的来源文件，仅对副本建立5种输出别名：首CLI stdout symlink、stderr symlink、stdout hardlink、execution.json alias及悬空stdout symlink。旧版新增5项均失败（总13项），实际副本收据被截断/覆盖或副本来源目录新增文件。raw red.log保留；未对真实科研来源变异，不推断历史收据曾被篡改。

复用#4已审阅的check_output_target/atomic_output，固定来源9ba7e2ad24a0936e7893e9721e1c806e29053286；将内部检查函数名check适配为require，按本runner的7个运行标签枚举全部stdout/stderr及execution.json。保持独立可运行，没有新增跨PR运行依赖或通用框架。

预检在mkdir、旧成功撤销和子进程之前，拒绝符号链接（含悬空）、多链接文件及非普通文件。写入前再次检查，以同目录临时文件原子替换日志/结果；剩余直接write_text仅用于新建私有临时沙箱内的故意负例。数值与收据判断代码不改，原报告/旧日志保留。

不安全别名拒绝优先保护来源，可能保留以前的COMPLETE内容，消费者必须检查本次退出码和新收据身份；安全普通文件重用与旧成功失效行为保持。仍要求稳定输出父目录、不同并发运行使用不同输出目录，建议每轮新目录保留历史日志；不声称提供父目录并发锁。

## 真实验证

- 13个方法（原8+新5），普通与-O各通过，共26次成功执行；直接执行测试文件也包含全部方法，只有底部一个unittest.main。
- 最终独立完整replay exit0。3条正例归档CLI成功，486项完整收据比较通过；旧B对截断/重复收据的2类假阳性仍如实重现，新覆盖门均拒绝；错误distance的2条负例CLI拒绝。没有修改旧B算法或历史科学验收。
- 6份来源前后SHA256相同，Git blob与最后抓取main一致；code/source hash、实际命令、输出清单和完整原重放收据见evidence/execution.json与replay-execution.json。
- 独立上下文内部审阅者重跑两模式全部测试，无发现；确认7标签全覆盖、原件只读与完整来源树字节保持。这不是外部科研复现。

```bash
python3 -B -m unittest discover -s research/codex_audit/r248_s44_replay -v
python3 -B -O research/codex_audit/r248_s44_replay/test_replay.py -v
python3 -B research/codex_audit/r248_s44_replay/run_audit.py . --output /tmp/new-r248-safe-output
```

示例输出须为新目录或明确允许覆盖的安全普通文件，不指向历史归档目录。外层测试/新增保护使用-O；原历史子进程仍保留原启动选项，不声称所有后代均优化。全仓库/原模型完整单测、Python3.11、CI本轮NOT_RUN。

## 交付与科学边界

普通快进更新现有 https://github.com/edwardsage419/Psychohistory-Research/pull/7 ，目标分支codex/r248-s44-replay-20261029；推送前核对固定head，若并发变化则停止受影响操作。只改Codex自有runner/test并新增本日期证据，不新建重复PR，不合并/关闭/强推。未改R/B原程序、原始数据、冻结协议、科研结论、R073或PESEN。

NONBLIND_INTERNAL_ARTIFICIAL_E1；新E2/E3/外部团队复现0。文件写入保护不验证预测有效性，科学验收不升级。剩余为owner/reviewer采用决定；#8同类直接日志写入尚需独立动态复现，#17的固定依赖pin本轮不改。
