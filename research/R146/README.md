# R146 | Meltzer–Richard 1981：多数投票、劳动供给和财政再分配

日期：2026-10-20。原239模型目录 P2 / 06-004 Political Economy Equilibrium Models。

一手论文：Allan H. Meltzer and Scott F. Richard (1981), *A Rational Theory of the Size of Government*, *Journal of Political Economy* 89(5):914–927, DOI [10.1086/261013](https://doi.org/10.1086/261013)。[Haverford保存的原刊全文扫描](https://www.haverford.edu/sites/default/files/MeltzerRichard-RationalTheory.pdf)，真实核验原刊917页Eq(1)，918页Eq(2)–(4)，920页Eq(13)决定性选民的最优税率，921页相对生产率排序与投票权，922页Fig1及Eq(15)。**本研究的二次劳动成本/线性消费效用不是原作者严格凹的消费—闲暇效用，属于项目原创的可复算特例，不是原作者完整数值模型重现。**

固定居民人口5、7、9，每人生产率取{0,1/4,1/2,3/4,1}，所有升序多重集合 **126+330+715=1171种人工经济**，没有人工随机抽样或真人记录。单一税率t∈[0,1]，均等转移全部居民且预算恒等平衡。个人视转移为既定时，劳动n_i=(1−t)x_i，私人支付后效用为$U_i=(1−t)^2 x_i^2/2+t(1−t)\overline{x^2}$。中位投票者根据本例独立分析有理数最优税率，且在21个政策税率网格下用全选民原始劳动/税收帐簿独立计算两两简单多数比较。

主要结论：
- 1171种分布连续中位选民均衡税率为正751种，税率为0共420种，**其中3种全部零生产率样本实际对所有税率无差异，因此选0是预设的选举平局口径，不是唯一均衡**；
- 基准9居民经济平均平方生产率$4/9$、中位数平方生产率$1/4$，连续中位决定税率$7/23$；仅提高一位高生产率居民，平均升至$71/144$且中位数不变，税率升至$35/106$；
- 如果决定性选民也变化，一例平均平方生产率从$5/28$升至$2/7$，中位平方生产率从$1/16$升到$1/4$，税率反从$13/33$降为$1/9$。不能概括为“平均收入更高一定增加税率”；影响由**平均与决定性选民相对位置**共同决定；
- 固定9居民的税基/转移人群，投票资格调整为五位最富者时中位决定性税率从$7/23$降到0。绝不可通过直接剔除居民改变税基并把它误当投票权改革；
- 固定劳动量的错误对照中，低于平均生产率的中位选民会倾向t=1；内生劳动反应则使本例均衡小于1/2。税收扭曲是真实需要纳入的数学机制，但不构成实测政策福利大小的历史证据。
- **本项目效用的消费边际效用是常数**，缺少作者u(c,l)的财富效应与正态效用边界；有限居民在策略上仍视总转移为既定。这两个刻意假设的限制必须先于任何外推。

[事前冻结协议](../../protocols/R146_MELTZER_RICHARD1981_MAJORITY_REDISTRIBUTION_LABOR_ENDOGENOUS_EXACT_PRESCORE_FREEZE_2026-10-20.md) | [完整科学报告](R146_MELTZER_RICHARD1981_REDISTRIBUTION_MAJORITARIAN_TAX_EXACT_SCIENTIFIC_REPORT_2026-10-20.md) | [完整源码、113项测试与全部1171经济JSON ZIP](R146_MeltzerRichard1981_113_Tests_1171_Economies.zip) | [正式验收状态](R146_FINAL_ACCEPTANCE_STATUS.json) | [GitHub CI](../../.github/workflows/r146-meltzer-richard-113-tests.yml)。

原始ZIP采用标准Python支持的ZIP BZIP2压缩，解压请运行 `python -m zipfile -e R146_MeltzerRichard1981_113_Tests_1171_Economies.zip out`，在out目录执行 `python -m unittest -q test_r146_meltzer_richard_exact.py` 及 `python r146_meltzer_richard_exact.py > replay.json`。JSON使用有序无损的8字段位置模式存储每种分布，无须外部依赖。本期新真人E2=0、历史E3=0，R073/PESEN v0.1冻结。先完成全部R研究，再统一归纳分类，最后熔炼。
