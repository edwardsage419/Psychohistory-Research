# R268 AIC与BIC模型选择（11-028，P1）

研究状态：**CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_BERNOULLI_AIC_BIC_SELECTION**。九个p_true×n人工Bernoulli世界，每世界完整枚举所有0/1有序序列，3312种原source。比较固定q0=1/5的M0（0可调参数）与同数据MLE拟合M1（1参数），严格采用AIC=-2LL+2d和BIC=-2LL+d ln n。

[先行冻结协议](../../protocols/R268_AIC_BIC_NINE_BERNOULLI_WORLDS_3312_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [原生源码](r268_exact_aic_bic_bernoulli.py) · [全部3312原来源CSV](R268_ALL_3312_BERNOULLI_ORDERED_SOURCE_TYPES.csv) · [完整九世界选择概率与每K统计](R268_EXACT_RESULTS.json) · [SHA256凭证](R268_MACHINE_RECEIPT.json) · [正式科研报告](R268_SCIENTIFIC_REPORT_2026-10-23.md) · [机器正式有界验收](R268_FINAL_ACCEPTANCE_STATUS.json)。

样本数n=4的分歧恰K=0与2，BIC在这两个K选复杂M1而AIC选M0；n=6没有分歧；n=10的分歧恰K=4，AIC选M1、BIC选M0。九world选择概率由有序全集逐Fraction加权与独立Binomial(n,p_true)解析权重两路一致。样本内准则选择不能被误当作样本外独立预测优越性。

[CI run39901449413](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39901449413)：Python3.11和3.12各84项真实单测，共168项全部通过；第三真实全source审计job成功，三job总体success。原CSV、JSON及SHA永久归档[GitHub commit215333c1](https://github.com/edwardsage419/Psychohistory-Research/commit/215333c1b7e3abaf6c43e8094d4a86e8244af12a)。

新增真实人类E2=0、真实历史E3=0，R073与PESEN v0.1冻结。下一候选目录11-029 Cross Validation（P0，拟R269）。原R系列完成前不开始统一分类与熔炼。
