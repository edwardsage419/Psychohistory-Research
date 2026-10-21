# R196 事前冻结后数值校验精度订正：70位ELBO比较被默认28位Decimal截断

日期2026-10-21。性质：PRE_RESULT_NUMERIC_COMPARISON_ERRATUM。

## 失败原始记录

原R196预评分协议于commit `95643c7eae50f51cc882e29cbb28967a9945994c`提交main，固定全部6真目标、m=1/2重复正证据、COARSE及FINE两个嵌套网格、408个均值场评分候选以及用70位`Decimal.ln`形成ELBO与KL的比较规则。随后第一版正式代码于commit`e4b6ed733040beba493163d64b2ceac1d3d36e8b`入库。

初次GitHub Actions run [39587074398](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39587074398)，Python3.12实际32项测试31项成功，仅`test_optimal_coarse_fine_nested`失败，Python3.11随后cancelled，完整研究结果归档job skipped。该失败没有构成真正的数学反例。

问题发生在比较完整70位Kullback–Leibler结果时：
* 细网格返回完整70位`Decimal('0.08338614749880478752955209099147306967402824893451348337183697570169442')`；
* 粗网格返回**同一个最优候选的同一个完整值**，但测试表达式`Decimal(coarse)+Decimal('1e-50')`因Python外层默认context.prec=28被舍入为`Decimal('0.08338614749880478752955209099')`；
* 结果把70位细网格数与经28位四舍五入的粗网格数比较，错误地报细网格更差。该截断也可能影响正式run中的嵌套网格比较条件，必须在全量科研验收前修复。

## 精确订正方式

只在**粗细网格比较的两处**（一次完整世界运行检查、一次单元测试）设置显式`with localcontext() as context: context.prec=80`，再比较原来70位Decimal分数并加原来定义的1e−50容差。不得变动任何一套源权重、先验、likelihood、真后验计算、候选集合、格点顺序、目标函数、成功阈值、70位ELBO评分实现或冻结理论结论。必须保留原CI失败时间线、重新执行双Python全部测试，并让完整24世界408项评分和永久归档通过三job后才能结题。

本更正属于**评分前暴露的校验舍入问题**，不是通过选择数据更改统计结论。证据只限E1人工模型，无真人E2或历史E3新增，R073与PESEN v0.1依旧冻结。
