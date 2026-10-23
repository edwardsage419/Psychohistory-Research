# 心理史学R272至R274：样本外、跨群体与跨时期独立评价，原R连续有界E1研究与归档索引

日期：2026-10-23 Asia/Taipei。依原239候选目录严格连续研究12-002 Out of Sample Prediction（R272，P0）、12-003 Cross Population Validation（R273，P0）、12-004 Temporal Holdout Validation（R274，P0）。三项均先将计算及验收协议冻结并GitHub提交，随后形成完整原随机来源与可执行模型和独立解析路线，用Python3.11和3.12进行真正单元测试、GitHub第三job重新核验所有来源和SHA256、永久机器人归档全部原CSV/结果JSON/哈希，最后发布正式科学报告与机器有界结题收据。

## R272：已见训练 vs 真正独立样本外标签
[冻结协议](../protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [研究完整入口](../research/R272/README.md) · [科学报告](../research/R272/R272_SCIENTIFIC_REPORT_2026-10-23.md) · [机器有界验收](../research/R272/R272_FINAL_ACCEPTANCE_STATUS.json) · [CI run39903106107](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903106107) · [原来源永久归档dd4995e8](https://github.com/edwardsage419/Psychohistory-Research/commit/dd4995e82cd62cc35c493b79f3525854c06a7eab)。

三个人工真p×三个模型，九world各有四条训练bit与两条独立测试bit的全部64原source，共**576带模型标识来源配置**。MLE、Laplace平滑、半概率常数逐source列出训练及测试Brier。p=1/2时MLE训练Brier 3/16最小，但未来真独立Brier 5/16，比常数模型1/4还差。未截尾边界MLE未来零概率冲突可导致+∞对数损失。完整原来源与独立训练K~Binomial(4,p)期望逐Fraction一致。Python3.11/3.12各83项真测试共**166项成功**，三job completed/success。

## R273：源分布与新目标分布之间的转移风险
[冻结协议](../protocols/R273_CROSS_POPULATION_27_WORLDS_1728_COMPLETE_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [研究完整入口](../research/R273/README.md) · [科学报告](../research/R273/R273_SCIENTIFIC_REPORT_2026-10-23.md) · [机器验收](../research/R273/R273_FINAL_ACCEPTANCE_STATUS.json) · [CI run39903300167](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903300167) · [完整机器人原来源归档1d57f507](https://github.com/edwardsage419/Psychohistory-Research/commit/1d57f5078d172d1feb4b6a07a68e8732c102edf6)。

源p_a×目标p_b三取值各自独立，共九对分布×三个模型=27个人工world，每world原四源训练bit、二目标独立测试bit的完整64个原配置，合计**1728模型标识完整来源**。若源真率1/4、目标真率3/4，SOURCE_ORACLE目标Brier 7/16，SOURCE_LAPLACE 55/144，而TARGET_ORACLE（依赖不可知目标真率，仅理论下界）3/16。SOURCE_ORACLE也依赖源真率，均不可冒充只凭数据拟合的可部署预测器。全部27个目标风险以原source穷举、独立Binomial(4,p_a)解析式和第三原CSV来源审计逐Fraction一致。双Python各172项真测试共**344项成功**，三job completed/success。

## R274：时间严格向前评估，禁止使用未来标签回填
[冻结协议](../protocols/R274_TEMPORAL_HOLDOUT_9_SIXBIT_WORLDS_576_ORIGINAL_SOURCE_PRESCORE_FREEZE_2026-10-23.md) · [完整研究入口](../research/R274/README.md) · [科学报告](../research/R274/R274_SCIENTIFIC_REPORT_2026-10-23.md) · [机器验收](../research/R274/R274_FINAL_ACCEPTANCE_STATUS.json) · [CI run39903501667](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39903501667) · [原来源永久归档df5ad9d9](https://github.com/edwardsage419/Psychohistory-Research/commit/df5ad9d907fed3fe1c2c17d8d12eb10ad25c081b)。

三冻结人工时间机制：STABLE_HALF旧/新概率均1/2、RISING_RATE 1/4→3/4、FALLING_RATE 3/4→1/4。过去四bit训练、未来两bit测试，三个预测政策形成九world及**576完整原source类型**。合法PAST_ONLY_LAPLACE在STABLE_HALF未来Brier 5/18，合法PRECOMMITTED_HALF为1/4；非法HINDSIGHT_POOLED已将评价的未来Y纳入q并对同一Y再评分，取得27/128，绝不能将这一“成绩”当作预测绩效。两种变点世界中合法历史模型未来风险55/144、半概率1/4、非法回填131/512。独立Binomial(4,a)×Binomial(2,b)15类别解析法全部世界精确一致，第三独立来源重建了每源future label leakage标识与预测变化。双Python各82项真测试共**164项成功**，三job completed/success。

## 连续科学证据与归档完整性边界
三项原R正式有界E1结题：人工world总数9+27+9=**45**；带模型/世界ID的完整人工原source类型576+1728+576=**2880**，不同world共享部分随机空间，不是2880个独立真实样本；双Python真实unittest执行166+344+164=**674次均通过**；三个GitHub Actions每个三job全部completed/success，合计**9个成功job**；三项均有先行冻结、完整原CSV、数学源码、解析独立路线、机器SHA256凭证、正式科学报告与验收状态。

**科研推断仍仅限E1**。三项均未引入任何真实人类E2或真实历史E3数据，未取得R073冻结模型在新实验场次的独立重复验证，未修改PESEN v0.1。相比之前模型，本轮推进的是如何区分训练内评分、跨群体转移、时序前瞻评估及非法标签泄漏的**模型评估方法**，不能作为对现实心理历史系统的实证效度证据，也没有提前开展模型熔炼。

原239模型目录下一项已核实为**12-005 Equifinality Analysis（P0，拟R275）**，之后12-006 Model Identifiability。继续遵循用户明确研究顺序：先完成全部原R系列模型学习研究，再统一归纳、分类，最后开展原创模型熔炼。
