# R275/S71：原生复算及优化模式错误接受修复候选

2026-11-12，Codex B；main `d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c`。
正式154队列12-005/P0，仍27 P0/82 P1/45 P2，不改正式队列或科研等级。
R277独立PR37交付后重新fetch main与检查开放R275 PR（0），选此具体未关闭的门。

## 发现与范围

旧S71 R报告及B远端addendum明确：原Node CLI NOT_RUN；归档Python B门与已运行开发副本
blob不同，故归档B对持久化完整文件的原生执行也NOT_RUN。本轮复用原算法补齐这两个门。
实际先取得最小RED：仅将人工结果JSON的evidence从E1_ARTIFICIAL_NONBLIND改E3，
原B普通模式exit1、stdout空；**同一输入加`-O`后exit0，输出3072行/status PASS**。
修复前stdout/stderr、argv及退出码保留[evidence/baseline.json](evidence/baseline.json)，
各文件SHA256见[evidence/baseline-hashes.json](evidence/baseline-hashes.json)。

根因：原校验器全部18条数学/资格检查依赖`assert`，Python优化模式删除这些检查。
正式复算进一步表明：重复、遗漏、错误来源概率、MAP标签、后验及证据升级6类坏输入
在原B普通模式均拒绝，在`-O`均错误接受。遗漏案例甚至输出source_rows=3071/status PASS。
这证明优化模式存在具体验证缺陷；**不声称原默认模式或历史数值错误**，也不推断有人曾以
该模式执行正式实验。原S71完全人工，历史真人影响不适用；R077影响仍UNKNOWN。

## 最小候选，不复制数学算法

[explicit-guards.patch](explicit-guards.patch)仅把原B的18条assert替为显式require，
不满足时raise ValueError；新增5行helper。原文件未修改，只在临时复制目录check/apply。
未新增另一份数学验证器；原Fraction/K计数oracle归原B作者。

AST审计从原源码构造期望树：原18个条件逐一保持，原duplicate消息保留；其余原AST完全
不变，helper也必须精确匹配。两种实际候选变异（1/16似然改1/15、证据条件改True）均被
PATCH_SCOPE门拒绝。此门证明补丁限定范围，不替代原数学算法的正确性证明。
所有18 guard的原行号和条件见[guard-inventory.json](guard-inventory.json)。

## 来源身份与真实输出

S71先冻结 `8c2964149055b7fa824bd9b10446ffd1e0613768`；
旧R/A/B产物提交 `1dc5efb14eeb2f4c140cd03205070c3c5a2a46ff`。
完整11来源（两源码、两产物、两协议、旧报告/验收、队列）见[pins.json](pins.json)。
运行前后均匹配实际字节及main固定对象。

| 对象 | Git blob | SHA256 |
| --- | --- | --- |
| 原B，3109字节 | 687aebf163193a4fb8f4667ec01774fcc047b2f4 | d6da1a90f84a81a5a0c1a9db252cdb4b977ffa47903a0929ed5281bc604a39ed |
| 补丁后B，3568字节 | 556848c45030e49b7d7610fcb062e2f759b9e18b | 27ee7c88b02f70fb989f1dddea23279f7dbd18996c75c73462792e3ceebcacf0 |
| 再生CSV，159435字节 | bceacf74de761188fe945518d8e5d7cff7d3339e | 71f25b29b294dc8827ba2803e80ae89c446550134d0009ea4ae7b7c5cef88fab |
| 再生JSON，2577字节 | 4d8900e0e91a7c9941fe6a2ac5a27a2cae57a1f1 | 632da3835df48660dac38d9e69d8e0679382f34d1de8b38f487ad51efc120532 |

原R Node `--emit`真实再生两份产物，均逐字节等于归档。完整3072行含480个零质量占位行，
无删样本。原B与候选B，两模式分别读取相同归档/再生快照：8次正向调用均完整PASS，
3072来源、4噪声值、36混淆格、4 MAP均值；还检查每行来源质量、标签、后验及K决策。
四平均正确率保持`23/24`、`4541/6144`、`79/128`、`1/3`，未作任何参数/噪声网格优化。

