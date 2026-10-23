# R267 Latin Hypercube Sampling：九个人工三层二维网格、6885全部原source、同预算LHS与IID方差反例，事前冻结

日期：2026-10-23 Asia/Taipei。原239候选目录11-027 Latin Hypercube Sampling（P1），研究编号R267。第一来源McKay, Beckman & Conover (1979), Technometrics 21(2):239–245, DOI https://doi.org/10.1080/00401706.1979.10489755；Stein (1987), Technometrics 29(2):143–151, DOI https://doi.org/10.1080/00401706.1987.10488205 。原文含连续变量和渐近结论；本项只使用离散人工3×3格点证明有限条件下的边界，不声称逐字节复现两篇论文、连续LHS或高维渐近最优性。

## 完全冻结来源、函数及设计
基础X,Y独立且均匀分布在{0,1,2}，真实积分为全部九格f(x,y)的算术均值；每次抽样预算恰好三个f评价。
IID：抽取三个独立格点(x_i,y_i)，各来自9格均匀，原样本空间为9³=729个等质量source（每源1/729）。
LHS：独立随机排列X三个层级与Y三个层级，按位置一一配对。完整两排列原空间3!×3!=36个source（每源1/36），每个坐标层级恰好用过一次。位置排列对估计均值没有影响，但须保留原全部36个取值设计；不能把6个相对排列冒充36个原source。
九个冻结world（每world一个f）及均值:
1 ADD_X: x, mean=1;
2 ADD_X_PLUS_Y: x+y, mean=2;
3 ADD_SQUARES: x²+y², mean=10/3;
4 PRODUCT_XY: xy, mean=1;
5 CENTERED_INTERACTION: (x-1)(y-1), mean=0;
6 EQUAL_INDICATOR: 1[x=y], mean=1/3;
7 MODULAR_SUM: (x+y) mod 3, mean=1;
8 THRESHOLD_SUM_GE2: 1[x+y≥2], mean=2/3;
9 CORNER_22: 1[x=2 and y=2], mean=1/9.
全冻结来源：9×(729+36)=**6885个原source类型**；源文件逐原设计记录世界、三对独立/配对的坐标序列、每次函数值、原概率质量、估计器、真实均值及平方误差。完全人工概率空间，非6885个真人或实际随机抽样结果。

## 两条数学路线和第三解析式
路线A遍历九世界所有729 IID与36 LHS源，逐有理质量求所有18个p帽完整PMF、均值、方差、bias、MSE。每设计各世界来源唯一、全质量1。
路线B不依赖路线A的原source枚举。IID使用九格f值的单次分布进行三次离散卷积；LHS根据x层级固定顺序，遍历全部3!=6个相对y排列，等质量1/6构造完整PMF。要证明36源原排列与6相对排列是同一估计分布，不能只靠恰好一样的方差。
第三解析式：IID样本均值方差Var(f(X,Y))/3，LHS采用双向残差r_ij=f(i,j)-mean_row_i-mean_col_j+overallmean，方差=sum_{i,j}r_ij²/[n²(n-1)]=sum r²/18（n=3）。如果纯加性f=g(x)+h(y)，全部残差0，离散三层完整覆盖可以得零方差；有交互残差时不保证LHS降低小样本误差。

## 事前冻结九世界均值和方差真值
|world|真实均值|IID方差|LHS方差|LHS/IID|
|---|---:|---:|---:|---:|
|ADD_X|1|2/9|0|0|
|ADD_X_PLUS_Y|2|4/9|0|0|
|ADD_SQUARES|10/3|52/27|0|0|
|PRODUCT_XY|1|16/27|2/9|3/8|
|CENTERED_INTERACTION|0|4/27|2/9|3/2|
|EQUAL_INDICATOR|1/3|2/27|1/9|3/2|
|MODULAR_SUM|1|2/9|1/3|3/2|
|THRESHOLD_SUM_GE2|2/3|2/27|1/27|1/2|
|CORNER_22|1/9|8/243|2/81|3/4|

两个设计在九世界均无偏，MSE=Var。前三个加性函数固定三层抽样LHS方差0；中心化交互、相等事件和模3函数三项LHS反而比IID大50%。这构成有限n和离散取点下“LHS总比IID方差小”的反例，与Stein (1987)的大样本渐近结果并不矛盾。

## 验收门槛及边界
冻结协议必须先于程序。源码需无第三方依赖、双Python3.11/3.12各至少45项真实测试、完整6885源CSV、18组PMF双路线精确一致、独立网格残差公式核验、永久GitHub机器归档与SHA256凭证、真实三job全绿后才能结题E1。离散网格无连续分层区间内随机jitter，未涉及相关X/Y分布；没有新真人E2或真实历史E3，R073与PESEN v0.1冻结。完成原R学习前不开始熔炼，R268主题再查原目录。
