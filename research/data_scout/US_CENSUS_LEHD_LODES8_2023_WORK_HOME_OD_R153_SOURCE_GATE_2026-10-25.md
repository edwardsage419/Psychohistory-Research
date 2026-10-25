# A 公开实证数据侦察：US Census LEHD LODES8 工作地与居住地 OD 2023

日期：2026-10-25 UTC+08。研究轨 A。写入前 main HEAD `6ceb9ca81f99e7f4efe0b37e305783d3e9df2146`。已检查现有 `research/data_scout/US_CENSUS_ACS_2016_2020_COUNTY_OD_E3_SOURCE_GATE_2026-10-25.md`；本来源为就业通勤流，ACS来源为一年迁居的五年汇总抽样，行为含义与数据生产机制不同。未找到仓库中已有LODES专属登记的提交，仍须在未来下载后做更细去重。

## 一手官方英文来源与版本

1. U.S. Census Bureau, LEHD Data Products for Workforce Analytics, https://lehd.ces.census.gov/data/ ，说明 LODES 为公开发布的就业OD数据，LODES8采用2020人口普查区块地理单元，覆盖多数州2002至2023年。
2. 官方 LODES 8.4 技术说明（2025-12-03修订），https://lehd.ces.census.gov/doc/help/onthemap/LODESTechDoc.pdf ，直接核对第1、5页的CSV压缩、OD文件命名和13字段。
3. 官方俄勒冈州 OD 目录，https://lehd.ces.census.gov/data/lodes/LODES8/or/od/ ，实际网页列出 `or_od_main_JT01_2023.csv.gz`（约8.8 MB）和 `or_od_aux_JT01_2023.csv.gz`（约832 KB），前者工作地与居住地均在州内，后者工作地在州内、居住地在州外。目录存在是已核实的网页事实，文件字节、CSV行数及hash尚未取得。
4. 官方开放数据与引证说明，https://www.census.gov/topics/research/research-transparency-public-access/open-data.html 及 https://www.census.gov/about/policies/citation.html 。确认此产品属于官方公共数据分发渠道，引用需注明机构、产品、文件名、版本和访问日。LODES文件专属授权条款尚未独立逐条核读，未来再分发原始数据前须核验。

## 字段与时间单位核查

OD文件格式：`w_geocode`（15位工作地 Census Block）、`h_geocode`（15位居住地 Census Block）、`S000`（就业岗位总数）、`SA01/SA02/SA03`（年龄组）、`SE01/SE02/SE03`（月收入分组）、`SI01/SI02/SI03`（行业分组）以及 `createdate`。来源方向需以 h_geocode→w_geocode 映射为居住到工作，不得颠倒。JT01 表示 Primary Jobs；JT00 为 All Jobs，两者不可混合后声称独立岗位。2023为数据年度，createdate为文件制作日期，均不是逐回合人类决策时间戳。主文件与辅助文件应合并后再解释州内工作地的完整来源范围；若只用main，必须明示跨州居住者被排除。

本数据属于公开披露处理后的岗位聚合流量。不存在个人身份、逐次选择、实验session或真人重复博弈行动。它可支持R153空间OD模型未来独立年度历史检验的设计，但R153原有24组人工边际和距离核不得直接视为已在现实估计。E3所需地理映射、零值解释、通勤距离、跨年区域边界一致性、训练年与留出年、基线及样本外评分必须另行预冻结。2020区块基础、披露保护和年度覆盖差异均可能影响比较。

## 可获得性、许可与复现难度

状态 `OFFICIAL_DIRECTORY_AND_SCHEMA_VERIFIED / RAW_GZIP_NOT_OBTAINED / FILE_LICENSE_TERMS_PENDING / E3_NOT_STARTED`。本环境直接网络下载受限，未取得2023原始gzip字节；无法声称CSV列已按行解析、完整度/缺失率、真实行数、实际空间零流或跨年可比性已核验。未来使用免费官方gzip文件，在本地标准库gzip/csv读取，保留压缩文件SHA256，验证15位区块码、非负计数、重复OD键、按居住/工作边际汇总，并固定训练2021至2022、留出2023等方案前先核对各年可用性。此训练留出安排只是待冻结候选，不能计为完成的E3预测。

R073冻结双人行动预测协议不适用此数据。E1新增0、E2真人预测新增0、E3历史预测新增0。无注册、无购买、无私人受限数据、无计费API、无云计算。来源均为英文官方页面。
