# R224 S20 负对照结果测量误差补充研究预评分冻结协议
日期：2026-10-28。研究类型：原R224八人工世界上的额外有限E1机制实验。冻结时main HEAD：`89b308c73a321f3e66e0085fd7b13975986bfc28`。
本协议独立于原R224正式验收；保留R224原八个SCM、4096条原始外生来源、每世界512行、原真实因果效应与R073、PESEN v0.1冻结。绝不把本补充研究计为新的original239目录完成项。
## 固定输入
`research/R224/R224_ALL_4096_ORIGINAL_NEGATIVE_CONTROL_SOURCE_ATOMS.csv`，其SHA256在原正式验收文件中记录为`cdbc43e01c115c20e551fa0088fed47962ac0b5547c8d4b74e4f257f16772f38`。原研究原生脚本`research/R224/r224_exact_negative_controls.py`，原结果JSON和正式验收状态只读。
## 预定五种测量核
原始二元W是潜在真实负对照结果；新增可观察Wstar。定义q_a=P(Wstar=1|W=0,A=a)，r_a=P(Wstar=0|W=1,A=a)。原始A,Z,Y、所有oracle及原外生源均不变。五核分别为：
1. IDENTITY：q0=q1=r0=r1=0。
2. SYMMETRIC_QUARTER：q0=q1=r0=r1=1/4。
3. SYMMETRIC_HALF：q0=q1=r0=r1=1/2。
4. FALSE_POSITIVE_A0：q0=1/4，q1=r0=r1=0。
5. FALSE_POSITIVE_A1：q1=1/4，q0=r0=r1=0。
这些值固定，不允许看到结果后修改。
## 预定估计和校验
对8世界×5核=40条件逐条从原始外生来源及Wstar两种状态计算联合质量，每条件1024个来源槽（允许零质量），总40960槽。输出四个观察关联D_AY、D_AWstar、D_ZY、D_ZWstar，朴素调整D_AY-D_AWstar，原真实ATE_Y，原真实A→W效应，测量后do(A)→Wstar效应，以及质量和与支持检查。观测统计只可用A,Z,Y,Wstar；oracle只用于单独的真值审计。Wstar由A依赖的测量核产生，不能将它误当作原W的排除条件。
R计算：逐原来源×两种Wstar值的Fraction权重直接枚举。
B计算：从原始(A,Z,W,Y)的16格观测联合分布作矩阵变换，独立得到Wstar联合分布和观察统计；从原do(A)的W oracle分别应用核计算测量后的干预效应。不得读取R已计算的S20统计。
预定比较：40条件×8个结果字段=320个精确相等比较（四观察差、朴素调整、真ATE、真A→W、测量doA→Wstar）；另外质量、原世界、零质量与身份条件。对称核预定解析关系D_AWstar=(1-2e)D_AW，D_ZWstar=(1-2e)D_ZW。身份核必须逐世界复现原R224结果。预先规定两个错误注入：篡改任一Wstar差值，和把FALSE_POSITIVE_A0核错用为FALSE_POSITIVE_A1，均应检出。
## 证据边界
仅人工E1。无真人E2、历史E3、外部独立团队复现。原R224正式验收保持原状。B为项目内部独立算法审计。禁止新增计费资源及GitHub Actions，除非先独立确认零费用。写入独立路径`research/validation/R224_S20_*`、`research/evidence_audit/B_R224_S20_*`，禁止覆盖旧文件。若发现冻结协议错误，另行保留勘误，不得悄然改写。
