# B轨：R290 S86 非盲态独立二项分布与完整训练来源审计

日期2026-10-30 UTC。目标键 (B,R290,S86-freeze-90998f55,binomial-heldout-risk-and-training-ledger-integrity)。状态：COMPLETE（本轮明确限定的内部非盲态程序性审计），S86整体科学验收PARTIAL，外部团队复现NOT_RUN。

## 事前冻结、读取范围和独立性

事前冻结提交90998f553dcc2697fdbf61a6355b9b4ffc3e5e95。已读R290原始条件分布和风险定义、S86事前冻结、R路线代码、远端24结果及1950来源收据。B脚本由同一执行主体在看过R计算目标与结果后编写，因此明确非盲态；独立性仅指数学方法与程序实现，绝非外部团队或全新数据的独立复现。

## 两条互补B审计路线

1. 独立二项分布路线：对每个证据格x，只需知道噪声训练计数Kn~Bin(m,pn[x])及信号训练计数Ks~Bin(m,ps[x])。两类计数独立，枚举(m+1)^2种计数对，按冻结的加一平滑和严格大于规则计算该格预测为信号的概率，再乘真实独立留出误报/漏报权重。五格求和得到每世界的期望风险。此方法不调用R路线，也不枚举完整有序训练序列。24个世界与m组合逐Fraction相等。
2. 独立来源严格检查：读取持久化1950行CSV，验证五列模式、三DGP、m=1/2、序列长度和字母表、(DGP,m,噪声序列,信号序列)唯一性、逐行概率等于两类条件概率乘积、完整5^(2m)笛卡尔覆盖、每DGP和m总概率恰好1。三DGP各25+625行，共1950行全部通过。

## 实际运行和负例

本地Python 3.13.5运行：

* python r290_s86_finite_likelihood.py --test：4项unittest PASS。
* python r290_s86_finite_likelihood.py --emit：实际生成24条JSON，文件字节Git blob f72cb9c9ac317e8673a215ca7a73429ce31c687e。
* python b_r290_s86_independent_binomial_oracle.py R290_S86_EXACT_RESULTS.json：24项精确风险 PASS；7个修改结果/元数据负例均拒绝，分别为重复键、遗漏记录、风险篡改、训练概率质量篡改、风险数值归零替代、E1错误升级E2、负后悔值。程序内部命名class_swap的负例实际把风险数值改为0，并没有真正交换原始类别计数；不得声称执行了真实类别交换对照。
* python b_r290_s86_source_ledger_gate.py R290_S86_ALL_1950_TRAINING_SOURCES.csv：1950行逐条精确核验 PASS；5个负例均拒绝，分别为重复、缺失、概率篡改、训练序列篡改、DGP标签篡改。

共12个B负例被拒绝，4个R单元测试通过。源代码原生命令行在本地执行，上传后通过Git blob核对字节身份；尚未从远端重新下载原文件并在隔离环境执行。GitHub Actions NOT_RUN。没有独立真人E2预测，也没有历史E3预测。

## 具体证据身份

* R原生源码Git blob ab79477e17d47cc57f9dc88f97cb85d714361a50。
* B二项式审计源码Git blob 5f1cf8e8299cfff0276b2bbee3d3af69ef0eb869。
* B训练来源审计源码Git blob 08dc8d1d586baef0621649c3c3149138fb355b9a。
* 24项精确结果JSON Git blob f72cb9c9ac317e8673a215ca7a73429ce31c687e。
* 1950来源CSV Git blob fb295926e26304042cf886dfa3285bb013596c4e。

全部身份均通过GitHub远端回读与本地实际执行文件的Git blob比较。身份一致只证明文件字节相同，无法证明全部科学假设成立。

## 验收缺口

真实外部团队复现0；未检验更多m值、真实类不平衡训练、真实人类校准、历史事件预测。B二项式脚本部分元数据检查使用assert，在Python优化模式下会被禁用；本轮仅在正常Python模式实际执行，不能宣称-O门通过。B结果审计仅检查24个唯一键及数值，严格全世界组合覆盖依赖R程序和独立来源审计的固定DGP检查，未来可另加显式24键集合保护。原R290正式验收不变，S86整体仍PARTIAL。

费用：本轮没有使用付费API、数据购买、收费runner或GPU。未核验账户账单，CI未启动。
