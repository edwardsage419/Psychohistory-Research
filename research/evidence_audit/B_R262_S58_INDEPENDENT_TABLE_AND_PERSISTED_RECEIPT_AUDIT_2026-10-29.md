# B轨 R262 S58 内部独立算法与落盘收据审计

日期：2026-10-29 UTC。目标键：(B,R262,S58 freeze 9822be38,exact table oracle and negative controls)。原R262完整报告、机制、已知像集与有限平均密度在本轮B脚本编写前已读，故不是严格全盲态；S58新的72项风险结果在B脚本编写和Python编译前尚未运行/阅读。

## 方法及实际执行

R轨使用Wolfram整数位移规则，逐原初态两步迭代，再按观察信息集分组，用 Fraction 计算平均条件Brier风险。B轨在独立文件 research/evidence_audit/b_r262_s58_independent_table_oracle_20261029.py 中使用111至000的完整8邻域真值字符串，按显式字符串键查表更新两次；使用组内成功数与组人数直接求 n1(n-n1)/(128n)，不导入R模块，不调用R轨规则位移函数，不使用R轨已生成状态缓存。

B轨Python脚本在运行R计算前完成写入并通过 py_compile。随后R Python CLI生成本地72项结果，B Python CLI --receipt 实际执行：exact_comparisons=72，失败0。四个故意错误注入分别为重复键、风险999、E1人工升级成E2真人、删除最后一项；均实际REJECTED。已保存B Python源文件的Git blob为 9e9123dcf91fc95c40c82a785ecd6f8621deaa33，与本地执行脚本 git hash-object 完全一致；R归档Python源文件Git blob 8842f8f62b5a26ce9e01cd164b1ef7697d6d9d90，与本地执行文件一致。

远端持久化收据 research/validation/R262_S58_PARTIAL_MACRO_BRIER_EXACT_RESULTS_2026-10-29.json Git blob 9b7c45485a22b01b916bfb9c5a579aeefaa83875。通过GitHub连接器读取完整JSON，隔离V8使用真值表重新独立生成72项风险及分组数，与远端落盘收据逐项比较，72/72通过、0不一致。该V8检查是第三执行路线，尚未构成远端JSON作为原样Python CLI文件输入的证明，故此最后一步仍NOT_RUN。

## 原来源门与证据边界

R262原CSV 311611字节、5760行、20列，经GitHub连接器在隔离V8逐行读取，核对全部40320个七位状态、规则号、初态、时间、质量、K和奇偶性，0错误；重算SHA256与原正式收据一致。此项与本地R/B Python CLI分开进行。本地原生R --csv 尚未运行，因为当前容器不能直接下载该文件；不能把隔离V8源核验写成Python本地CSV原生门PASS。

全部比较针对九个已知人工规则和128个穷尽原始构型，没有随机抽样、样本外留出、概率校准的外部检验、真实群体数据或第三方团队独立复现。风险0仅在完整状态与已知真实规则条件下成立。历史原R262验收维持，S58内部E1计算审计完成；新增真人E2=0、历史E3=0、外部团队复现=0。R073/PESEN v0.1冻结。CI未启动，未确认GitHub免费运行余额，不新增付费操作。

下一步若能免费获取原CSV到本地，执行 R Python --csv 原生门；再把远端完整JSON字节直接输入归档B Python --receipt 进行原样命令行核验。严格记录任何字节差异和失败，禁止覆盖原历史文件。
