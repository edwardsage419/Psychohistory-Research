# R151 科学报告 | Leslie 1945 年龄结构矩阵和 Keyfitz 1971 人口惯性问题的有限数学研究
日期 2026-10-20；目录原候选 P1 / 06-009 Age Structured Population Models。证据级别：一手出版信息核验 + **自行构造数学 E1**；新真人外部预测 E2=0；新历史事件预测 E3=0。

## 一手文献核验（访问权限如实声明）

P. H. Leslie (1945), “On the Use of Matrices in Certain Population Mathematics,” *Biometrika* 33(3):183–212, DOI [10.1093/biomet/33.3.183](https://doi.org/10.1093/biomet/33.3.183)，[Oxford出版方原刊条目](https://academic.oup.com/biomet/article-abstract/33/3/183/215959)。P. H. Leslie (1948), “Some Further Notes on the Use of Matrices in Population Mathematics,” *Biometrika* 35(3–4):213–245，DOI [10.1093/biomet/35.3-4.213](https://doi.org/10.1093/biomet/35.3-4.213)，[原出版方条目](https://academic.oup.com/biomet/article-abstract/35/3-4/213/280269)。Nathan Keyfitz (1971), “On the Momentum of Population Growth,” *Demography* 8(1):71–80, DOI [10.2307/2060339](https://doi.org/10.2307/2060339)，[原出版书目信息](https://pubmed.ncbi.nlm.nih.gov/5163984/)。原期刊的1945和1948全文属于需要访问权限的论文，本期仅核验原出版社条目；Keyfitz正文也未全文获取，严格禁止声称“已完整阅读原作者原始数学推导”或“复制原始回归/人口数据”。本报告**没有原作者历史人口样本**；下面的矩阵、参数和所有数值均为心理史学本项目另行设定，并非原论文实验/定理数值的复现。

## 与 R150 区分
R150使用单总人口粗出生率b与粗死亡率d计算人口净存量变化，不能跟踪生育年龄组随时间的移动。R151单独引入**幼年J、生育年龄组A、老年O**三个等价人口组。每一离散时间步对应一轮队列移动，但不映射具体自然年数；模型不分性别、不含国家迁入迁出经验数据、不将高龄者无限期保留在最后组，也不宣称真实更替生育率/TFR。

## 冻结协议与数学结构
计算代码之前，正式冻结协议commit `adb7319a1b8b3acbad6cecea3c9f62ab83fe4722`， [R151预注册协议](../../protocols/R151_LESLIE1945_KEYFITZ1971_AGE_COHORT_MOMENTUM_1092_CASES_PRESCORE_FREEZE_2026-10-20.md)。

项目自建基准有理矩阵：
\[
x_{t+1}=Lx_t,\quad
L=\begin{pmatrix}0&1&1/2\\3/4&0&0\\0&2/3&0\end{pmatrix},\quad x_t=(J_t,A_t,O_t)^\top .
\]
直接从模型：出生B=A+O/2，幼年存活3J/4，成人存活2A/3，老年为终末队列。死亡分账D=J/4+A/3+O，故每期严格满足
\[
N_{t+1}=N_t+B_t-D_t+M_t.
\]
这里N=J+A+O是人工期望人口单位，可为分数，无整数随机抽样。特征多项式
\[
\det(\lambda I-L)=(\lambda-1)(\lambda+1/2)^2
\]
具有首特征根1和其余负半衰减特征根−1/2（重根）。基准右平稳年龄分布的归一化份额
\[
w=(4/9,\;1/3,\;2/9),\quad Lw=w,
\]
左不变的“生殖价值”线性泛函
\[
v=(1,\;4/3,\;1/2),\quad vL=v,\quad v\cdot w=1.
\]
因此在此**特定人工矩阵**下，任意期v·x保持不变，而极限总人口N∞=v·x0；非主导模式因绝对值1/2而衰减。更强地，可对任意有限整数t直接复算闭式
\[
N_t=C+(a+bt)(-1/2)^t,\quad C=v\cdot x_0,\;
a=N_0-C,\;b=3C-N_0-2N_1.
\]
全式由项目矩阵线性代数得出，**不是作者原作数学公式的逐行复制**。对全部91个初始年龄组合及全部13个t=0…12时点，机器用Fraction独立验证等式和v值守恒，未使用浮点特征向量。

## 全范围预注册实验：1092 种合成队列
枚举全部三个非负整数年龄组份额J+A+O=12，共二项组合数C(14,2)=**91**组；再独立取生育乘数k∈{0,1,3/2}，幼年存活sJ∈{1/2,3/4}，生育年龄组存活sA∈{1/2,2/3}，合计91×3×2×2=**1092**个完全指定情景。每情景12期、保存13个精确有理数年龄向量及12期出生、死亡流量，总计全部原JSON854kB左右。所有结果先经两条互不共用状态更新公式的路径逐年比对：(1)显式 Leslie-like 三维矩阵乘法，(2)独立出生流、各组存活和死亡的账本会计，逐年要求一致。k=0的全部91×2×2=364情景，到第3期必然归零；不能假定老年终末组一直存活。

**同人口规模、同参数、不同年龄构成**的严格人工极端对照：
| 初始结构J,A,O | 初始总人数 | 长期总人数极限C |
|---|---:|---:|
| 900,0,0 | 900 | 900 |
| 0,900,0 | 900 | 1200 |
| 0,0,900 | 900 | 450 |

**更强的相同前两期总量、之后分化**：
- 初始(400,300,200)是平稳结构，N0=900，N1=900，N2=900，长期C=900。
- 初始(120,360,420)，N0=900，N1=900，但N2=1395/2=697.5，长期C=810。
这证明：在所定义模型中，仅两期汇总总人口的数据，不足以区分潜在年龄结构和之后人口轨迹；**不证明任意多期总量都不可识别，也没有在真实人口数据上完成可辨识性/统计误差评估**。

## 冻结的同人数不同年龄移民对照
起始平稳队列(400,300,200)，仅在第一次投影结束后额外加入2个不同年龄组单位；其他时期均不迁移。
- +2幼年：第一期后的不变C=902，即与无移入长期人口差2。
- +2生育年龄组：第一期后的不变C=2708/3，即长期人口相对无移入增加8/3。
- 对照无移入C=900。
虽然**迁入人口头数同为2**，最终替代人口影响不同。该差异完全来自人工生殖价值权重，不涉及真实移民政策、劳动力和生育观察。不得用这种方程给出实际国家人口或政策决策建议。

## 复现与科研验收
核心源码 [r151_leslie_age_exact.py](r151_leslie_age_exact.py)、实际105项测试 [test_r151_leslie_age_exact.py](test_r151_leslie_age_exact.py)、全1092轨迹JSON [R151_EXACT_RESULTS.json](R151_EXACT_RESULTS.json)、永久压缩源码/测试/数据包 [R151_Leslie_Keyfitz_1092_Cohorts_105_Tests.zip](R151_Leslie_Keyfitz_1092_Cohorts_105_Tests.zip)，均已在GitHub main以真实文件存在。ZIP Python标准库zipfile及ZIP_LZMA读写，不依赖第三方包；执行
`python -m unittest -q test_r151_leslie_age_exact.py`，
`python r151_leslie_age_exact.py > rerun.json`，
然后 `cmp rerun.json R151_EXACT_RESULTS.json`。

源码Git blob `7a14789ae08af850aad26c4ad2d89455b74f9343`；测试Git blob `f897d69518257ae656c8293d3bd6cce5f02c8266`；完整JSON Git blob `7b18a5826c66a21397a263792521969528e9da3d`；ZIP Git blob `e5eccb09306688ccfda1f79163f990e9d3e817f0`。SHA256：
- 源码`429102f53ffa282adaaf93237ded08b9dd07ffdf638a454798fa30b51908c870`；
- 测试`7f5f8dc8bcedd3a5c6471983baa6ad843274ae2eafdfb97932a6740578d1677b`；
- 原JSON`a0310f8f5352d623c7c76f8b7aded64839788d45329af750b7404aa669bcaf86`；
- ZIP`38d992ca797c6be8d69eb728e03c772fcfc6fe1f0e2ee63cd037980809d37a68`。

[第一次两环境独立CI run39423248522](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39423248522)：Python3.11/3.12各105项测试、共210次，原全JSON与两个生成ZIP的 SHA256在两版本中完全一致，上传了两个可下载完整工件。

[第二次固定哈希、自动永久归档CI run39423735601](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39423735601)：双Python环境再次各105项真实测试，总计210次、0失败；额外“publish-frozen-exact-results”独立第三个任务在两套全绿后再生成完整JSON和完整ZIP，分别按上述四个SHA256与两Git源对象验算通过，最终真实推送完整原JSON/ZIP至main，归档提交 `7701e9d2ee787eb7b344286c740c1d468ed99be7`。原始两次重复测试累计420次机器执行，但**只有105项不同单测；重复多机器验证不等于420项独立不同研究假设**。远端最终验收记录另见 [R151_FINAL_MACHINE_ACCEPTANCE.json](R151_FINAL_MACHINE_ACCEPTANCE.json)。

本期结题只能标记 **CLOSED_BOUNDED_E1**，不得主张原始作者全文实验复现、真人预测验证、现实历史精准人口预报。R073/PESEN v0.1继续冻结。下一目录原候选 P1 06-010 Gravity Models of Migration（拟R152）。优先完成全部原R模型，之后统一分类归纳，最后熔炼。
