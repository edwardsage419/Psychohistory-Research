# A 数据侦察：Andreozzi 2020 历史字段错位对作者公开分析脚本的静态影响范围

日期：2026-10-30 Asia/Singapore。目标键：(A,Andreozzi2020,author-979abf87,wrong-wide-o-lag-actual-analysis-references)。本轮只读作者公开代码，未拟合预测器。

## 固定来源
原作者仓库 https://github.com/seyhunsaral/stabilitycondcoop ，固定 commit 979abf87b5d3cfb7aa8be13b81ef233076c3bb75。
code/process_raw_data.R Git blob 522efd459f574ccaef3d9ce1dd2b086ffb70370e；code/main.R Git blob 3b4f79ce3ddb2d144ea31ccbed26aa03396c9e3c；code/functions.R Git blob 7c3e1e9cf8124805f9deb538d824c8e7c18ce07a。作者 README blob 3292568ac99ec45c22ebcf009fa929028e07608a，数据许可 CC BY 4.0、代码 MIT。论文 https://doi.org/10.1038/s41598-020-70681-z 。

## 实际代码核验
process_raw_data.R 第269行正确计算 opp_cond_class_wide_o_lag1 = lag(opp_cond_class_wide_o)；第274行在清除首轮缺失值时，错误调用 replace(opp_cond_class_wide_o, period==1, NA)，从当前轮字段覆盖 lag1。上一轮审计发现可比较1206行中813行错位。本轮复读代码第265至276行确认该赋值链。

完整静态搜索作者 code/main.R 的459行：opp_cond_class_wide_o_lag1 出现0次。其 Table 3 段落（第295至308行）使用的是 opp_action_lag1 和 opp_cond_class_narrow_lag1，构造 observed_opp_cond_class；回归式 isCC ~ period + treatment + 参与者与会话随机截距，并未引用有问题的 wide_o lag1 字段。作者其他图形分析读取的是当期 cond_class_wide_o 等字段。code/functions.R 的376行亦未检出该错误字段引用。

因此，针对当前固定版本的公开 main.R，尚未发现已识别错误字段直接进入作者主分析脚本的代码路径。该结论仅是静态引用审计，不能证明原论文所有图表、作者运行环境或其他未列入代码均不受影响。仍未完整运行 process_raw_data.R 与 main.R，亦未比较发表论文全部数值；不宣称原论文已被独立复现。

## 其他复现关口
lag(..., order_by=subject_unq) 位于 group_by(subject_unq) 内，排序键在每个组内恒定。上游第190行存在 arrange(session,period,stage,time)，目前 CSV 的轮次顺序与上一轮独立审计相符。若其他预处理改变行序，按 subject_unq 排序不能独立保证按 period 形成真正历史滞后。未来复现须明确 period 顺序并执行原始到 CSV 的字节级比对。

数据已公开且有CC BY 4.0声明；1340条、134名参与者、6会话及会话内重复测量结构沿用前轮已核验结果。本轮未重新下载或再分发参与者CSV；未做新 E2 预测。R073 冻结双真人100轮复验条件仍不满足。原数据处理影响审计状态 PARTIAL，下一步按会话重建原始处理并核对 Table 3。
