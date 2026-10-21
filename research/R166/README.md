# R166 文化选择模型｜48组有限群体文化选择与偏向转化的识别实验

日期：2026年10月21日。原始候选目录 **P1 / 07-008 Cultural Selection Models**。科学等级 **CLOSED_BOUNDED_E1**，仅为项目自建离散文化符号的精确数学实验。

## 文献关系纠错

原目录把 R166 的代表原始资料标为 `R19`。通过[真实GitHub Actions审计39532579568](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39532579568)读入此前永久归档的[原始R019研究包](../../archives/library-originals/心理史学_R019_正式研究包_2026-10-14.zip)，核实该包为**私人信念与公开发言的双网络先行理论审查**，共9份文件，ZIP SHA256为`080a786f4bd064494f8c57a7ec0cc32f183d2020e3eb643a0ea69881a721d797`，与本次文化选择研究主题不相符。原始R019压缩包保持不变。R166新建的[资料审计与纠错记录](R166_SOURCE_DEPENDENCY_TRIAGE_2026-10-21.md)明确区分档案存在、资料主题与科研验证等级。

重新核验[Mesoudi 2021年原刊](https://doi.org/10.1098/rstb.2020.0053)及作者公开[原生`model1.R`](https://github.com/amesoudi/culturalselection_biasedtransformation/blob/master/model1.R)，固定作者脚本Git blob SHA1 `1d2c4fa8db1d52ecfb3a233a7e6a216867e5c42c`。作者模型有连续文化特征、按概率复制价值最高示范者、采用指数修正高斯偏向变异及0到100的边界；该源码确实已阅读，**没有在本研究中执行作者原始R脚本，也没有复制原作者图表或真实数据**。另核查[Claidière等2014原刊](https://doi.org/10.1098/rstb.2013.0368)与[Boyd/Richerson1985出版方目录](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html)。

## 冻结模型与机制

[事前冻结协议](../../protocols/R166_CULTURAL_SELECTION_VS_TRANSFORMATION_48_FINITE_WORLDS_PRESCORE_FREEZE_2026-10-21.md)已先于源码在提交[1a55a14](https://github.com/edwardsage419/Psychohistory-Research/commit/1a55a14a67cc3b1386f73c83fd3beb03017d07a5)固定。

群体规模4或8人，每个群体设定4个初始文化A人数；三种人工条件为中性、偏向A、偏向B。每种条件分别构造两种不同机制。

**文化选择：** 根据原有A/B示范者权重`wA/wB`抽样，概率为\(q_s=w_Ap/(w_Ap+w_B(1-p))\)。

**偏向转化：** 随机复制后，以人工概率a把B转换成A，以b把A转换成B，概率为\(q_t=p(1-b)+(1-p)a\)。

共 **2个人数档×4个初始人数×3种条件×2种机制=48组**；每组保存t0到t4的完整人数分布。12套完整转移矩阵、48×5组完整概率路径与期望频率全部保存在[116,861字节原始JSON](R166_EXACT_RESULTS.json)。直接二项式有理数计算与独立模拟全部2^N种理论下一代组合的穷举概率法**逐个Fraction完全匹配**。

## 主要反例与模型边界

* 起点A占1/2时，偏向A的选择模型和偏向A的转化模型都以2/3概率生成A；**第一代全部人数分布完全相同**。偏向B则对应两者均为1/3。单凭这样的一个观察无法区分机制。
* 起点A占1/4时，偏向A的选择模型生成A的概率为2/5，转化模型则为1/2，因此不同初始条件可以区分它们。
* 对于N=4且初始k=2的偏向A世界，完整第一代分布完全相同，第二代的总变差距离精确为\(41284561/1093955625≈0.03773878945\)。第二代A期望频率分别为选择模型\(2192/2835≈0.77319224\)和转化模型\(7/9≈0.77777778\)。不同机制需要多期观察来进一步检验。
* 在偏向A世界中，A原本完全不存在时，单纯选择不能凭空创造A，而定向把B转为A的模型仍可生成A。该边界直接依赖模型中是否存在转化过程。
* 中性条件下，本阶段两种机制**都与已结题R165（零创新）精确二项式矩阵一致**，测试直接引用R165冻结程序检验。该重复基线没有计作新的外部科研证据。

模型适用于抽象离散两文化类型概率，**不代表人类真实文化选择心理模型、真实的文化价值评价、作者原始R的连续偏向变异，或历史事件预测**。

## 验证、证据及永久归档

[第一轮GitHub CI39533161253](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39533161253)与[固定SHA256并永久归档轮39533242415](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39533242415)均成功。Python3.11和3.12两轮各运行84项真实单测，最终独立归档任务再次执行84项，累计**420次实际测试执行，84种不同测试方法，0失败**。代码、完整JSON和源程序测试ZIP固定四项哈希并在[归档提交01234cb](https://github.com/edwardsage419/Psychohistory-Research/commit/01234cbdbf6cc38fd5285289d4b73aed299c6377)永久写入main。

全部材料：[正式科学报告](R166_SCIENTIFIC_REPORT_2026-10-21.md)｜[事前协议](../../protocols/R166_CULTURAL_SELECTION_VS_TRANSFORMATION_48_FINITE_WORLDS_PRESCORE_FREEZE_2026-10-21.md)｜[资料纠错记录](R166_SOURCE_DEPENDENCY_TRIAGE_2026-10-21.md)｜[源码](r166_cultural_selection_transformation_exact.py)｜[84项单测](test_r166_cultural_selection_transformation_exact.py)｜[完整JSON](R166_EXACT_RESULTS.json)｜[源码测试结果ZIP](R166_Selection_Transformation_48_Worlds_84_Tests.zip)｜[正式机器验收](R166_FINAL_MACHINE_ACCEPTANCE.json)。

SHA256：
* 源码 `37874e66c0b68c96d3e97f7dfb1e907dc7b9596c963b1471000668517b5148f3`
* 测试 `1744b160f6af1583ea086da2f8c982bad5a304d03c709dfaa6cbafb7dca0008d`
* JSON `ff50f5555841bac54db308c517543158ed3efc004cf4be42de4c6f3a3299e3a8`
* ZIP `831a2bac01b992ac1943e4e213db3ebdca2d4bec067ad317ee53ef92e32dea30`

复算：在 `research/R166` 运行 `python r166_cultural_selection_transformation_exact.py > R166_EXACT_RESULTS.json` 和 `python -m unittest -q test_r166_cultural_selection_transformation_exact.py`。跨阶段测试需要仓库相邻的R165模块；仅依赖Python标准库。

本阶段新增E2=0、E3=0；R073、PESEN v0.1保持冻结。下一模型原目录 **R167 P2/07-009 Cultural Group Selection（文化群体选择）**。继续先完成全部R系列，再统一归纳，最后模型熔炼。
