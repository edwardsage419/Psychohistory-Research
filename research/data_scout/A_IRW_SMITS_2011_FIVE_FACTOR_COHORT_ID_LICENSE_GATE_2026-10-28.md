# A轨：Smits等2011跨队列人格量表来源、身份及许可审计

日期：2026-10-28。状态：SOURCE_CODE_AND_METADATA_VERIFIED / ROW_BYTES_NOT_RETRIEVED / E2_NOT_QUALIFIED。

## 公开来源与原始研究

原论文 Smits, Dolan, Vorst, Wicherts & Timmerman (2011), *Cohort differences in Big Five personality factors over a period of 25 years*, DOI 10.1037/a0022874。论文摘要明确研究1982至2007年荷兰心理学新生人格问卷的跨队列测量等值性，发现70道题中女性11道、男性2道存在跨队列项目偏差；该发现来自原论文，未在本轮独立复算。论文公开摘要：https://pubmed.ncbi.nlm.nih.gov/21534699/

Item Response Warehouse (IRW) 数据页面 https://itemresponsewarehouse.org/tables/5personalityfactors/ ：记录623105条响应、8954个受访者、70道题、7类回答、响应密度0.994，成人样本，标注Longitudinal=FALSE、CC BY 4.0。网页显示IRW版本v600、Redivis数据集v74.0、manifest v74.0；此版本标识仅限本轮访问时看到的页面，须在正式复现前再固定实际下载字节哈希。直接CSV下载入口标记无需账户；本轮通过网页请求该CSV，工具返回不支持text/csv的读取错误，未取得数据字节，不能把元数据行数声称为逐行核验。

## 实读转换脚本与具体风险

读取原作者数据转换仓库 https://github.com/ben-domingue/irw/blob/main/data/5personalityfactors.R ，仓库main提交 `925f690f421cd4e24622fe79cfde4895ede1d7a3`，该脚本Git blob `2a8e6042c0769ceb1535eed3ac30356ad4facb62`。

脚本明确报告源字段TWNO有18个重复编号对，并将重复编号分别追加字母后缀，避免合并不同受试者。脚本注释举出同一TWNO编号具有不同性别与年龄的例子。该18对结论为转换作者的代码注释，尚未读取源表独立逐行验证。

转换程序把原始70道题从宽表变成长表，保留匿名id、item、resp、年龄协变量，剔除原始cohort和testweek；源数据注释称cohort有13个取值，testweek有25个取值。因时间字段未随IRW长表保存，这份标准化表无法直接复算原论文的跨队列项目漂移分析。原研究跨1982至2007年多批次抽样，不能误作同一受访者跨25年纵向追踪。

## 许可、身份与可获得性门槛

IRW页面标CC BY 4.0，转换脚本注释称DANS原存档为CC0；B2FIND聚合元数据同时出现CC0、restrictedAccess和OpenAccess=false，并有另一段CC BY 3.0说明，见 https://b2find.eudat.eu/dataset/ea398991-7a6f-56e6-bfa8-51ff62770063 。这些来源的权利声明与访问状态并不一致。原存档DOI为10.17026/DANS-Z5P-ZEDJ。未确认哪一许可覆盖当前可下载的具体数据版本，故本轮不复制人级原始数据到项目仓库。

字段门槛：响应值1至7、70题、匿名人ID、年龄在脚本中可确认；实际行数、身份碰撞修复、缺失值、分组可用性尚未从CSV独立确认。时间门槛：IRW衍生表缺cohort/testweek，无法进行跨期DIF实证复验。场次门槛：原研究是跨年度不同入学批次，独立抽样单元与重复参与须从原始源表复核。R073资格：人格问卷不属于双人100轮囚徒困境，直接评分=NO。复现准备状态：原始行字节BLOCKED；原论文跨队列机制复算BLOCKED；只读来源审计完成。

## 后续与证据级别

优先从明确无需账户且有明确授权的公开来源取得完整原始CSV及codebook，校验SHA256、时间字段、唯一ID、题目编码与各队列独立性；如原始存档限制访问则保持BLOCKED，不绕过权限。另继续寻找符合R073冻结协议的独立真人重复博弈。新增E2评分=0，新增E3=0。没有下载个人级数据、注册账户或产生费用。