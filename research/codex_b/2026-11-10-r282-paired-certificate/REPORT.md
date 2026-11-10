# R282 S78：同源配对计数的 GF(2) 补充门

2026-11-10，Codex B。**原 B 门会接受错误或缺失的配对差异计数；新增独立秩证书
补齐四个持久化整数的验证。** 归档的32/48计数及分类结果本身正确，未发现原模拟
数值错误。本包不改变历史科学结论或冻结规则，也不将新算法冒充原作者算法。

## 实际缺口及复现

`original_R282_paired_counts` 表示两个顺序日程相对 SYNC，在同一个六位来源下，
t1/t2联合状态不同的来源数。正确值为两日程各 `[32,48]`。它与“不同日程的未配对
状态分布相同”是不同的计算对象；把计数写为零会错误表示同源轨迹没有差异。

旧 `b_r282_s78_strict_remote_receipt_gate_20261030.js` 精确核对192行逆转移、
观察投影及四组分类摘要/36TV，确实提供有效保护，但未读取上述配对字段和根部
`schedules` 声明。实际 native Node CLI 对以下8种有效JSON坏输入均 exit0，输出
与好文件相同的192rows/4regimes/36TV摘要：配对全零、缺失根字段、单值999、计数
布尔false、t1/t2互换、缺失一个日程、日程声明倒序、重复配对JSON键（后值为零）。
两个控制——错误CSV转移、错误TV——旧门正确拒绝。不是笼统声称旧门无效。

最小反例只改 JSON：

```json
"original_R282_paired_counts": {"A_THEN_B": [0,0], "B_THEN_A": [0,0]}
```

完整反例可由 `test_certificate.py:bad_cases()` 重建；实际旧/新CLI输出、输入SHA和
退出码归档于两模式 `commands.json` / `summary.json`。新门10/10拒绝，含原先8个
漏检和2个正确拒绝控制。每种字段/类型控制的结果分别保存，没有将语法错误当拒绝。

## 独立算法及配对绑定

冻结原始变量按顺序 `a0,b0,eA0,eB0,eA1,eB1`，每个在GF(2)上独立均匀。
源码 `algebra.py` 用整数mask编码线性形式，mask bit0对应**第一个变量**，不是
source_index二进制的最低有效位。用冻结机制构造一步2×4系数矩阵，再符号代入两次。
它不导入原模拟器、逆映射、CSV或旧计数，不枚举来源来推导配对数量。

| 日程 | t1系数masks | t2系数masks | 相对SYNC的t1/t2差分秩 |
| --- | --- | --- | --- |
| SYNC | (6,9) | (25,38) | — |
| A_THEN_B | (6,14) | (30,62) | 1 / 2 |
| B_THEN_A | (13,9) | (61,45) | 1 / 2 |

差分矩阵分别为 `[0,7]`、`[7,24]`、`[11,0]`、`[36,11]`。
Gaussian elimination在GF(2)上精确求秩r。由秩—零化度定理，6维输入中使两输出
完全相同的核有 `2^(6-r)` 个向量，故不同数为 `64-2^(6-r)`，即32、48、32、48。
没有浮点、epsilon、数值拟合或测试集后调参数。

新 `audit.py` 读取CSV、JSON、旧B代码各一次，严格JSON重复键/非有限值/根字段
检查，绑定日程声明和四个计数的完整形状及精确int类型（不接受bool）。同时：

1. 将相同捕获字节传入固定原B代码的临时副本，保留既有独立逆转移/观察摘要核验。
2. 核对192条轨迹的符号线性形式，t1/t2共768输出bit比较；t0也匹配固定输入。
3. 在CSV按 `(schedule,source_index)` 唯一身份建立配对，核对完整3×64身份集，
   实数四个同源差异计数；与无枚举秩证书、JSON声明三方完全一致。

同源对照分母是64，S78带日程标签案例质量是1/192，二者未混用。补充只认证S78
持久化的相对SYNC四个整数；原协议其他配对命题/全部科学验收不由此自动完成。
旧B的原算法信用保留，新GF(2)算法明确标为本包独立补充。

