# C012 随机提示转化事件与自发报告漏记的共享参数模型：原著边界审计

日期：2026-11-06（Asia/Singapore）
track: theory / C
target_key: (theory-C,Ma-Mermelstein-Hedeker-2022,Statistics-in-Medicine-41-10,converted-random-prompts-vs-unseen-events-and-shared-parameter-identification)
observed_main_head_before_write: 8e257e3698fc7c08f4f27b20e862564b7acbce45
status: METHOD_NOTE_BOUNDED; ORIGINAL_FULLTEXT_SPECIFIED_SECTIONS_READ; NO_PERSONAL_DATA; NO_PRODUCT

## 原始文献与实际阅读

[A] Qianheng Ma, Robin J. Mermelstein, Donald Hedeker (2022), “A shared-parameter location-scale mixed model to link the responsivity in self-initiated event reports and the event-contingent Ecological Momentary Assessments,” *Statistics in Medicine* 41(10):1780–1796. DOI: https://doi.org/10.1002/sim.9328 。开放原刊 https://pmc.ncbi.nlm.nih.gov/articles/PMC9007897/ 。本轮直接阅读开放全文的 Introduction、The Shared Parameter Approach §§3.1–3.3（特别是式1、4、5、6）、Simulation §§5.1–5.2、Discussion 及 Conclusion；未逐格核算结果表、未执行附录SAS代码，部分章节及补充材料未完整审计。出版页确认作者与页码，原刊声明研究数据不共享。

## 原著可核查机制

1. 作者区分受试者自发报告事件 SI 和随机提示恰好发现正在发生事件、转化为事件报告 RC。RC 的存在提供部分自发漏报信息。没有被 SI 或 RC 捕获的真实事件仍可能存在。
2. 主要结果的均值层：Y_ijk = X_ijk' beta + Z_ijk' v_i + epsilon_ijk（式1）；位置和尺度随机效应允许不同个体的均值及波动不同。每日 RC 计数 C_ij 假设服从 Poisson(mu_ij)（式4），log(mu_ij/t_ij)=L_ij' tau+lambda_i（式5），t_ij 为曝光 offset。
3. 式6以 v_i=lambda_i gamma+eta_1i 和 omega_i=lambda_i delta+eta_2i 连接事件计数的随机效应与结果均值、波动的随机效应。gamma/delta 是模型内相关结构参数，单凭估计符号不能确认真实漏记原因或因果方向。
4. 模拟在每组100个合成数据集、每数据集100人×7天条件下比较无关联与有关联的生成机制；另外研究300人和低事件频率的情形。作者报告低频情形每人每日观测数均值1.07、中位数0，较高频情形均值16.09、中位数5。上述数字为作者报告，未独立复算。作者讨论随机效应高维积分成本、初值敏感性。
5. Discussion明确指出随机提示本身的无响应未纳入模型；RC数量可能只是漏记的下界代理；共享参数有效性依赖 random-coefficient-dependent MNAR 假设。未被两条路径捕获的事件无法直接计数。

## 本轮独立识别反例（构造性，非原作者实验）

设每个单位时间的真实事件计数服从Poisson(lambda)，事件在自发路径的捕获概率为s，随机提示额外捕获的概率为r。仅在独立稀疏事件捕获等额外假设下，两个可见计数的均值可写成 E[SI]=lambda*s、E[RC]=lambda*(1-s)*r。若r未知，取世界A(lambda,s,r)=(10,0.5,0.2)，世界B=(20,0.25,1/15)，均有 E[SI]=5、E[RC]=1。两个世界产生相同的两类边际Poisson计数均值，却具有不同真实事件强度和自发漏记比例。若捕获过程还存在依赖，则可识别性更弱。此例只是额外简化观测机制的构造性反例，**不是**Ma等作者的RC生成模型或原文模拟；随机提示捕获正在进行的事件还受事件持续时间、提示时刻与曝光定义影响。即使共享参数模型拟合良好，仍须用外部信息约束事件强度、提示覆盖和漏记机制。

## 与已有C研究去重及候选证伪

C003已研究一般MNAR及部分识别界限；C007已研究测量反应性；C011已研究回顾性事件报告与日记覆盖。本文件独立聚焦**随机提示转化事件的观测合同、Poisson曝光和共享随机效应假设**。它不重建既有C003/C007/C011理论，也不升级R实证等级。

候选观测：随机提示时刻、是否答复、提示时事件是否正在进行、SI报告时刻、RC计数、提示曝光时长、事件持续时间、状态量表及量表版本。不可观测：未由任一机制捕获的事件及其状态。可证伪设计：在完全合成事件流中预先设定事件强度、持续时间、SI捕获、随机提示时点及提示拒答机制；比较同一模型在提示拒答依赖潜在状态、持续时间依赖状态、以及正确设定条件下的参数覆盖和校准。若模型在上述违反条件下系统失准，则“无条件可恢复真实事件漏记率”的推广被否定。设计未执行，未采集真实个人数据。

## 证据及费用边界

原著指定章节阅读 COMPLETE；独立构造性识别论证 COMPLETE（指定假设）；独立算术脚本 NOT_RUN；作者原始数据重算 NOT_RUN；真人实验 NOT_RUN；因果识别 NOT_RUN；个人决策产品 NOT_RUN；CI NOT_RUN。D003本周完成日期2026-11-02，已只读核对。R073、PESEN v0.1冻结及R E1/E2/E3与MARKET等级不变。新增收费服务0，实际账户账单 NOT_VERIFIED。下一步先核本日C登记，再审原文结果表及随机提示响应的假设；转向弱覆盖领域原著，避免长期占用单一统计专题。
