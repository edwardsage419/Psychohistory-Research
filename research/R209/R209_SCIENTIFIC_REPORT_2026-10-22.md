# R209 创新扩散补充研究：36人工世界、完整独立两轮轨迹与结构性机制不可辨识

日期：2026-10-22（Asia/Taipei）。归档编号R209，**原239目录的关联补充研究，非独立catalogue条目**；科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_TWO_ROUND_ADOPTION**。原239项JSON不存在先前预冻协议误填的`08-033`，已经在[目录映射校正公告](../../docs/R_SERIES_CATALOG_MAPPING_CORRECTION_2026-10-22.md)透明说明。此次数学工作与原目录`04-005 Simple versus Complex Contagion`、`06-013 Bass Diffusion Model`概念有关，**不是**任何一篇原作者完整模型的复现，更没有真人数据。下一按真正239目录需要开始`09-001 Randomized Controlled Experiment`，可登记为R210，但R208/R209补充研究不可抵扣239条目的覆盖率。

## 原文起点与此次自造机制的区别

* Bass, F. M. (1969), [A New Product Growth for Model Consumer Durables](https://doi.org/10.1287/mnsc.15.5.215), *Management Science* 15(5):215–227，原著以创新者和模仿者与购买时间探讨耐用品采纳，并分析历史消费品样本。此次未实现其完整微分增长方程或使用原样本。
* Granovetter, M. (1978), [Threshold Models of Collective Behavior](https://doi.org/10.1086/226707), *AJS* 83(6):1420–1443，讨论临界他人数量和集体行为，警惕只看平均数忽略阈值分布。此次四人两轮Bernoulli风险不构成该原模型完整实现。
* Centola, D. and Macy, M. (2007), [Complex Contagions and the Weakness of Long Ties](https://doi.org/10.1086/521848), *AJS* 113(3):702–734，强调复杂传播需要来自多个联系来源的社会强化；此次只模拟一个固定“至少两名不同已采用邻居”的假定概率规则。

**事前冻结**：[原人工机制与来源协议](../../protocols/R209_ADOPTION_36_WORLDS_972_TRAIN_26244_INDEPENDENT_PRESCORE_FREEZE_2026-10-22.md)，提交[deebc102](https://github.com/edwardsage419/Psychohistory-Research/commit/deebc1026000555d89923ba701262826556b53d8)，发生在执行与评分前。原协议的研究设计与定量规则从未根据观察到的评分调整。协议误填原目录`08-033`是**元数据错误**，保持原版本不回写，以独立的校正公告记录，避免伪装始终准确。

## 三类真实来源、三图×四种seed和两轮完整采用轨迹

固定4人0..3，STAR边(01,02,03)、PATH边(01,12,23)、CYCLE边(01,12,23,30)，共三图；每图初始唯一已采用者seed=0,1,2,3四种。两轮同步更新t=1,2，已采用者永久保持采用，尚未采用的其他3人对前一轮结束时的已采用邻居数量k独立抽样：
* BASE：无论k，首次采用概率1/4；
* SIMPLE：k≥1时概率3/4，否则1/4；
* COMPLEX：k≥2时概率3/4，否则1/4。
三者真实来源同时是三个训练时可选候选；同分时按 BASE、SIMPLE、COMPLEX 先后优先。完整采用轨迹把seed的采用时间记0、其他每人的首次采用时点记为1、2或3（3表示两轮内一直未采用）。因此每图、seed、真模型有3³=27条完整真轨迹且各条概率严格大于0，三图×四seed×三真模型=**36个纯人工源世界、972条完整原始训练轨迹**。每个模型的27条轨迹概率通过六或更少真实Bernoulli条件因子逐Fraction求出、和为1，全部原记录永远保存。

从一条真实人工训练轨迹根据三个固定候选的完整离散概率最大值决定预测机制，不调用任何真实来源名或未来信息。然后**全新独立重抽**同图、同seed、同真正机制的另一条两轮采用轨迹。对每个训练来源严格枚举27种新测试原轨迹，组成**972×27=26,244条真正训练×独立新轨迹联合来源事件**；每条真正联合来源概率 P_true(train)·P_true(test)，组内加和为1。全部真实新轨迹采用时点、完整模型新轨迹概率、新轨迹logscore和新期末2+新增采用事件的Brier逐原来源保留。

**两个测试目标各自独立**：第一是完整27类别离散轨迹负对数评分−ln P_selected(test)，训练以精确Fraction概率比较不需要log，独立新评分由math.log计算并对每个不同真实Fraction概率用70位Decimal对数交叉核验。第二是新两轮到期时新增采用人数≥2的二元Y，新概率q来自已选模型27路径完整求和、每条新实际测试路径误差(q−Y)²，先按27个新来源再按27训练来源完整Fraction加权；双路核验与严格解析 Bernoulli 最小真实来源风险 p_true(1−p_true)+(q−p_true)² 一致。Oracle预知完整真实真机制的独立logscore与Brier、固定始终BASE模型分别当作不同权限的明确对照，不偷看未来真轨迹调选模规则。

## 完整三图×三真机制、每组四种seed等权的独立预测

不同机制在不同网络结构下的概率分布未必可被观察区分。以下都是四种事前固定seed设计条件**各权1/4**之内、用真完整独立来源加权的期望分数；分数越小越好，不能把四seed当作四项现实重复实验。

|图|真实机制|平均新增采用数|选模后独立完整轨迹logloss|固定BASE完整轨迹logloss|预知真机制oracle完整轨迹logloss|
|---|---|---:|---:|---:|---:|
|STAR|BASE|1.312500|3.107028|2.952260|2.952260|
|STAR|SIMPLE|2.484375|2.960064|4.023934|2.530508|
|STAR|COMPLEX|1.435547|3.170658|3.087440|2.952260|
|PATH|BASE|1.312500|3.145186|2.952260|2.952260|
|PATH|SIMPLE|2.402344|2.892486|3.933814|2.530508|
|PATH|COMPLEX|1.417969|3.260377|3.068129|2.952260|
|CYCLE|BASE|1.312500|3.171970|2.952260|2.952260|
|CYCLE|SIMPLE|2.664063|2.754991|4.149421|2.389924|
|CYCLE|COMPLEX|1.523438|3.412208|3.183998|2.952260|

同一36世界的**独立2+新增采用事件 Brier、各候选完整训练选中概率、模型分布是否精确相同、完整真source概率**均已单独写入 [36世界精确结果](R209_EXACT_RESULTS.json) 和 [972条原训练](R209_ALL_972_ORIGINAL_TRAIN_ADOPTION_TRAJECTORIES.csv)，不能从这张logscore表凭猜测推断二元Brier会同向改善。

总体显示：真SIMPLE在STAR/PATH/CYCLE上，只有一条完整训练轨迹时允许三机制选择依然获得比固定BASE更好的独立新完整轨迹分布评分，但与已知真实机制的先验oracle仍有差距。真BASE或真COMPLEX时，同一选模程序的完整新轨迹logscore反而通常**明显差于**固定BASE；因此仅凭允许更多机制候选，不保证更好的独立预测，也不能把训练对已知机制的准确识别率等同于新轨迹预测质量。

## 机制审计一：存在完全同分布的不可辨识设计

**STAR seed=0（中心先采用）**：中心已经采用，其他叶子每个只连着中心，全部未采用者一生最多只有一个已采用邻居，COMPLEX的k≥2条件对任何仍有机会采用者永远不可能发生。因此任何完整两轮轨迹在COMPLEX下的概率**逐27路径精确等于BASE**，没有任何样本差异可以恢复真模型身份。在同分优先BASE的候选选择规则下，如果真生成机制标签为COMPLEX，选中其自身的概率**0**；真生成BASE时可选中BASE的概率945/1024，剩余概率选SIMPLE，COMPLEX仍是0。该不可辨识性**不是多拿几个同图同seed样本就能靠拟合解决的估计方差**，而是给定设计没有任何符合复杂强化条件的可观察事件。

**STAR seed=叶节点1、2、3**时，COMPLEX可与BASE区分：未采用中心在第一轮除了原seed以外，其他未采用叶子可能各自按1/4自发采用；若中心至第二轮仍未采用，第二轮可能面临≥2已采用邻居，COMPLEX才有额外采用概率。这个反例严格说明**图结构、起始种子与可观察轮数**共同决定采用机制是否有可观察信息，不仅是“节点的总邻居数量”决定。

完整36世界的所有27类别概率逐Fraction比对，共发现精确等价对仅一对，即**STAR seed=0: BASE ≡ COMPLEX**。其余图/seed和候选间有真正可测分布差异，但不保证有限训练后容易分辨。

## 机制审计二：可辨识性存在，不意味着短轨迹足够识别

**CYCLE seed=0**时，COMPLEX真实为双邻居强化，只有那些在第二轮仍未采用、且上一轮邻居恰好多人已采用的节点能够表现出额外倾向。两个轮次的一条随机真轨迹大多数时候不会为这一高阈值产生足够证据，实际选中真COMPLEX概率**81/1024≈7.91%**；有**789/1024≈77.05%**概率反而选择BASE，剩余77/512选择SIMPLE。这里COMP与BASE确实不是同一真实27轨迹分布，但短期信息不足，独立全轨迹分布评分选模后**3.412208**差于固定BASE的**3.183998**，而已知真机制oracle为**2.952260**。

相反同一CYCLE seed=0，当真正机制为SIMPLE时，选中SIMPLE概率为**405/512≈79.10%**，独立完整新轨迹logloss**2.754991**优于固定BASE**4.149421**，但仍差于真oracle**2.389924**。不同机制表现差异必须限定在此p=1/4与3/4、同步两轮、四节点、seed已知、真模型在候选内的人工世界中；并没有“复杂传播在社会中更难识别”这种超范围真人实证结论。

## CI首次失败和修复记录，科学/归档证据区别

在本轮前两次CI运行中存在真正工具/代码错误，未隐藏或以成功状态替代：
* [首轮run39735323094](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39735323094) 在进入测试前发现一个单元测试中的Python括号语法错误，经[提交e8e16ca7](https://github.com/edwardsage419/Psychohistory-Research/commit/e8e16ca7946ad92a92de35b22fa719061184e418)修复，不改变研究冻结来源。
* [第二轮run39735540884](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39735540884) Python3.11与3.12两批42项测试均**success**，第三归档作业因独立验收片段导入`Fraction`却写了`F(...)`发生`NameError`，未发布不合格材料。修复验收脚本别名[提交246dc9ad](https://github.com/edwardsage419/Psychohistory-Research/commit/246dc9ad2bdff5bdca4b5380770e19ef3cf4b7a8)，同样没有调整科学拟合/评分。
* **最终正式核验**[GitHub Actions run39735660871](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39735660871)：Python3.11和3.12各**42项测试、总84项全部成功**，第三作业完整输出36世界、972原训练、26244联合新轨迹，验收两个独立评分路径、全部来源概率、文件SHA，然后**真正永久提交main**。[真正原结果归档c68e2542](https://github.com/edwardsage419/Psychohistory-Research/commit/c68e254217af9f7732990ac9e61f51cf6abe5e64)。最终三个作业均success。

永久研究材料及SHA：
* [原计算前冻结协议](../../protocols/R209_ADOPTION_36_WORLDS_972_TRAIN_26244_INDEPENDENT_PRESCORE_FREEZE_2026-10-22.md)；
* [纯Python标准库与42项单测](r209_exact_two_round_adoption.py)，运行`--test`和`--emit`；
* [全部36个世界与完全候选选择概率的主结果](R209_EXACT_RESULTS.json)，SHA256 `d57bbf5c2a093f4fc4238888ed74e9b4b71cf8802c405c73c69566a6070e9cc5`；
* [972个真正原完整训练采用来源](R209_ALL_972_ORIGINAL_TRAIN_ADOPTION_TRAJECTORIES.csv)，SHA256 `3095abfd084d65f96b5261537ccad4c9ce9a021bbb658ebb6c728b0c3fcad908`；
* [26244条真正独立重抽完整新轨迹联合来源和两个损失](R209_ALL_26244_INDEPENDENT_NEW_TRAJECTORY_PAIRS.csv)，SHA256 `e6cd09ab77224fef14f0eaa239df45e1a084ddf7ef6db62d68160e05bda61455`；
* [三个原结果文件数量、真实哈希和抽样独立性机器验收](R209_FINAL_MACHINE_ACCEPTANCE.json)；
* [事后科研结题机器记录](R209_FINAL_ACCEPTANCE_STATUS.json)，须注明catalogue_id=null及R209为补充研究。

本R仅人工条件概率机制E1；新增真人E2=0、真实历史E3=0，R073与PESEN v0.1冻结。所有R目录项目应以[原239目录JSON](../../docs/MODEL_CANDIDATE_CATALOG_v0.1.json)真实编号核对；本项不占`08-033`。**下一项R210应进入原目录实际`09-001 Randomized Controlled Experiment`**，优先完成全部原R列表后统一分类，再进行模型熔炼。
