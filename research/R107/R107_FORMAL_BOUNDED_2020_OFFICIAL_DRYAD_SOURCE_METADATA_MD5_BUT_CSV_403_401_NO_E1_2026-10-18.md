# R107 2020原作者Dryad空间博弈数据：第一手文件目录和官方MD5确立，但两条公开交付路径均受限，E0正式止损结题

日期2026-10-18。**`R107=CLOSED_E0_ORIGINAL_PUBLIC_DATA_ACCESS_BLOCKED`，官方文件元数据确立，完整原文件SHA/MD5匹配尚不能执行，E1=NO，真人预测E2=0。R073及PESEN v0.1冻结。**

## 一、实验与2020原作者公开原数据的可独立佐证部分

Grujić与Lenaerts 2020论文，*Do people imitate when making decisions? Evidence from a spatial Prisoner’s Dilemma experiment*, `Royal Society Open Science` 7:200618，DOI [10.1098/rsos.200618](https://doi.org/10.1098/rsos.200618)。第一手公开作者数据集[Dryad DOI 10.5061/dryad.7fq25s8](https://doi.org/10.5061/dryad.7fq25s8)，2020-07-27公开，包含`DataSet.csv`、作者英文README及两类原实验英文说明。论文及数据介绍的真实人类行为任务为16人4×4周期网络、四邻居、多轮策略选择及两个有/无收益反馈制度条件。作者论文里报告的实验轮数等并不等于本项目真实文件核验，不能由其直接制造样本计数。实验团队与R106 2025伯明翰独立实验不同；作者Lenaerts与R096团队有交叉，受试者样本是否重叠仍需原实验招募记录证实，不能仅凭DOI不同宣布完全独立队列。

## 二、源A严格文件原先已冻结，只得到真正HTTP403

在任何人体原始行动处理之前已冻结[官方Dryad原CSV第一手严格双重下载和仅表头协议](../../protocols/R107_PHASE_A_GUJIC_2020_DRYAD_ORIGINAL_DATASET_CSV_OFFICIAL_DOUBLE_SHA_HEADER_ONLY_FREEZE_2026-10-18.md)，固定公开UI里`/downloads/file_stream/296893`文件ID，HTTPS exact host/path、拒绝域外跳转、文件最多1MiB；16项纯synthetic测试先通过。真正GitHub Actions run [39128368647](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39128368647)的原始源下载返回**`R107_A_OFFICIAL_DRYAD_403_FORBIDDEN`**并安全终止；[A完整失败收据](R107_PHASE_A_LIVE_CI_DRYAD_2020_SPATIAL_ORIGINAL_CSV_DOUBLE_SHA_HEADER_RECEIPT.json)真实存入main。未读取原CSV正文，亦未触碰人类行为。403不能证明资料错误或不存在。

## 三、独立预冻A2官方元数据只读恢复官方精确文件身份

据[Dryad官方REST接口文档](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/README.md)独立预冻[A2两条精确元数据URL协议](../../protocols/R107_PHASE_A2_DRYAD_PUBLIC_API_FILE_METADATA_AFTER_403_FINAL_DIAGNOSTIC_FREEZE_2026-10-18.md)，12项纯synthetic通过。真正GitHub Actions [A2脱敏收据](R107_PHASE_A2_LIVE_CI_DRYAD_OFFICIAL_PUBLIC_API_METADATA_DIAGNOSTIC.json)实测两官方JSON接口HTTP**200**，实际匹配数据集DOI和文件名：
- 真原作者**DataSet.csv**，Dryad官方原文件ID **296893**。
- 出版方原文件完整元数据字节数 **215,221 bytes**。
- 出版方发表原文件的**MD5 `039b5cc661fb62210509ac9f8de388d7`**，算法`md5`。**仅出版社官方元数据摘要，未曾与原数据文件实字节重算相匹配**，不可虚称E1成功。
- 本次A2未下载一字节原CSV；从元数据不能推断实验参加人数及实际观察轮数。

## 四、一次且仅一次冻结官方API候选文件下载，真实HTTP401终止

从A2发表的真实元数据出发，另行预冻[A3唯一允许的官方API文件URL与发表MD5全文匹配规则](../../protocols/R107_PHASE_A3_OFFICIAL_DRYAD_API_296893_MD5_BOUND_ALTERNATE_DOWNLOAD_FREEZE_2026-10-18.md)：`https://datadryad.org/api/v2/files/296893/download`，只能当前HTTPS网站原域、拒绝新重定向、精确215221字节及发布MD5，独立两次下载+SHA相等、应用仅解析CSV表头。14项纯synthetic顺序先通过，真实源执行得到**`R107_A3_OFFICIAL_API_REQUIRES_AUTH_401`**，属于公开下载需认证的**HTTP401**，并自动归档[真实A3来源拒绝收据](R107_PHASE_A3_LIVE_CI_ORIGINAL_DRYAD_API_296893_MD5_DOUBLE_SHA_HEADER_ONLY_RECEIPT.json)。原发布方元数据仍然成立，原字节下载未完成。

两条经独立冻结的官方候选交付路径分别403和401；按照A2/A3止损条件，**不继续猜测镜像/重定向/令牌，也不要求项目主人开支、注册或绕过权限**。该源码本身留作可复现实证出处，与无法开展下一层科学评分严格分开。

## 五、科学验收与下一工作

| 科学/归档要素 | 结果 |
|---|---|
| 2020独立发表论文与Dryad DOI存在 | 已核实 |
| 原作者文件准确ID、文件名、元数据大小和官方发表MD5 | **元数据真实验证** |
| 原CSV 215221字节实际下载、原发表MD5实算相等 | **BLOCKED** |
| 原CSV字段、真实实验session、唯一人号、网络格点与位置 | **UNKNOWN** |
| 原真人策略值或个人记录被项目读取 | **0** |
| 独立次轮目标及模型M0–M4评分 | **0** |
| A1/A2/A3预冻协议、40+纯来源synthetic与真HTTP阴性收据 | **ARCHIVED** |
| 结论 | **E0受限，不属于心理史学理论阴性实证** |

这一次阻断对于模型竞争只说明**样本来源不能在冻结的合法权限条件下使用**，不能解释为四邻居历史无效、模仿机制没有发生或2020原实验结果不可信。下一编号R108检索优先出版社公开直接来源和独立MD5、真实原实验场次、人/对手身份及逐回合原行动，提前设同分布/同方差真实错误对手和普通收缩负对照，不能把同一数据仓库的转载记为独立实验。R073/PESEN v0.1继续冻结。
