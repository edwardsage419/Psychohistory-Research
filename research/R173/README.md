# R173 跨社会比较模型：真实来源档案入口，尚未正式科研结题

2026-10-21。原目录 **P1 / 07-015 Cross Societal Comparison Models（跨社会比较）**。状态 **ORIGINAL_SOURCE_AUTHENTICATED_MODEL_NOT_YET_SCORED**。尚无文化变量间关联结果、因果论断或真实社会独立预测，也未冻结或执行R173正式比较模型。

本阶段直接采用 [D-PLACE/dplace-data](https://github.com/D-PLACE/dplace-data) 原研究数据仓库，经严格核验原始提交 **9bfed2c8c206be00f55f71516f262bbca2234e5a**，使用 **CC-BY-4.0** 许可。应同时引用 [Kirby等2016 D-PLACE原刊](https://doi.org/10.1371/journal.pone.0158391) 和被研究变量所对应的Murdock等原始人类学材料；数据集中各社会并非在同一时点、用统一实验程序观察得到。

首次原生CI [39546923926](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39546923926)取得6份原始文件且全部Git blob校验通过，第二轮 [39547050424](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39547050424)独立重新下载全部原始字节、固定结构报告和完整原始资料ZIP的哈希后**成功永久归档**，提交 [65be6eb](https://github.com/edwardsage419/Psychohistory-Research/commit/65be6eb410e8efeb3b383d5265d5bb1d5c04283b)。

实读原始EA数据结果：**121354条文化变量编码行、1291个不同社会、94项EA变量、756条代码说明**。原始EA社会表映射中**186**条明示SCCS采样关系，SCCS映射表本身也为**186**行。但文本映射关系尚未按具体社会ID完成一对一严密检验，不能据186条映射文字直接声称成功建立186份可比较的完整变量观测。

已核对原始三个文化变量的具体释义及合法取值：EA003（渔业依赖，0—9序数）、EA005（农业依赖，0—9序数）与EA006（婚姻财物转移类别，代码1—7）；EA003和EA005都是有比例约束的生计构成部分，**负相关可能有机械成因，不得借此证明农业与渔猎间的心理或历史因果关系**。EA006分类不应被用来对社会进行简单价值排序。参见[原始文献与独立性审计](R173_CROSS_SOCIETAL_PRIMARY_DATA_AND_NONINDEPENDENCE_GATE_2026-10-21.md)。

原始文献[Murdock与White1969标准跨文化样本](https://doi.org/10.2307/3772907)提出按文化分区选取186个社会以改善样本独立性，但不同社会仍可共享历史、语言亲缘、地理条件与扩散通道，**不能把简单的社会数量理解为同等数量的独立实验**。D-PLACE聚合CLDF仓库另采用CC-BY-NC-4.0，不能与本轮明确为CC-BY-4.0的原始数据仓库混为同一版权边界。

**已归档原始资料：** [逐字段和来源哈希JSON](R173_ORIGINAL_DPLACE_EA_SCCS_SOURCE_AUDIT.json)、[六份原始EA/SCCS原数据与审计程序ZIP](R173_First_Hand_DPLACE_Original_EA_SCCS_Source_Audit.zip)（2921462字节）、[实际来源审计Python](r173_original_dplace_source_audit.py)、[双次成功来源CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39547050424)。

下一关口：**先验证具体变量EA005、EA006在每个社会的非缺失编码和重码、原始社会映射及观察年份；然后单独提交计算前冻结的比较模型协议**，再进行全EA与SCCS设计样本的相关性敏感性计算。科研分级只达到SOURCE_AUDIT，不得宣称R173 E1模型正式结题；E2/E3新增0。R073与PESEN v0.1冻结。全部R系列研究完成后统一归纳分类，最后熔炼。
