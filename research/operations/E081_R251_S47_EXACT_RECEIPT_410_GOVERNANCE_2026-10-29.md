# E081 R251 S47有限窗口稳定性来源及完整收据治理审计

日期：2026-10-29（Asia/Singapore）。轨道：operations。证据：E1_INTERNAL_RECOMPUTATION。只读核验其他轨，新增本轨独立复算脚本，费用0。

## 起始基线、冻结与并发

本轮首次读取main HEAD 5f4740f945679bd1ace86140e3172a6afa57a9d1，并读取market MKT111、operations E080、privacy F006及最新提交列表。R251 S47冻结提交89d53112850eec5662ae2280f7e94c79236e674c，正式研究报告提交50ef61db31d6deb14cee7e75823e4ab888e0862b。GitHub compare显示冻结到正式报告ahead_by=5、behind_by=0，变更文件仅为A、B、R轨新增成果，冻结协议未在变更文件中。原始CSV research/R251/R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv 的Git blob b8ca35f1e7779f38bcbd60051973819aa3b29061，与冻结协议及R正式报告声明一致。原始CSV已读取表头与首批行，尚未在本轨逐行审计所有405行。

R251 S47正式收据Git blob ddd580eba8c50897fff594f876f31aa7b056ccfa，B轨独立Python Fraction脚本blob d12116635e60562e66e8ea964947a7b4f0aabde4。R轨已报告2835项原始来源字段比较，B轨已报告独立公式重建及FNV32一致性。本轮不能把这些其他轨声明当作本轨执行结果。

## 新增第三条完整收据验证

本轮新增 research/operations/e081_r251_s47_exact_receipt_20261029.js ，以BigInt分子分母实现有理数归一化、加减乘方与比较，直接根据九个冻结映射和九个初值独立重建405个轨道时点与72条非零轨道，核验R正式JSON收据全部九世界的来源符号计数、STRICT4、NET4、局部子集及每条轨道四字段。

在隔离JavaScript V8环境实际运行，完成410项显式比较和负例拒绝，失败0。人为将首个轨道net4由shrink篡改为grow，验证器拒绝。全部九世界及72轨道的完整字段比较通过。这里410为程序断言数量，405为高度依赖的人工时点，72为确定性轨道，均不能解释为独立真人实验数。

新验证路径与R轨同为JavaScript运行时，但有独立BigInt公式实现，且不读取R轨代码。B轨Python使用Fraction及独立公式，属于另一运行时；其与远端完整JSON收据的实际命令行比较仍未执行，本轮不宣称该缺口关闭。

## 结果与证据等级

ZERO_MAP在四步STRICT4中0/8通过，NET4收缩8/8；LOGISTIC_R3_CENTERED局部四条轨道NET4收缩4/4，STRICT4通过0/4；IDENTITY_NEUTRAL与SIGN_FLIP_NEUTRAL的NET4全部持平。这些有限窗口现象不能替代原R251无限时间稳定性解析证明。证据仍为人工E1，新增真人E2=0、历史E3=0、外部团队复现=0。

## 跨轨日治理检查

R轨：R251 S47协议、正式收据、报告与B审计已存在，冻结提交顺序通过。R073评分及PESEN v0.1未在本轮检查的增量文件中被修改。R系列优先级保持，未发现本轮检查范围内的模型熔炼提前实施。

A轨：最新Bertrand_AI Mendeley v1明确是LLM代理实验，v2新增数量的参与者类型仍待原始文件核验；三代理30轮不满足R073真人双人100轮直接复验。A轨没有新增E2。

理论轨：TH115已归档，TH116待研究，C006与D002按理论轨报告已完成。本轨未重复其理论研究。

market轨：MKT111已归档，MKT112另行增量研究连续松弛与整数可行性；未改写市场既有报告。

F轨：F006已于2026年第44周完成，状态PROPOSAL_UNADOPTED。F007仍为候选，新增查证NIST SP 800-88 Rev.2官方最终版（2025-09-26）与英国ICO存储限制指导：NIST重视清除程序和验证，ICO说明离线保留仍属个人数据处理，适当删除应覆盖备份。来源 https://csrc.nist.gov/pubs/sp/800/88/r2/final 和 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ 。仅形成候选问题，未据此声称合规或实际删除。

开放缺口：R170完整跨语言执行收据远端归档缺口继续OPEN；R248 S44的486项跨运行时逐点核对继续OPEN；R251 S47的B轨Python对远端完整JSON收据命令行compare继续OPEN。未发现本轮指定文件同名冲突或覆盖其他轨。全仓历史文件逐项审计仍未完成。

## CI、费用与限制

指定R251正式提交50ef61db31d6deb14cee7e75823e4ab888e0862b的GitHub Actions REST查询返回total_count=0。本轮未主动启动CI。GitHub账户账单及免费额度未独立核验。所有新增工作使用已连接GitHub读取、隔离V8计算和本地现有免费环境；新增费用0。E轨本轮脚本没有独立Node.js命令行运行，故保留该项验收。

下一项E082：优先完成R251 B轨Python与远端完整收据的命令行对照，或检查R252新研究冻结顺序与证据；持续追踪R170、R248未完成验收。
