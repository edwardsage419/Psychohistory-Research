# R277/S73 原生运行与归档连接：有界补证

日期2026-11-12，Codex B。起点及执行时main：
`d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c`。
正式154项待核队列仍为27 P0/82 P1/45 P2，目标12-007/P0。
没有改队列或原R277的CLOSED_BOUNDED_E1状态。

## 问题与增量

原S73的R科学报告、B审计和20261029交接均保留“native Node CLI读取完整归档
CSV/JSON NOT_RUN”。旧V8内的六位积分/解析转移核/8类篡改证据已充分，予以复用。
开放PR30–36无S73原生工作；旧PR21曾阅读S73，但交付的是R279/S75。
本轮不重算R273，不复制既有数学证书，不改旧R/B程序。

**COMPLETE（有界）**：本机原生Node执行原R/B入口，两份产物逐字节再生，归档、再生、
重排行三组完整文件被原B CLI核验，8类实际坏文件均拒绝，12项固定来源前后不变。
**未发现新的数值错误**。新补的是原先NOT_RUN的运行和文件连接证据，不是新数学发现。

## 版本与来源

原R277冻结 `923a161bbdc012c138e53f1fa316e6085ff2704e`；
S73冻结 `53e3b18b28d46c0c5e26194dd8e85bc408450af6`。
完整12项路径、Git blob、字节数、SHA256见[pins.json](pins.json)。
每次运行先后检查实际字节身份，并与上述main固定Git对象逐字节比较。

| 固定对象 | Git blob | SHA256 |
| --- | --- | --- |
| 原R JS，5270字节 | 6d250fe671cba6307af7275ff4ef35648020f04f | 8b4a1a7f7805405c3bb0cbeaa63b79520e254438aec621d72aad8f648a955aab |
| 原B JS，3847字节 | b7ef1d4f185c60fefa2c76c31aa9910c7c5c3475 | 9cd89a6df40447e38a5697a51e21f960b6656d2961bae77882b9fc5b9e63d6e5 |
| CSV，2449字节 | 0ed6a96fcbdbd4b5d361e1db14fd8c90dd18a791 | 4e78fd4724011ee6e40f67907dde299fcbf6e3f868efddc2ea48e3529f74d463 |
| JSON，5349字节 | 2580b4dd7f7ab5e53e0cbdc4d47cde0f7a3e193a | d8d6e5626996afbe28aba630ad1222dc826738e7896946183a80a162a079e607 |

## 实际命令与结果

现有Linux、Python3.12.14、Node24.22.1；仅标准库，无安装、网络或收费调用。
从仓库根运行（输出目录必须尚不存在）：

```sh
python3 -B research/codex_b/2026-11-12-r277-s73-native-replay/replay.py --output research/codex_b/2026-11-12-r277-s73-native-replay/evidence/native
```

exit0。15个实际子命令，30份stdout/stderr流均有完整归档及哈希；不是15项单元测试。
本轮没有新增单测方法，也不重记原R277的100次历史单测。
主执行摘要见[evidence/native/summary.json](evidence/native/summary.json)，
原始流见[evidence/native/streams.tar.gz](evidence/native/streams.tar.gz)。
所有30份流的长度及SHA256已从压缩包重新核对。

原始JS按固定字节复制到临时目录；下列是命令结构，真实绝对argv及退出码均在summary：

| 实际入口 | 次数/结果 |
| --- | --- |
| `node --version` | 1次exit0 |
| `node R.js`、`node R.js --csv`、`node R.js --json` | 3次exit0；default完整文本匹配，CSV/JSON逐字节等于归档 |
| `node B.js archived.json archived.csv` | exit0，完整预定摘要及8控制标签相等 |
| `node B.js generated.json generated.csv` | exit0，同上 |
| `node B.js archived.json reversed.csv` | exit0，72行全部逆序仍通过（行键资格不依赖CSV顺序） |
| `node B.js bad.json bad.csv` | 下述8次均exit1、stdout空、领域错误匹配；语法/导入失败不算通过 |

原B各正向输出完整包含72概率格、27混淆格、9 TV格、72 CSV行；还实际核验24个MAP选择、
3宏正确率及原冻结/证据字段。核验方法归原B作者：独立解析转移核，不调用原R六位积分。
重现宏正确率A=`13/24`、B/C=`73/192`，反持续与持续TV为A=`1/2`、B/C=`0`。
这些均为旧结果复算，不声称新科学结论。

## 实际坏文件与拒绝

复用原B预定8控制，写为真正临时文件后单独启动原生CLI；改动及坏输入SHA256在summary。

| 坏输入 | 预期领域错误（均exit1） |
| --- | --- |
| B_ODD反持续000概率改0 | probability |
| A_ADJACENT IID→IID混淆概率改0 | confusion |
| B_ODD反持续/持续TV改1/8 | TV |
| evidence改E3 | evidence |
| 原冻结SHA改wrong | source identity |
| 删除C_EVEN | windows |
| 附加重复CSV行 | CSV coverage |
| 删除末行CSV | CSV coverage |

最后两项只证明当前控制在行数门被拒绝，不声称穷尽所有等行数替换或任意CSV模式攻击。
原R默认输出中的“2 mutation controls”实为复制字段的差异检查，并非独立校验器拒绝；
本轮不将其算作新增拒绝证据。有效拒绝证据来自原B的真实错误文件调用。
没有给原B补通用严格schema：它未承诺检查所有额外JSON键、protocol/method字段或额外CSV列；
本轮结论仅覆盖固定归档和列出的8控制，不外推为任意输入安全证明。

## 冻结边界、交接与未完成

S73冻结文本写“可运行标准库Python”，实际历史R/B报告明确归档Node标准库JS。
本轮只执行该归档实现，**不静默改协议、不将JS冒称Python、不宣称全部协议已满足**。
该语言差异如何处置留给ChatGPT/科研owner；原R277本体Python验收不受本轮改动。

保留所有旧文件，新增仅在本B专属目录；原模型、参数、先验、三个窗口、MAP平局顺序、
数据、结果、冻结协议、A目录均未修改。生产/正式执行入口接入交Codex A，NOT_RUN。
S73仍EXPLORATORY_E1_NONBLIND_INTERNAL；真人E2/E3新增0、外部团队复现0；
跨环境一致性与正式科学重验NOT_RUN。正式154队列净关闭0，不能由本补证追认科学验收。
R073/PESEN v0.1冻结。

R077：本轮另在PR31修正与PR30联合部署的来源固定依赖并已向A35评论交接；
该变化不重记数学验证。真人数据许可/原字节/评分授权仍未全部满足，26个session与
15个Session/26个sessionid映射交科学主线；1040事件、15场规则与历史票数不变。
不探测旧失败端点，不评分真人，历史影响UNKNOWN。

本轮CI NOT_RUN，额度未核验；未dispatch或使用收费资源。560份现有workflow静态文字检查
无覆盖新增目录的quoted glob或缺paths的自动事件；这是保守文本检查，不是账单/完整YAML证明。
提交及PR使用skip ci，发布后另查all-events实际运行；未merge、force或升级科学等级。

下一步：A可接收S73原生CLI证据；科学主线决定协议语言差异与外部验证。
B在最新队列再选未覆盖的P0实际计算门，不重复R277已有算法及R273/282/289/290/300证书。
