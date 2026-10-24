# A 数据侦察：stratEst公开真人实验包的来源去重与字段资格

日期：2026-10-25。性质：公开英文官方R包手册与GitHub Git对象目录级核验；本轮未成功读取二进制RData逐行记录，不新增E2评分。

## 固定来源与实际访问
CRAN英文手册 https://stat.ethz.ch/CRAN/web/packages/stratEst/refman/stratEst.html ，官方作者仓库 https://github.com/fdvorak/stratEst ，CRAN镜像固定提交 a6373b23d80dc816a63f18f973d372c9e8421914 ，目录 https://github.com/cran/stratEst/tree/a6373b23d80dc816a63f18f973d372c9e8421914/data 。通过GitHub连接器实际读取目录元数据，确认以下对象存在：
* DF2011.rda Git blob 52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0，3298字节；data.DF2011.rda blob 4c2586af1a5465a9e690b41e6f839c33096a4903，5082字节。
* FRD2012.rda blob 6b196ca1624081850b41dc2084c762257d59dd8f，26923字节。
* DFS2020.rda blob 8aa04408d48ceb504cde44e58c8bcad7f440ca3a，1931字节；data.DFS2020.rda blob bad46f196c56d9dd2f78618ea3ee02380efd3963，1997字节。

## 已核实的来源重复
* DF2011：CRAN手册标注 Dal Bó 与 Fréchette (2011), DOI 10.1257/aer.101.1.411；手册报告7358行、6字段 treatment,id,game,period,choice,other.choice。项目R074已使用同一原作者2011实验来源并进行真人场次留出评估。该R包可能是经过整理的子集，不能将7358行视为新增独立实验或声称与R074原始行一一相同。需要原始记录哈希与键级比对才可确认具体重叠行。
* FRD2012：手册标注 Fudenberg、Rand、Dreber (2012), DOI 10.1257/aer.102.2.720，13126行、9字段，含上一轮本人及对手行动。项目R075已研究同一原作者论文数据。此镜像不是新的独立作者实验；字段级与原始ZIP的行映射尚未验证。

## 可能有价值的不同实验
* DFS2020：手册标注 Dvorak、Fischbacher、Schmelz (2020), Incentives for Conformity and Anticonformity，569行、7字段：id,game,period,others.choices,choice,intercept,conformity.score。公开数据对象存在且较小；任务是三人社会影响与从众/反从众，不适用于R073双人重复囚徒困境冻结评分。
* 当前仅手册级字段、数据对象可见性已验证；真实ID唯一性、场次边界、逐轮对手身份、行为时序、缺失、分配随机化和来源独立性仍待二进制解析及其他R研究去重。
* 手册在DFS2020的Usage小节仍写 data(DF2011)，属于文档级可能误导，后续须以实际对象名和源码为准，不可据此加载错误数据。

## 访问和许可
本轮对 DFS2020.rda 的 Git blob 文本读取实际返回UnicodeDecodeError（压缩二进制，非UTF8）。没有绕过访问控制，没有购买或上传原始参与者数据。CRAN包元数据标记 GPL-3；包许可与人类原始记录再分发许可须分别核对，暂不再分发二进制数据。后续可在免费本地R或开源RData读取器下读取并核验原始数据对象，再预先冻结预测协议。当前仅数据侦察登记，新增独立E2评分=0，R073与PESEN v0.1保持冻结。