## 真正执行的命令与数量

运行环境为已有 Linux / Python3.12.14 / Nodev24.22.1，标准库，无安装依赖。
仓库根目录执行（输出目录必须新建）：

```bash
python -B research/codex_b/2026-11-10-r282-paired-certificate/replay.py --output research/codex_b/2026-11-10-r282-paired-certificate/evidence/normal
python -O -B research/codex_b/2026-11-10-r282-paired-certificate/replay.py --output research/codex_b/2026-11-10-r282-paired-certificate/evidence/optimized
```

两模式均exit0，新增 **12个unittest方法/模式，共24次正向方法执行**。
每模式另10个坏输入全部exit2结构化REJECTED；旧门8个falseaccept/2个正确拒绝。
故意把新rank函数截为至多1，`test_exact_count_formula`产生1个断言失败exit1，
没有导入/语法错误。此控制与正常12项分开计数。TDD原始RED为22个断言失败、1个
KeyError（12方法及子例），GREEN通过，日志均保留；不改写历史失败。

归档R S78脚本真实原生Node CLI在临时目录执行，两个输出逐字节等于归档：

| 输出 | 字节 | SHA256 |
| --- | ---: | --- |
| 完整CSV | 12480 | 910875ab4ac50873819b67b76702999c386a2411c9f1eea2b25d8bdba4fc5e43 |
| 完整JSON | 5789 | ff12fbed817500fffd48036084d3adfe78bfdb13d8e51da9b3e06b07b42c7668 |

旧B strict CLI、旧独立inverse CLI对归档及再生成文件均实际运行通过；新门对两套
输入生成相同完整证书。代码/输入/两冻结/ODD共13份指纹前后一致；固定版本见
`pins.json`和两模式 `summary.json`。主要Git blobs：

- 原R S78 JS：`c3d3bbfd8a60241eaf04e08de547a17979b6fb5e`
- 原B inverse JS：`6d406b2596456cee10e50da77d2b387cbb87c1f1`
- 原B gate JS：`b5fbbe829512f5d9d1790f55947773d23acec9e3`
- CSV：`2ee948c77f68a89fbd6f02a35fba1f3648f24957`
- JSON：`b44b423fbb2c8251b326bcfabdba52798547e437`

原始argv/cwd/退出码、非空stdout/stderr字节、每条流SHA256均归档；空流以0字节
和哈希记录。临时目录删除是设计行为，重放会再创建，不依赖残留临时文件。

## 协作、冻结与未验证范围

初始main `b3b3b9a1`；复算后main新至 `558ef502ed2e06e76bb35bffdde785075b04f71e`，
仅新增Tolbert–Zucker理论文档。独立未发布分支将保留该主线增量；代码输入指纹另查。
初读21个开放PR，A10/11/12新增输出别名保护与本配对门无重叠，A14整合工作不碰。
R280时间隔离已有充分保护，R281同分冻结失败已登记，均不重复处理。
读取原R282协议/ODD、S78冻结、R/B报告/补充/交接/E112；参考指纹在context manifest。
范围快照不是原子任务锁，也不宣称能排除隐藏工作。只新增Codex B本目录。

人工、非盲态E1；区分归档程序原样复算、新独立GF(2)核验及故意篡改验证。
新真人评分、独立真实数据预测、E2/E3、外部团队复现均0。R073/PESEN v0.1、模型、
参数、划分、指标、原代码/数据/历史结论均不变，154项待核正式净关闭0。
原R282完整测试/第三CI job、全仓库、其他平台、真实历史时序、生产接入及科学
重新验收均NOT_RUN；新门未绑定原生产调用。固定正常文件环境有证据，不承诺
敌对并发写入/运行时安全；需全新、稳定输出目录。字节一致不等于外部有效性。
无付费API、资源购买、依赖安装、workflow dispatch或自动合并，账单/免费CI额度
NOT_VERIFIED；Actions状态发布后单列，0条记录不计为测试通过。
审查及PR/main最终状态见PROGRESS.md、HANDOFF.md。
