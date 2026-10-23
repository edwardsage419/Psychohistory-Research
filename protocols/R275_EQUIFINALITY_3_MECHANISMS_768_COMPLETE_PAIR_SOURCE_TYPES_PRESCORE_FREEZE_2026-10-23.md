# R275 等效机制：三种机制、四组二元配对观察、768完整原source；先行冻结

日期2026-10-23 Asia/Taipei。原239候选目录12-005 Equifinality Analysis（P0），R275。概念源von Bertalanffy (1968), *General System Theory*, equifinality （https://www.panarchy.org/vonbertalanffy/systems.1968.html）；Ruddell et al. (2019), *Information Theory for Model Diagnostics: Structural Error is Indicated by Trade-Off Between Functional and Predictive Performance*, Water Resources Research, DOI https://doi.org/10.1029/2018WR023692；统计辨识定义参考 *Linking Item Response Model Parameters*, https://pmc.ncbi.nlm.nih.gov/articles/PMC4978781/ 。R275只建立自定义有限人工机制等效与观测分辨的数学例子，没有原作者实证复现。

## 事前冻结的人工机制
每source恰四个有序pair (A_i,B_i), i=0,1,2,3。每组pair独立，A_i~Bernoulli(1/2)。共有三种冻结生成机制：
* IID_PAIR：B_i与A_i独立，B_i~Bernoulli(1/2)。每pair四种(00,01,10,11)同为1/4；
* COPY_PAIR：B_i=A_i，各pair只有00与11非零质量，均1/2；
* FLIP_PAIR：B_i=1−A_i，各pair只有01与10非零质量，均1/2。
完整原source按4个有序二bit pair排列，共4^4=256个有序串，每个机制保留全部256原source及其精确有理概率，**包括0质量配置**；3机制共768个带机制ID的人工source配置，非零质量分别256、16、16条，合计288条。零质量来源是固定完整样本空间的占位，绝不能当作可能发生事件。三机制的**只观测A序列**联合分布完全相同，每个四bit的A向量均精确1/16，单变量成功次数、所有完整A向量分布均不能区分生成机制。

## 比较两种冻结观测设计
* PARTIAL_A_ONLY：只保留每pair的A比特；所有机制对此观测的似然为1/16。三模型等先验1/3，MAP并列时事前规则按ID顺序选择IID_PAIR。任何仅用这四条A数据的分类器，在等机制先验下的最大Bayes平均分类正确率不超过1/3。
* FULL_AB_PAIR：保存4对完整AB；在原source下IID_PAIR似然1/256，若全部四pair均相等，COPY_PAIR似然1/16（其余0）；若全部四pair均相反，FLIP_PAIR似然1/16（其余0）；其他混合pair则COPY和FLIP都是0。三模型均等先验1/3，MAP选择最大似然，严格顺序规则在并列时IID、COPY、FLIP。FULL_AB下当真模型IID时，只有所有四pair都相等或都相反时错判，因此成功概率1−2×(1/2)^4=7/8；当真COPY或真FLIP成功概率都为1。先验三机制等权Bayes平均成功率=(7/8+1+1)/3=23/24。

## 原子分布后验与核心命题
对FULL_AB观察任意全等pair序列，后验P(COPY|data)=16/17、P(IID|data)=1/17，P(FLIP|data)=0。全反序列则FLIP=16/17、IID=1/17、COPY=0。混合pair序列后验IID=1。PARTIAL_A_ONLY每个完整A四bit观察的模型后验均恰1/3。三组pair的单个A和B边缘也全为Bernoulli(1/2)，因此只看个体边缘或A向量都面临严格机制等效；在本冻结条件下额外捕获完整pair的B以及配对关系即产生观测辨识信息。**有限样本分类成功不等于生成机制被无误识别**：IID的16/256+16/256观察可能与其它机制共享支持，故IID条件正确率为7/8、不是1。

## 独立复算及结题条件
路线A枚举全部三机制×256完整原source，记录原4pair码、仅A四bit、四pair相等次数、原source精确质量、PARTIAL与FULL两种设计各自的3机制似然和后验、冻结MAP分类及对真机制是否正确；按原质量求每真模型正确率。
路线B不使用来源枚举器而只从独立4对A真率1/2的理论和三模型的likelihood support做分类概率推导：PARTIAL共同likelihood均1/16，FULL误报在IID下是两个相斥的四pair全等/全反事件、每事件概率(1/2)^4；真COPY/FLIP必为各自典型支持，因此得到7/8、1、1。另单独枚举16种A序列求质量1/16×16验证完全边缘同一性。
路线C第三GitHub Actions独立重读768条原source CSV，重新产生所有pair似然、原质量、后验分布、Bayes MAP和两种分类正确率，校验包括零质量source、原来源集合、结果SHA256。
协议先独立commit，后执行标准库Python3.11/3.12各≥45真实unittest，来源完整CSV/JSON/机器SHA归档，GitHub CI全部三job completed/success后只按E1有界人工数学结题。新增真人E2=0、真实历史E3=0，R073/PESEN v0.1冻结。原239目录下一项12-006 Model Identifiability（拟R276），全R完成后再统一归纳、分类和熔炼。
