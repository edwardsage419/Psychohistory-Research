# E011 R172 国家聚类、历史回测证据等级及独立 bootstrap 只读审计

run_date: 2026-10-26 Asia/Singapore
track: operations
subflow: E incremental readonly after E004 daily check and E010
status: COMPLETE_BOUNDED_READONLY_INDEPENDENT_RECOMPUTATION
preflight_main_head: 0654573d938e5c351a4f74c7e97f82a13e3c9f42
prior: E004 E009 E010 MKT041 MKT042 F002
cost: ZERO_ACTIVE; overall billing and GitHub free entitlement NOT_INDEPENDENTLY_VERIFIED
ci: NOT_TRIGGERED
scope: R172 new third method, B independent arithmetic route, A Cason access gate, inherited R170/R136/original239 issues

## 1. 并发、冻结与文件范围

实际读取 main 最新HEAD、market目录至MKT042、operations目录至E010、F002本周专题、近期30条提交、R172冻结协议、原始319行预测CSV、主研究报告及机器收据、B独立预执行协议/报告/收据、A轨Cason数据门槛。E004已经满足当日正式日检，本次只追加R172变化，不重复创建全量日检。没有修改R、B、A、TH、C、D、market、F的既有文件及索引。

R172新方法冻结提交 c758dd2f8815bcc9137dd404bfa963515887f530，科学报告提交 7c89948001ab10cf9c2294437fe17680200dcbfc。GitHub compare显示冻结至科学报告 ahead=6, behind=0。B独立算法冻结 b372d95b7d370c43298052ec9fd47bc182e8d0db，B审计 e54a3a7b86f86f98d3bc5854d54eb7a4c4381ff7，compare ahead=6, behind=0；B冻结至R172新科学报告 ahead=5, behind=0。B在本轮新增科学结果之前冻结，但已经可以看到2026-10-21的旧R172历史数据及结果，不属于对原始R172历史结论的盲法预注册。

R172新冻结协议在冻结提交及本轮main中的Git blob同为 206f2ace8862869a76681dfcd54fdd7bb6500c2c。原始预测CSV在两处的blob同为 00d0379d77ec8e776a00cbb9c6e9dd5a00958dce。只证明这两个指定对象的版本未改变，不推断全仓所有冻结协议均无漂移。

## 2. 从原始CSV实际独立重算

直接从 GitHub 读取研究仓库的319行 CSV，按列解析三种有理数概率分数，再由本次独立 JavaScript 算式计算伯努利NLL、Brier、预测事件总数及按国家完整删除的模型损失差。执行11项结构及数值断言，11 PASS，0 FAIL。

读取结果：319 country-year，35 episode，32 country，18 breakdown event，年份2000至2017；每个episode-year组合唯一，所有三模型概率在(0,1)。模型结果：

M0：NLL=0.23588112665232605，Brier=0.054407113235041195，sum(p)=7.1132075471697656。
M1：NLL=0.2452353284461805，Brier=0.05466702789383375，sum(p)=6.320792401225919。
M2：NLL=0.23453041515744208，Brier=0.05410527159252932，sum(p)=7.5794595076190205。

结果与R172主机器收据相符。18个实际事件与所有模型约6.32至7.58个预期事件存在明显绝对风险低估。M2相对M0的微小年度NLL优势，在删除 BGD、HTI、LBY、MRT、THA 中任意一国后反转；其余27国删除仍维持原符号。该现象说明该样本下相对优势对国家单位有依赖，不能声称新的独立测试。

进一步从同一CSV独立执行冻结PRNG：seed=20261026，state=(1664525*state+1013904223) mod 2^32，32个国家按字典序抽样，每次有放回抽取32国，完整保留每次抽中国家的全部年度记录，共1024次。对M1/M2相对M0的年度NLL与Brier差分别计算2.5%及97.5%线性插值分位点，**8个端点全部与主机器收据在1e-12内一致**，最大绝对差1.42e-15（双精度浮点舍入）。重算区间：

M1 NLL [-0.001151695604, 0.020978334353]；M2 NLL [-0.018137214492, 0.014862938159]。
M1 Brier [-0.000130822424, 0.000659161203]；M2 Brier [-0.001016908357, 0.000205690866]。

全部区间跨0。总计本轮19项独立断言或数值端点核对通过。这里的独立性是审计者重新编写解析、计算和随机重采样路径；输入仍为同一份归档CSV，无法独立确认最初的历史变量时间可得性、源数据抽取过程或外部研究团队复现。

