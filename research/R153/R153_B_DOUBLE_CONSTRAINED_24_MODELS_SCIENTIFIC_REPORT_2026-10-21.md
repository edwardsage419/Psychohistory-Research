# R153-B 限定增量科学报告：Wilson空间交互族与双边OD列系数不识别

日期2026-10-21，原固定候选 P2 / 06-011 Spatial Interaction Models。**不是替代原R153 60组2×2模型；新增为严格独立的24组3×3人工数值研究E1。** 前者原冻结commit99183f2、74种单测及原始输出完整保存。

## 一手科学来源与有效核读范围
Alan G. Wilson (1971), *A Family of Spatial Interaction Models, and Associated Developments*, *Environment and Planning A* 3(1):1–32, DOI https://doi.org/10.1068/a030001，直接读取SAGE原期刊摘要、卷期页，说明空间相互作用模型是受不同约束的一族。该论文PDF访问受限，**不能声称逐页精读全文、复现Wilson原始实证案例**。

Richard Sinkhorn and Paul Knopp (1967), *Concerning Nonnegative Matrices and Doubly Stochastic Matrices*, *Pacific Journal of Mathematics* 21(2):343–348, DOI https://doi.org/10.2140/pjm.1967.21.343，[原刊PDF](https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-s.pdf)。本研究实际视觉核读了印刷第343–344页，包含完全正方阵交替行列归一化结论、非负矩阵total support与support区别及其可行/唯一性条件。请勿把原始**双随机单位边际定理**直接写成涵盖任意不匹配边际和结构零支撑的广义定理。本次所有数据都是项目设计而非作者原样观察。

## 先行冻结、首次未收敛、透明修订
[第一次冻结协议](../../protocols/R153_WILSON1971_SINKHORN_KNOPP1967_DOUBLE_CONSTRAINED_SPATIAL_IPF_PRESCORE_FREEZE_2026-10-21.md) main提交`26d713ef35ed0420fce3b47dad999fc7f24cacca5`在生产运算以前形成，预先指定24配置、两个独立算法、Decimal精度≥65、余额差≤1e-25及两算法单元差≤1e-24，初始最大迭代150。前置诊断暴露 **4/24个完整场景在150轮内未达精度**，包括 near/far α2 与m1，残差约1e-20到1e-15，故不能将初始冻结称为首轮通过。严格在正式阶段归档前提交[修订001](../../protocols/R153_AMENDMENT001_IPF_150_TO_450_KEEP_STRICT_1E25_2026-10-21.md)，main提交`6bf830c8bf98c745ec24f379d975ea9d9fe125b7`，**仅增加上限到450；场景、误差要求、数值精度均保持不变**。最终最慢263轮收敛。本项操作明示属于接触初步计算结果后的透明算法预算修订，不可描述为完全盲式预注册验收。

## 人工自建三地区双约束模型
两座坐标布局 `near=(0,1,4)`、`far=(0,2,6)`；三距离阻力指数α=0/1/2；两目的地列偏好 `A=(1,1,1)` 与 `A=(1,2,3)`；两组明确起点终点容量：(R,C)∈{((10,20,30),(15,25,20)), ((20,20,20),(10,30,20))}。共2×3×2×2=**24**人工情景。每布局自区内活动被允许，距离 `d_ij=1+|x_i−x_j|`，严格正核
\[
K_{ij}=\frac{A_j}{d_{ij}^{\alpha}}.
\]
设满足两边际固定的 `T_{ij}=u_i K_{ij}v_j`，`Σ_jT_ij=R_i` 和 `Σ_iT_ij=C_j`，正权重不含自环禁止。这是人工单位活动流，不等于R152真实迁移人头或其它观察样本。

本研究写出两份不共享状态更新代码的Decimal实现：①对当前OD矩阵直接每轮依次按每行、每列的比率调整，②单独估计行列乘数 `u_i=R_i/Σ_j K_ijv_j` 与 `v_j=C_j/Σ_i u_iK_ij`。两种算法**24场景最终全9格相互吻合至1e-24**、各自全部行列余额≤1e-25；原JSON保留每个场景两者迭代次数、余额、单侧约束原流量、最终3×3 OD矩阵（固定28位十进制字符串）和流量变化L1指标。这里的3×3结果是**高精度十进制迭代**而非所有输出格都是有理数解析精确值，不能把Decimal误报为Fraction全程运算。

