# R164 内容偏向传承｜72组人工内容权重与文化频率有理数动力学

日期：2026年10月21日。原始目录 **P1 / 07-006 Content Biased Transmission**。研究阶段正式 **CLOSED_BOUNDED_E1**。本研究仅观察人工信息A/B的抽象频率，不使用实际心理实验材料、真人记忆、真实文化故事、宗教信念或历史社会变迁数据。

一手出版来源：[Barrett与Nyhof2001原论文](https://doi.org/10.1163/156853701300063589)及[牛津大学研究记录](https://ora.ox.ac.uk/objects/uuid%3Aa6ed93bb-3ba0-4934-adec-9bb827cf8e9f)研究某些违反预期的叙事特征在记忆和传递中的优势；[Boyer与Ramble2001原论文](https://doi.org/10.1016/S0364-0213%2801%2900045-3)在法国、加蓬和尼泊尔开展记忆实验，区分不同种类的概念预期违反；[Stubbersfield等2015原刊](https://doi.org/10.1111/bjop.12073)区分信息接收、记忆提取及主动转发。我们核对正式出版方及大学记录，**未获取原论文的参与者逐项回忆资料，也没有复算其效应大小**。详细来源及理论限制载于[正式科学报告](R164_SCIENTIFIC_REPORT_2026-10-21.md)。

**冻结72组人工场景：** 初始人工A内容比例四档，A内容抽样权重r三档（1、2、4），按内容倾向复制的比例h三档（0、1/2、1），对称随机替换份额e两档（0、1/4），共72组。每组运行从t0至t4的五个时间点。项目自建加权选取公式\(S(p,r)=rp/(rp+1-p)\)，更新\(p_{t+1}=(1-e)[(1-h)p+hS(p,r)]+e/2\)。所有变量仅为数学符号，**r没有由真实记忆实验校准**。

**两套独立有理数实现：** 直接公式Fraction递推；另外独立把A与B信息视为不同抽样权重的两类筹码，分别计算随机复制、内容偏向复制与替换。全部72组×5期的每个A频率严格相等。所有中间概率及完整输出均保存在[89,087字节原始JSON](R164_EXACT_RESULTS.json)。

**预设数学结果：**
* 当内容优势r=1时，是否使用内容加权没有影响；h=0时，r无论是多少都不影响整个频率路径。后一情形即使有全部频率观察，仍不能根据这一路径识别r。
* 人工起点A占1/5且r=4时，A被内容加权选取的概率为1/2；若完全按照内容抽样且不出现重置，采纳A的赔率每期乘以r。
* 当p=4/5、r=2、h=1、e=1/4时，内容抽样前倾向A的概率从4/5增加至8/9，但经对称重置后实际下一代频率成为**19/24，约0.791667**，低于初始4/5。单一内容优势因素不能推断所有条件下最终频率必然上升。
* 内容频率高不自动表示真实性、知识质量或实际适应价值。此研究没有测量任何信息真值或实际认知过程。

**真实远程计算验收：** [首轮GitHub Actions 39529224497](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39529224497)、[固定四项哈希轮39529293414](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39529293414)及[最终归档轮39529323641](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39529323641)均成功。Python3.11与3.12三轮各102项真实测试，独立归档另执行102项，共714次单测执行、102种不同测试、0失败。完整JSON及源码测试压缩包已永久写入[归档提交ccb1f2f](https://github.com/edwardsage419/Psychohistory-Research/commit/ccb1f2fa8be0075a43d1e47a8d85708b8901a9ee)。

全部材料：[事前冻结协议](../../protocols/R164_CONTENT_SALIENCE_72_FRACTION_COPYING_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交5c403e6）｜[科学报告](R164_SCIENTIFIC_REPORT_2026-10-21.md)｜[原生程序](r164_content_salience_exact.py)｜[102项测试](test_r164_content_salience_exact.py)｜[完整结果](R164_EXACT_RESULTS.json)｜[原生完整ZIP](R164_Content_Salience_72_Worlds_102_Tests.zip)｜[正式机器验收](R164_FINAL_MACHINE_ACCEPTANCE.json)。

固定SHA256：
* 程序 `27252e908413335780e43f8bb4bb089d2abb0cd4ba31cc2967d63480f6f89133`
* 测试 `a5dc28d23e8ed11f3c3b6b4ec3b8bd3e8d5d8ff3d6ef1e7ccc85f4666b84b013`
* JSON `ce27a70aee6ee82ca360efc93b12632c44f6bbd7a73b32bf1aaafc602df69f52`
* ZIP `271beda59c738310a608b7e65eb88f9144159d40441aef180ddf7aa11b4f3e55`

复算方法：进入 `research/R164`，执行 `python r164_content_salience_exact.py > R164_EXACT_RESULTS.json` 和 `python -m unittest -q test_r164_content_salience_exact.py`，仅用Python标准库。

**科研证据等级仍为E1，新增真人独立验证E2=0、历史外推E3=0。** R073与PESEN v0.1继续冻结。下一原目录 **R165 P1 / 07-007 Neutral Cultural Drift（文化中性漂变）**，全部既定R研究完成后再统一分类、最后开始熔炼。
