# R101 Phase A：Stallen 等2023独立合作实验原作者DataverseNL元数据来源闸门

日期：2026-10-17。状态：BEFORE_ORIGINAL_DATA_METADATA_VERIFICATION_FROZEN。R100已行政限定结题，其数据的C:Z实际贡献值从未读取；PESEN v0.1继续冻结。

## 公布的候选来源（论文事实，不等于项目原CSV验收）

Stallen, Snijder, Gross, Hilbert, De Dreu (2023), *Partner choice and cooperation in social dilemmas can increase resource inequality*, [Nature Communications 14, 6432](https://doi.org/10.1038/s41467-023-42128-2)，公开真人336人，以八人群体为互动结构，在每个回合根据固定分配或自行选择偏好配对成双人公共品局。作者发表原数据与代码位置[OSF CASQZ](https://doi.org/10.17605/OSF.IO/CASQZ)。另有作者机构[UvA官方人员页面](https://www.uva.nl/en/profile/h/i/l.p.hilbert/l.p.hilbert.html)明确提供同一论文数据归档[DataverseNL DOI 10.34894/EYFM5L](https://doi.org/10.34894/EYFM5L)。这两源都尚**未**由R101实际下载任何原研究数据或验证其来源文件字节。336、八人、回合配对等均暂属于论文设计数字，不能当本项目来源识别出的真正样本与独立session。

## Phase A只允许元数据检查

1. 唯一准用API为 `https://dataverse.nl/api/datasets/:persistentId/?persistentId=doi%3A10.34894%2FEYFM5L`，只许HTTPS及精确 `dataverse.nl`、路径、查询；重定向到外域、权限403/503、返回值异形均安全阻断，不能改用任何搜索代理或克隆站点的数据假装官方。
2. 原始API JSON须小于2MiB，无认证token或用户隐私文件；仅从原服务官方`data.latestVersion.files`目录提取文件数、匿名扩展名、大小/官方原MD5有无、文件类型、是否具可判别文本CSV/TSV候选。不得下载`/api/access/datafile`内容、不得读取source行动、个人或对手ID；所有样本数字尚未核验。
3. 官方Dataverse dataset DOI由API元数据和配置锚定，必须确认来源自身声明与`10.34894/EYFM5L`对应，不能把原论文引用当API真实性。确认失败即E0。
4. 报告不保留原fileID或私人URL；只保存格式种类、来源DOI、有效文件总数、已声明MD5的条数、文本文件候选数、错误类型及**实际真人评分0**。官方MD5即使出现仍未实际核验下载字节，不能将“元数据有哈希”称为E1原文件真实性。
5. 必须先跑纯synthetic覆盖伪域、错误DOI、非JSON、缺版本、文件数异常、恶意格式；再跑真正Dataverse元数据，只产匿名JSON收据并通过GitHub机器人永久归档。此阶段一律不判成绩正负。

## 下阶段资格

A成功仅证明官方元数据目录能访问；然后另先冻结实际源文件下载的URL/fileID、已发表MD5/完整SHA、人物/伙伴/轮次/场次**非行为**字段审核标准。即使原作者说336人，真实数据如缺明确actor/opponent和多实验室独立session，也必须有界拒绝或降低留出单位，不能和R073原规则混称完全同目标复制。OSF若再现R097的503应保留负证；可使用正式DataverseNL发布但必须认证来源。PESEN v0.1=FROZEN。
