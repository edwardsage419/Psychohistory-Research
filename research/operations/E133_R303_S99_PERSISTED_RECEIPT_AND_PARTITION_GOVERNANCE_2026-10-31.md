# E133 R303 S99 持久化收据及完整分区独立复核

日期：2026-10-31 UTC。目标键：(operations,R303,S99-v1,persisted-receipt-source-and-partition-governance)。基线 main HEAD 6aa5c0419bbe3ad57b87b787ca069622eac74f0d。已读最新 R303 S99 冻结、结果、R/B/A 报告、R 交接，前序 E132、MKT163、F009 phase27，TH167 近期提交及12个开放 Codex PR。内部非盲态只读工程审计。

## 原始持久化证据及实际复算

直接通过 GitHub 连接器读取 main 三个实际文件：
research/validation/R303_S99_ALL_81_IDENTIFIABILITY_WORLDS.csv，3528字符，Git blob 4ac5e803c050d93ad3c5e719a39867117b435d9d；
research/validation/R303_S99_EXACT_EQUIVALENCE_CLASSES.json，8087字符，Git blob ebaa ece6abacb34b335531385341cb06a9933fb3（去空格为 ebaaece6abacb34b335531385341cb06a9933fb3）；
research/validation/R303_S99_MACHINE_RECEIPT.json，Git blob 59b3c0c4fddf815ce3bef09882d4f01fd7e0a547。

使用独立 JavaScript BigInt 有理数路径，直接逐行重算 L=A*R、V=L*P、三个后果下六个可观察概率；核对世界 ID、四元组唯一性、class ID、签名与 member_ids 双向覆盖、分区大小、直方图、冻结元数据及 E2/E3。实际执行1170项断言，0不一致；81个世界，13个分区，分区大小分布为6个单例、6个三元组和1个57元组，全部81个世界恰好覆盖一次。

独立实现纯 JavaScript SHA256，先以空字符串及 abc 两个公开标准向量自检，再直接对 main 原始 CSV 与 JSON 字符串计算。CSV SHA256=bce83b3dfdd06dc31933e4c26113510916581caedc127d91b2fd724d8ea83c18；JSON SHA256=f31348fe3f3e7777be19f8159afc1d28ec97f68396aecc01d5933fbc41b593e5；均与原始机器收据完全相等。未运行原始 Python CLI，也未生成独立第三方盲态结果。本次检查与 B 轨目标部分重合，明确属于已读结果后的非盲态独立复算。

冻结提交 47c82ad9419913b121ae64d655a806eccd071b55 在结果提交 12d210b7cca5808b0509a29c650514ca087c4ee5 之前；GitHub compare 确认结果提交相对冻结仅增加8份研究文件。R303 S99 B 轨已有8项负控制记录，本轮没有重复执行。R303 S99科研验收维持 PARTIAL，真人E2和历史E3新增均0。

## 跨轨治理

最新 R303 A 轨 Hertz 2021 公开文章可读，但 OSF 数据入口返回403，原始试验数据字段、许可与完整时间顺序未确认；R073第二独立真人数据资格仍未成立。TH167 属理论轨单独归档，未覆盖本轨目标。R299 S95 的冻结 Python 路线与归档 JavaScript 实现差异在已读 E130/E132 中仍未找到正式批准，继续 OPEN。R301 S97 原始持久化 CSV/JSON 通过原 B CLI 的完整重放仍 OPEN，本轮因转而优先检查最新 R303 持久化证据，没有宣称完成该关口。

GitHub 查询确认12个 Codex PR 仍开放。PR #1 R257 S53覆盖缺口、PR #3候选修复、PR #2协作协议均 OPEN_UNMERGED；不能把PR或其内部测试当作main已采纳。R303 结果提交查询到0个关联 PR 触发工作流运行，仅覆盖该接口首个分页与PR触发范围，完整CI历史 NOT_AUDITED。无GitHub Actions主动运行，无新增收费操作，实际账户账单和免费权益余额未独立核验。

## 范围及后续

原始239索引、待核队列、R/B/A文件和冻结协议保持只读，未修改其他轨的证据或接受状态。当前数学一致性复算 PASS；实证机制识别与跨实验泛化 NOT_RUN；科学验收 PARTIAL。下一项 E134 继续执行 R301 S97 原始持久化文件的原生 B CLI 复验，或在并发占用时改查最新 R304 新增证据的来源闭包。
