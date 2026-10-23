# R252 熵与信息论（11-012，P1）

九人工六bit世界、全部576原来源，正式有界E1状态`CLOSED_BOUNDED_E1_EXACT_SYMBOLIC_SHANNON_MUTUAL_INFORMATION`。非有理互信息保存为**精确有理系数+log₂素数**，不把小数当作数学证明。

[计算前协议冻结](../../protocols/R252_ENTROPY_9_SIXBIT_WORLDS_576_ORIGINAL_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告](R252_SCIENTIFIC_REPORT_2026-10-23.md) · [原生Fraction及素数log₂代数源码](r252_exact_shannon_information.py) · [576完整六bit原source CSV](R252_ALL_576_ORIGINAL_SIXBIT_INFORMATION_SOURCES.csv) · [九world联合概率/精确信息量及人工干预JSON](R252_EXACT_RESULTS.json) · [SHA256机器来源收据](R252_FINAL_MACHINE_ACCEPTANCE.json) · [正式验收](R252_FINAL_ACCEPTANCE_STATUS.json)。

条件信息反例：XOR_SYNERGY中I(X;Y)=0，但给定Z=X XOR Y后I(X;Y|Z)=1bit；COLLIDER_AND中独立X/Y条件于其AND输出之后I(X;Y|Z)=(3/4)log₂3−1>0；完美复制DIRECT_COPY和隐藏共同原因HIDDEN_COMMON_CAUSE_ALIAS在所有相同原bit来源上的全部可见(X,Y,Z)完全一样，但人工do(X翻转)下的Y响应不同，故仅观察熵及互信息不足以识别因果结构。

[首次CI run39895196152](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895196152)模型和来源数学验证成功，但归档push遭遇GitHub并发非快进冲突，**整体failure不可算最终结果**；仅增加有界fetch/rebase/push重试后的[最终CI run39895279784](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895279784)三个job success，Python3.11和3.12各85真实单测共170项通过，576原source永久机器人归档[a63c75a0](https://github.com/edwardsage419/Psychohistory-Research/commit/a63c75a047dee455382f5983c70a4c9935e6182a)。

新增真人E2/真实历史E3均0，R073/PESEN v0.1冻结。下一真实原目录11-013 Information Cascade（R253）。
