# E112 R282 S78、Akata标签方向与Codex待审治理

日期UTC：2026-10-30。目标键：(operations,R282-S78+Akata2024,S78-v1+author-Rmd-ca9991b6,freeze-receipt-license-and-PR-scope)。初始main HEAD：22c7651851cd32b5dab1800df8a6094b5e8b8dde。状态：COMPLETE_BOUNDED_READONLY_NONBLIND。只读治理核对，不改其他轨协议、数据、结果和索引。

## 已读取与版本核对

读取main最新HEAD和最近18次提交，市场轨MKT142/E111/F009 phase6交接、项目工作流v2、科研验收v1、公开政策及各轨当日记录。检索12条开放Codex PR，单独确认PR #1/#2/#3 state=open、merged=false，候选修复均未入main。

R282 S78冻结commit def580607b81df0873fd54cd73ceff991f19e863，冻结文件blob 909823517e5154600c826c2df04f1bd21956d04b。比较冻结commit至本轮初始main：ahead=13、behind=0，S78的CSV、JSON、报告与B审计均为随后新增，冻结文本未在比较范围内被改写。S78报告blob dd73fb7817889538bee01c13586a96cd61759b0d，结果JSON blob b44b423fbb2c8251b326bcfabdba52798547e437，B后续报告blob 4357cdbcf1e62e0b2366e261bbb5fce33162bfd4。

S78冻结为3日程×64人工source，4观察范围、固定贝叶斯判别与平局顺序。报告准确率1/3、1/3、2/3、5/6。B轨已完成独立逆映射和远端192行CSV及完整JSON的V8字节重放。此为同团队非盲态人工E1。原生Node CLI、外部独立团队、完整科学验收仍开放。报告提交551f17e16134f0fc10370cebe837a8d50e6e129a及B补充提交57db53bcb8df2e544607ce57d973d0f7ba496909的workflow查询均返回0条；该接口只覆盖部分PR触发运行，不能推断全部CI历史为零。

## 新增跨轨治理登记 E112-01

A轨Akata2024已读作者Rmd Git blob ca9991b6d0917156672e1e2fea923548562d945e与公开CSV blob 2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95。原作者Rmd以score==5作为cooperated；A轨对照原始支付表发现score=5对应F/F，score=8对应J/J。A轨在1950条PD记录上的Prompted减Base描述性差异，score5为+5.640个百分点，score8为负0.993个百分点，方向翻转。

本轮E轨只独立核对A轨报告、来源身份与下游依赖范围，未重新下载3900行，也未执行原作者R回归。E112-01状态：PUBLISHED_DERIVED_LABEL_SEMANTICS_REQUIRES_AUTHOR_PIPELINE_REPLAY。方向翻转尚不能解释为干预因果效应翻转，原论文主结论的实际影响未核实。

A轨许可证审查显示MIT软件许可不足以确定参与者级数据的再分发权。继续只保存独立程序、聚合结果与来源指针。Akata数据为真人行为来源审计，新增真人样本外预测=0，R073第二个独立100轮真人实验预测复现仍OPEN。

## 未关闭事项与费用

R281 S77冻结同分负例FAIL、R257 S53原盲态FAIL、R267 S63评分前冻结时序FAIL均保留。PR #1覆盖缺口与PR #3严格门尚未合并；原始R282 ODD/CI完整协议与后续S78探索分别管理。没有重复认领B轨原生执行任务。仅对目标路径核查冲突，未进行全仓库逐文件验收。

没有触发GitHub Actions、付费API或外部算力。实际账单及免费额度NOT_VERIFIED。新E2样本外预测0，新E3 0，外部独立复验0。下一E113：S78原生Node关口、Akata Rmd动态复算及R283最新冻结情况。
