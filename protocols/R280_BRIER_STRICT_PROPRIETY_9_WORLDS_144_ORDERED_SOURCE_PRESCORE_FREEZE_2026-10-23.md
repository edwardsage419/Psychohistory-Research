# R280 Brier评分：九个人工真率与报告率世界、144完整有限来源、严格适当性及有限样本误选；先行冻结

日期2026-10-23 Asia/Taipei。原239研究目录12-010 Brier Score（P1），研究R280。原始方法文献Brier (1950), *Verification of forecasts expressed in terms of probability*, Monthly Weather Review 78(1):1–3, DOI https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2；Gneiting & Raftery (2007), *Strictly Proper Scoring Rules, Prediction, and Estimation*, DOI https://doi.org/10.1198/016214506000001437，原作者公开论文 https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf 。R280严格限定自建Bernoulli四bit人工世界，未声称原创Brier理论或原作者实证复现。

## 冻结数据、评分及原source全集
真Bernoulli概率p∈{1/4,1/2,3/4}，固定预测报告q∈{1/4,1/2,3/4}，共3×3=9个人工world。每source由4个独立同p的有序Bernoulli结果组成全部2^4=16种序列，准确原概率p^K(1−p)^(4−K)，K为成功个数，合计**144个带(p,q)world标识的完整人工来源类型**；同p的三个q共享16原随机来源，绝不等于144位独立真人。

严格冻结单行Brier loss(q,y)=(q−y)^2，source四行平均Brier=S(q,x)= [K(1−q)^2+(4−K)q^2]/4；测试无模型调参，固定q在看见x之前已确定。比较每world的预测q与知道真实p的不可部署数学真率基准q=p，计算source内差Δ=S(q,x)−S(p,x)、该报告q在该source的Brier严格低于真率报告的“样本偶然胜出”标志，以及同分标志。

## 冻结理论精确值
真实未来总体risk R_p(q)=p(1−q)^2+(1−p)q²=p(1−p)+(q−p)²，严格适当性在任意真p及固定q下成立，risk regret=(q−p)²，仅q=p时为0。该“真率最优”是**对原数据生成分布的期望比较**，不宣称在有限四次实际样本上真率每次都会评分更低。九世界冻结真值：
|真p|报告q|期望Brier|期望regret|P[固定q样本评分严格优于真p]|P[固定q与真p样本同分]|
|---|---|---|---|---|---|
|1/4|1/4|3/16|0|0|1|
|1/4|1/2|1/4|1/16|67/256|0|
|1/4|3/4|7/16|1/4|13/256|27/128|
|1/2|1/4|5/16|1/16|5/16|0|
|1/2|1/2|1/4|0|0|1|
|1/2|3/4|5/16|1/16|5/16|0|
|3/4|1/4|7/16|1/4|13/256|27/128|
|3/4|1/2|1/4|1/16|67/256|0|
|3/4|3/4|3/16|0|0|1|

所有12? 本研究仅**九个world**。上述P胜出概率来自先固定q和p，观察四bit后按严格Brier均分比较。例如真p=1/2而错误报告q=1/4，四次观察中有5/16概率q=1/4获得更低样本分数，即使其总体期望Brier为5/16大于真率预测1/4。真p=1/4、错误报告3/4时，K=2导致分数相等，故同分质量P(K=2)=27/128。避免混淆单次样本偶然“胜出”与整体风险可优越。

## 双独立数学路线和第三来源审计
路线A完整穷举九world各16个有序原source，逐行保存原bit、四次固定q-Brier、四次真率p-Brier、两个平均Brier、delta、严格胜出和同分标记，原质量Fraction积分各world risk/regret/胜出与同分概率。
路线B不调用全部有序来源，直接从K∼Binomial(4,p)五类别用真实组合数计算两种样本Brier、win/tie事件真概率，并独立从平方损失期望推出R_p(q)=p(1−p)+(q−p)²。这两个路径所有九world逐Fraction相等。
路线C GitHub Actions第三作业独立重读144原source CSV，复建准确来源质量和逐行评分、source胜出与同分、各world风险与误选质量，校验完整原概率空间、结果SHA256。冻结协议先行GitHub main commit后才实施Python3.11及3.12各≥45真unittest，完整CSV/JSON/SHA机器凭证永久归档，三job完成并成功方可正式有界E1结题。

新增真人E2=0、真实历史E3=0；R073/PESEN v0.1继续冻结，下一原目录12-011 Logarithmic Score（拟R281）。保持先全R学习完成后归纳分类，最后熔炼。
