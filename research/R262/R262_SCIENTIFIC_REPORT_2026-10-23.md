# R262 元胞自动机：九Elementary CA规则、七格周期环5760完整原source与宏观相同/微观可逆性不同

日期2026-10-23（Asia/Taipei），原239目录`11-022 Cellular Automata`（P1）。正式科研状态`CLOSED_BOUNDED_E1_SEVEN_CELL_PERIODIC_ELEMENTARY_CA_COMPLETE_INITIAL_STATES`。仅对七格环、七原初值bit全部128种和五个有限时点的人工数学结构进行精确解析，不证明无穷大空间和长期规则30/110复杂度/混沌/图灵完备性，也不构成真实人类传播、文化演化或历史轨迹的外部验证。新增真人E2=0，历史E3=0，R073/PESEN v0.1冻结。

## 一手理论与有限设计

Stephen Wolfram (1983), [*Statistical mechanics of cellular automata*, Reviews of Modern Physics 55:601–644](https://doi.org/10.1103/RevModPhys.55.601)，介绍一维二状态最近邻同步元胞自动机。本R仅选用有限长度N=7、周期边界的9条elementary 8位规则，将更多文献关于无穷环或自然系统的宏观推断**排除在本项可验收范围之外**。[九条规则、5760来源、两条完全独立局部规则执行路线和预冻结数值](../../protocols/R262_ELEMENTARY_CA_9_RULES_SEVEN_RING_5760_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)于原算法/评分运行前独立提交[8dc5cbb9](https://github.com/edwardsage419/Psychohistory-Research/commit/8dc5cbb95ed011e5fd190d42e63336df938ccd40)。

每world七独立公平初值位`x0∈{0,1}⁷`，完整2⁷=128种原初始结构；五个时点n=0,1,2,3,4对**同一初始结构沿同一确定性轨道重复观察**，因此每world128×5=640完整`初始构型×时间`source，九world共**5760条完整人工原source**。每source设计质量1/640，但每world独立初值只有128种，不能把五个时点算作640个独立初值更不能把5760条当真人。全部CSV逐原source保留七个原初值、时点、每一个体7bit状态、当前1计数K与global parity、规则号及人工设计权重。周期边界`x_{i+7}=x_i`，同步更新规则在每个时点先读取**上一个完整七维状态**，不得把异步逐格顺序更新混入。

所有world使用Wolfram十进制规则编号r，输入`(a,b,c)`按左邻、中心、右邻顺序，二进制索引`4a+2b+c`，下期输出为rule二进制该索引位。第一源路线按位右移读取规则码，逐五时点传播全128初值；**独立第二路线不读取原source状态也不调用原右移计算或其上一状态缓存**，对九world各自冻结的8邻域111,110,101,100,011,010,001,000布尔真值字符串查表，从每个初态独立重新运行至指定n。全部5760条×7位置原bit同步状态**逐格完全一致**，从第二路线再次独立枚举完整一步像集数、固定点数及五时点群体密度。

## 九冻结规则的全部有限一时点像集和固定点

| world（十进制规则） | 一步128种初值产生的不同七维下一态数 | 一步固定点数 | 均匀初值下t4平均状态1份额 |
|---|---:|---:|---:|
| ABSORB_ZERO（0） | 1 | 1 | 0 |
| ABSORB_ONE（255） | 1 | 1 | 1 |
| IDENTITY（204） | 128 | 128 | 1/2 |
| SHIFT_RIGHT（170） | 128 | 2 | 1/2 |
| SHIFT_LEFT（240） | 128 | 2 | 1/2 |
| XOR_NEIGHBORS（90） | 64 | 1 | 1/2 |
| XOR_THREE（150） | 128 | 2 | 1/2 |
| RULE30（30） | 106 | 1 | 61/128 |
| RULE110（110） | 79 | 1 | 17/32 |

全部九world的固定点、一时点不同像集基数和每个时点平均群体1比例均由**完整128原初态、两独立执行路线**严格整数核算。RULE110均匀完整七bit初值的平均1比例从t0=1/2，t1=5/8，t2=17/32，t3=33/64，t4=17/32；RULE30在t0至t3平均1/2，t4变为61/128。这些比例是已冻结七格周期边界、128等质量初态下的有限确数，**不能由五个时点和一条环大小断言真正无穷格的稳态、熵率、统计力学普适类或现实文化周期**。另一方面一个规则的像集大小106或79本身不能直接当Shannon熵bit数，因为不同输出状态拥有的前像数可能不同，需要完整输出分布才能算精确熵。

## 三个核心机制边界

**第一：宏观平均密度相同，但一步信息可恢复性不同。** XOR_NEIGHBORS规则90给出`x'ᵢ=x_{i−1} XOR x_{i+1}`。在长度7的环上，每个原bit恰被两个输出包含，所以所有下一态的一元奇偶校验必为0。一时点像集只有64个不同7bit状态，完整128个原初始状态对每个像恰有**2个前像**，核是两个均匀全0/全1差异（在GF(2)中相差全部1向量）。因此在“128初态等概率”这一明确有限先验下，初态Shannon熵7bit，一时点输出恰均匀分布在64种像上，输出熵6bit，**单步丢失1bit初始信息**。XOR_THREE规则150为`x'ᵢ=x_{i−1} XOR x_i XOR x_{i+1}`，在七格周期环128初态映射成**128个唯一输出**，是一一对应的置换；每个原bit影响恰三个输出，整体奇偶校验保持。两个规则在所有五时点的**均匀来源平均1份额均为1/2**，但规则90是非单射、规则150是双射且保持parity，因此以全局平均比例断言信息保留程度完全错误。这是一种固定7环的精确数学例子，不证明对所有环长90/150都同样可逆。

**第二：总采用人数保持相同，却无法推出空间传播方向相同。** SHIFT_RIGHT规则170下一期每格复制右邻；SHIFT_LEFT规则240复制左邻。任一原初始7bit状态的所有时点下，两条轨道都只是旋转原排列，所以总1数K_n始终等于初始K0，两个world每一相同原source的完整五时点宏观计数**严格相同**。但由于环长7为奇数，若一步左邻与右邻复制后得到相同全七维结果，则原状态满足x_{i−1}=x_{i+1}∀i，在七格中只能全0或全1；于是**其余126个不同原source在t1有不同的完整空间状态**。总体传播比例不识别空间影响的方向，除非实测位置标签/个体转移信息，这不提供实际社会传播的证据。

**第三：规则30、110显示有限非平凡图像，不构成“复杂历史可预报”的证明。** RULE30在七格一步像集106、固定点1；RULE110一步像集79、固定点1、均匀初态在五时点平均密度按上表变化。该有限计算只证明这两个特定局部规则在这些边界条件下具有特定整数像集和统计值，不推导无限系统的长期行为、计算普适性或真人网络文化发展机制。不能从有趣有限图样直接推出真实社会复杂系统“混沌”或适用于长期历史演化预测。

## 实际双版本CI与完整原source/SHA永久归档

[原生Python整数元胞规则位移与独立真值表执行程序](r262_exact_elementary_ca.py) · [九world全部5760七bit原source CSV](R262_ALL_5760_ORIGINAL_SEVEN_RING_CA_SOURCE_ATOMS.csv) · [规则表/像集/固定点/五时点密度JSON](R262_EXACT_RESULTS.json) · [原CSV/JSON SHA256完整来源凭证](R262_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39899036629](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39899036629)总状态completed/success，三个job全部success。Python3.11与3.12实际日志分别`Ran 82 tests`、`OK`，共**164次真实双版本单测通过**。第三独立原source审核逐world确认640唯一原初始7bit×五时点source、每source1/640、九规则Wolfram十进制编号、各自冻结的8邻域完整真值、全部原source七格逐位计算与独立真值表重运行一致、K/parity、每world完整128初态的一步image/fixed及各n平均密度、规则90的64像每像2前像且一步parity必偶、规则150的128像和parity保持、左右移位逐source同K与t1的126个微观差异、原CSV/JSON SHA。实际审核日志`R262_ALL_5760_ORIGINAL_SEVEN_RING_CA_STATES_AND_INDEPENDENT_TRUTH_TABLES_VERIFIED`、`R262_ALL_5760_ORIGINAL_SEVEN_RING_SOURCES_PERMANENTLY_ARCHIVED`。完整原CSV/结果JSON/SHA机器来源永久由GitHub bot提交main [59f984ad](https://github.com/edwardsage419/Psychohistory-Research/commit/59f984ade41f22cfa2efd16a0584c2a54bd15bd2)。

原CSV SHA256 `6bc81d5ae6aae67d8f0b271b6baa02240439a3bf87313a6b812a2e51bdae6adb`，完整结果JSON SHA256 `ef9fff3f511b3101b75d9c76e5804276bda8472a49048eac66b524cb808ba174`。

正式科研资格仅`CLOSED_BOUNDED_E1_SEVEN_CELL_PERIODIC_ELEMENTARY_CA_COMPLETE_INITIAL_STATES`，没有真人E2/历史E3外部证据、无限空间理论验收或历史长期预测能力证明。R073/PESEN v0.1均冻结，下一原目录11-023 Genetic Algorithms（拟R263，P2），仍全部原R结束后归纳分类，再最终模型熔炼。