B轨报告称96项BigInt精确国家删除等式、64项跨路线比较及两项负对照通过。E011已读机器收据及报告，未重新执行B的全部BigInt证明；这些数字必须标注为B轨已归档执行声明，不能算成本次E独立19项检查。

## 3. 证据等级与CI判定

原始R172有真实历史来源的**回顾性历史留出**，属于限定的历史来源证据，可按项目口径注明 E3_SOURCE_HISTORICAL_RETROSPECTIVE。该新方法只在既有319行、35段历史事件和32国上做聚类稳健性及校准检查，**没有新增独立历史数据或真实前瞻E3预测**。R172科学报告已披露原训练与留出可能重合国家、协变量事后回填可得性尚未验证、不同国家可能共享冲击。不能从“历史留出”直接推断未来事件预测能力，也不能把本次E1数学复算算作新增E3样本。真人博弈E2新增为0。

直接调用GitHub Actions REST head_sha 查询主冻结 c758dd2f、主科学报告 7c899480、B最终报告 e54a3a7b，三项均返回 total_count=0。这里只能说明指定SHA没有返回关联Actions运行。新文件均带[skip ci]，本轮没有启动CI，绝不报告远端CI PASS。

## 4. 其他轨及开放问题

A轨最新Cason 2026 Dryad来源新增公开CC0政策审查，2.75MB原始CSV通过现有公开下载链接尝试时HTTP 403，故实际字节、哈希、行数、session切分尚未验收。三类别间接互惠实验不满足R073冻结的双人同步二元博弈直接迁移条件，不能算第五个R073独立E2实验。该数据的真实参与者设计信息来自官方README，尚未进入冻结预测评分。

原有高优先级阻塞继续开放：E009 R170跨语言全状态逐项比较证据缺口；R136原冻结负对照失败及1215行原始CSV未完成远端字节核验；original239中154项逐项证据审计待办是E004此前读取的计数，本轮没有重算；R171独立路线冻结晚于主结果及79,800对距离未全量跨路线存证。未对所有研究轨逐文件扫描，不能宣称整个项目零遗漏或零同名冲突。

F：2026-W44 F002已经完成，本轮不重复建立专题。Exist滚动中位数导致参照漂移、星期组小样本及派生快照撤权问题仅列入候选风险。零真实敏感数据接入，零个人决策产品开发。

## 5. 治理结论及下一步

E011-01 HIGH OPEN：R172所有模型对本批历史留出事件显著低估绝对风险，M2相对优势对5国删除敏感。保留原研究记录并要求未来外部时间可得性审计、国家依赖和独立时间段验证，不能自行重拟合或改写冻结预测。
E011-02 MEDIUM OPEN：历史来源回顾性E3与真正前瞻E3必须分开，避免证据等级抬升。
E011-03 MEDIUM OPEN：指定三项提交Actions运行数为0；CI未验证。
E011-04 HIGH OPEN：R170和R136既有验证缺口继续保留。
E011-05 MEDIUM OPEN：Cason原始CSV 403、哈希与实验分组未验证，不能计入新增E2。
E011-06 MEDIUM OPEN：本轮只抽查指定R172与关联轨道，跨任务同名文件及全仓冻结漂移未完成普查。

下一次E优先审查R173或新R轨的冻结、原始数据和独立收据，并继续追踪R170与R136。研究主线保持全部R系列完成后归纳分类，最后模型熔炼。

## 6. 直接读取的GitHub来源

1. https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R172_COUNTRY_CLUSTER_CALIBRATION_THIRD_METHOD_PRESCORE_FREEZE_2026-10-26.md
2. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R172/R172_REAL_HELDOUT_PREDICTIONS.csv
3. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R172_COUNTRY_CLUSTER_CALIBRATION_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R172_COUNTRY_CLUSTER_CALIBRATION_THIRD_METHOD_RECEIPT_2026-10-26.json
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R172_COUNTRY_DELETION_EXACT_BRIER_PRESCORE_FREEZE_2026-10-26.md
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R172_EXACT_COUNTRY_DELETION_SCIENTIFIC_AUDIT_2026-10-26.md
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R172_EXACT_COUNTRY_DELETION_RECEIPT_2026-10-26.json
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/CASON_2026_CRSU_PREDECISION_LICENSE_DOWNLOAD_ADDENDUM_2026-10-26.md
9. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E010_R171_INDEPENDENT_GRAPH_RECEIPT_AND_CI_SCOPE_DELTA_2026-10-26.md
