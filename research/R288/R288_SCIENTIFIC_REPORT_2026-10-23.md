# R288 科学报告：原239目录01-002 前景理论的参考点与损失厌恶子模型

日期2026-10-23 Asia/Taipei。由用户所定研究顺序推动：原239项全部学习→统一归纳分类→最后原创模型熔炼。**本项是原目录P1补缺，而不是新增第240/241/242项原候选**。始终区分外部文献理论线索、人工模型数学与真实人类样本的实证验证。

[先行事前冻结](../../protocols/R288_PROSPECT_REFERENCE_LOSS_AVERSION_9_WORLDS_576_SOURCES_PRESCORE_FREEZE_2026-10-23.md) GitHub提交[d94d9d7f](https://github.com/edwardsage419/Psychohistory-Research/commit/d94d9d7f275082a6672fbea0e191ac76a54bed87)，先于完整结果生成。

## 模型、文献与严格范围

文献Kahneman & Tversky (1979), *Prospect Theory: An Analysis of Decision under Risk*, Econometrica 47(2):263–291，DOI https://doi.org/10.2307/1914185。论文原模型包含编辑、参考点/得失价值和非线性的决策权重；**本项目仅研究一个参考点加分段线性损失倍数的子模型，固定真实50%/50%决策权重不扭曲**，不是整个1979理论重现，也没有取得原作者被试数据或其拟合参数。

每个世界固定人工参考点r∈{−2,0,2}和损失倍数L∈{1,2,3}，得失价值v(x;r,L)=x−r当x≥r，否则L(x−r)。确定方案S得0，另一G独立公平概率获得+3或−2。每world完整64个六bit投币来源，9world一共576个完整人工source，所有来源质量1/64。路线A逐六bit算实际风险收益及其价值并源质量平均，路线B以0.5v(3)+0.5v(−2)闭式独立导出。

关键冻结条件：r=0、L=2时风险彩票的预期参考价值−1/2，确定零值0，模型偏好确定方案；仅把参考点改为r=2时，同一风险G参考值−7/2、确定S为−4，偏好风险方案，**排序反转**。但L=1全三个参考点的风险减确定差恒为+1/2。参考点/损失厌恶的效果不是从真实受试心理实验推断，而是函数结构直接代数结论。

第三独立机器源码不导入原模拟器，逐CSV检查所有六bit原始轨迹、每源价值、9种闭式矩、SHA256。所有人工世界都保留完整负得失，未挑数据支持命题。依然缺失1979论文完整累积概率权重和被试E2真实效度；不能据此称已验证描述性前景理论。

## 验收记录及源保全

全部来源：[R288_ALL_576_ORIGINAL_REFERENCE_LOSS_SOURCES.csv](R288_ALL_576_ORIGINAL_REFERENCE_LOSS_SOURCES.csv)，共576个带机制标签原始数学配置，9个人工世界；[解析和枚举结果JSON](R288_EXACT_REFERENCE_RESULTS.json) · [SHA256机器凭证](R288_MACHINE_RECEIPT.json) · [运行源码](r288_exact_reference_loss.py)。原CSV SHA256 `8f7df1a741d0f472667fe0eceed2544791051d034d7f2e5fa2c2dbbadafcda4e`，结果JSON SHA256 `ae5d955f29aad941e2cb7a3f1b8912667360b165011b2a3ff226493706609e28`。

[GitHub Actions run39910074038](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39910074038)三个作业全部completed/success，Python3.11与3.12各81个**真实运行**的unit test，共162通过；第三独立审计执行[不导入原模型的审核代码](../catalogue_audit/independent_r287_r289_source_audit.py)，直接逐CSV重建所有原来源、精确质量、实际结果、独立数学解析和SHA。所有原CSV/结果JSON/摘要经机器人永久main归档[提交301c10dd](https://github.com/edwardsage419/Psychohistory-Research/commit/301c10dd25d5bc0a6e827e0c62a15ef8edccd53b)。

正式研究决定：**CLOSED_BOUNDED_E1_ARTIFICIAL_R288_MODEL_MECHANICS**，原01-002获得一个独立、可复现、仅人工数学范围的主R。未读取真实个体被试的trial-level资料，未实现完整原作者具体实验复现，新增真人E2=0、真实历史E3=0，R073及PESEN v0.1维持冻结。其它早期研究包可能已包含文献介绍，后续避免重复计为独立实验。下一项按照原目录剩余待核队列推进。
