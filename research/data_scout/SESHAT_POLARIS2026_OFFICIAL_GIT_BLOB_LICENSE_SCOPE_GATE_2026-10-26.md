# A子流程：Seshat Polaris2026 官方历史面板来源资格门控

日期：2026-10-26。状态 `OFFICIAL_REPOSITORY_BLOB_VERIFIED / XLSX_CONTENT_UNREAD / DATA_LICENSE_SCOPE_UNRESOLVED`。

一手来源：Seshat Global History Databank 官方数据页 https://seshatdatabank.info/data 指向 https://github.com/Seshat-Global-History-Databank/build_polaris_dataset 。官方称 Polaris-2026 为最新快照，包含按主题工作表组织的历史社会与制度变量；该仓库提供构建脚本及旧版 Equinox2020.05.2023.xlsx 供比较。GitHub 官方仓库固定提交 `55ca5fbc2b563ddbbc1a3413071d4bd243d0a5fa`（2026-02-25），实际从Git树验证文件 `Polaris2026.xlsx` Git blob `18b1116fa3322839d1366f967280d693f34af3be`、大小2,899,093字节，`Equinox2020.05.2023.xlsx` Git blob `b414ec5ca21831b61294f21289997f274b4956af`、大小1,720,038字节。

已验证来源和Git对象存在；由于当前连接器不支持二进制工作簿下载，**没有读取工作簿单元格**，不能宣称已核验变量字段、行数、政治体ID、开始结束年、时间粒度、缺失率或具体观测值。历史数据适合后续考察制度变迁和文化演化，但研究单位可能是相互继承的政体与地区，绝不能当独立随机样本；必须先建立政体连续性、时间切分、因变量泄漏门控和基线。

许可冲突门控：仓库LICENSE显示MIT软件许可证；Seshat历史数据官方公开资料曾采用CC BY-NC-SA数据使用声明。软件仓库的MIT不能自动授权工作簿全部数据作商业再分发。**数据文件专属许可尚未确认**，按非商业研究的最小权限处理，不复制或重新分发原始工作簿。无付费账户、无收费API。下一阶段需实际取得官方XLSX字节并独立检查工作表、时间和许可，再冻结任何E3评分设计。

该候选与R173民族志横截面来源不同，但尚未进行跨来源可比性或独立性验证；新增E3评分0。
