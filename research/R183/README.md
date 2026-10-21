# R183 逻辑回归：45组原始人工计数模型的分离与样本外预测

2026-10-21。原239目录P0/08-007 Logistic Regression。正式科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC**。

[先于评分冻结协议](../../protocols/R183_LOGISTIC_SEPARATION_45_WORLDS_PRESCORE_FREEZE_2026-10-21.md)固定两组二元行为、每组n=4/8/12、三组真边际概率对和五类R177独立、Beta二项相关或结构零生成机制，共**45个人工世界、4125条完整原始计数对**。每条计数概率及两个组别MLE预测均可逐项复算，独立的分数网格似然最大化和Logit score根验证严格相符。严格区分闭概率域极大值与logit参数是否有限，原始一组k=0或n的观测可能令二系数MLE不有限；两组全0与全n正反事件另归类为完全分离。

固定真实零效应p0=p1=1/4、n=4时，独立二项训练源使非有限logit MLE概率53.802%、完全分离0.247%；强组内相关BetaBinomial浓度2对应非有限79.468%、完全分离5.383%。所有45世界未经收缩MLE面对独立新单次事件的**无条件期望对数损失为INF**，固定半计数预测`(k+1/2)/(n+1)`则给出有限预测分数。未来Brier用原始4125对完整联合概率与独立一二阶矩代数双法严格Fraction一致，半计数未来logloss使用独立math.log和Decimal.ln双路检验。该半计数方法是明确定义的Beta(1/2,1/2)预测基线，不声称完整实现Firth的一般惩罚逻辑回归。

[正式科学报告](R183_SCIENTIFIC_REPORT_2026-10-21.md)、[45世界完整JSON](R183_EXACT_RESULTS.json)、[4125计数对完整CSV](R183_ALL_4125_TRAINING_COUNT_PAIRS.csv)、[机器科研验收](R183_FINAL_MACHINE_ACCEPTANCE.json)、[完整数学程序与27单测](r183_logistic_separation_exact.py)、[固定时间戳完整ZIP](R183_Logistic_45_Worlds_Exact_Separation_Archive.zip)全部入库。[GitHub Actions39561106676](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39561106676) Python3.11/3.12各27单测共54次执行与第三job完整45世界评分/数据归档均success。[原始结果提交977743d](https://github.com/edwardsage419/Psychohistory-Research/commit/977743d70ef674ec7e3bb3b77b9f908aab6d74bd)。

文献：[Cox1958](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x)、[Albert/Anderson1984](https://doi.org/10.1093/biomet/71.1.1)、[Firth1993](https://doi.org/10.1093/biomet/80.1.27)。本轮只达人工数学E1，新增真人E2/外部历史E3均0。R073和PESEN v0.1维持冻结。下一 **R184 P1/08-008 Poisson Regression（泊松回归）**。全部R研究完成后统一分类，再模型熔炼。
