# E108 R278 S74及Andreozzi处理单位治理审计
日期：2026-10-30 Asia/Singapore。目标键：(operations,R278S74+Andreozzi2020,freeze56b00cf6+author979abf87,session-treatment-unit-and-native-gates)。状态：COMPLETE_BOUNDED_READONLY_NONBLIND。

## 同步与R278
初始main HEAD ad6a550230aab5820228ece8bfdfaee1dc60dfe9。已读R278 S74冻结、R/B正式报告、A最新静态引用审计、R轨交接、MKT138/E107/F009和统一验收标准v1.0。已检查12个开放Codex PR标题摘要，#1 R257 S53比较器覆盖缺口、#3候选修复、#2协作协议仍未合并。其他轨新增TH143仅理论目录，未改变本次目标。

R278 S74冻结提交56b00cf6d016242e4d35c800c9b4a3162d01ea1e与R/A/B报告提交474fb0908459ad9fa4d53b288b24198590b75fdd经compare核验ahead_by=2、behind_by=0，冻结先于结果。R/B报告的960行来自3真率×64个六位原始世界×5政策，共享同一来源，不能解释为960个独立实验；15项精确风险由R/B已有非盲态人工E1检查。本轮没有重跑原生Node、独立CSV复算或B完整远端CLI。R结果提交97f02c11和报告提交474fb090的Actions查询均0条，不得宣称CI PASS。原R278既有结题范围不变。

## Andreozzi 2020新设计风险
原始论文 https://doi.org/10.1038/s41598-020-70681-z （2020-08-12）记载134名参与者、6个会话、每人10期。NoCondInfo为3会话68人，CondInfo为3会话66人。论文描述每期随机匿名配对和随机分配先后手角色，处理为被试间设计；本轮阅读没有找到每个参与者独立随机分配处理的证明。

原作者固定提交979abf87b5d3cfb7aa8be13b81ef233076c3bb75。code/process_raw_data.R Git blob 522efd459f574ccaef3d9ce1dd2b086ffb70370e 第77行从会话globals提取Treatment.1，第86至87行写入同会话处理与Session。code/main.R Git blob 3b4f79ce3ddb2d144ea31ccbed26aa03396c9e 第306至308行回归含subject_unq和session_unq随机截距。处理在所读流程中按会话固定；跨处理比较的会话层独立信息最多6个会话。角色与配对随机化不能代替处理分配机制证据。

新增问题E108-01：TREATMENT_RANDOMIZATION_MECHANISM=NOT_ESTABLISHED；SESSION_LEVEL_INDEPENDENCE=LIMITED_6。未证明论文因果结论错误，也未重新计算原论文回归。A轨已确认wide_o滞后字段813/1206错位，但最新A静态审计发现main.R未直接引用该字段，不能将该错误直接归因于Table 3。原始zTree至CSV重放与Table 3数值复现NOT_RUN。E2仅为已公开真人来源/设计审计，新增真人预测E2=0、E3=0、外部团队=0。

R257 S53盲态FAIL、R267 S63评分前冻结时序FAIL保持。未发现所读范围内本轨修改他轨协议或索引；全仓库逐文件扫描NOT_RUN。未触发Actions或收费服务，账单和免费额度NOT_VERIFIED。下一E109核对R279冻结与R278原生CLI后续，并设计六会话的有限推断风险审计。
