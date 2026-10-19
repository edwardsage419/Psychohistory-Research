# R110 Phase C2：2015 UCL 原始合作字段独立作者说明 yes/no 有界编码检查

日期：2026-10-19（Asia/Taipei）
状态：SOURCE_ONLY_PRE_SCORE_FREEZE
原论文：Bone et al. (2015), https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0117183
原S1：https://doi.org/10.1371/journal.pone.0117183.s001

## 1. 独立作者依据与问题

出版方论文S1 Supporting Information 明言原字段 Partner coop prev 中 yes=partner cooperated、no=partner defected in previous round。论文Table 4 将二元玩家合作语义定义为 defection=0 与 cooperation=1；但作者在所引网页未独立给出 Player cooperated 原CSV确切词项。先验证两个原始合作字段是否符合事前假设的ASCII英文字母 yes/no 编码；任何不符合的行为字段只能记录未知，绝不因研究者期望改写。

已有C1原12,000行证实两个合作字段每条都是非空、非数值文字。C0原冻结只接受0/1，始终保持 C0 失败结果；C2只做原文本的非预测来源字典检查，不赋予合法C0有效目标或真人E2。

## 2. 来源约束及字段

仅允许原已经验证的PLOS S1官方链接和A0认证委托存储，且完整文件SHA256固定 ea70b0f3d98075f9d3e4401becfcdec8f6bdb5cae00c4dad63a697f9b61d7b5f。必须先调用既有B1签名与120人×两游戏×50轮原身份键结构验证。原CSV只读取八列索引 Round、Subject ID、Player type、Partner type、Partner coop prev、Game type、Player cooperated、Partner opt out prev。禁止任何其它行为、惩罚、人口学、收益字段读取。

## 3. 预设词项解析

对合作字段只允许ASCII两侧空白裁除，再做ASCII大小写折叠；预设 yes 映射合作1、no 映射合作0。禁止对缩写、true/false、1/0、NA、缺失、其它语言、部分词匹配、前缀、类似发音或数值强转。按各字段、各原游戏匿名槽分别统计 yes、no、空白、其它非空。绝不公开原词、加密摘要、原参与者ID、原个人连续行动。任何两位原参与者交叉的稀疏单元统计不输出。

源Partner opt out prev另行依C0原严格数值0/1解析计数，不得混入合作字段字典。读取 t=1 的伙伴前轮信号也只作编码计数，所有t=1仍不具备下一轮资格。

## 4. 资格与停止条件

若两合作字段每行都符合 yes/no，则 C2_SCHEMA_MATCHED_AUTHOR_WORDS_BOUNDED；它只支持“来源文字词典匹配”而不是合作因果或评分。若出现任何不符合的原字面，只返回 C2_UNMAPPED_SOURCE_TEXT_REQUIRES_CODEBOOK，包括各类匿名计数，不推测具体原词。若原真实来源再次传输受阻或摘要不合，C2_E0_ORIGINAL_SOURCE_BLOCKED。所有状态真实Brier模型评分条目计数一律零。不得把纯合成或本轮来源词项频次作为预测得分。

如果C2完全匹配，以后需要另立C3含退出/破产/行为可观测合法性、完整身份与条件层结构、同目标模型五版本、新的预评分门槛的独立协议；冻结在任何真实模型得分前，保留C0原报告和此时字典验证收据。若C2不能全匹配，来源学习有界结题并继续既定R任务，除非出版社提供新的第一手精确码本。无需无限猜测原词。

## 5. 先合成后真人、存档与限制

先合成反例覆盖大小写、ASCII空白、未知文本、数值、缺失、错误全源SHA、混合游戏、不合法首轮、未输出原始行动和不触碰C0评分。真实来源最多一次，归档匿名JSON与结果报告至GitHub。C0和所有R073/PESEN v0.1固定研究均不修改。无独立真实伙伴人物ID或实验室场次ID，不推断真实LOS0、心理机制因果或前瞻E3。
