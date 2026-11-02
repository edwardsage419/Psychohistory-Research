# TH212 Kermack与McKendrick 1927年原刊公式31微分系数核验及孟买鼠疫竞争解释

track: theory
subflow: main
run_date: 2026-11-02 (Asia/Singapore)
observed_main_head_before_write: b733bc39c14a210aee9a4d91842daa89bc83f0db
target_key: (theory,Kermack-McKendrick1927+rspa.1927.0118,1927-published-scan,eq30-to-eq31-derivative-and-historical-explanation)
status: COMPLETE_BOUNDED_PRIMARY_EQUATION_AUDIT; PARTIAL_PUBLISHED_ERRATUM_CHECK; NO_REAL_DATA_REESTIMATION
evidence_scope: PRIMARY_PUBLISHED_SCAN; CONSTRUCTIVE_EXACT_MATH; HISTORICAL_COMPETITOR_ABSTRACT_ONLY; NONBLIND; NO_R_E1_E2_E3_UPGRADE
ci_status: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_FREE_QUOTA_NOT_VERIFIED

## 原始来源、版本与直接阅读范围

[A] W. O. Kermack、A. G. McKendrick (1927), *A Contribution to the Mathematical Theory of Epidemics*, *Proceedings of the Royal Society of London A* 115(772):700–721, DOI 10.1098/rspa.1927.0118。直接阅读原刊完整印刷pp700–721的公开扫描及文字层，重点逐式核对pp702–705式(2)–(15)、pp707–709式(20)–(22)、pp713–715式(29)–(31)及孟买图、pp716–718阈值与初始感染年龄限制。**直接目视核验原刊扫描p713的式(29)、(30)、q定义和p714的式(31)及图形**。合法阅读链接：https://jxshix.people.wm.edu/2009-harbin-course/classic/Kermack-McKendrick-1927-I.pdf 。原始扫描含JSTOR版权及使用条件，仅记录原创短式和分析，不复制PDF或图像入仓库。

[B] Advisory Committee on Plague Investigations in India (1907), *XXII. The Epidemiological Observations Made by the Commission in Bombay City*, *Journal of Hygiene* 7(6):724–798, DOI 10.1017/S0022172400033684。核验Cambridge正式书目、原刊摘要与目录；原刊pp753的图表**未直接读到**。https://www.cambridge.org/core/journals/epidemiology-and-infection/article/xxii-the-epidemiological-observations-made-by-the-commission-in-bombay-city/70E413474CBA678B3D22FD72A33E0D1E 。

[B] Advisory Committee (1907), *XXIV. General Considerations Regarding the Spread of Infection, Infectivity of Houses etc. in Bombay City and Island*, *Journal of Hygiene* 7(6):874–894, DOI 10.1017/S0022172400033702。仅正式摘要，记载当时研究者以鼠间流行及鼠蚤传播解释城市鼠疫；未直接读取全文。https://www.cambridge.org/core/journals/epidemiology-and-infection/article/xxiv-general-considerations-regarding-the-spread-of-infection-infectivity-of-houses-etc-in-bombay-city-and-island/80612090FEE2F1D29999F2DEB3A475D0 。

[B] Nicolas Bacaër (2012), *The Model of Kermack and McKendrick for the Plague Epidemic in Bombay and the Type Reproduction Number with Seasonality*, *Journal of Mathematical Biology* 64:403–422, DOI 10.1007/s00285-011-0417-5。仅直接核验PubMed正式摘要；作者称历史年度反复出现季节性流行，常参数反推不合理，提出季节性鼠蚤模型。**正式英文全文尚未读**；法文开放版本已定位，未以其替代英文正式原刊。https://pubmed.ncbi.nlm.nih.gov/21404076/ 。

## 原著理论机制与严格限定

原文§2–§3的基础是按感染后时间θ分组的感染年龄核函数：B(θ)=exp[-∫₀^θ ψ(a)da]为存留感染状态的概率，A(θ)=φ(θ)B(θ)为年龄相关传染力与存留的乘积；易感者减少率由既往各期感染者的卷积决定。其一般形式容许感染力、移出率随病程改变。§10的常数φ=κ、ψ=l才给出式(29)三组常微分方程 x'=-κxy, y'=κxy-ly, z'=ly。不能将1927年整篇原作等同于只有常参数SIR。

