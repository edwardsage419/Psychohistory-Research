# R245 更新过程：九有限离散间隔机制、4608完整九位原来源、更新方程与隐藏混合；事前冻结

日期：2026-10-23（Asia/Taipei）。原始239目录 **11-005 Renewal Processes（P2）**，编号R245。研究顺序保持全部原R→统一归纳分类→最后熔炼。仅有限人工E1，真人E2/历史E3新增0；R073与PESEN v0.1冻结。

## 原始定义与文献
MIT 6.262 *Discrete Stochastic Processes, Chapter 4: Renewal Processes*: https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/931ffa0940899c27f34b71ad64fd2bb0_MIT6_262S11_chap04.pdf 。NPTEL *Renewal Function and Renewal Equation*: https://archive.nptel.ac.in/content/storage2/courses/111103022/module8/lec3.pdf 。更新过程严格以 **IID非负间隔** W1,W2,…定义S_k=∑_{j≤k}Wj，N(t)=max{k:S_k≤t}；有限时间更新函数 m(t)=E N(t)，满足 m(t)=F(t)+∑_s p(s)m(t−s)，p(s)=P(W=s)，F(t)=P(W≤t)，这里s∈{1,2}且m(0)=0。本R仅枚举四个正间隔，t∈{0,1,2,3,4}；四间隔已足够完整确定此有限时间窗，不能从四步验证推断所有未来更新率、强大数定律或均衡剩余寿命。

## 全原源和观测
每世界九个等概率且独立二元外生位 (U,R11,R12,R21,R22,R31,R32,R41,R42)，其四个R对均匀取{0,1,2,3}，共2^9=**512种完整人工原类型/world**，九world共**4608条**。每原类型概率1/512，保存完整隐藏U/各R/真四间隔W1…W4/真前四更新时刻S1…S4/真累计计数H0…H4、可见观察计数Y0…Y4及源权重。源外生位是结构枚举，不是4608个实际被试或历史事件记录。可见观察只能利用五元(Y0…Y4)，不得读取完整未来间隔与oracle隐藏机制；研究人员可进行隔离的人工源概率核验。

## 九机制（全部间隔∈{1,2}）
1. IID_FAIR：四个独立gap短W=1概率1/2，长W=2概率1/2。
2. IID_SHORT_3OF4：四独立gap短概率3/4。
3. IID_LONG_1OF4：四独立gap短概率1/4。
4. DETERMINISTIC_UNIT：四个gap恒为1。
5. DETERMINISTIC_TWO：四个gap恒为2。
6. LATENT_RATE_MIXTURE：隐藏U对完整一条四gap路径固定，U=0短概率3/4，U=1短概率1/4；个体在给定U内gap独立同分布，但总体观察去U后的gap序列**不独立**；每一gap单独边际短概率仍1/2。预冻结：P(W2=1|W1=1)=5/8、P(W2=1|W1=2)=3/8；E N(2)=21/16，而按单gap边际错误代入IID公式会得到5/4。
7. ALTERNATING_RATE：奇数gap短概率3/4，偶数gap短概率1/4，互相独立但**不等分布**，不是普通IID更新；E N(2)=1+(3/4)(1/4)=19/16。仅用第一gap的p1=3/4套IID更新式则得到25/16。
8. COMMON_GAP_SHOCK：四间隔都由第一个R两位决定，全为1概率1/2或全为2概率1/2，四gap完全相关；单gap短率1/2而E N(2)=3/2，错误套IID式为5/4。
9. STATIC_HIDDEN_EVENT_SENSOR_ALIAS：真正隐藏事件H0…H4完全0，不发生任何真实更新；观察仪器Y报告按IID_FAIR相同原R生成的伪更新计数。因此**逐完整九位外生来源**可见Y路径与IID_FAIR完全相同、隐藏真事件数不同；此反例只有在允许报告器独立制造或模拟计数时成立，不能据此怀疑独立校准可信的实体计数。

## 全路径分布、来源与解析双轨验收
A. 完整来源第一路径直接用冻结阈值根据四个R对生成4间隔及四个S累计，y0…y4严格由所有S_k≤t的次数得到；九world每world512完整原来源正质量、总质量1。观测全五元计数序列的PMF去重求和（可能合并多个未观察的晚期gap）。
B. 独立第二路径**不读取来源函数或原CSV**，按完整16可能四gap向量产品概率解析：IID用每gap同一个p；ALTERNATING用各时点不同p；LATENT是两IID四gap产品律的1/2混合；COMMON仅(1,1,1,1)与(2,2,2,2)各质量1/2；DETERMINISTIC唯一完整四gap；STATIC_SENSOR用IID_FAIR。再把各gap路径转成有限观测计数轨迹并汇总概率，逐world和完整原来源观察联合严格一致。
C. 第三路线仅对五个真正IID gap机制（IID_FAIR/SHORT/LONG、DETERMINISTIC_UNIT/TWO）和**观察计数恰同IID的STATIC_SENSOR作为统计观察层**计算单gap pmf的离散更新方程，逐t=0..4重算m(t)并与源观察count一/二路线的期望一致；对非IID的LATENT/ALTERNATING/COMMON明确报告从单gap边际误用IID更新方程的偏差，**不将失败误判成概率公式错误**。
D. 观察可辨别：LATENT与IID_FAIR具有每一gap相同边际短概率1/2，但观测完整计数分布不同，尤以E N(2) 21/16 vs5/4；COMMON与IID_FAIR的单gap边际同1/2，但E N(2)=3/2；ALTERNATING与IID_SHORT在第一gap短率3/4相同，但第二gap依赖时间位置且E N(2)=19/16 vs25/16。
E. 源真实隐藏H与实际Y的完全观察等价仅为IID_FAIR和STATIC_SENSOR；真隐藏H在后者严格为0。记录真实事件/观测报告区别，不能混淆数学可见计数拟合与现实事件存在。
F. 对IID_FAIR单gap≤2全部，准确E N(1)=1/2，E N(2)=5/4；确定UNIT的N(4)=4、确定TWO的N(4)=2。更新方程仅在t≤4冻结验证，不做长期推断。
G. 验收最低Python3.11/3.12各≥45实际单测，第三独立CI job验收九机制4608全部结构来源、全观察五元联合、双轨完整概率、IID更新方程与非IID偏差、隐藏报告别名、SHA256并用GitHub bot永久写main；真实success和归档后才形成科学报告和正式结题。
H. 下一个已核原239条目11-006 Poisson and Hawkes Processes（P1），拟R246。需要独立冻结和区分离散事件机制与连续Poisson/Hawkes过程。
