# A轨：WXZ2014真人重复石头剪刀布数据源登记与资格门槛

日期：2026-10-27。状态：SOURCE_BINARY_BLOB_VERIFIED / SCHEMA_DOCUMENTED / ROW_DECODE_PENDING / R073_DIRECT_TRANSFER_BLOCKED。来源研究为Wang, Xu and Zhou (2014), *Social cycling and conditional responses in the Rock-Paper-Scissors game*, Scientific Reports 4, 5830，DOI 10.1038/srep05830。期刊原文：https://www.nature.com/articles/srep05830 。

## 实际来源核验

本轮通过GitHub连接器直接读取公开cran/stratEst仓库两个RDA文件的base64表示，实际确认可获取原始字节及Git blob身份：
1. data/WXZ2014.rda，Git blob c6424a938312f6044133f80894bda8c34dabc226，base64去空白后40112字符，解码长度30084字节，文件头BZip2编码。
2. data/data.WXZ2014.rda，Git blob 1de215778a02edfcb5344abf8d076df3a00bd20d，base64去空白后47608字符，解码长度35705字节，文件头BZip2编码。

两个blob是不同的数据对象，不能直接合并或当作独立实验。已读取仓库DESCRIPTION，blob 15e36a79a3112a0a94e1818b2efd54a3540cb8fd，版本1.1.8、软件许可GPL-3、版权详情指向COPYRIGHTS；在本次GitHub镜像中未找到该COPYRIGHTS文件，真人数据的单独再分发授权保持UNKNOWN。期刊论文标记CC BY 4.0，不自动替代数据集授权。

## 公开字段、时间和独立单位

官方R软件包英文文档 https://search.r-project.org/CRAN/refmans/stratEst/html/WXZ2014.html 声明72名真人参与者、每人300轮、六人匹配组，原始对象21600行、6列：id、game、period、choice、other_choice、result。三行动为rock/paper/scissors；other_choice是当期对手行动，不能直接作为当期决策预测特征。衍生对象官方文档 https://search.r-project.org/CRAN/refmans/stratEst/html/data.WXZ2014.html 声明21600行、7列，新增input为上一轮自身行动，首轮NA。对应R/data_WXZ2014.R原作者包文档Git blob cca7ed02b7718371ff5541633ee68d9ddc507112。

目前21600行、72人、300轮均为官方文档声明；本轮实际验证的是公开二进制对象存在、字节长度、Git blob和字段文档。尚未解码RDA，也未逐行核验行为、对手镜像、六人组标识、缺失值、参与者跨组重复或原作者与第三方整理文件逐字节一致。按照72/6可推得12个六人组的名义数量，独立场次标识及是否互相独立仍待数据级验证。

## 复现资格与下一步

此数据是三行动重复博弈，适合未来研究条件反应、群体循环、转移矩阵及独立六人组留出；R073冻结的二元囚徒困境模型及评分规则无法直接迁移。禁止事后把三类压缩成二类以制造R073通过。需先用免费本地R或可复现RDA解码器读取固定blob，验证行数、时间顺序、对手镜像、组间独立性、缺失与授权，再另行冻结适用的R系列研究协议。不能以作者论文的总体结论代替逐行数据核验。

来源没有使用中文语言网站。没有采集私有数据、注册付费账户或再分发个人记录。新增真人预测评分0项，新增历史E3评分0项。主动新增费用0。