# R268 正式科学报告：AIC与BIC有限二元序列的惩罚方向逆转及模型选择分歧

日期：2026-10-23（Asia/Taipei）。原目录11-028 AIC and BIC（P1）。正式研究R268，证据等级E1（人工概率空间数学完整枚举）；没有新真人E2或真实历史E3。

## 1. 理论来源
Akaike, H. (1974), *A New Look at the Statistical Model Identification*, IEEE Transactions on Automatic Control 19(6):716–723, DOI https://doi.org/10.1109/TAC.1974.1100705 ；Schwarz, G. (1978), *Estimating the Dimension of a Model*, Annals of Statistics 6(2):461–464, DOI https://doi.org/10.1214/aos/1176344136 。原文提出与推导信息准则，R268只作冻结人工Bernoulli微型例子的算术验证，不复现其原研究案例、贝叶斯积分或渐近正当性证明。

## 2. 事前冻结的两模型和九世界
[冻结协议](../../protocols/R268_AIC_BIC_NINE_BERNOULLI_WORLDS_3312_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md)在程序之前提交，[冻结提交6ab880be](https://github.com/edwardsage419/Psychohistory-Research/commit/6ab880be304cebf916948aa9877e6d233b6a5e69)。真实人工源机制每世界n个IID Bernoulli(p_true)的有序y序列，p_true为1/5、1/2、4/5，n为4、6、10，两组参数3×3=九世界。每世界枚举全部2^n个原始有序序列，设计质量p_true^K(1-p_true)^(n-K)，全部九世界**3312种原source**，每世界来源概率和严格1。

候选M0固定q0=1/5、无可调参数（d=0）。候选M1用同一训练样本拟合Bernoulli qhat=K/n，只有一个待估参数（d=1）。所有模型同一观测支持、同一似然格式；K为0或n时MLE位于0或1边界，零次项采用0 log 0连续延拓，不应将最大LL误记为无穷。

```text
AIC = -2 log L(MLE) + 2d
BIC = -2 log L(MLE) + d log(n)
M1 preferred by AIC iff 2*(LL1-LL0) > 2
M1 preferred by BIC iff 2*(LL1-LL0) > log(n)
```
在本研究中n指单条序列中的IID观察数，而不是全部3312种理论序列或跨world观察池。评分同分优先M0。

## 3. 相互独立的数学复核
路线A：所有3312条完整有序原source逐个计算LL、AIC、BIC及两个选择结果，利用其精确Fraction设计质量得每world选M1概率、分歧概率和K完整概率质量。
路线B：完全独立地计算Binomial(n,p_true)的n+1类原K概率C(n,K)p^K(1-p)^(n-K)，用KL式直接构造2(LL1−LL0)并按n阈值分类。九世界的三种选择概率、每个K选择均与路线A严格吻合；对数似然是浮点近似，但来源质量与选择概率均保持精确有理数，并以冻结阈值与数值容差审计。

## 4. 九世界完整分歧概率

|人工真p|n|P(AIC选择M1)|P(BIC选择M1)|P(两准则分歧)|
|---|---:|---:|---:|---:|
|1/5|4|17/625|369/625|352/625|
|1/5|6|5641/15625|5641/15625|0|
|1/5|10|445797/1953125|54753/390625|172032/1953125|
|1/2|4|5/16|3/4|7/16|
|1/2|6|43/64|43/64|0|
|1/2|10|849/1024|639/1024|105/512|
|4/5|4|512/625|609/625|97/625|
|4/5|6|15361/15625|15361/15625|0|
|4/5|10|1951437/1953125|388137/390625|10752/1953125|

由于ln4与ln6均小于2，当前例子的BIC参数惩罚更轻；在n=4仅K=0和K=2时选择分歧、BIC偏向复杂的M1。n=6尽管惩罚仍不同，当前离散K只能取7个整数且没有阈值之间的偏差值，因此两准则严格一致。n=10时ln10大于2，AIC参数惩罚更轻，只有K=4出现分歧、AIC偏向M1。分歧发生概率随p_true改变，却不能通过概率较大直接判断模型选择准则的真实预测价值。

## 5. 反例边界：模型选择不是独立预测验证
M1在训练数据全0或全1时拟合qhat=0或1。九世界所有真实p_true均严格位于(0,1)，因此下一期独立抽样有正概率出现反向结果；MLE插入概率会给此事件预测概率零、对数损失为+∞。不能把训练期最大似然和AIC/BIC胜者直接记为校准的样本外预测机制，也不能据此断定更好模型的真实因果/历史机制已识别。这里没有外部真人留出、独立验证集或竞争非嵌套模型的一般性评价。

## 6. 完整证据与验收
[原生完整执行源码](r268_exact_aic_bic_bernoulli.py) · [3312原source CSV](R268_ALL_3312_BERNOULLI_ORDERED_SOURCE_TYPES.csv) · [九世界全部概率及逐K模型选中表](R268_EXACT_RESULTS.json) · [SHA256机器凭证](R268_MACHINE_RECEIPT.json)。[GitHub Actions run39901449413](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39901449413)在Python3.11与3.12各84次真unittest全部通过，共**168真实测试通过**，第三独立全原source审计和永久归档完成，三job completed/success；[原全部source永久归档commit215333c1](https://github.com/edwardsage419/Psychohistory-Research/commit/215333c1b7e3abaf6c43e8094d4a86e8244af12a)。

原CSV SHA256：`a4b6ece370f8d03585634a21476cb9b906c92362a769bf36fd4c88e4503c3751`；结果JSON SHA256：`0ecde5588400bcff11f71403b526afa8b260bab01e4bc32a94b8934dfbcfef90`。

## 7. 证据范围与顺序
结果成立于一个固定q0的零参数模型与一个一参数MLE的Bernoulli人工比较，不能推广成所有模型、相关观测、小样本或非正则模型的AIC/BIC无条件选择结论。新增真人E2=0，真实历史E3=0，R073/PESEN v0.1继续冻结。按原239目录下一模型拟R269 Cross Validation（11-029，P0），保持R系列学习研究优先；之后统一归纳分类；最后熔炼原创体系。
