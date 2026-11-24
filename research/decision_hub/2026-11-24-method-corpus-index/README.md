# 智能决策中枢第八轮：真实科研资产清单及注册表来源身份审计

2026-11-24。用户要求先充分积累数据，暂不启动 Codex。状态 SOURCE_INVENTORY_COMPLETE / CONTENT_REVIEW_PARTIAL / INDEPENDENT_ACCEPTANCE_NOT_RUN。起始 main 16986d537f3f974fe97e3865fd6f349f76846b0e；PR #61 仍 Draft（96b4293aa6b4d3c4cf16ece126e4dff07f25874f），#59/#60 仍 Draft。已核对 AGENTS、v3.1、科研同步规程、近期提交与产品交接；无新增 R 系列专项，不更改冻结协议。

## 数据范围与身份
实际读取三个未截断的 Git 树：当前 16986d537f3f974fe97e3865fd6f349f76846b0e，注册表默认历史来源 5909e1ae58dbfcb0d14d00c0561726ecb35e1028，v0.5 扩展来源 f6115556ecf3ee6eed8f96b043497a51e5f1bf9a。全量清点 research/decision_methods 下154份 blob 的路径、哈希及大小；filenameTerms仅用于文件名发现，未做全文或语义索引。读取五个方法模块及注册表、v0.5 装配源码，人工核对 Method.sources、常量、_card调用、版本和依赖；静态正则复核五模块声明的方法键集合。对全部来源关系逐一比较方法声明历史 commit 与当前 commit 的文件哈希。默认方法依赖声明为空；硬约束优先由 hub 另行执行；v0.5 注册时为VOI及timing增加硬约束依赖，timing采用结构范围。该映射为源码审查，不是实际 import/运行注册表。每个登记方法仍是代码描述的 SYNTHETIC_ENGINEERING_CANDIDATE，正式执行需既有验证器与授权。未映射资产不能凭检索文本获得执行许可；不排除其他工程模块在本轮范围之外引用这些材料。全文证据、科学验收及许可不从文件名、路径或代码引用推断。

实际汇总：
{
  "assets": 154,
  "registeredMethods": 15,
  "linkedAssets": 26,
  "unmappedAssets": 128,
  "declaredSourceEdges": 38,
  "matchingEdges": 37,
  "missingEdges": 0,
  "changedEdges": 1,
  "numberedGroups": 37,
  "multiFileNumberGroups": 11,
  "identityControls": 152,
  "shortIdComparisons": 33,
  "shortIdUnsupported": 10,
  "excerptReviewed": 8,
  "relations": 5
}

相同C编号多文件包括正常补充与真正不同主题；短号不能当唯一文档标识。对真实C号来源边构建短号替代测试：用同编号文件替代已声明来源，短号匹配基线会接受全部，精确来源检查仅接受真实固定映射。未支持的替代指当前方法源关系中没有该文件身份，并非否认该文档科研价值。路径、版本、哈希负控均为研究规则，不是生产安全或原生运行验证。当前索引采用精确路径+blob+方法版本+声明历史commit，检索只作候选发现。任何来源变更需要人工审查，不自动替代或提升。

## 内容增量与去重
阅读8份档案前部摘录，单列审阅范围及5项有明确文字依据的关系：Arkes/Blumer 11月23日记录是重复补充，优先11月22日更深原文核查（不删历史）；Flyvbjerg 11月22日是11月20日的验收补充；C036对损耗模型的镜像线性场景解析扩展；C034精确截断边界补充；VOI不可退预付费扩展。未独立查原论文，本轮也未重做已有数学证明。C028 Manski反事实部分识别与C028硬约束不同，C035偏好测量和联合可行性不同，C036回忆体验与两阶段调配不同。上一轮小规模检索采用10张卡，本轮扩至154份文件身份，真实方法 ID c028_interval_feasibility@1.0.0 经源码证实；VOI存在5个注册入口，早期小实验的研究-only标签不得当作全库准入结论。Arkes重复文档本轮显式链接，不将其再计新理论。剩余文件内容证据待审查，不声称已全文学习或形成154个可执行模型。

## 交付与下一责任
corpus_index.json 是固定来源清单，identity_results.json 为实际执行的JS核对结果，replay_index.js 用 Node >=18 读取归档索引复算逻辑。重放不能替代未来重新查询Git对象或原生代码运行。独立验收轨可用不同编号/同题变体/伪造文档挑战索引；模型轨维护精确方法契约与来源升级；数据轨和理论轨核查证据级别。手动窗口下一轮优先扩大跨领域真实资料和白话语义/证据边界样本，随后用冻结独立留出检验检索；不因数量增大启动Codex。无真实个人数据、训练、合并PR、CI、部署、新费用或生产修改。