## 核心可识别性定理与确定对照
若目的地偏好仅作为正列乘数，令 `K'_{ij}=K_{ij}A'_j`，则原双边平衡 `T=uKv` 能改写为 `T=uK'(v/A')`，并保持两边际不变。严格正核及固定边际下平衡流量唯一，因此**把目的地吸引列因子从(1,1,1)改为(1,2,3)，在这套模型里不改变24场景对照成对得到的12对平衡OD表**。这仅证明*可自由缩放的列吸引力*在固定目的地总额条件下无法单独由最终T识别；不是否定社会资源、机会和区位偏好存在因果影响，亦不能推广至非列可分形式。

α=0时核为只随目的地j变化的列向量，不论布局、A，理论解精确为 `T_ij=R_i C_j / 60`；各情景与Fraction代数答案差≤1e-24，验证了不依赖地理配置的负对照。

**起点单侧约束 vs 双边约束**： `T^O_ij=R_iK_ij/Σ_kK_ik` 严格维持每行预算，却一般不能同时维持给定列总额。例如 `near,alpha=2,flat,m1` 时单侧列总量相对目标之绝对误差和约**20.0780**个人造活动单位，调整到完全双边约束时全部单格变动绝对量之和约**20.4769**。该对比说明两套约束的数学含义不可混同。

**独立有理分析对照**：2×2正核 `K=((3,1),(1,1))`，R=(2,3)，C=(3,2)，存在完全Fraction平衡 `T=((3/2,1/2),(3/2,3/2))`，交叉乘积比 `T00*T11/(T01*T10)=K00*K11/(K01*K10)=3`；并非作者原始数值表。结构性零值 `K=((1,0),(0,1))`，等量双边预算(1,1)/(1,1)可行；预算(2,1)/(1,2)不可行。本研究使用行子集到达的目的容量不小于对应起点预算的全部子集有限检验，**不将含结构零的矩阵输入严格正IPF**，以免误用原1967定理的支持条件。

## 复算来源与实际机器验收
本地116项**真实不同unittest方法**通过；包含24个独立命名模型参数测试、12个列因子不变性对照及24个单侧边际偏差对照。完整原始压缩研究包[ZIP](R153_Wilson_Sinkhorn_DoublyConstrained_24_Cases_116_Tests.zip)包含源码 `r153_spatial_double_constraint.py`、测试 `test_r153_spatial_double_constraint.py`、原24情景内部结果JSON `R153_EXACT_RESULTS.json`（此为ZIP内文件名，**仓库树中使用独立补充文件名以避免与R153-A冲突**）。[补充原JSON](R153_WILSON_SINKHORN_24_CASES_EXACT_RESULTS.json)永久保存在GitHub。

SHA256：原源码 `7f27797739074f2504dfe10b9e3442441dd72d682c896c4cecdde732157516b1`；原测试 `3a92a292d6e43bb35e13e416751889aa718d5fc40b0f89b9046a332031f56afd`；补充原JSON `5e66403d0011e02e8a5575403b6408d33aff2a8c2b0aa5727cfcac894648f9b7`；ZIP `86857ec889b25950778e5a16434bd3710970e25717a008861bd7196d7726e05c`。

[正式更正文件名之后的GitHub Actions run39619651934](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39619651934)：Python3.11 job119289374779 116 tests in1.211s、Python3.12 job119289374391 116 tests in1.277s，两个job均通过四份SHA256+独立JSON完整字节复算与全部数学检查；第三归档job119289475417重新核对包含压缩源运输在内5份固定SHA256，全部success且旧R153-A原JSON未被改写。原首次[run39618843001](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39618843001)也完成双116 tests；第二次运行主要是修正**正式公布路径冲突和防止重复运行覆盖前一研究**，不应把多个重复CI运行误报为更多彼此独立科学假设。

**审计补充**：原R153-A `R153_EXACT_RESULTS.json` 曾被新归档任务临时写入错误内容；经历史固定原档Git commit `9aaeccf4290eb6b2d0badda85292cc7a199c57d4` 取原始blob `ea1e43aa468b1fdd0f91f3ad9aa916dcc629044e`，在修复提交 `0f533a8eb46825ab4c7d5e3aabb23137142b7731` 恢复原有文件。补充24组在独立路径blob `6491aaa9b05571fbae7dee243906144a6f1a916d`；CI发布路径也已永久修正为补充独立路径。永久保留这条错误与补救证据，不写成自始完全无归档错误。

新增E2真实人群/现实出行预测=0；E3外部历史预测=0。R073/PESEN v0.1继续冻结。原目录之后虽为P1/06-012 Stock and Flow System Dynamics，仓库也可能已有独立并行研究后续更多R项目，本增量不代表将研究序号倒退或要求重复学习。
