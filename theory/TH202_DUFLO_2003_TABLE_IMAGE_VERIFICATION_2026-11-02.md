# TH202补记：Duflo 2003正式版三张关键表格的页面图像核验

track: theory
subflow: primary_source_visual_verification
run_date: 2026-11-02 (Asia/Singapore)
observed_head: d868ce264417fa631e684c5f883b2a1eabdbd344
target_key: (theory,Duflo2003-WBER17-1,2003-published,Table3-5-7-image-versus-text-verification)
status: COMPLETE_BOUNDED_TABLE_IMAGES; NO_NEW_EMPIRICAL_ESTIMATE

## 直接来源与页面

Esther Duflo (2003), *Grandmothers and Granddaughters: Old-Age Pensions and Intrahousehold Allocation in South Africa*, *World Bank Economic Review* 17(1):1–25, DOI 10.1093/wber/lhg013，世界银行保存的正式期刊排版PDF https://documents.worldbank.org/curated/en/672331468115470710/pdf/774010JRN020030PUBLIC00Grandmothers.pdf 。本轮使用原始PDF页图直接目视核验印刷p9 Table 3、p15 Table 5、p21 Table 7及各表的列标题、显著性星号、脚注。此前同一研究的正式版正文已读范围及2000工作稿对照见TH202_DUFLO_2003_PUBLISHED_ESTIMAND_AND_IV_CORRECTION_ADDENDUM_2026-11-02.md。

## 图像核验结果

1. p9 Table 3女童列6为女性养老金资格0.61（SE0.19）、男性资格0.056（SE0.19），样本1533；列7为实际领取养老金的2SLS女性1.19（SE0.41）、男性负0.097（SE0.74），样本1533。列7注释明确使用男女资格作为工具变量，SE允许同户相关与异方差；该表星号为5%阈值。两列估计对象不同。
2. p15 Table 5女童列3将祖辈存活作为处理变量，女性×YOUNG为0.40（SE0.27），无星号；列4是领取养老金2SLS，女性×YOUNG为1.16（SE0.56），有星号。此表星号注释为10%阈值。此表中的0.40不能解释为养老金领取IV，不能把2000年早稿的祖辈存活IV自动当作正式版结论。
3. p21 Table 7储蓄2SLS中女性养老金收入系数0.82（SE0.16），男性0.53（SE0.22），非养老金收入0.50（SE0.041）；表格说明使用就业状态、行业、工作类型及女性资格、男性资格等工具变量。两点估计差0.29，缺乏协方差矩阵时不可独立声称男女差异显著。
4. 三张表的页面图像与此前PDF可提取文本记录的上述关键单元格一致，关闭此前TH202补记标注的三张表格视觉核验缺口。仅核对指定列、行和表注，未逐格审计所有表格，也未下载原始SALDRU微观数据。

证据级别：同一篇论文的文献版本/图像核验，无新增独立研究、样本、统计重估、因果识别或R E1/E2/E3。C010已于2026-11-02完成、D003已于2026-W45的2026-11-02完成，本轮只读。新增费用0，实际计费NOT_VERIFIED，CI NOT_RUN。

下一步：继续检查正式版未核对的其他表格或原始微观数据的合法取得路径，优先推进不同学科的独立原著阅读。