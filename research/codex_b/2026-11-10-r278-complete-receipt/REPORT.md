# R278 S74 完整收据字段、类型与条件协方差验证

2026-11-10。初始main `e5f2baa7f6b13b1a2bf95f48ed49571f732e7611`；
发布前同步main `0d086e5565d93438e67e45b2901b5adc35841412`（仅新增一份理论文档）；
独立分支 `codex-b/r278-s74-complete-receipt-20261110`。
范围：补全持久化机器检查，复用既有B数值路线，保留所有历史程序/协议/收据。

## 实际缺口与反例

原B CLI对15个期望风险和960条来源做了有效检查，但没有覆盖整份JSON。
对真实归档的**人工E1**收据复制件，下列9种错误仍使旧门返回PASS：

1. 删除全部 `conditional_forecasts`；
2. K=2的 `joint_predictive_covariance` 改成字符串999；
3. 主要 `BMA_joint_minus_product` 差值改为999（改变比较结论）；
4. R073声明改为MODIFIED；
5. 数值计数 `new_E2_predictions=0` 改为boolFalse；
6. 已检查的风险出现两个同名JSON键：先999、后正确值；
7. 条件协方差改为非标准NaN JSON常量；
8. CSV增加同名 `source_probability` 列，首列999被后一个正确列覆盖；
9. CSV一行多出一个999单元格，被DictReader忽略。

第10项控制改错一个世界风险，旧门正确拒绝，说明不是所有校验都失效。
第11项为CSV质量字段1/0，旧数值检查也拒绝；本次审查后补齐新CLI的
结构化异常输出，避免ZeroDivisionError直接抛traceback。
新门对以上11项均明确拒绝，exit2；旧门9个PASS、2个非零退出。
完整真实argv/cwd/退出码、stdout/stderr和变异SHA在 `evidence/review-final-*`。
这些变异发生在临时副本，原文件没有变化。

这是**持久化程序覆盖边界**；原B报告曾手工逐项核过3个比较差，本包不
否认历史手工计算。也没有发现原15风险或原条件协方差的数值错误。
“旧门PASS”只支持其已检查的范围，不能自动验收被省略/篡改的冻结字段。

## 最小补充与数学路线

`complete_receipt.py` 的完整期望由固定协议产生，不接受调用者提供“答案”：

- 复用原B `analytic()` 的五个二项计数K及四类预期平方损失，避免重写已有
  15风险和960原子核验；原B代码在编译执行前固定Git blob，并执行同一份字节。
- 新条件路线用低/高Bernoulli似然求后验w，逐四类计算联合混合和边缘乘积。
  预测协方差由全协方差公式 `w(1-w)(3/4-1/4)^2` 独立导出，而非导入R脚本。
  K=2时w=qbar=1/2，联合分布为(5,3,3,5)/16，乘积分布各1/4，协方差1/16。
- 固定完整21个根字段，比较全部**140个叶字段**（含73个精确分数值），
  三组记录按唯一(p,policy)、p、K标识建索引，允许记录顺序变化，拒绝遗漏/
  重复身份、缺失/多余字段。分数必须是有限整数/有理数字符串；2/4与1/2
  数值等价可接受，float/bool冒充数字计数则拒绝。
- JSON解析在任何计算前拒绝重复键、NaN/Infinity；CSV严格检查13字段表头、
  960数据行和每行13格。数值来源核验仍交给原B程序。
- CSV/JSON各读取一次，保存到独立临时字节快照，让新旧数学检查看到相同
  内容；不回写输入，也不靠再次读取外部文件来认定快照SHA。

元数据/历史声明（例如`mutation_cases_rejected`、旧边缘风险不变等）仅验证
字段、类型和值与固定档案约定一致，**不因此证明所有历史事件重新发生**。
本轮重跑的负例是上述10项，不冒充重跑了历史全部实验或完成科学验收。

## 归档程序原样执行与字节身份

在隔离目录实际执行原Node CLI，之后原B和新门分别检查真实归档及再生成
文件，每模式共5个正向CLI调用。Node v24.22.1产生：

| 输出 | 字节数 | SHA256 | 对归档 |
|---|---:|---|---|
| CSV | 68025 | `1903f31991dfac80ae3f07cd5839ec26015414246b65900c6700a3b1779f74a7` | 字节全等 |
| JSON | 4851 | `64c03afd576bc8cd1f95b9f5eac20de128c02dacec147fdde325da2ecd6f0a45` | 字节全等 |

