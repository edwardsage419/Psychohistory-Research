# B轨 R302 S98 非盲态独立算法与负例审计

UTC日期：2026-10-30。目标键：(B,R302,S98-v1,alternate_double_integral_and_mutation_coverage)。预定检查项目见R302 S98事前冻结协议，commit cfd7991944488c4424870d00cb94e7174d6aefa4。

## 审计输入与方法

已阅读原R302 Python Beta CDF积分算法、原81世界/162来源CSV、R302 S98冻结协议及本轮主线输出，属于非盲态内部程序复核。审计程序 research/evidence_audit/b_r302_s98_independent_double_integral.py 不导入R程序，以独立多项式双重积分计算P(theta_A>theta_B)。固定两个后验Beta(a,b)、Beta(c,d)：

p = [B(a,b)B(c,d)]^(-1) * sum_{j=0}^{b-1} sum_{k=0}^{d-1} [(-1)^(j+k) C(b-1,j) C(d-1,k)]/[(c+k)(a+c+j+k)]。

此积分展开与R使用的Beta CDF二项式表达不同。所有值用Python Fraction精确计算。对全部81个唯一计数世界逐项检查世界身份、后验均值、p、贪婪行动、三种即时期望奖励、两种机会成本；重新聚合平均成本、正零数量、最大值及其世界、平局数量。核验结果：81/81一致，摘要全部字段一致。

## 实际预设变异测试

八种错误注入在本地逐一实际执行，全部被检查器拒绝：重复世界、遗漏世界、Thompson概率篡改、机会成本篡改、贪婪奖励篡改、汇总平均篡改、真人E2证据标签错误提升、世界身份错误。程序退出状态0，输出result=PASS。原R主线5项本地unittest通过。远端CSV Git blob ec23bcd5152d37beda224564b0f723cd107a643f及结果JSON Git blob 3989d33bd843300dc932d46adec322a6616d813c，与本地计算文件一致。

## 仍未满足的验证条件

远端归档Python源文件原样下载后原生CLI复算NOT_RUN，GitHub Actions NOT_RUN，外部研究团队独立复现NOT_RUN。不存在真人样本外预测、经验概率校准、独立人类实验或真实奖励观测。固定人工计数网格的后验预测风险无法充当实际奖励生成过程的独立验证。原R302历史正式验收不受本轮改变。

B_STATUS=PASS_NONBLIND_INTERNAL_MATH_ONLY；SCIENTIFIC_ACCEPTANCE=PARTIAL；E1人工；新增E2=0、E3=0。R073及PESEN v0.1冻结。
