# R163 成功偏向传承｜72组人工收益比较与模仿策略的独立精确验算

2026年10月21日。原始目录 **P1 / 07-005 Success Biased Transmission**。正式研究状态 **CLOSED_BOUNDED_E1**。本轮只研究两个匿名文化选项A/B、三位虚构示范者的有限人工收益表，没有真实的技能、社会影响力、个人试验记录、原作者演化模型或历史预测。

**一手文献：** [Baldini 2013 原刊](https://doi.org/10.1016/j.tpb.2013.03.005)区分比较各变体平均收益 Compare Means 与模仿单个最成功者 Imitate the Best，[Baldini 2012](https://doi.org/10.1016/j.tpb.2012.06.005)分析随机收益可能导致成功偏向不如随机模仿。[Mesoudi 2011 原期刊](https://doi.org/10.1016/j.evolhumbehav.2010.12.001)使用真人箭头设计实验比较包括收益偏向、个人学习、符合与随机模仿的策略。我们查阅出版方可见的文章介绍与摘要，定位作者原PDF，但没有取得逐次实验参与者数据，也未复算文中统计估计。[Kendal等2018综述](https://doi.org/10.1016/j.tics.2018.04.003)强调学习策略存在情境转换与混合。详细文献审计见[正式英文科学报告](R163_SCIENTIFIC_REPORT_2026-10-21.md)。

**计算前冻结：** 六套人工三人行为与收益表×三种显示收益变化（原样、顺序反转、全部同分）×两种成功选择策略×两种事先指定正确答案，共 **72组**。随机基准为在三个示范者中等概率挑一人；最高个人收益模仿在得分相同的人之间等概率选择；平均收益比较只在两种可用文化行为之间等概率处理均值平局。所有约定在[计算前冻结协议](../../protocols/R163_BALDINI_SUCCESS_BIAS_72_PAYOFF_WORLDS_PRESCORE_FREEZE_2026-10-21.md)内明确，且均为项目自建规则。

**独立精确计算：** 直接算个人最高分、分类均值与全部正确率；另一路分别穷举最高分者和用乘积比较两个文化行为的组均值，单独复算正确率。72组中的复制概率、随机基准、指定正确答案下的理论正确率及差值，完全以Fraction精确匹配并保存全部[47,799字节原始JSON](R163_EXACT_RESULTS.json)。

**机制与边界：**
* 人工行为(1,1,0)、收益(12,0,8)：模仿最高收益者肯定复制A，比较各行为平均收益则肯定复制B。另一组(1,0,0)、收益(8,12,0)方向恰好相反。因此“从成功者学习”必须明确具体规则。
* 在第一组案例中，若真实正确答案是A，模仿最高收益者比随机模仿提高正确率1/3；若真实答案是B，同一人工观察到的收益信号却令正确率降低1/3。收益记录可靠性必须独立验证。
* 个人最高分打平和行为平均收益打平的抽样办法不同；当三人得分全部相同时，最高分者抽样复制A的概率2/3，行为均值打平时复制A概率1/2。光看最终复制频率不能唯一恢复学习者的心理机制。
* 一次有限示范不能代表复杂环境、长期选择和真实文化适应度；本研究没有估计真实收益信息质量。

**三轮CI与永久归档：** [第一轮39528469903](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39528469903)、[SHA256校验轮39528566826](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39528566826)与[完整归档轮39528599475](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39528599475)全部成功。前两轮各Python3.11、3.12环境分别运行102项测试；末轮两个环境各102项，第三归档任务又重跑102项，累计714次真实单测执行、不同方法102种、失败0。全部源码、测试和结果ZIP已经由[归档提交310acad](https://github.com/edwardsage419/Psychohistory-Research/commit/310acadf9b16124b0df5a386620aa6aa851db964)永久写入GitHub main。

全材料：[正式科学报告](R163_SCIENTIFIC_REPORT_2026-10-21.md)｜[事前冻结协议](../../protocols/R163_BALDINI_SUCCESS_BIAS_72_PAYOFF_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交a7cc84b）｜[原生程序](r163_success_bias_payoff_exact.py)｜[102项测试](test_r163_success_bias_payoff_exact.py)｜[完整JSON](R163_EXACT_RESULTS.json)｜[源码/测试/结果ZIP](R163_Success_Bias_72_Worlds_102_Tests.zip)｜[机器验收](R163_FINAL_MACHINE_ACCEPTANCE.json)。

SHA256：
* 源码 `c680c53cbbcbc52200ffdd3c7b40b37a32ea6736c0011a64a9c21107271e7262`
* 测试 `c2349e512b8c1fc1c23dd905109f1416e58940b56eee41ac45f5bc8aaa5f611c`
* JSON `23979510af73c9b92e9cadb85ee86a9223401c4d13a00240f832938f046dde22`
* ZIP `a3313a85ab0d5aa4865f28747ec05a7c3bcdc36716a12fddf6fa54d286e279cf`

进入 `research/R163`，依次运行 `python r163_success_bias_payoff_exact.py > R163_EXACT_RESULTS.json` 和 `python -m unittest -q test_r163_success_bias_payoff_exact.py`；仅依赖Python标准库。

**新增长期或真人独立证据E2=0、历史外推E3=0**，R073及PESEN v0.1维持冻结。下一原目录 **R164 P1 / 07-006 Content Biased Transmission（内容偏向传承）**，继续优先完成R系列后再统一分类、最后熔炼。
