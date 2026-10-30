# R291 S87 科学报告：意向代理测量误差与规范变量的残余预测价值

日期：2026-10-30 UTC。状态：**PARTIAL，内部非盲态E1有限人工研究**。原R291的CLOSED_BOUNDED_E1正式验收不变；R073与PESEN v0.1冻结。E2真人新增0，E3历史新增0，外部研究团队独立复现0。

## 来源、冻结和独立问题
R291原理论来源：Fishbein & Ajzen (1975), *Belief, Attitude, Intention, and Behavior*，作者页面 https://people.umass.edu/aizen/f%26a1975.html 。原R291合成模型及参数由项目自定义，不代表原作者实证参数。原冻结commit 161d40a01451f1e89be045910f95ec536768754c。

本轮S87预评分冻结协议先行独立提交：commit **4f51f8119ab5faba95fcf4b7b44b63eb6bb3621b**，文件 [S87 freeze](R291_S87_NOISY_INTENTION_PROXY_PRESCORE_FREEZE_2026-10-30.md)。冻结后才计算S87结果。

独立研究问题：当真实意向I满足完全中介时，如果只观察到含对称误分类的意向代理J，主观规范N是否仍能提高B的预测准确度？这涉及测量误差与可观测条件独立性，不构成现实因果效应识别。

## 人工机制和评价
原R291四组(a,n)权重与MEDIATED(d=0)/DIRECT_NORM_STRESS(d=1)完全保留。新增代理误分类率e=0、1/4、1/2。联合来源P(A,N,I,B,J)=P(A,N)P(I|A,N)P(B|I,A,N)P(J|I)，总计8×3×32=768条完整带标签来源，其中e=0的128条为零概率来源，仍全部保留。

预测在观察到A、N、J之后、B实现之前进行，I不作为可见特征。比较已知人工DGP的最优Brier风险R(FULL_ANJ)与遗漏N的R(AJ)。额外核验遗漏J的AN及只保留A两种对照。全部计算使用BigInt精确分数；人工oracle已知生成参数，未进行真实数据拟合。

## 精确发现
| 人工配置 | e=0规范遗漏额外Brier | e=1/4 | e=1/2 |
| --- | ---: | ---: | ---: |
| BALANCED，完全中介 | 0 | 11/4480 | 1/256 |
| ATTITUDE_HEAVY，完全中介 | 0 | 1/308 | 1/256 |
| NORM_HEAVY，完全中介 | 0 | 4/385 | 1/64 |
| NORM_NULL，完全中介 | 0 | 0 | 0 |
| BALANCED，直接规范负对照 | 7/480 | 1199/40320 | 9/256 |
| NORM_NULL，直接规范负对照 | 1/64 | 1/64 | 1/64 |

主要反例：BALANCED MEDIATED的真实B只依赖真实I，给定真实I后N没有额外直接作用。J有25%独立误分类时，N在给定A,J之后仍提供 **11/4480≈0.00245536** 的额外Brier风险改善。J完全准确时为0，J完全不含I信息时为1/256。这证明合成DGP中“观测到规范的残余预测价值”可由意向代理测量误差产生，单凭预测改进不能断言存在规范对行为的直接因果路径。

NORM_NULL MEDIATED是严格负控制：三个误分类率下均为0。NORM_NULL DIRECT_NORM_STRESS三个误分类率下均为1/64，区分了一个预先设置的直接规范路径。其余18组完整结果见 [24世界JSON](R291_S87_EXACT_RESULTS.json)。

## 已实际执行的验证与未执行事项
R路线：在当前执行环境的JavaScript V8中真实执行完整768条生成和24组风险计算；检查每个世界32唯一来源、总概率1、零概率来源保留、全部预冻结断言；四种来源篡改负控制由严格生成器拒绝。源码 [r291_s87_noisy_intention_20261030.js](r291_s87_noisy_intention_20261030.js) 和 [768条完整CSV](R291_S87_ALL_768_PROXY_SOURCE_CELLS.csv) 已持久化。

B路线：独立的条件Bernoulli方差聚合算法，不调用R生成器；真实读取远端完整CSV与JSON，核验24世界、768条、128条零概率来源、全部四种风险及三个差值；5项错误注入全部拒绝。另用本地Python Fraction按(A,N,J)聚合并独立核对24个主要差值。B审计源码另存research/evidence_audit。

原生Node命令行执行、GitHub Actions和外部独立研究团队复现均为NOT_RUN。V8实际执行不等同于Node CLI原生验收，也不等同于完整科学结题。

## 统一验收 A01 至 A06
A01 PASS（冻结问题、观测时点、人工范围）；A02 PASS（原R291固定来源与S87提交先后已记录）；A03 OPEN（V8执行和独立核对已做，归档原生CLI尚未执行）；A04 PASS（零来源与负控制保留）；A05 PASS（仅E1合成，oracle与现实推断边界明确）；A06 OPEN（需最终远端提交与CI状态复核及可重复原生命令行证据）。

本轮S87状态PARTIAL。后续优先执行归档R/B原生Node --test/--check，进行源字节重放；只有确认GitHub Actions不产生新增费用才可考虑CI。未来若研究真人意向量表，需独立核验量表可靠性、群组/时间分割、校准与外部样本，禁止直接沿用这些人工效应数值。
