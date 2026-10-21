# R155 Bass 1969技术采纳扩散｜75组数学场景、96项测试、原刊3行参数复算

2026-10-21。原既定模型目录 **P1 / 06-013 Bass Diffusion Model**。正式状态 **CLOSED_BOUNDED_E1**。本期首次针对该模型实际查看 [Bass 1969年原始论文扫描](https://pdodds.w3.uvm.edu/files/papers/others/1969/bass1969a.pdf) 的原刊216至219页，并与[出版方原始DOI记录](https://doi.org/10.1287/mnsc.15.5.215)核对。完整年销量数据未取得，未重新拟合作者对11款耐用品的回归，未预测任何独立真实样本。

数学对象：原论文 \(dF/dt=(p+qF)(1-F)\)，其中\(F(0)=0\)，固定市场容量\(m\)、创新率\(p\)、模仿率\(q\)。**5种p×5种q×3种m=75种冻结组合**。各组保存t=0、1/4、1、3、5、10时的采纳率、采纳流量与市场容量换算值。独立RK4数值积分与闭式解析解逐例比较，全75×6项的最大绝对差为 **2.4×10⁻¹⁵**。

理论边界验证：p=0且无初始采用者时，即使q>0也不会启动采纳；q>p时有内部销量峰值，\(t_*=\ln(q/p)/(p+q)\)，q≤p时销量峰值在时间原点。两种不同m和p组合可能具有相同初始流量mp，但未来路径不同。人工p=.2、q=.8、Euler步长10会错误得到采纳比例2，而连续解析解在t=10为0.99977304156678。

作者原表算术核验：原刊第218页Table I中冰箱、冷冻柜与黑白电视三个产品的公布p、q、m参数已逐项转录并独立代入模型峰值公式计算。峰值时点分别为20.211910、11.866076、7.879661个作者系数时间单位；对应最高首次购买率约2209.307、1149.500、7493.138千单位/时间。其意义严格限于**对原表四舍五入后参数的数学推导**，不是历史销量外部检验。

**验证与归档：** [首次CI run39519390119](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39519390119)双Python环境各96个真实单测成功；[固定四项SHA256再运行CI run39519534803](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39519534803)双环境各96个测试，独立归档任务另96个，全部成功；累计480次单元测试执行、不同方法96项、失败0。结果JSON和完整源码、测试ZIP已在[归档提交b7891cb](https://github.com/edwardsage419/Psychohistory-Research/commit/b7891cb30ef47d07a3bd3a6ed2b4709e6ceb9ae0)永久进入main。

材料：[计算前冻结协议](../../protocols/R155_BASS1969_75_DIFFUSION_SCENARIOS_SOURCE_TABLE_PRESCORE_FREEZE_2026-10-21.md)（提交ff1c9ea）｜[完整学术报告](R155_SCIENTIFIC_REPORT_2026-10-21.md)｜[完整75组结果JSON](R155_EXACT_RESULTS.json)｜[源码测试ZIP](R155_Bass_75_Worlds_96_Tests.zip)｜[正式机器验收收据](R155_FINAL_MACHINE_ACCEPTANCE.json)。

四项SHA256：
* 代码 `5f7fe3a8b539f449906669468f39f401fa62a74e45250271589f61715c7dc5c2`
* 测试 `8f61e0635f124c05f91003c8d1f2e240824548a5cb4986d360a2b0aeb25ca9c6`
* 结果 `0b0be2d0edd4ed0564504d97e4dddd417a42f17674e25717649cac672b88949a`
* ZIP `03bea5d262c63b687ba10a097a3465c584841901adcb5fe47bd7b95daf0fdec1`

复算：在 `research/R155` 中执行 `python r155_bass_continuous.py > R155_EXACT_RESULTS.json` 及 `python -m unittest -q test_r155_bass_continuous.py`。仅使用Python标准库；ZIP为ZIP_LZMA。

**科研等级仍为E1，新增真人E2=0、历史外推E3=0。** R073及PESEN v0.1继续FROZEN。下一原目录 **R156 P2/06-014 Endogenous Growth Models**，按既定顺序完成所有R之后再归纳分类、最后模型熔炼。
