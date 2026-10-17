# R075 第三独立真人重复博弈的冻结 E3 模型结构传输协议

日期：2026-10-17。**在任何 R075 第三真人实验七模型真正评分之前独立提交 GitHub main**，并在以下源证据已经审计的前提下制定，禁止事后据模型优劣调整任何定义。此前 R073/R074 的冻结规则原样保留，PESEN v0.1 冻结。

## 一手来源、来源审计与观测资格

原作者 Fudenberg、Rand、Dreber（2012），*Slow to Anger and Fast to Forgive: Cooperation in an Uncertain World*，American Economic Review DOI `10.1257/aer.102.2.720`。共同作者 David G. Rand 网站公开 `https://davidrand-cooperation.com/s/slow-to-anger-and-fast-to-forgive-data-and-code.zip`。独立原文件 ZIP 长度 **1,129,409 bytes**，SHA256 `328346c3cf88a71a3d6cf574f7d6ba741dcea460f3926c16266f1784d3a699ef`，27个ZIP成员 CRC PASS；其中唯一 24列、34446行动行 TXT 文件原始 SHA256 `ff552ba21a92c254e2d867670910f908f5ea8e3aa34b4fa6c05443a020fa56b7`，其余包括18个按真实场次组织的 MATLAB `.mat` 文件、MATLAB分析代码与 Stata 分析程序。作者网站文件和AEA/openICPSR归档之间**未建立字节等价**，严禁冒称相同。

原始作者代码核验 [原作者实际代码审计CI 38990685555](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990685555)：MATLAB程序说明原始矩阵 `actual move` 和 `intended move` 各自编码为1=C、2=D，另一处理逻辑明确 `REAL [INTENDED] CHOICE THIS ROUND (0=D,1=C)`。本次作者完整 TXT 的 `decision` 只有0或1，编码为**意向合作 C=1，意向背叛 D=0**；`you_p_1`、`other_p_1`、`you_p_2`、`other_p_2` 在 t>=3 均能提供本人与伙伴上一及上上轮的**已执行且可见**行动历史（同源原作者处理程序结合实施噪声相符），转换到 C=1 D=0 二元值。不能使用 `decision[t-1]` 和 `decision[t-2]` 代替已有的已执行历史，因为 noise 使两者不同，且 R073 原协议限定只用当时可观察历史。

[真源字段宇宙CI 38990465782](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990465782)：18个 `file` 实际 session，384个 session 内身份槽（原始数值 `subject` 在不同 session 多次复用，严禁当成全球独立数字ID）、17223双人配对轮、34446个选择、每个 `file` 恰一种 `bc×error` 处理。6个处理所含真实场次依次为 (bc1.5,error0.125)3、(bc2,error0.125)2、(bc2.5,error0.125)3、(bc4,error0)3、(bc4,error0.0625)3、(bc4,error0.125)4。[一手时间与反馈核验CI 38990601050](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38990601050)：全部配对记录每组两人、同一 `interaction` 内伙伴不更换，连续 t>=3 具有四个历史信号的**共同评分目标为26116**。发生执行错误时历史行动与当轮选择差异符合指定 `error`；零噪声组与上轮本人与对手意向行为严格一致。

## 七冻结模型与训练限制

严格从 R073 已冻结实现 `research/R073/r073_human_ipd_memory_loso.py` 原 Git blob `c8a0b47fd27bf05e7be5b87419a0824355fc911a` 复用 `MODEL_NAMES`、`state_for`、`predict`、`brier`、`logloss`，守卫不符则 fail-closed。模型 M0 同处理其他场合作率、M1 上轮本人已执行选择、M2 上轮实际对手已执行选择、M3 上轮双方历史联合、M4 前两轮双方联合、M5 TFT 固定0.05噪声、M6 WSLS 固定0.05噪声。M1至M4一律 `(n_C + 20*p0)/(n+20)`，无任何事后调参，未见态回退训练 `p0`；不可新增、删减模型，不可为噪声环境修改超参数。注意 R075 的当前预测目标明确是原作者的**意向 C/D**；R073、R074无动作翻转的选择目标语义更简单，因此跨实验只对预冻结条件预测结构及模型对比作有界解释，不能隐瞒不同研究的行为实现差异。

严格**完整原始 `file` 留场次**共18折。每次训练集仅包含同一个 `bc × error` 处理的其他全部真实 session，绝无留出场任何人任何局任何当前或未来的目标。由于各处理场数不同，其余训练场为1、2或3场，明确如实标注且不声称具备R073的5场训练或R074的2场统一训练。训练风险集与测试风险集都采用在同一个 `file+subject+interaction` 内完整连续 t>=3 的共同决策，不能跨 supergame 拼接，不能读取当轮他人实际行动、当前回报或未来意向；仅历史反馈是 teacher-forced 一步条件预测。训练 `p0` 从同处理其他场合格 t>=3 意向 C/D 计算，若p0为0或1，必须FAIL，不得偷改平滑公式。

评分基线：每个heldout session内部全部个人目标的Brier算术平均与log loss算术平均；18个真实session**等权**汇总，再分别给六个处理场次等权均值和胜负数。不得因每场事件数不同自动总体目标加权。七个模型同一测试共同风险集。两项主对比为 `M3_JOINT_LAST − M1_OWN_LAST` 与 `M4_JOINT_TWO_LAGS − M3_JOINT_LAST` 的Brier配对差，必须报告所有正负场次数与六处理均值；保留其余与M0的四项预先比较，并报告全七模型log loss。原模型固定TFT/WSLS的5%“噪声”只是理论预测概率参数，不代表第三实验真实执行噪声大小相等，不能将它自动替换为实验 `error`。

禁止公布任何完整人类原始动作序列、真实文件中session编号/玩家编号、个人/具体小场得分或各fold训练状态条件概率。CI分独立合成代码检查job和真实源job，必须先测试再真实，源ZIP、内部TXT SHA、源宇宙、场次、两人配对、完整两轮二元历史都先核对，再计算模型。任何强制前置不符即失败。实际独立第三实验 E3 若成功只能表述为**第三作者来源上的冻结模型结构独立内场次留出复验**；不是将R073拟合参数零样本搬来、不是社会反馈记忆因果识别、不是普适心理史学长程预测，独立实际参与者实体在不同日期是否重返仍需作者招募记录核验。

`R075_THIRD_AUTHOR_E3_PROTOCOL=FROZEN_BEFORE_FIRST_REAL_SCORES`
`M0_TO_M6=UNCHANGED_R073_MODEL_PRIMITIVES`
`R075_TRUE_SOURCE=FIRST_PARTY_COAUTHOR_SHA_PINNED`
`R075_E3_RESULT=PENDING`
`PESEN_v0.1=FROZEN`
