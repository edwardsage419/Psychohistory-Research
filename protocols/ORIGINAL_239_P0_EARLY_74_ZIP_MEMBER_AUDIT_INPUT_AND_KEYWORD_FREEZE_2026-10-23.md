# 2026-10-23 P0三条目早期归档成员级核对：审计前规则冻结

目的：核查原239目录仍无后期主R对应的P0三项01-008 Softmax Choice Rule、02-002 Temporal Difference Learning、04-001 Granovetter Threshold Model，在2026-10-15归档的74份ZIP原件里是否有一手数学研究或历史学习文件。属于回顾性文件取证，不是实验预评分，**不得因关键词出现认定原论文研究已经科学完成**。

数据锚：`manifests/LIBRARY_ORIGINAL_ZIPS_2026-10-15.csv`原清单共74条，路径全在`archives/library-originals/`；`manifests/RECOVERY_STATUS_R001_R064.csv`64轮、73个ZIP引用，额外一份知识包。两文件 GitHub main 当日已有元数据审计[39908490800](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39908490800)通过。逐ZIP验证真实当前磁盘字节SHA256、Git blob SHA1、清单size、ZipFile.testzip() CRC、文件/字节数等，与旧清单逐一同一严格对照；出现任意CRC/哈希/目录缺失立刻FAIL，不允许以既有manifest状态替代重新读字节。

词典预先冻结：
- `01-008`强线索：softmax、soft max、soft-max、Boltzmann、玻尔兹曼、软最大、softmax choice、soft-max choice、logit choice；相关线索：逆温度、选择概率、条件logit、conditional logit。
- `02-002`强线索：temporal-difference、temporal difference、TD learning、TD-learning、时差学习、时序差分、时差强化、sarsa；相关线索：Q-learning、强化学习、reward prediction error、预测误差。
- `04-001`强线索：granovetter、threshold models of collective behavior、集体行为阈值、集体参与阈值；相关线索：threshold、阈值、collective behavior、集体参与。
强、相关只是**全文检索线索**，不能表示目标条目科学完成、原作者被直接阅读、亦不表明ZIP内确有合法重分发的原文。扫描ZIP成员名及可解释为纯文本的文件内容，跳过二进制、超大项、解码失败项，并记录不可检索盲区。不得在用户或仓库输出复制大段旧论文或敏感原文：每成员每条目最多取两个长度不超过160字符的局部上下文。对所有74个原ZIP同等处理，不在看过结果后修改检索词解释。程序可另运行独立核对来源CSV、结果SHA和真正ZIP对照。产物`research/catalogue_audit/scan_early_zip_P0_2026_10_23.py`、`docs/ORIGINAL_239_P0_EARLY_74_ZIP_CONTENT_SCAN_RESULTS.json`、`docs/ORIGINAL_239_P0_EARLY_ZIP_SCAN_SHA256_RECEIPT.json`、正式解释报告。

模型主映射保留R118主原目录03-019；当其实际论文也明示Granovetter1978，可建立**共享来源对应线索**而不假装新独立复现。R111主原目录01-005 McFadden条件Logit应检查是否实质覆盖softmax；R063模仿学习机制不能自动充当TD的独立验证。现阶段保持239原目录科研整体结题NOT_ESTABLISHED；新增真人E2=0、真实历史E3=0，R073/PESEN v0.1冻结。