Node机器收据stdout与实际生成的机器JSON一致，两个SHA均独立重算相等；
该新生成机器收据单独保存在 `native-generated-receipt.json`。未复制整份CSV
到本PR；代码和命令可在临时目录再生它。原R/B报告保留的原生CLI NOT_RUN
历史不倒写，本次为这个固定版本新增真实原生执行证据。

源版本（完整SHA256与字节数另见summary）：

- 原Node Git blob `4fc696cd690a182968dfa0e930933025982286ab`；
- 原B Git blob `f1ba4dcb2e80a612f14b3d7c10896c1d6fccfa62`；
- 原CSV Git blob `494c688596cda6186fb6f0e1c588584009659934`；
- 原JSON Git blob `1d9963435f044b72b69704e64e7ba8fe1609a021`。

8份代码/数据/冻结协议指纹在两次最终重放前后一致，历史文件另外与HEAD
Git树独立匹配。R278原核心研究、历史S74协议和所有主线收据保持原样。

## 实跑命令和计数

仓库根目录实际执行最终版本：

```bash
python -B -m unittest discover -s research/codex_b/2026-11-10-r278-complete-receipt -p 'test_complete_receipt.py' -v
python -B research/codex_b/2026-11-10-r278-complete-receipt/replay.py --output research/codex_b/2026-11-10-r278-complete-receipt/evidence/review-final-normal
python -O -B research/codex_b/2026-11-10-r278-complete-receipt/replay.py --output research/codex_b/2026-11-10-r278-complete-receipt/evidence/review-final-optimized
```

Python3.12.14标准库，未安装依赖。**14个正向测试方法普通/-O各通过，合计
28次最终执行、零失败/错误**。11个实际CLI拒绝案例单独计数，不当作22个
额外unittest。140个内部字段比较也不称为140个单元测试。
初版 `red.log` 12方法9失败/3错误，`green.log` 12通过；CSV歧义回归
`csv-shape-red.log` 13方法1失败，随后 `csv-shape-green.log` 13通过。
审查指出零分母拒绝虽非零退出，却缺结构化JSON；`review-red.log` 14方法1失败，
仅补CLI捕获ZeroDivisionError后 `review-green.log` 14通过，再完整重放两模式。
初版 `normal/optimized`、`final-*` 保存，最终以 `review-final-*` 为准。

原B第37行无with的CSV读取在unittest环境出现 **ResourceWarning**；真实
警告已保留于stderr和summary，未将警告抹除或声称输出无警告。本轮未改
历史B文件句柄实现；这不影响已执行的数值/类型拒绝结果。
重放目录必须全新，拒绝复用旧输出；全部检查完成前不产生成功summary。

## 证据分类与仍未验证的边界

原R Node为**归档程序原样复算**；原B为**既有内部独立二项解析路线重新执行**；
新条件似然/全协方差为**内部解析验证补充**；完整字段和坏输入拒绝为
**程序验证**。三真率×64六bit来源按5政策重复使用，不是960次独立实验。
均为人工非盲态E1，独立真实数据预测、新真人E2/E3、外部团队复现均0。

本轮只处理R278 S74完整收据，不重复A轨PR整合/来源认证和B的R073–R077
工作。初始18个开放PR及主线已读；未提交的聊天活动不可观测。队列154项
（P0=27/P1=82/P2=45），正式净关闭0。
原R278核心测试、全仓库测试、生产/CI调用采用、真人来源/参数评分、历史
科学重新验收、其他运行平台均 **NOT_RUN**。Actions **NOT_RUN**，无付费API、
购买资源、依赖安装或workflow dispatch；账单/免费CI额度 **NOT_VERIFIED**。
R073/PESEN冻结不变，原研究结论和负结果不改。

独立上下文审查无Critical/Important问题，一项结构化异常Minor已按上述回归
修复。审查者重跑两模式，独立六bit枚举核对15风险/3差值，140个叶字段逐一
篡改均拒绝，核对两份原生输出字节/摘要以及8份输入指纹；元数据不升级科学
证据的边界保持。审查后没有第二轮重复审查，依靠失败回归与完整重放验证修复。
审查与交付记录见 `PROGRESS.md`。仅新增本Codex B目录，通过独立draft PR
交付，使用 `[skip ci]`，不自动合并。已创建独立
[Draft PR #19](https://github.com/edwardsage419/Psychohistory-Research/pull/19)，
最终head及远端状态见交付消息。
