# Cavalli-Sforza 与 Feldman（1981）第二章原著范围及稳定性边界
track: theory
date: 2026-11-17 (Asia/Singapore)
observed_main_head: 4e95a91a98e6c3a95d27f3dfeab88d76b86d2b0b
target_key: (theory,Cavalli-Sforza-Feldman-1981,DOI:10.1515/9780691209357-018,chapter-2.1-stationarity-versus-stability)
status: PARTIAL; PRIMARY_PUBLISHER_OPEN_EXCERPT; NO_FORMULA_REPRODUCTION; NO_EMPIRICAL_VALIDATION

## 原始来源与实际阅读
Luigi Luca Cavalli-Sforza and Marcus W. Feldman (1981), *Cultural Transmission and Evolution: A Quantitative Approach*, Princeton University Press, Chapter 2, §2.1 “Introduction”, pp. 77–78, DOI https://doi.org/10.1515/9780691209357-018 。2026-11-17直接阅读出版社公开网页中第77页的英文原著正文节录；第78页正文、§2.2及后续递推公式未获得完整可核全文，均标为未读。出版社书籍目录及简介仅作书目信息，不能替代正文。没有购买付费内容。

## 实际新读命题与理论边界
1. 原作者明确限定第二章的基本问题为**二元文化特征的亲子垂直传递**，并暂时忽略代内差异与年龄结构。该限定排除把第二章初始模型直接用作同伴水平传播、教师斜向传播或有年龄结构的人口预测。
2. 原文区分 stationary trait frequency（频率不变）、fixation（某状态固定）、polymorphic stationary state（多个状态共存）及 stability（能否从特定初始频率达到平衡）。因此仅解出递推的不动点，不能据此断言该点可达、稳定或代表真实历史长期状态。
3. 原文列明自然与文化选择、突变、迁移、有限人口随机效应及其与传递方式的交互属于研究目标。第77页是研究计划与术语限定，不能当作作者已在此页证明各因素的定量效应。

## 独立逻辑检查（非原著公式）
令文化频率递推为 F(p)。满足 F(p*)=p* 只说明不动点。例一 F(p)=p² 在[0,1]上有不动点0和1，任意0<p<1迭代趋向0，故1虽为不动点却不能从内部初值吸引到达。例二 F(p)=2p-p² 同有0和1，内部初值趋向1。相同不动点集合不确定吸引域。两例仅为自建数学反例，不归于原作者模型，未执行程序测试或真人检验。

## 竞争解释与识别
群体文化频率稳定可能来自垂直传递平衡、水平学习补偿、迁移流入流出相抵、选择与创新抵消、抽样或测量误差。仅凭两期横截面频率无法识别这些机制。需亲子配对、同伴/教师接触、迁移及重复测量，并预先规定文化特征测量一致性和样本流失处理。与现有Hardin 1968文化再传播构造性反例的关系仅为适用范围核查，未进行项目级模型融合。

## 研究状态
新增证据：首次核实出版社公开的§2.1第77页原始正文对传递类型、年龄结构和稳定性问题的限定。未核第78页及正式递推公式，故原著公式验收PARTIAL。C 2026-11-17合格新增成果未确认；D 2026-W47既有D005仍PARTIAL。R科学验收关闭0；R073/PESEN v0.1冻结，R E1/E2/E3及MARKET不变。Tests NOT_RUN; CI NOT_RUN; 费用账单NOT_VERIFIED，未主动使用收费API或付费资源。下一步读§2.2与§2.3原始公式及其稳定性条件，优先合法开放来源；如仍不可得则转向其他开放原著。