# E107 R277 S73冻结与Andreozzi真人CSV独立全量复核

日期：2026-10-30 Asia/Singapore。目标键：(operations,Andreozzi2020+R277S73,author979abf87+freeze53e3b18b,full-CSV-independent-lag-negative-control-and-freeze-CI)。状态：COMPLETE_BOUNDED_READONLY_NONBLIND。只读其他轨，未修改A/B/R/理论结果或共享索引。

## 1. 同步基线与冲突检查

初始main HEAD bfcc264766a5cf582f2c89641b6bdd5ff2de8afa，最近提交包括R277 S73正式报告及B独立审计、A轨会话留出检查、TH142理论来源审计；市场最新MKT137/E106/F009 phase1。读取12个开放的codex/* PR标题、摘要和head，包括#1 R257 S53比较器假阳性、#3严格数学验证器、#10 R271 S67原生复验、#12 R266 S62原生复验。12个PR均开放，不能作为main已合并科学结论。Codex同步协议仍在PR #2分支，依任务自含规则执行。

统一验收标准v1.0、先全R后分类最后熔炼的owner决定、README历史快照、R277 S73科学报告、B审计、A公开CSV审计、作者清洗脚本、market短交接均已读取。README顶部仍为R200历史导航，不能用它代替main当前HEAD。TH142只是理论轨研究，没有发现本轮已读提交启动熔炼。没有进行全仓库历史逐blob扫描或实际账单审计。

## 2. E107新增：完整真人CSV第二路线独立解析

固定作者公开来源：https://github.com/seyhunsaral/stabilitycondcoop/tree/979abf87b5d3cfb7aa8be13b81ef233076c3bb75
公开CSV data/csv/subjects.csv Git blob bd4c1550002621bee7dfb50e0d15d317764d1ea9；清洗程序 code/process_raw_data.R Git blob 522efd459f574ccaef3d9ce1dd2b086ffb70370e。

本轮通过GitHub连接器**实际读取全部425701字节CSV**，在独立V8中以逐字符、双引号转义感知的解析器重建67字段、1340行，按subject_unq和period=1..10组成134条完整时间序列。与A轨已公布的检查实现分开运行，属于已读A结果的非盲态复核。具体结果：

| 检查 | E107独立实算 |
| --- | ---: |
| CSV字段宽度异常 | 0 |
| 真人记录 / 唯一参与者 | 1340 / 134 |
| 缺少完整10期的参与者 | 0 |
| 第1期滞后字段为NA | 134/134 |
| 第2至10期可比行 | 1206 |
| 发布wide-o lag字段等于**当前期** | 1206/1206 |
| 发布wide-o lag字段等于**真正上一期** | 393/1206 |
| 发布wide-o lag字段与真正上一期不一致 | **813/1206** |
| opp_cond_type_lag1负控制等于真正上一期 | 1206/1206 |

直接读取作者脚本第269和275行：先正确生成lag1，随后以当前期opp_cond_class_wide_o覆盖同名lag1字段。完整CSV实算、作者代码语义及A轨此前结果一致。此次复核与A轨共享同一作者原始数据，属于非盲态内部**E2来源/测量审计**，不能作为独立真人预测实验或E3。原始R/zTree全处理流程、归档A轨Python原生命令行仍NOT_RUN。不得将发布错误lag列直接用于预测，未来应另存修正列并保留来源身份及差异收据；不改原作者文件。

## 3. R277 S73冻结、计算与CI范围

S73冻结提交53e3b18b28d46c0c5e26194dd8e85bc408450af6；正式科学报告提交ca6c08c4dcc57590b3e559bbea14df1e566a12be。GitHub compare返回ahead_by=7、behind_by=0，包含R/B/A七份新增文件，证明提交祖先顺序。研究者已经看过原R277机制，S73自标EXPLORATORY_E1_NONBLIND_INTERNAL；冻结祖先关系不能证明此前从未见过相关结果。

R轨与B轨在固定人工192条来源、72项可见概率、27项混淆、9项TV及8项篡改控制中报告精确一致。E107本轮读取报告与B收据，**未重新执行原生Node CLI或独立重算72项**。对正式报告SHA的GitHub Actions查询total_count=0，故不能声称CI PASS。R277原CLOSED_BOUNDED_E1状态不因S73自动升级。新增真人样本外预测E2=0，独立新总体E3=0，外部团队复现0。

R257 S53原盲态FAIL、R267 S63评分前冻结时序FAIL继续有效；PR #1/#3未合并不解除失败。未发现所读文件发生同名覆盖、未经批准协议改写或其他轨被本轨修改；没有审计全仓库所有文件，不能据此给出全局PASS。

## 4. 费用、开放事项和下一步

本轮没有主动触发Actions、注册收费服务、使用计费API或访问非公开数据。GitHub账户账单与免费额度NOT_VERIFIED。E108优先查看A轨真实实验随机化单位和公开清洗链可否核验，以及R278下一次冻结时序；避免重复已经完成的S73算法复核。所有科学失败与E1/E2/E3边界保留。
