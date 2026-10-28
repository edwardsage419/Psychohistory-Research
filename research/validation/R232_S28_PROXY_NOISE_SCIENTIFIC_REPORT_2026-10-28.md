# R232 S28：代理中介测量误差的精确敏感性与偏差抵消反例

日期：2026年10月28日（Asia/Singapore）。证据等级：E1 人工。原 R232 正式有限 E1 验收不变。研究问题：当真实结构机制不变，只提高中介代理 W 的独立测量噪声，观察 OLS 中介路径是否仍能代表真实因果间接效应？

## 预先冻结、来源与执行

在任何本轮计算归档之前，单独提交预先冻结协议 `e21b7c3f394afeceacb6a92882075b71c6a4d7c1`。原 R232 八个世界、1024条完整外生来源、真结构方程及 do(A) 效应全部保留。原始来源 CSV Git blob `97be4f33d8c31c1a36541a9e50afd13447a942ec`，SHA256 `86add6aeacc8c4b34bdc7d82738fb0382e1e2e627ef31bb30a5d2ac9ada1d38f`。本轮只设定 `W_lambda=M+(w_E+lambda) E_W`，其中 lambda 预先固定为0、1、2、3，E_W 是原独立均匀±1外生源。共8×4=32组，32×128=4096个加权来源槽；每组原来源权重1/128，未新增真人数据。

R脚本从原始CSV逐行读取实际观察 A、W、Y、Z1、Z2，按 lambda 改写 W，枚举完整五维可见联合分布与精确总体协方差，用有理数重建观察OLS路径。隐藏M、U和干预结局只作分隔的人工真值，不进入观察OLS。归档32组全部25个协方差元素、六项观察路径与三个真效应、联合支持数及联合分布SHA256。

## 精确结果

| 人工世界 | 真中介效应 | lambda=0观察乘积 | lambda=1 | lambda=2 | lambda=3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| RANDOMIZED_MEDIATED | 1 | 1 | 1/2 | 1/5 | 1/10 |
| RANDOMIZED_NULL | 0 | 0 | 0 | 0 | 0 |
| LATENT_CAUSAL_ALIAS | 1 | 1 | 1/2 | 1/5 | 1/10 |
| LATENT_COMMON_ALIAS | 0 | 1 | 1/2 | 1/5 | 1/10 |
| RANDOMIZED_DIRECT_AND_MEDIATED | 1 | 1 | 1/2 | 1/5 | 1/10 |
| RANDOMIZED_MEDIATOR_CONFOUNDED | 1 | 3/2 | 1 | 1/2 | 3/11 |
| RANDOMIZED_DIRECT_ONLY | 0 | 0 | 0 | 0 | 0 |
| RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR | 1 | 1/2 | 1/5 | 1/10 | 1/17 |

**反例一，代理噪声造成虚假的直接路径。** 在RANDOMIZED_MEDIATED世界，真实直接效应恒0，真实间接效应恒1。lambda=1时观察乘积降至1/2，控制W后的观察A路径升至1/2；lambda=3时两者分别为1/10和9/10。观察总回归始终1，路径分解发生严重错归因。

**反例二，两个错误恰好抵消。** RANDOMIZED_MEDIATOR_CONFOUNDED中，真实间接效应恒1，未测共同原因U依然同时影响M与Y。lambda=0时观察乘积3/2；lambda=1时乘积恰好等于真实间接效应1，观察直接路径恰好为0；lambda=2时乘积1/2。中间的数值吻合只属于这一人工配置中的测量误差与中介混杂偏差抵消，不提供中介无混杂或可识别性证明。

**反例三，完整观察等价持续存在。** LATENT_CAUSAL_ALIAS与LATENT_COMMON_ALIAS的五维观察联合分布在四个lambda下逐状态一致，人工真总效应仍分别为1和0。增加独立代理噪声不会修复A=U造成的重叠缺失。即使有两个U的带噪测量Z1、Z2，这一对冻结人工世界依然观察等价。

## 复算与审计

复算脚本：`research/validation/r232_s28_proxy_noise_exact_20261028.js`。正式收据：`research/validation/R232_S28_PROXY_NOISE_RECEIPT_2026-10-28.json`。收据SHA256 `b76e1d292472500da84e68f2d86d8812a4ddda4a842684ec62d4a919fe98e553`。源文件经GitHub连接器重新读取，1024行、原Git blob及SHA256核对成功；本轮上传的远端R脚本在独立JavaScript执行环境重新执行，生成对象与远端归档全部字段一致。lambda=0与原R232正式结果逐字段比对272项，失败0。

B轨使用完全独立的七维外生系数向量内积计算25格协方差和路径，32组共1088项精确字段比较，失败0；篡改观察中介乘积为999被检出。详见 `research/evidence_audit/B_R232_S28_INDEPENDENT_STRUCTURAL_MOMENT_AUDIT_2026-10-28.md`。此复核是同一项目内部不同算法的程序性验证，外部独立复现新增0项。

## 科学范围与后续

此处是限定线性、均匀±1外生源的人工E1数学敏感性分析，没有实际SEM拟合、有限样本区间、样本外预测、真人E2、历史E3或因果中介的一般识别结论。原R232正式状态不被重写。R073模型与评分规则、PESEN v0.1继续冻结。下一步优先沿原R队列研究R233测量等值性，先核验是否已有同类补充；后续再统一归纳分类与模型熔炼。此次未运行GitHub Actions，CI=NOT_RUN；没有新增费用操作。
