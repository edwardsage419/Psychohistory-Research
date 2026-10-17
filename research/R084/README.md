# R084：七实验室真实制度选择实验的原作者数据来源门（2026-10-17）

当前研究范围：2023年 [Lo Iacono 等发表于 PNAS Nexus 的七实验室合作制度选择复验](https://doi.org/10.1093/pnasnexus/pgad091)。这是2023年已经发表的 **1008人、7个实验室×12组×12人、30轮**内生制度选择实验，研究对象是参与者自主加入有奖励/处罚制度SI或无惩罚制度SFI之后的公共品贡献与收益。作者报告预注册的三项联合复验标准有5个实验室全部满足，Oxford、Warsaw未全部满足。这是**作者发表的历史结果，R084尚未独立从原始真人决策行算出任何一个效应值**。

研究问题：验证原作者公开在OSF的实验数据与分析代码是否真实可取、是否具备以后按人-实验室-组-轮复算的来源资格，而不是把R083的个体条件性惩罚偏好直接类比成真实制度选择的因果效应。原始发表文章在Data Availability与Introduction分别给了两个不相同的OSF访问链接，应保留证据不将不同网址自动当作同一稳定版。

目前已在 OSF 自身的公开 Trove 元数据 [Sergio Lo Iacono 原作者条目](https://share.osf.io/trove/index-card/eccbea3d-0a61-4584-92c5-2dec9dd84f6f)找到 OSF 元数据记录：component `r7y9n`（Replication Data），原始文件ID `fjyg3` 名为 `Utrecht_sbj.csv`，版本1，公开索引SHA256 `f85367e8fff52c29384e51b48baa2b4efed4014c2ef08c00c9ec4549e6d65f3d`；**这些只是文件索引的公开元数据，不能当作我们的真人文件校验通过或实际复算结果。**

新 R084 来源运行之前已冻结 [限定协议](../../protocols/R084_MULTILAB_INSTITUTIONAL_SELECTION_SOURCE_GATE_FREEZE_2026-10-17.md)，commit `43dd26ecaad1160ea33015c795751a3630302e76`。本阶段只允许元数据巡检、原始文件身份验证和访问状态，不获取任何原始个人选择行。已建立[元数据来源守门程序](r084_original_osf_7lab_metadata_source_gate.py)、[26项纯合成安全测试](test_r084_original_osf_7lab_metadata_source_gate.py)及[首次真实官网元数据访问CI](../../.github/workflows/r084-original-2023-seven-lab-OSF-metadata-source-gate.yml)。正式E2必须在成功获得原始来源字节、冻结字段/组聚合与评分规则、且作者源码资格验收后重新授权另立执行关口。

特别边界：个人在每轮主动选择加入SI/SFI使其行为不是随机分配制度的简单因果比较；原文的“5/7通过”是实验复验结果，不等于“七实验室均获独立制度因果识别”；R083个体惩罚偏好与本实验没有共同参与者的可验证链接；PESEN v0.1继续FROZEN。
