# TH172 行政代理指标、群体测量等值性与制度版本漂移

研究日与非中文来源检索日：2026-10-31（Asia/Singapore）。track: theory。状态：THEORY_NOTE_BOUNDED。
target_key: (theory,ADMIN_PROXY_GMTMM_IRT_DIFFERENTIAL_ERROR,TH172-theory-v1,group_measurement_invariance_and_version_drift)。
承接TH171，非盲态互补理论研究。只研究公开原始论文与人工二元代理指标模型。未使用用户敏感资料、真实Smartcards微观数据或收费工具。R系列优先顺序不变。

## 一、来源与直接阅读范围

S1 [A，作者开放预印本全文，直接审读第1节、第2.1至2.5节、第3.1节；未执行作者模型] Oberski, D. L.; Kirchner, A.; Eckman, S.; Kreuter, F. (2015 preprint, 2017 journal). Evaluating the Quality of Survey and Administrative Data with Generalized Multitrait-Multimethod Models. arXiv:1508.05502, https://arxiv.org/abs/1508.05502 。正式版 Journal of the American Statistical Association 112(520):1477–1489, DOI:10.1080/01621459.2017.1302338。预印本与正式版未逐字比较，具体模型归于所读预印本。原始德国就业关联数据受法律限制，未取得。
S2 [A，原作者开放同行评审全文，直接审读第2至6节及表1；未运行Mplus] Muthén, B.; Asparouhov, T. (2014). IRT studies of many groups: the alignment method. Frontiers in Psychology 5:978. DOI:10.3389/fpsyg.2014.00978。https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00978/full 。研究多组IRT的题目阈值、载荷与部分等值，原作者使用跨国公民知识测验及Monte Carlo。作者为所用Mplus软件开发者；本轮未使用商业软件。
S3 [A，作者机构开放正式论文PDF，直接审读原刊543至544页及548至553页的定义、识别假设和敏感性分析；未运行作者复现数据] Imai, K.; Yamamoto, T. (2010). Causal Inference with Differential Measurement Error: Nonparametric Identification and Sensitivity Analysis. American Journal of Political Science 54(2):543–560. DOI:10.1111/j.1540-5907.2010.00446.x。https://imai.fas.harvard.edu/research/files/merror.pdf 。原文讨论处理变量差异性误分类的ATE界限，本轮人工描述性界限属于不同估计对象。
S4 [B，仅核对原刊摘要和书目] Meredith, W. (1993). Measurement Invariance, Factor Analysis and Factorial Invariance. Psychometrika 58(4):525–543. DOI:10.1007/BF02294825。https://www.cambridge.org/core/journals/psychometrika/article/abs/measurement-invariance-factor-analysis-and-factorial-invariance/914A4C29515ACA7E0554B9E79F20D36C 。全文未审读。
S5 [A，继承TH171的已归档公开表审计，本轮没有重新通读全部报告] Atanda, A. A. (2019). Biometric Smartcards and payment disbursement: a replication study of a state capacity-building experiment in India. 3ie Replication Paper 23, DOI:10.23846/RPS0023。https://www.3ieimpact.org/sites/default/files/2019-06/RPS23_Biometric_Smartcards_and_payment_disbursement_India_3.pdf 。第7地区NREGS 1425人个人持卡字段全缺失、GP状态有记录，仅用于提出验证问题。

## 二、竞争理论及适用边界

1. Meredith及多组IRT路线：比较群体潜在构念需检验阈值、载荷和锚题等值。Muthén与Asparouhov的alignment可容许部分参数偏移，仍依赖多个共同题目、模型识别及近似等值结构。单个GP行政二元状态无法直接构成个人持卡的IRT潜变量量表。
2. Oberski等GMTMM路线：调查和行政记录均可能存在系统误差与随机误差。多特质多方法设计在识别假设成立时可分离部分潜在特质、方法效应与残差。第2.2节的条件独立结构、第2.5节的识别秩及合法可关联数据是关键门槛。作者应用于德国就业数据，不能直接声称适用于Smartcards。
3. Imai与Yamamoto部分识别路线：差异性误分类使因果ATE的识别依赖额外假设，部分界限可能很宽。本轮独立构造的二元真实比例界只研究描述性状态，不属于其ATE定理。
三条方法路线的目标量分别可能是潜在均值、误差成分、描述性真值比例和因果效应，必须单独归档。

## 三、人工二元代理模型

设同一个体、同一时期的真实状态T和代理Z均为二元。p=P(T=1)，se=P(Z=1|T=1)，sp=P(Z=0|T=0)，q=P(Z=1)。恒等式为：

q = se*p + (1-sp)*(1-p)。

当se与sp有外部可辩护校准，且se+sp不等于1时，p=(q+sp-1)/(se+sp-1)。分母趋近0会放大误差。GP转换是村级行政指标，个人持卡是个体指标。缺乏同单位配对时，此式不能直接用于GP到个人持卡的转换。

### A. 同一代理率下的相反真实群体差

