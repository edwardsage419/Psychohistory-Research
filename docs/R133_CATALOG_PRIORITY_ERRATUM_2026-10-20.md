# R133 目录优先级勘误（原冻结协议保留原字节）
日期：2026-10-20

复查未改动的 docs/MODEL_CANDIDATE_CATALOG_v0.1.json，原条目 05-009 Evolutionarily Stable Strategy 的 priority 字段实际是 P2。R133计算前冻结协议中将其误录为 P1；原冻结文档保留，禁止静默覆盖历史协议。

正确映射：R133 -> 05-009 -> P2。下一R134 -> 05-010 Multi Population Evolutionary Games -> P2。

此处仅改元数据。原ESS公式、625项输入集合、1973页码与25个舍入数、三策略反例、标准库36项单测以及Github Actions真实性均未改动。原239目录全体仍保持原始版本。