§6原刊式(20)含初始输入y₀：-log[(1-p)/(1-y₀/N)]=ANp，其中A=∫A(θ)dθ，N=x₀+y₀，p=(N-x∞)/N。§11推导N₀=1/A的阈值和近阈值规模约2n时，明确假设y₀/N可以忽略。p含初始输入病例；y₀>0时不宜将阈值下的零大流行叙述误读为数学上完全零感染。原文p717–718还明确指出，感染年龄异质时峰值时刻的易感人数一般不能严格等同初始输入病例所定义的阈值。

## 新增高价值核验：原刊式(31)相对于式(30)少一个sqrt(-q)因子

原刊p713式(30)及其q定义，令D=√(-q)>0、K=l²/(κ²x₀)、u(t)=lDt/2-φ：
z(t)=K[(κx₀/l-1)+D tanh(u(t))]。
直接求导：
z'(t)=K D(lD/2)sech²(u(t))=[l³(-q)/(2κ²x₀)]sech²(u(t))。
原刊p714式(31)的**印刷系数**为[l³√(-q)/(2κ²x₀)]sech²(u(t))。两者差一个D因子。p713和p714原刊扫描图像均已目视确认，排除文字转录把D²误读成D的可能。

构造性精确反例：取κ=l=x₀=1，y₀=1/8，得到D=1/2、φ=0。式(30)成为z(t)=(1/2)tanh(t/4)，故z'(0)=1/8，与原刊式(29)的ly₀=1/8一致；照式(31)印刷系数则给z'(0)=1/4，矛盾。Python标准库Fraction核对D²=1/4、导数系数1/8、印刷系数1/4及初始ODE关系均PASS。此核验只说明**式(30)和式(31)在同一参数条件下不相容**；原刊的tanh曲线来自小规模展开，整体近似误差仍在。未查到可证实的正式勘误，是否已有勘误=PARTIAL。p714另行给出的890 sech²(0.2t-3.4)是拟合曲线形式，不能据此直接证明从原始微分方程估计参数正确。

## 独立竞争机制与可识别性

构造性模型比较：密度作用dI/dt=κSI-lI，取κ=1/100、l=1，初始S≈N为50时早期增长率为-1/2，N为150时为+1/2。频率作用dI/dt=β(S/N)I-lI，取β=3/2、l=1、S≈N，两种N的增长率均为+1/2。固定易感比例下，密度变化在两种接触归一化中产生不同阈值。属于模型假设的反例，未指称任何城市实际传染机制。

1927年p714–715的1905-12-17至1906-07-21孟买死亡曲线由鼠疫人类死亡数近似代表移出率。作者明确承认鼠、蚤及病程常参数等条件未严格满足，图仅是粗略近似，不应反推实际参数。1907年调查委员会的鼠蚤解释和Bacaër2012的季节性解释构成竞争机制：单次钟形曲线可与易感耗竭、季节性媒介变化、观察口径变化等机制相容。仅凭曲线形状无法识别主因。原始1907逐周表、跨年度季节序列及鼠蚤微观数据均未独立重算；本轮不升级为真实历史因果证据或未来疫情预测。

## 覆盖、去重、测试与边界

本轮理论索引已检查，无Kermack/McKendrick或感染年龄SIR原著直接阅读记录；新增跨学科原始数理流行病学与20世纪初印度城市疫情史。与TH209 May/Holling生态系统稳定性区分：本轮为感染年龄核函数、传染机制及原刊公式内部一致性，未开展跨模型熔炼。

Python标准库Fraction执行11项限定算术/逻辑断言PASS；式(30)导数已逐步手工推导并与式(29)初值核对。无原作者代码复算、1907历史表重建、现代传染病实证评分、外部团队验证，均NOT_RUN。源文件未下载/上传到公开仓库。

C010于2026-11-02完成，D003于2026-W45的2026-11-02完成，均读取现有main原文件，只读COMPLETE；不重复生成C或D。最新main的R180 original239 08-004审计仍为有限内部E1，正式采纳PARTIAL；R272生产P0、R257盲序P0仍开放，R073与PESEN v0.1保持冻结，R E1/E2/E3及MARKET不升级。Codex开放PR未并入main。

## 后续

优先核查Royal Society原刊的勘误记录及其他独立扫描，确定式(31)是否已被正式修正；随后直接阅读1907年原始鼠疫委员会p753及跨年度图表，核验Bacaër2012季节性主张的数据来源。若原件不可合法免费取得，保留PARTIAL并转其他弱覆盖领域。不得用单次曲线拟合解释社会传播，更不得把疫情模型当成群体政治/历史事件的已验证预测模型。零新增付费服务，未触发CI，实际账户计费/免费额度NOT_VERIFIED。
