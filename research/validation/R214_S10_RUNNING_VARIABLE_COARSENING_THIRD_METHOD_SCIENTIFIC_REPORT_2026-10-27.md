# R214-S10 运行变量测量扰动与离散门槛附近观测差的有限E1研究

日期：2026-10-27（Asia/Singapore）。原239目录09-005 Regression Discontinuity Design。状态：COMPLETE_BOUNDED_INTERNAL_E1_SUPPLEMENT_WITH_DISCLOSED_POSTEXEC_CONTROL_ERRATUM。

## 科研身份与来源

在R214正式12世界192原噪声来源、R214-S2七世界7168来源和R214-S9九世界576来源均已完成后，新增独立的R214-S10补充方法研究。原有正式验收与结果文件全部保持不变；S10不增加239原目录条目。输入直接取R214-S9归档的576条人工来源，固定Git blob `27de4f8239c25c4946f050c68691c3793b8b09af`。计算前冻结协议：`protocols/R214_S10_RUNNING_VARIABLE_COARSENING_THIRD_METHOD_FREEZE_2026-10-27.md`，冻结提交 `bbb15b85c941b495ec4ef883f84a089a8598aede`，先于R计算代码提交 `e86785688e9a2b6883da71fe485efb91eeb11d46`。

方法背景：Imbens and Lemieux (2008), DOI 10.1016/j.jeconom.2007.05.001；Lee and Lemieux (2010), DOI 10.1257/jel.48.2.281。引用用于限定RDD的条件均值、阈值与连续性背景。本轮没有复现论文真人数据或开展真实密度检验。

## 设计与实际计算

固定原九个真世界、16个R位置、原U/E/观测Y/原始来源权重，真处理D=1{R>0}。独立增加三点运行变量测量扰动Z，观测W=R+Z，P(Z=±1/8)=q，P(Z=0)=1−2q，q∈{0,1/4,1/2}。严格有理数BigInt计算9×3=27条件，每条件64原来源×3扰动槽，共5184槽，正概率槽3456。每条件概率总和精确为1。

比较W=±1/8的观测结果条件均值差G、W=0的真实处理比例、把A=1{W>0}误当真实处理的错配质量，以及只在最后引入真结构oracle τ(0)计算G−τ(0)。G不使用潜在反事实或真τ。这里G是固定有限支持上的**观测差诊断量**，不自动具有RDD因果识别资格。

| 人工世界 | 真τ(0) | q=0的G | q=1/4的G | q=1/2的G |
|---|---:|---:|---:|---:|
| LINEAR_CONSTANT | 2 | 9/4 | 7/3 | 5/2 |
| SORTED_LATENT_TYPE | 2 | 13/4 | 10/3 | 7/2 |
| PLACEBO_JUMP_NO_TREATMENT | 0 | 5/4 | 4/3 | 3/2 |
| TREATED_SIDE_CURVATURE | 2 | 145/64 | 227/96 | 41/16 |

LINEAR_CONSTANT即使q=0，最近两点的观测差仍为9/4，已高于真阈值处理效果2。q从0增加至1/2时，该观测差进一步升至5/2，偏差从1/4增至1/2。原因是测量扰动改变了给定观测W时的真实R混合。PLACEBO_JUMP_NO_TREATMENT的真效果为0，观测差仍从5/4增至3/2，显示仅凭有限点观测跳跃可能产生虚假的因果解释。

在q>0的18个条件中，W=0具有质量q/8。8个R左右质量对称的世界在W=0的真实处理比例为1/2；DENSITY_JUMP_ONLY为3/4。观测阈值A=1{W>0}与真实D的错配质量，在普通世界为q/16，在密度跳跃世界为3q/32。这些都是人工已知生成概率的精确量，未估计真实人群阈值操纵。

## 负对照事件及审计界限

原冻结协议错误预期把A=1{W>0}改为A'=1{W≥0}会在所有q>0条件改变总体错配率。R计算后发现：左右质量对称时，A和A'在W=0逐来源标签不同，总体错配率却相等。已经以新增文件 `protocols/R214_S10_POSTEXEC_NEGATIVE_CONTROL_ERRATUM_2026-10-27.md` 明确记录，未修改冻结协议。B独立审计证实16个条件的原预期不成立，另2个密度不对称条件总体错配率改变；18个条件均存在正质量的逐来源标签分歧。事后诊断不追认为事前负对照成功。

B使用原576行的R条件概率与结果一阶矩逆向卷积，与R逐来源扩展枚举形成不同计算路线。27条件×15字段=405项精确字段比较通过，另有18项原S9近门槛均值回归、9项来源质量检查通过。程序性内部复核通过，外部独立复现0。

## 文件与科学验收

* R完整可运行脚本：`research/validation/R214_S10_RUNNING_VARIABLE_COARSENING_EXACT.js`，Node.js 18+，命令：`node research/validation/R214_S10_RUNNING_VARIABLE_COARSENING_EXACT.js research/R214/R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv`。脚本核验原CSV的Git blob。
* R完整27条件机器收据：`research/validation/R214_S10_RUNNING_VARIABLE_COARSENING_EXACT_RECEIPT_2026-10-27.json`。
* B独立脚本与审计收据：`research/evidence_audit/b_r214_s10_conditional_moment_convolution_20261027.js` 与 `research/evidence_audit/B_R214_S10_CONDITIONAL_MOMENT_AUDIT_RECEIPT_2026-10-27.json`。
* B科学报告及A公开数据审计另存各自专用目录，不修改共享索引或其他研究轨成果。

证据级别仅为人工E1。没有真实RDD样本、无限趋近阈值的支持、测量误差参数估计、实际随机抽样置信区间、真实样本外预测或外部独立复现。新增真人E2=0，历史E3=0。R073及PESEN v0.1冻结；个人决策产品开发继续暂停。新增CI如未实际运行，明确标记NOT_RUN。
