# R121 — Independent Cascade：一次传播机会与每边独立随机活边的原文机制预冻结

研究日期：2026-10-19（Asia/Taipei）
研究编号：R121，原模型候选目录P0 / 04-004 Independent Cascade Model，原候选review_status待逐项文献审查。R120的LT已单独限定结题；本轮不重复作为新独立外部实证。
所有者顺序保持：逐项完成此前既定R系列模型学习 → 全面分类 → 最后熔炼。R073/PESEN v0.1继续冻结。

## 第一手源和实际核读

Kempe, D.; Kleinberg, J.; Tardos, É. (2003), *Maximizing the Spread of Influence through a Social Network*, ACM SIGKDD 2003:137–146, DOI https://doi.org/10.1145/956750.956769 。原作者Cornell托管的10页原期刊PDF：https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf ；冻结前真实核阅PDF零基1页 “Two Basic Diffusion Models”对IC的逐轮定义，以及零基3页 “Independent Cascade”/Theorem 2.2与 Claim 2.3的原证明。原作者明确：有向边(u,v)的概率p_uv固定；u首次变为active后的下一步只对每个尚未active的邻居v进行**一次**Bernoulli激活尝试，无论成功失败该u永不能再次尝试激活同一v；不同尝试成功概率独立于既往历史；一轮有多个新激活邻居u尝试v时可以按任意顺序处理。成功的v在t+1阶段才成为新的传播源，已active不退出。Claim2.3声明提前为每条有向边掷**相互独立**的随机硬币，最终活跃节点集合等于初始种子沿所有成功边可达节点集合。Theorem2.2期望活跃节点数σ(A)对种子A单调、次模。这两条结论不同于R120（LT）“每个节点至多选择一条入边或无入边”的构造。

来源补充：Goldenberg, J.; Libai, B.; Muller, E. (2001), *Talk of the Network: A Complex Systems Look at the Underlying Process of Word-of-Mouth*, *Marketing Letters* 12(3):211–223, DOI https://doi.org/10.1023/A:1011122126881；原三作者所属Tel Aviv大学出版记录：https://cris.tau.ac.il/en/publications/talk-of-the-network-a-complex-systems-look-at-the-underlying-proc/ 。本轮仅核实学术出版和摘要，未将Goldenberg团队的随机元胞自动机直接当成2003年KKT的同一组已估计参数，也没有读取原商业社交网络的逐人行为。

## 两个独立计算机合同

有向n∈[1,5]个匿名节点，编号0..n−1，边为有序(u,v,p_uv)且u≠v，p_uv为Fraction∈[0,1]。无重复相同(u,v)，允许反向边、零概率边和必定成功边，最多12条边以控制指数枚举。初始种子为显式合法唯一节点集合，可为空、可全部。无个人信息、无外部平台操作。自循环、负概率、超1、浮点权重、bool伪装编号、重复seed及重复边一律失败（fail-closed）。

求解器A **轮次随机尝试的精确分布枚举**：从当前active及当期新激活frontier出发，当前frontier的每个u仅对**上一期仍inactive**的每个出边目标v独立尝试一次，分支概率p_uv；可由多个本期尝试成功合并同一目标，目标在下一轮加入active与frontier。前代frontier永不再次获得传播机会；若当前没有新激活目标则停止。每条可尝试边的随机选择只在轮次实际尝试时计分；所有终态frozenset节点集合的概率严格加总为1。此算法不允许使用活边法结果，仅用状态(frontier,active)递归/动态概率分支。

求解器B **逐有向边独立预掷硬币**：所有边(u,v)独立以p_uv live/以1−p_uv blocked，枚举全部2^m可能硬币状态（零/一概率分支可跳过），针对每个完整结果从初始种子沿所有live边有向可达性搜索。不准调用求解器A。精确Fractions统计完整final-active-set概率分布，严格与A一致，且各自归一。比较不只是E人数或边平均数量。

**不可混同R120**：IC每个有向边成功事件相互独立，LT则每个目标节点至多选择一条入边（彼此排斥），所以即使设置两条入边概率相同，最终集合分布可能不同；不能在本轮把IC又称Linear Threshold live-edge那一种。

## 事前锁定的解析案例

1. 三节点，0→2概率1/2、1→2概率1/4。种子{0}则Pr(2 active)=1/2，E总活跃=3/2；种子{1}概率1/4，E=5/4；种子{0,1}则Pr(2 active)=1−(1−1/2)(1−1/4)=**5/8**，E=**21/8**。两出边同时live的联合概率是1/8；R120相同数值当作LT入边权重时，{0,1}使目标被激活概率3/4、E=11/4且两入边不可同时被选中。**IC和LT不可用“单源边际一样”推导一般等价**。
2. 四节点有向链0→1 p1/2、1→2 p2/3、2→3 p3/4，种子{0}时E=**25/12**，Pr(3 active)=1/4。
3. 三节点有向环0→1、1→2、2→0均p1/2，种子{0}时E=**7/4**，已激活节点没有复活或再获得尝试的资格。
4. 节点0→2和1→2各p=1（确定性成功），种子{0,1}使2在下一轮激活一次，不允许“重复占用”或多次增加节点数量。
5. 三节点只有0→1 p=0、1→2 p=1，种子{0}不能激活其他节点。p=1全链时始终100%传播到底；空seed时始终空集合。
6. **非原作者原实验数字**的时间限定样例：0→1=1、1→2=1、0→2=0，从种子0起，t0激活0，t1激活1，t2激活2，节点0没有在t1重试0→2（其原第0次失败/零概率）。用于验证每条边单次时机。

## 完全有限测试和证据门

对n∈{1,2,3}所有没有自环的有标签有向简单图(1、4、64种)，分别应用两组概率赋值：所有边p=1/2；或每边按源/目标编号确定性选择p=1/4或3/4（精确定义在代码中冻结的确定性函数）。逐图比较每个可能的种子集合（分别2、4、8个），**2×(1×2+4×4+64×8)=1060个纯数学图-种子-权重配置**，两方法所有最终frozenset概率完全相等、概率和严格为1。再对每张小图的σ(A)完整种子幂集检查单调与边际次模性，不假装这1060为真实社交网络观测。至少35项独立unittest，Python标准库，无下载真实数据或真人E2。

如果真实Github Actions未success、机器SHA256结果未回存main，就不能结题。全部成功时可记限定学习状态 LEARNING_COMPLETE_BOUNDED_KKT_2003_IC_ONE_CHANCE_INDEPENDENT_LIVE_EDGES。原作者Greedy最大化在大合作网络上的实验没有重新运行，真人预测E2为0，规范压力/信息动机因果不建立，PESEN v0.1与R073不变。