## 实际执行

现有Linux、Python3.12.14、Node24.22.1，仅标准库，无安装/API或新增费用。
从仓库根运行，输出目录必须尚不存在：

```sh
python3 -B research/codex_b/2026-11-12-r275-s71-native-guards/replay.py --output research/codex_b/2026-11-12-r275-s71-native-guards/evidence/native
```

exit0；36子命令/72原始流全部有argv/退出码/长度/SHA256，压缩包实际重新核验72流。
36包括Node版本1、git patch check/apply 2、原Node emit 1、8正向Python、24坏文件Python。
另有2次进程内AST变异拒绝；不是38项单测，也不重复原R275的100次历史单测。
Python实际使用隔离`-I -B`，优化调用额外加`-O`，不受PYTHONOPTIMIZE环境变量混淆。
详细机器证据：[evidence/native/summary.json](evidence/native/summary.json)、
[evidence/native/streams.tar.gz](evidence/native/streams.tar.gz)。

| 实际坏文件（复用旧6类） | 原B普通 | 原B -O（保留失败） | 候选普通及-O |
| --- | --- | --- | --- |
| 附加首行重复source | exit1 AssertionError | exit0/PASS，错误接受 | 各exit1，duplicate source |
| 删除末行source | exit1 AssertionError | exit0/PASS，错误接受 | 各exit1，complete_source_keys |
| 首行来源1/256→1/255 | exit1 AssertionError | exit0/PASS，错误接受 | 各exit1，source_probability |
| 首行MAP改FLIP_PAIR | exit1 AssertionError | exit0/PASS，错误接受 | 各exit1，MAP_and_correct |
| 首行IID后验1/17→1/18 | exit1 AssertionError | exit0/PASS，错误接受 | 各exit1，posterior |
| JSON evidence改E3，CSV字节不变 | exit1 AssertionError | exit0/PASS，错误接受 | 各exit1，evidence |

候选12次拒绝均stdout空、`ValueError: R275_S71:<guard>`匹配，无语法/导入错误替代。
原B 6次优化错误接受在摘要明确标RED，不计为成功拒绝。没有逐一为全部18条件另造负例；
未承诺任意schema/异常类型/恶意文件鲁棒性。此候选仅保持原校验条件在优化模式生效。

## 状态与交接

**COMPLETE有界候选**：原R/B实际字节的原生执行与两产物连接；确认6类-O错误接受；
独立最小补丁使同6类在普通/-O均拒绝；AST保证公式/条件保持。
**PARTIAL生产修复**：补丁未写入历史原文件、未绑定正式入口，交Codex A评审接入；
原B历史代码在-O下仍有已知失败。不得宣称生产缺陷已关闭。

原三模型、平滑/概率、先验、噪声网格、序列、平局顺序、数据/旧报告、原协议均不改。
原R275正式CLOSED_BOUNDED_E1及S71 E1_ARTIFICIAL_NONBLIND保持不变；正式154队列净关闭0。
新增真人E2/E3/外部团队复现0；跨版本/跨环境、完整科学重验与生产接入NOT_RUN。
R073/PESEN冻结。R077数据/许可/映射/真人评分授权阻塞交科学主线；无新探测或评分。

没有修改A目录；560现有workflow保守文字检查无匹配新增路径或无paths自动事件，
见evidence/workflow-check.json。额度未核实，不dispatch；提交skip ci。发布后另查
all-events实际运行，CI不以本地测试代替。未merge/force/升级科学等级。

下一优先：A审查并接入本B候选（生产修复尚未完成）；科学主线处理R077资格/协议决定。
B另选最新P0队列中真实未覆盖计算门，不重复本包6控制、R277数学及既有成熟证书。
