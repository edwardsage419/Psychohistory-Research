# A 子流程：美国 ACS 2016至2020县际迁移 OD 公开来源及 E3 准入登记

日期：2026-10-25。候选与 R152 人口迁移引力模型有关。数据来源为美国 Census Bureau 官方英文资料，研究阶段为来源与字段核验。未取得实际迁移行记录，历史E3验证尚未开始。

## 一手来源与数据可获得性
官方2016至2020 ACS县际迁移页面：
https://www.census.gov/data/tables/2020/demo/geographic-mobility/county-to-county-migration-2016-2020.html
官方2016至2020技术说明，17页：
https://www.census.gov/content/dam/Census/topics/population/migration/guidance-for-data-users/acs-migration-tutorial/2016-2020-Migration-Flows-Documentation.pdf
官方迁移流API概览：
https://www.census.gov/data/developers/data-sets/acs-migration-flows.html

页面确认全国县际有向迁移流固定宽度文本文件存在，All flows 文件约105.9MB，另有县际流入、流出和净/总迁移Excel或文本文件。官方文档第6至9页定义固定宽度字段。当前执行环境无法取得数据文件字节；尝试打开 Census 2020 API variables.json 未成功，且官方API总览提示目前查询需要API key。遵守零新增费用与无新账户要求，本轮没有申请API key或下载收费资源。原始数据逐行行数、哈希、缺失率、实际数据许可文件级条款仍未核验。公开发布页面已确认，具体许可条款仍为待核，不擅自推定。

## 已核对的字段与时间语义
技术文档列明现居地州县FIPS代码（固定宽度第1至6位）、一年前居住地州县FIPS（第7至12位）、现居县和一年前居住县名称、县际迁移人数估计（第374至380位）、对应90%误差幅度（第382至388位）。独立的Net/Gross文件包含双向流量、逆向流量、净流量及总流量，且有各自90%误差幅度。

2016至2020为五年汇总样本窗口，问题询问调查时点的一年前居住地。不能把它当作五个逐年独立迁移事件或完整个体追踪轨迹。美国ACS为抽样估计，包含抽样和非抽样误差；空白、无记录与披露限制必须依官方说明区别处理。不能直接把迁移估计数视作精确整数微观行动。

## 适用性与阻塞
适合R152未来E3历史空间迁移聚合检验，前提是固定地区集合、真实地理距离、训练与独立时间窗、估计不确定性和边际预算规则。R152当前四个人工地区的参数不可直接当作真实美国县际参数，须另行预冻结经验模型及评分协议。连续五年重叠ACS窗口不能视为独立年份样本。该来源不符合R073二元真人重复博弈协议，禁止挪作R073外部预测。

本轮状态 `SOURCE_AND_FIXED_WIDTH_SCHEMA_VERIFIED / RAW_ROWS_NOT_OBTAINED / LICENSE_FILE_TERMS_PENDING / E3_NOT_STARTED`。下一步仅在零费用下尝试读取可控大小的官方文本子集，核验实际字段与方向、缺失、许可和时间窗，再设计独立历史样本外评分。新增独立真人实验0，新增E2评分0，新增E3评分0。
