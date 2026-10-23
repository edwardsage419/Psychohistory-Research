# R240 编码者一致性（10-014）：九人工二值编码世界与2304完整原来源

日期2026-10-23。原目录 `10-014 Inter Coder Reliability Models` P1，正式科学资格 `CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_INTER_CODER_RELIABILITY_AND_ACCURACY`。

[事前完整冻结协议](../../protocols/R240_INTER_CODER_RELIABILITY_9_WORLDS_2304_FULL_ANNOTATION_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告、首轮失败修复证据](R240_SCIENTIFIC_REPORT_2026-10-23.md) · [2304完整双编码人工原来源CSV](R240_ALL_2304_ORIGINAL_TWO_CODER_ANNOTATION_ATOMS.csv) · [原生Fraction Python生成及统计](r240_exact_intercoder_reliability.py) · [九世界κ/有限α/真实准确率结果](R240_EXACT_RESULTS.json) · [SHA256完整来源机器收据](R240_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界科研验收](R240_FINAL_ACCEPTANCE_STATUS.json)。

三组全观察`P(S, coderA, coderB)`严格相同的冻结机制均两人编码完全一致、Cohen κ=1、完整双编码有限nominal α=1，但它们的**人工真值正确率分别1、0、3/4**，证明一致不等于内容真实。人工稀少正类世界两独立编码者的原一致率Po=25/32远高于两独立平衡随机编码Po=1/2，但Pe也25/32、κ仍0，显示频率组成影响原一致。选择删掉不一致的1/4原来源后，实际入选两编码κ=1而全源真Po只有3/4，必须记录完整编码率。

首轮[CI run39887482918](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39887482918)双版本模型单测都成功，但第三归档作业误将Python整数和JSON字符串做等值比较而失败、主run failure；[只修正归档校验ba0c4776](https://github.com/edwardsage419/Psychohistory-Research/commit/ba0c4776add4d4fc63aebe629db8c7fb838ab081)后最终[CI run39887571982](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39887571982)三job completed/success，3.11和3.12各84单测通过、合计168真实测试；原2304来源及SHA机器人永久提交[262e0b9d](https://github.com/edwardsage419/Psychohistory-Research/commit/262e0b9d2305c80f8cbdb164d0c011365fca954d)。

仅E1人工，新增E2=0/E3=0；R073/PESEN v0.1冻结。下一真实原目录`11-001 Ordinary Differential Equations`（R241），先原R全部完成后统一分类，最后熔炼。
