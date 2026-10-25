# A 数据侦察：UN WPP 2024 年龄结构人口数据，R151 真实历史 E3 候选

日期：2026-10-25。状态：OFFICIAL_METADATA_AND_LICENSE_VERIFIED / FULL_ROW_EXTRACTION_NOT_COMPLETED / HISTORICAL_SCORING_NOT_STARTED。

## 来源与版本
联合国人口司 World Population Prospects 2024 官方入口：https://population.un.org/wpp/ 。官方英文页面说明：1950年以来的年龄和年度人口估计、2024年以后的未来情景，提供单岁和五岁年龄组数据，CSV批量下载入口公开。2024版以237个国家或地区为覆盖对象，但不能据此声称全部237个国家的每个年份、每个年龄字段完整。

官方指标元数据：
- 五岁年龄组与性别，indicator 46：https://population.un.org/dataportal/data/indicators/46/locations/158/start/1950/end/2099/metadata?df=8e78a9c1-5faa-4199-9058-d0cb5d0041a5
- 单岁年龄组与性别，indicator 47：https://population.un.org/dataportal/data/indicators/47%2C49/locations/756%2C276%2C40%2C250%2C380/start/2024/end/2024/metadata/metadataindicators?df=a3b3fb95-9793-47de-b312-6f6d8d5ba0bd
- 官方数据 API 说明与许可：https://population.un.org/dataportalapi/index.html ，页面注明 CC BY 3.0 IGO，且 API 数据端点需要授权 token。当前无需注册的 CSV 下载路径优先于 API，未申请 token 或付费账户。

## 数据字段与时间门
候选主键：国家或地区 location，year，sex，age group，variant。人口值应核实 persons 与 thousands 单位，不得将不同接口的单位混合。WPP 2024 的1950至2023段属于估计历史，2024以后为预测情景。历史数据是经过模型协调与插值的统计估计，不是每个年龄每年都有独立原始普查测量。

R151 人工三年龄组 J、A、O 未定义真实年龄界限。必须在历史评价前事先冻结三组年龄区间、性别合并、时间间隔、人口迁移处理、年龄上界组和预测基线。WPP 单岁/五岁人口不能直接作为 R151 现有三组方程参数的已验证实测输入。人口年龄分布可以用于外部描述性核对，模型训练、参数拟合和留出预测需要新协议，且原 R151 E1 冻结不变。

## 实际获取与风险
本轮已读取联合国官方英文 WPP 首页、五岁年龄组指标元数据、单岁年龄组指标元数据及 API 文档。尚未获取原始批量 CSV 的完整字节、固定校验值、行数、国家年份交集、缺失率或许可随文件元数据；不能声称历史 E3 复现完成。API 授权 token 要求是本轮接口阻塞，不等于免费 CSV 不可获取。未访问私人数据、未使用中文网站、未购买数据。

下一步：在免费 CSV 下载中心获取并固定 WPP2024 文件、SHA256 和字段；剔除世界及地区汇总避免与国家重复计数；仅保留历史估计年份，先冻结跨国家/年份留出与概率或点预测评分协议，再进行 E3。若数据仍不可取得，记录阻塞。R073 与 PESEN v0.1 保持冻结。
