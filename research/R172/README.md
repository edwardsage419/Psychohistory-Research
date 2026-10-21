# R172 历史事件史：1731条真实国家年份资料与时间留出预测

**日期：2026年10月21日。** 原研究目录 P1/07-014 Historical Event History Models。**正式状态：CLOSED_BOUNDED_REAL_HISTORICAL_RETROSPECTIVE_HOLDOUT**。采用真实历史国家—年份记录，严守计算前时间切分及模型参数冻结。**只构成回顾性预测检验，不是先于历史事件发生而发布的现实预测**，也没有复制原作者的 Cox 或政治制度统计模型。

## 来源数据及风险集审计

来源：[Pérez-Liñán与Mainwaring《Democratic Trajectories in the Third Wave》Harvard Dataverse官方公开数据](https://doi.org/10.7910/DVN/WFO1N1)，版本1.1、CC0-1.0许可。原始上传文件265851字节，官方MD5为4343114d56124f88bce9d9cc3ce81523；官方按表格格式转换后的公开TSV为428013字节，SHA256为ed8e29368d06d0fa6d597df567eb21e7ac27fa849e1cdfd90b76167c8b5778ba。二者格式不同，不能混用MD5。原作者17387字节Stata复算代码另行核验并归档。三份资料全部在 [source/](source/) 内，原始数据文件归档提交 [94ff7c5](https://github.com/edwardsage419/Psychohistory-Research/commit/94ff7c5368000e3dda1cdba10a724337f9bf1422)。

原始表包含1731行、103个不同制度时期、83个实际可区分国家代码；其中45行为制度中断、1680行为未中断、6行结局缺失。六行全部来自尼日利亚NGA2011时期，已按事前规则**整组剔除**，不擅自将缺失当成未中断。有效资料因此为1725行、102个时期。原数据确有19个时期在转型当年即有一条观测，与来源简介的「之后第一个完整年份」口径并非逐行一致。首次远程CI [39545470112](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39545470112)因此在评分前发生输入检查错误，之后单独提交[事前来源修订说明](../../protocols/R172_SOURCE_SAME_YEAR_OBSERVATIONS_PRESCORE_ADDENDUM_01_2026-10-21.md)（a83088f），只允许合法的来源同年观测，**未修改原始数据、模型、评价或测试划分**。

## 1999年截止的严格历史回顾时间切分

[计算前冻结的正式模型和评分协议](../../protocols/R172_REAL_HISTORICAL_EPISODE_TEMPORAL_HOLDOUT_3_HAZARD_MODELS_PRESCORE_FREEZE_2026-10-21.md)固定：训练仅使用转型不晚于1998年的时期在1999年及之前的真实年度风险记录；测试保留转型不早于1999年、年度观测始于2000年或之后的**全新时期**，一直评分至2017年。同一时期不跨训练和测试，但同一国家在不同时期可能出现于两侧。

| 实际分区 | 年记录 | 制度时期 | 制度中断事件 |
|---|---:|---:|---:|
| 训练：截至1999年 | **581** | **67** | **12** |
| 留出：2000—2017年 | **319** | **35** | **18** |
| 旧时期在1999年以后的观测，强制不使用 | **825** | 旧时期组成部分 | **15** |
| 尼日利亚缺失结局，整体排除 | **6** | **1** | 未知 |

留出的35个制度时期中，有18个以已记录的中断事件结束，17个为观测终点右删失。风险率按**已观察且此前未中断的一个制度时期在下一年度发生首次中断的条件概率**定义，不等同于制度未来永远持续或失败的累计概率。

## 预先冻结的三种模型与实际结果

全部风险参数用 Python Fraction 有理数计算，仅依赖581条训练记录：

* M0 恒定风险：p=(E+1)/(N+2)=**13/583**；
* M1 持续时间：预定年龄段0—2、3—7、8—15、16年以上；按M0先验平滑，伪计数权重20；
* M2 持续时间加首次观察年度的原始初始自由民主指标 libdem0，高低固定切点50，权重20；首个观察年份t=0以及该指标缺失时**必然回退到M1**，避免使用尚未观察到的初始指标。

| 模型 | 留出年度平均对数损失 | 留出年度平均Brier分数 |
|---|---:|---:|
| M0 恒定基线 | **0.235881126652** | **0.054407113235** |
| M1 仅持续时间 | 0.245235328446 | 0.054667027894 |
| M2 持续时间和初始制度指标 | 0.234530415157 | 0.054105271593 |

指标越低越好。**M1比基线差；M2仅略优于基线，优势极小。** 对35个留出时期整体重抽512次（固定种子20261021），M2相对M0对数损失差为−0.001350711495，自助重采样2.5%至97.5%区间 **[−0.016429154960, +0.017785036532]**；Brier分数差为−0.000301841643，区间 **[−0.000926727569, +0.000277502808]**。两个区间都包含零。M1对应两个差值区间也都包含零，见 [完整科学报告](R172_SCIENTIFIC_REPORT_2026-10-21.md)。不能声称某个制度指标已获得稳健的额外历史预测能力，也不能据此作制度存续的因果解释。

本研究只有12个训练事件，部分国家重复参与不同事件时期，统计区间采用**制度时期级**而非国家级重采样，而且数据本身是后见整理的历史资料；因此不等同于当年实际签发的外部实时预测。

## 真实GitHub工作流及完整研究包

通过[首次成功双Python CI39545672065](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39545672065)和[SHA256固定与完整永久归档CI39545815533](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39545815533)，Python3.11与3.12分别在两个工作流各执行92种真实测试，独立归档任务另外复算92种，合计**460次测试执行、92种不同测试方法、0失败**。完整原始数据及预测包已通过 [e88784b](https://github.com/edwardsage419/Psychohistory-Research/commit/e88784bc28b5fbd45f85c9c7cf0ced8e7e503c14)提交GitHub main。

成果：[科学报告](R172_SCIENTIFIC_REPORT_2026-10-21.md)｜[原始数据](source/)｜[正式冻结协议](../../protocols/R172_REAL_HISTORICAL_EPISODE_TEMPORAL_HOLDOUT_3_HAZARD_MODELS_PRESCORE_FREEZE_2026-10-21.md)｜[来源年度规则修订](../../protocols/R172_SOURCE_SAME_YEAR_OBSERVATIONS_PRESCORE_ADDENDUM_01_2026-10-21.md)｜[原始风险集审计](R172_REAL_HISTORICAL_EPISODE_STRUCTURE_AUDIT.json)｜[原始模型程序](r172_real_historical_retrospective_hazards.py)｜[92项测试](test_r172_real_historical_retrospective_hazards.py)｜[319行完整留出结果CSV](R172_REAL_HELDOUT_PREDICTIONS.csv)｜[所有评分和拟合参数JSON](R172_EXACT_RESULTS.json)｜[原始程序、数据、测试和结果ZIP](R172_Real_Historical_Holdout_3_Hazards_92_Tests.zip)｜[正式机器验收](R172_FINAL_MACHINE_ACCEPTANCE.json)。

关键输出SHA256：
* 模型源代码：633a4b65b9e9ffe31442f814f878bc6347444c435c830c9394e2780478150cd6
* 92项测试：e88020b3f87a1c3f538aab9aea84c87f0fde883f224e6df4647b87e1d134eadb
* 全量JSON：0cb8adfbe92cf32b27731f47068bd94cad9346e8545444a684a0c63040a10857
* 319条预测CSV：e7f81816d5d7ffc4c50e864dfd534db00477fd8bec81e04d306dbf479e5eee1d
* 原始资料及程序完整ZIP：3d352c1014fc36db74a8c14587be7503ad7758bc7cbbf76d7066a1910db293bf

复算：在 research/R172 目录执行 python r172_real_historical_retrospective_hazards.py 和 python -m unittest -q test_r172_real_historical_retrospective_hazards.py，只需标准Python，无新增订阅或付费接口。

**证据验收：真实历史资料已完成独立时期与日历时间留出评价，但仍属于回顾性、原数据内的验证。** R073真人重复博弈E2和真正事前发出的历史外部预测E3均未新增证据（E2=0，E3=0）；R073和PESEN v0.1保持冻结。下一原目录为R173 P1/07-015 Cross Societal Comparative Models。完成所有R系列后再统一分类，最后熔炼。
