# R263 遗传算法：九人工三bit双亲一代演化世界及9216完整外生源

日期2026-10-23 Asia/Taipei。原239目录11-023 Genetic Algorithms（P2）。正式有界科学状态 `CLOSED_BOUNDED_E1_TWO_INDIVIDUAL_THREEBIT_ONE_GENERATION_GENETIC_ALGORITHMS`；本R不包含自然或真实社会适应性研究、跨代演化、一般遗传算法全局收敛定理或真人历史E2/E3。

## 来源、先冻结协议与问题边界

John H. Holland, *Adaptation in Natural and Artificial Systems*，University of Michigan Press 1975，后MIT Press版，[出版社来源](https://mitpress.mit.edu/9780262581110/adaptation-in-natural-and-artificial-systems/)。本项仅取交叉、突变、适应度、生存选择的有限数学结构，不宣称原作者代码或长期算法数据的实证复现。[九world与全部来源数学命题先行冻结](../../protocols/R263_GENETIC_ALGORITHMS_9_WORLDS_9216_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，冻结提交[e50f5408](https://github.com/edwardsage419/Psychohistory-Research/commit/e50f54089dac1bab48bd898b3fc1f1dd89c20ebf)。

每个world两个三位bit基因组父代共6原bit，另4独立公平原位分别为交叉标记、交叉断点（1或2）及两个子代固定位置翻转触发。因此2¹⁰=1024完整外生source/world，九world**9216条完整原结构来源**，每来源设计质量1/1024。每个source按人造适应度评价原两个父代、交叉/突变候选两个子代、精英或非精英生存双个体的最佳分数，并保留全部原10bit、候选基因组、幸存者、同分选拔规则与适应度变化。这里9,216是人工算法所有原事件类型，而不是9,216名个体或现实突变序列。

世界包括无交叉/无突变克隆，单纯交叉，单纯突变，交叉+突变，以及它们的确定性**精英保留前两名**版本；第九world采用陷阱目标TRAP，000分数4、其他基因型按1位数计分，故111分数3而不是全局最优。交叉位置按指定cut交换两个父代后缀，突变仅可翻转子代0的第0位和子代1的第2位，**不是每基因位独立突变的通用GA模型**。精英生存从父0、父1、子0、子1四个可重复个体记录中按适应度降序、位串升序、原记录顺序破平手挑前两名，不做去重。

## 完整条件概率、核心数学发现

独立第一来源线路径直接按十个原bit采用Python位串切片/条件翻转/四人排序运行。**独立第二路线**不调用原source的切片重组或幸存者发生器，以三bit整数掩码重组/异或及分数排序，枚举全部64原双父代基因组和16独立算子bit模式，为每一固定双父代构建下一代两幸存者基因组的**完整有理联合概率分布**。每world64个条件父代集合上的16事件等概率1/16，两路线按重复最终基因组汇总后的全部条件联合PMF完全一致。这检验的不只是平均分，而是所有有限原算子事件的实际后代概率律。

| 人工world | 最佳适应度上升的完整原source数 | 下降的原source数 | 平均最佳适应度变化 |
|---|---:|---:|---:|
| CLONAL_ONEMAX | 0 | 0 | 0 |
| CROSS_ONEMAX | 80 | 80 | 0 |
| MUTATE_ONEMAX | 232 | 232 | 0 |
| CROSS_MUTATE_ONEMAX | 242 | 236 | 0 |
| ELITE_CLONAL_ONEMAX | 0 | 0 | 0 |
| ELITE_CROSS_ONEMAX | 80 | 0 | 5/64 |
| ELITE_MUTATE_ONEMAX | 232 | 0 | 29/128 |
| ELITE_CROSS_MUTATE_ONEMAX | 242 | 0 | 123/512 |
| ELITE_CROSS_MUTATE_TRAP | 266 | 0 | 53/128 |

注：非精英交叉+突变世界的平均最好分数变化恰0，尽管上升242/1024、下降236/1024，因正负改变幅度并非都为1。**不能用改善来源数多于下降来源数就直接断言期望改善为正。**精英world每一完整source都将两个原父代列入候选竞争，因此下一代最好分数不可能低于原最佳，这是源级逐项验证且由选择集合包含原父代的定义保证的有限数学不等式；**不推出长期演化收敛、分布外适应性或全局峰必能找到**。无突变交叉仅交换两个双亲后缀，整个双人口每个基因位置上1的总数不变；个体组合与最好分数仍可能变化，不能将基因频率守恒误称每个个体的适应度恒定。TRAP峰000=f4、111=f3是完全人为冻结的偏好结构，不能当自然适应度或现实制度福利事实。

## 三job完整CI、可复现来源及有界资格

[原生Fraction条件生存概率及两套重组算子源码](r263_exact_genetic_population.py) · [九world9216完整十bit来源CSV](R263_ALL_9216_ORIGINAL_TWO_PARENT_GENETIC_SOURCE_ATOMS.csv) · [各world源级最好分数变化及条件联合审计JSON](R263_EXACT_RESULTS.json) · [完整原CSV/JSON SHA256机读收据](R263_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39899578544](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39899578544)总体completed/success、三个job全部success；Python3.11和3.12实际日志各`Ran 82 tests`、`OK`，共**164次真实双版本测试通过**。第三独立source archive job逐world验证1024唯一十bit组合、质量1/1024、实际切片断点/突变固定bit/四候选精英排序、每来源前后适应度、独立条件后代分布机读资格、九world增长/下降/平均正确、精英永不损失、无突变交叉保留每位置总体1数、CSV/JSON SHA；日志`R263_ALL_9216_ORIGINAL_GENETIC_CROSSOVER_MUTATION_ELITISM_SOURCES_VERIFIED`与`R263_ALL_9216_ORIGINAL_GENETIC_SOURCE_ATOMS_ARCHIVED`。完整CSV、结果JSON及机器收据已GitHub bot永久归档main提交[8de31843](https://github.com/edwardsage419/Psychohistory-Research/commit/8de31843bccdf8827dba91a6bd69186b618d12d0)。

原CSV SHA256 `dcc0d852ce914b84cdbc2c07bad300d89baa7a36d503cbf4b16b62332d2f072a`，结果JSON SHA256 `42166bedb52f4551c8699c2338e88932a2922d63afee8f9e0925623c3595f581`。新真人E2、历史E3=0，R073/PESEN v0.1冻结。下一原目录11-024 Approximate Bayesian Computation（R264，P2）。
