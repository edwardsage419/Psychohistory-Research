# R072 REV008：独立于回应结果的 S8 数值档案编码字典核验

日期 2026-10-17。冻结顺序：本协议先于首次对真实 9 条非候选行应用新语法规则。REV006 已扫描到 service、neutral、female、male、israel、yes、no 关键词；REV007 在八个匿名组中独立复算了作者公开 Table1 的(人数,回复人数)多集。后者不能倒推 profile 实验处理代码，否则产生 outcome→treatment 泄漏。本研究属事后探索性编码证据恢复，不是新的样本外实验。

原始一手来源：van Apeldoorn & Schram 2016, PLOS ONE doi:10.1371/journal.pone.0152076，原出版者 S8 doi:10.1371/journal.pone.0152076.s008；38647字节，SHA256=5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b。源 URL、签名委托路径、ZIP 安全和 189 候选数据行继承上游冻结规则。八个模型中的profile数字是人工编号而非人类ID，不得公布原代码值。

## 冻结判定

仅研究非候选的九条尾注，而不检查任何人类回应字段、效应大小和 Table1 回应频数。先构造真实第一列八个不同数字编码的内存集合，不打印编码。然后寻找两种独立编码字典形式：
A. 单一注释 cell 文本明确呈现数字代码与服务历史或中性标签在同一等号、冒号、连字符后的一对一关系，例如人工字符串 1: service profile；
B. 同一非候选行不同 cell 分别具有唯一数值代码与明确的服务历史或中性标签，且代码来自真实八码集合。

只有内容中明确出现 serving、service history、service profile（视为服务历史）或 neutral（视为中性）其中一个概念，才算语义绑定。若同时出现两者、存在多种可能数字、代码不属于真实八码、重复代码指向相反类型，必须记录冲突或丢弃候选，不能靠已发表 96/93、八个作者回应率、作者叙述方向补齐。

另记录是否存在整数范围形式的代码提示，仅作为 RANGE_HINT_UNVERIFIED，绝不自动当作编码字典。为避免研究者凭合计倒猜哪组，输出仅为聚合布尔：是否完整覆盖八码、是否各四码、是否有冲突、是否只有范围线索；不输出任何原始码、性别国籍、文本、行序号、稀疏类别数量或唯一成员资料。若全部八码都有唯一独立语义且各四码，最高判 FULL_AUTHOR_CODEBOOK_CANDIDATE，不在本轮计算 96/93、89或处理效应；若未覆盖则 BLOCKED_NO_UNAMBIGUOUS_SOURCE_CODEBOOK。

最低12项纯虚构xlsx测试覆盖A/B成功、重复冲突、混合语义、未列于真实八码、无数字说明、范围提示、个人资料禁输出、源SHA、不能利用回应及错位编码。真实 GitHub Actions 先测试再从PLOS取得锁定SHA原件，只上传匿名布尔、来源收据，原始人类 XLSX 永不入库。

原R072=CLOSED_BOUNDED不变；原自制IMAGE/STANDING/STERN真人E2仍未验证；E3 OPEN；PESEN v0.1 FROZEN。
