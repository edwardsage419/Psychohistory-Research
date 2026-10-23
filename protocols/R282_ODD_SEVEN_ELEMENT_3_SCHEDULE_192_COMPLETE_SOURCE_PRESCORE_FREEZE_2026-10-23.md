# R282：ODD规范、复现协议与有限ABM严格时序审计；事前冻结
日期2026-10-23 Asia/Taipei。原239候选目录12-012 Open Reproducible Workflow and ODD（P0）。第一来源Grimm et al. (2020), *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*, JASSS 23(2)7, DOI https://doi.org/10.18564/jasss.4259；首次更新Grimm et al. (2010), DOI https://doi.org/10.1016/j.ecolmodel.2010.08.019 。本研究在遵循ODD2020七要素的前提下自建最小社会交互ABM；既不复现Grimm文章的原模拟，也不宣称真实心理行为机制。
## 事前冻结模型、完全原来源、前瞻验收真值
实体A、B，状态a,b∈{0,1}，离散步t=0,1,2。冻结每次模型运行的六bit原随机来源 `a0 b0 eA0 eB0 eA1 eB1`，各bit独立Bernoulli(1/2)，所有2^6=64有序原source质量1/64。对来源设置`source_index=0..63`，严格定义bit字符串=六位补零二进制表示的source_index，目的是**枚举全部源与复现**，不是调用PRNG生成伪随机数，也不许冒称64独立真人受试。
每步两个固定扰动bit eA,eB 在开始时已作为完整原source给定。社会更新采用`new_a = (current_b XOR eA)`和`new_b = (current_a XOR eB)`，但计算输入视激活日程而定。三政策：
* SYNC：两agent各读取**同一步开始**a,b，新的(a',b')=(b XOR eA, a XOR eB)；
* A_THEN_B：先a'=b XOR eA，再b'=a' XOR eB，读取更新后a；
* B_THEN_A：先b'=a XOR eB，再a'=b' XOR eA，读取更新后b。
每source重复两步、逐个保存t0,t1,t2两人二元状态、e四bit、schedule、各状态质量及指定观测。三政策×64原source＝**192个带日程标签的完整原source配置**；每policy有同一64六bit配置，绝不能称192个独立历史事件或人类个体。
冻结核心校验：
1. 每policy最终t2状态四种(00,01,10,11)各出现16/64，故只观察最终状态聚合分布**无法辨别日程**。
2. 与SYNC在**相同六bit源**配对，A_THEN_B与SYNC的t1状态不一致32/64、t2状态不一致48/64；B_THEN_A与SYNC同样32/64和48/64。
3. A_THEN_B与B_THEN_A在同源t2状态不一致48/64。以上分子是来源数量，概率直接/64。
4. 个别来源source_index=1即000001，三日程具体t0=(0,0)、t1=(0,0)，t2结果：SYNC=(0,1)、A_THEN_B=(0,1)、B_THEN_A=(1,1)。将用于反事实审计日程差异。
## ODD 2020文档约束
必须单独创建`research/R282/R282_ODD2020_SEVEN_ELEMENT_MODEL_DESCRIPTION.md`，含标准ODD2020的**七要素**及源定义和代码定位：①Purpose and patterns，②Entities, state variables, and scales，③Process overview and scheduling，④Design concepts，⑤Initialization，⑥Input data，⑦Submodels。明确说明无学习/适应、无空间和无现实输入；说明逐来源枚举、伪随机种子不可替代输入流、调度有复现相关性、每步扰动独立、无经验校准。研究受制于模型实现完整可追溯，不等于ODD出版物审查认证。
## 验收路线
A全枚举192原source，执行精确两步模型，保存每条初始、扰动和三时间状态及最终状态和来源质量CSV。
B完全不调用A的模拟器，另写位运算闭式求t2：SYNC经两次同步更新有`a2=a0 XOR eB0 XOR eA1`、`b2=b0 XOR eA0 XOR eB1`；A_THEN_B在每轮最终 `b_t=a_t XOR eB_t`；B_THEN_A在每轮最终`a_t=b_t XOR eA_t`。依据这些代数对所有64来源独立复算，统计上述32/48/48原source不一致数和四终态均匀分布。
C GitHub Actions第三job无源码导入地从CSV重算每source六bit起始、两步状态、时间序、调度、64原source全集、源概率、三schedule终态分布和配对差异，以及ODD文件七标准要素、所有CSV/JSON/机器哈希。另单元测试刻意删除ODD必要元素应FAIL、改变日程应改变指定反例轨迹、重复执行同source bit stream须字节级相同。
协议先行单独commit，后提供无依赖Python程序、ODD七要素、原source CSV、结果JSON/SHA256机读凭证及科学报告，双Python3.11/3.12各≥45真单测，三job completed/success与机器人永久main归档后才可**有限人工E1正式结题**。无真人E2/真实历史E3，R073/PESEN v0.1保持冻结。下一目录12-013 Systematic Review and Meta Analysis（R283，P1），再12-014发表偏差12-015多重比较。