| 人工世界与群体 | p | se | sp | q |
| --- | ---: | ---: | ---: | ---: |
| A群体1 | 1/4 | 1 | 2/3 | 1/2 |
| A群体2 | 3/4 | 2/3 | 1 | 1/2 |
| B群体1 | 3/4 | 2/3 | 1 | 1/2 |
| B群体2 | 1/4 | 1 | 2/3 | 1/2 |

两世界的代理组差均为0，真实组差分别为负1/2和正1/2。各组se+sp>1，代理仍与真值正向相关。

### B. 制度版本漂移导致虚假趋势

人工固定p=1/2。旧版se=4/5、sp=9/10，q=9/20=0.45。新版se=9/10、sp=7/10，q=3/5=0.60。代理率上升15个百分点，真实比例不变。缺少版本化校准时无法将代理趋势解释为真实趋势。

### C. 有误差下限的尖锐描述界

在q=1/2、se与sp均介于3/4和1之间时，真实p的可达区间为[1/3,2/3]。下端由p=1/3、se=1、sp=3/4达到，上端由p=2/3、se=3/4、sp=1达到。两个群体的真实比例差可达区间为[-1/3,1/3]。这些界限依赖外加误差下限，不包含抽样误差，也不属于因果ATE界。前述p=1/4和3/4的世界不满足这里的误差下限。

### D. 弱校准的不稳定性

当se=sp=51/100时，q=1/2给出p=1/2；q仅增加1/1000至501/1000，逆算p变成11/20，增加1/20。此时se+sp-1=1/50。校准参数本身的不确定性尚未纳入。

本地Python标准库Fraction精确审计16项单元测试通过。测试只检查人工恒等式、端点、奇异矩阵与输入约束，未拟合IRT、GMTMM或任何真实人群数据。

## 四、十四项条件命题及反例

TH172-01 [S1] 行政与调查记录均可能带随机及系统误差；任意一方为完美金标准是额外假设。反例：两来源共用错误时间窗口。
TH172-02 [S1] GMTMM的误差分解依赖条件独立、足够特质/方法及识别秩。反例：共同制度因素同时改变两来源的错误。
TH172-03 [S2] 跨群体潜在均值比较需审查题目阈值与载荷。反例：政策版本改变题目解释。
TH172-04 [S2] Alignment容许部分非等值，依赖可锚定指标及近似等值。反例：多数锚题同向漂移。
TH172-05 [S3] 差异性处理误分类会扩大因果ATE的识别范围。此处人工比例界与原作者ATE界分开。
TH172-06 [S1,S2] 可靠性、构念效度和跨群体等值性提供不同证据。高重复一致率可伴随稳定偏差。
TH172-07 [人工A] 代理组差为0时真实组差可为正或负1/2。
TH172-08 [人工A] 即使代理与真值在每组均正向相关，组间误差矩阵不同仍可掩盖真实差异。
TH172-09 [人工B] 真值不变而代理率上升15个百分点，须保存行政变量版本、编码与日期。
TH172-10 [人工C] 误差下限可使真实比例界收窄到[1/3,2/3]，收窄依赖外部可检验假设。
TH172-11 [人工C] 相同误差下限下的组差界仍跨零，代理率相等不能自动推出群体公平。
TH172-12 [人工D] 校准矩阵接近奇异时微小代理变化可引起较大真值逆算变化。
TH172-13 [S5] GP行政转换与个人持卡属于不同层级、处理版本与测量时间，缺失个人标签无法从GP状态无条件恢复。
TH172-14 [S1,S2,S3] IRT、GMTMM和部分识别各有识别条件；条件未核验应登记IDENTIFICATION_OPEN。

## 五、四层连接与验证清单

个体：持卡、使用、领取、被问及及缺失原因分开。群体：地区阈值、报告激励、缺失机制及代理误差可能不同。制度：GP转换、问卷版本、主键、编码更新及执行日期可能改变代理矩阵。历史：跨时期趋势须固定构念、观察单位、参考期与样本总体。

未来验证：一，合法恢复问卷、变量字典、适用模块及编码日期；二，建立地区×时期的构念、单位、分母、缺失规则矩阵；三，多题时预先确定锚题并检验configural、metric及scalar条件，免费开源工具优先；四，多特质双来源时审查GMTMM条件独立、关联误差和识别秩；五，单代理且无校准时报告宽界及明确假设下的敏感性曲线；六，第7地区个人持卡缺失原因保持UNKNOWN，不能自行填补真实值。

未决：原始Smartcards问卷、字典及随机化单位身份未恢复；跨地区误差矩阵未知；行政GP与个人层配对时点未知。

科学状态THEORY_NOTE_BOUNDED。原始理论审读及人工E1数学检查，真实微观复算0、真实因果估计0、历史留出0、前瞻预测0；R系列E1/E2/E3新增科学验收0。C008已满足2026-10-31，D002已满足2026-W44，保持只读。未触发付费工具或CI。

下一候选TH173：多来源行政测量的三特质双方法识别秩、条件独立破坏与最小校准样本设计。
