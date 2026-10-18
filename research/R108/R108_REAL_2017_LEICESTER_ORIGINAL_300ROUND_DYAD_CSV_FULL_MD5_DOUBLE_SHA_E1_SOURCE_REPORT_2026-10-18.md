# R108正式研究结果：2017莱斯特大学固定双人300轮实验原作者真实CSV通过出版社全文MD5与双重SHA；目前E1，原列身份尚未确认

日期：2026-10-18。**R108=E1_VERIFIED_ORIGINAL_PUBLISHER_FILE_BUT_PERSON_PAIR_ROUND_MAPPING_PENDING；原创行为E2=0，R073与PESEN v0.1 FROZEN。**

## 原作者实验与样本独立性

英国莱斯特大学Colman、Pulford、Krockow，2018年 *Acta Psychologica*论文 `Persistent cooperation and gender differences in repeated Prisoner's Dilemma games: Some things never change`，DOI [10.1016/j.actpsy.2018.04.014](https://doi.org/10.1016/j.actpsy.2018.04.014)。论文说明实验采用**固定两人配对、连续300轮**的有限视野重复囚徒困境，且在英国的新样本中研究策略合作与终局效应。2017-09-14由原作者在[莱斯特大学正式Figshare数据页面](https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938)公开原始数据及实验说明。该来源与R106 2025年英国伯明翰260真人不同作者、机构、时间与任务设计，**但是否有可用于独立实验场次留出而不跨人物的来源标识仍未实际核实**。大学Figshare页面标明All Rights Reserved，研究不对外转发原个体数据。

## A0原作者真实官方文件目录：正式出版社摘要首次绑定

[先冻A0仅发行目录元数据](../../protocols/R108_PHASE_A0_LEICESTER_2017_FIGSHARE_300ROUND_FIXED_DYAD_ORIGINAL_PUBLISHER_FILE_METADATA_ONLY_FREEZE_2026-10-18.md)，13项synthetic成功；GitHub Actions[真实A0机器收据](R108_PHASE_A0_LIVE_CI_UK_LEICESTER_FIGSHARE_2017_ORIGINAL_FILES_METADATA_RECEIPT.json)证明真正出版社文章文件ID **10194938**，真源CSV文件ID **18370526**，源名 `Repeated Prisoner's Dilemma_raw data-data.csv`、准确**36,526字节**、发布方原全文**computed_md5 `7afc755c293dc261d696d1b3f9ba796a`**；另官方实验说明文件ID 18370529。A0不读取原个体数据。

## A1/A2/A3一次正式合法委托源链验证与安全否定

[A1冻结精确原官方下载路径+MD5+双源SHA](../../protocols/R108_PHASE_A1_2017_LEICESTER_FIGSHARE_ORIGINAL_DYAD_18370526_PUBLISHED_MD5_DOUBLE_SHA_HEADER_FREEZE_2026-10-18.md)，15项synthetic先通过；首次真官方下载报告`R108_A1_UNAUTHORIZED_ORIGINAL_SOURCE_REDIRECT`（原路径官方Figshare将文件302重定向，原安全白名单禁止隐式跨域）。[A2独立冻结不读取文件正文的重定向主机审核](../../protocols/R108_PHASE_A2_FIGSHARE_OFFICIAL_DOWNLOADER_REDIRECT_HOST_NO_BODY_FREEZE_2026-10-18.md)，11项纯synthetic与真实执行后[机器收据](R108_PHASE_A2_LIVE_CI_FIGSHARE_OFFICIAL_DOWNLOADER_REDIRECT_HOST_ONLY.json)确认官方URL重定向主机恰是**`s3-eu-west-1.amazonaws.com`**，完全未输出带签名下载URL、路径或源码正文。

[A3在原行为读取前再冻唯一原站到原已见Amazon S3主机的合法授权链](../../protocols/R108_PHASE_A3_2017_LEICESTER_OFFICIAL_FIGSHARE_EXACT_S3_HOST_MD5_DOUBLE_SOURCE_FREEZE_2026-10-18.md)，原25项synthetic通过，并真正从官方源链取得**36,526字节**且先经全文件MD5验真后尝试解析源CSV表头。此时受限于过窄的表头identifier正则规则，首次真正A3执行[run 39129870687](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39129870687)以`R108_A1_ORIGINAL_HEADER_NAMES_NOT_ASCII_SAFE`合法拒绝；原失败收据工作流另有仅收据字段名白名单不一致，运行日志全部保留。**这不意味着MD5/来源失败，也未读真人行为或隐式改数据。**

## A4真实独立来源哈希E1终于完成

另冻[A4仅源CSV单表头字符类别以及真正全文件MD5/SHA的狭义兼容合同](../../protocols/R108_PHASE_A4_PUBLISHER_MD5_VERIFIED_CSV_HEADER_CLASS_ONLY_AFTER_ASCII_BLOCK_FREEZE_2026-10-18.md)。经过**35项纯源合成测试先于真正文件读取**，GitHub Actions真实成功[run 39130128287](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39130128287)，[永久真实第一手E1收据](R108_PHASE_A4_LIVE_CI_TRUE_PUBLISHER_MD5_DOUBLE_CSV_HEADER_CHARACTER_CLASS_SOURCE_E1.json)确认：

| 真原作者原文件完整来源指标 | 机器实测 |
|---|---|
| 出版社Figshare dataset article/file ID | 10194938 / **18370526** |
| 真文件字节 | **36,526 bytes** |
| 作者发行方独立全文件MD5 | **`7afc755c293dc261d696d1b3f9ba796a`** VERIFIED |
| 项目原文件SHA256 | **`e7dbb6ddc96cc5c65368be0d1918c3ebc7a83c14addd03ab44eeb07790575c18`** |
| 第二次独立源下载哈希与原字节 | **完全相等** |
| 原CSV物理数据行数（未解析人类行为） | **1,804** |
| 首行CSV表头字段数量 | **5列** |
| 原首行字段名中的空值/重复字段个数 | **4空；3重复** |
| 原表头非ASCII字段/控制字符 | **0** |
| 真原个体行动、男女、来源人号等值实际应用读取 | **0** |
| 下一轮真人行为模型得分 | **0** |

这个真原始文件**首行字段结构异常，不能假定“每一行就是一位固定配对玩家的一轮行动”，也不能直接由1804个物理行推断配对数/有效目标数**。从第一手文件证据能诚实接受的是**出版方原CSV字节E1**。论文所述固定两人300轮和个人或实验场次信息仍需要精确列布局与原作者说明来源互证。

## 下一科学关口

独立冻结B0仅原CSV逐行字段数/行宽结构统计，不读取或输出任何真实CSV单元格值；确认首行与其他行是否为独立矩阵、区块表头或长格式，且原始作者源说明未解码前不建虚构`session/person/partner/round`键。只有取得合法真实身份、时序、任务行为和可分离来源独立场次，才可另外冻结与R106相同本人预测权重、等收缩和同频/同方差**错误对手负对照**。若只是固定几对而无真实实验室场次，就只能称配对组LOO，而不能把300轮当作300独立样本。保留R105资源4人组中同权伙伴对照阴性和R106真实双人26场中对手历史正面的竞争证据；跨目标任务与独立来源不伪合并。

**`R108=ORIGINAL_SOURCE_E1_CONFIRMED`；`ORIGINAL_FILE_36526_MD5_SHA_VERIFIED=YES`；`TRUE_PAIR_SESSION_MAPPING=NOT_ESTABLISHED`；`REAL_HUMAN_E2=ZERO`；`R073/PESEN_v0.1=FROZEN`。**
