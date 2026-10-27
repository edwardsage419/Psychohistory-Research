# A轨 Dal Bó与Fréchette 2011真人重复博弈：公开RDA二进制来源资格

日期：2026-10-27。状态：PUBLIC_BINARY_VERIFIED / SCHEMA_DOCUMENTED / FULL_ROW_DECODE_PENDING / LICENSE_SCOPE_PENDING / R073_FROZEN_GATE_NO。

原论文 Dal Bó, Pedro and Guillaume R. Fréchette (2011), *The Evolution of Cooperation in Infinitely Repeated Games: Experimental Evidence*, American Economic Review 101(1):411–429, DOI `10.1257/aer.101.1.411`。公开第三方R包`fdvorak/stratEst`默认分支master，`data/DF2011.rda` Git blob `52e216b02e1a7ab7fb1a6e335b5f7e2ef6b7f5a0`。本轮通过GitHub连接器实际读取完整base64内容并按base64字母表解码，获得3298字节，首四字节`BZh9`，确认是可获取的bzip2压缩二进制；尚未解压R数据对象或逐行检验。

包原作者文档`man/DF2011.Rd` Git blob `de410a6423521fe78f6995c17f3677b0d6164417`声明7358行、6列：`treatment,id,game,period,choice,other.choice`。treatment为六级处理，id为受试者标识，game为supergame，period为场内轮次，choice和other.choice为同轮自身及对手行动。派生`data.DF2011.rda` blob `4c2586af1a5465a9e690b41e6f839c33096a4903`，文档第七列`input`代表上一轮双方行动，首轮缺失。7358行来自作者数据字典，尚未独立逐行复算。

软件DESCRIPTION声明GPL-3，但未定位论文原始数据的单独再分发许可和COPYRIGHTS文本，故未复制原始RDA至本仓库。该2011实验与R073 Montero 2022来源不同，Nay与Vorobeychik 2016聚合数据已包含来源代码DF，故须与聚合来源去重。session身份全局唯一、配对镜像、每个supergame长度和许可均未验证。R073冻结100轮、12场次及评分协议不能直接用于该不定长博弈。任何当轮`other.choice`不得预测当轮`choice`。新增E2/E3评分均0，费用0。

英文来源：
https://github.com/fdvorak/stratEst/blob/master/man/DF2011.Rd
https://github.com/fdvorak/stratEst/blob/master/data/DF2011.rda
https://github.com/fdvorak/stratEst/blob/master/DESCRIPTION
https://doi.org/10.1257/aer.101.1.411
