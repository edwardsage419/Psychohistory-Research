# A轨公开历史事件数据侦察：UCDP GED 26.1

日期：2026-10-30 UTC。目标键 (A,UCDP-GED,26.1,source-schema-license-time-leakage-access)。状态：PUBLIC_SOURCE_AND_SCHEMA_DOCUMENTATION_CONFIRMED / RAW_CSV_NOT_PARSED / E3_NOT_RUN。

## 实际读取的原始发布方材料

1. Uppsala Conflict Data Program 官方下载中心 https://ucdp.uu.se/downloads/ ，2026-10-30读取。GED Global 26.1 为逐事件组织暴力数据，官方描述地理位置可精确至村庄、时间可至单日。官方提供 CSV、Excel、codebook，全部当前UCDP数据免费，CC BY 4.0，可在署名并按要求引用文献条件下再分发。历史事件覆盖1989至2025年，版本26.1。官方要求引用Davies、Pettersson、Öberg (2026) 和 Sundberg & Melander (2013)，并记录数据版本。
2. 官方API文档 https://ucdp.uu.se/apidocs/index.html ，2026-10-30读取。版本26.1示例含 id、relid、year、type_of_violence、conflict_new_id、dyad_new_id、side_a_new_id、side_b_new_id、country_id、date_start、date_end、date_prec、where_prec、latitude、longitude、deaths_a、deaths_b、deaths_civilians、deaths_unknown、best、high、low、source_article、code_status 等字段。示例仅为文档示意，未取得真实记录。
3. 官方API现要求经邮件申请免费的访问token，网页说明每日5000次请求限制。当前阶段不申请token，不调用API；优先未来直接下载官方免费CSV及codebook。下载页面许可与API认证分别记录。

## 可复现性与研究适用性

* 观测单位：有时间及位置的组织暴力事件；事件 id、冲突/双方dyad ID可作为候选连接键，须核验跨版本稳定性。时间字段 date_start/date_end 为日期区间，date_prec 表示时间精度；不能把所有事件无条件当作精确单日观察。
* 历史研究价值：适合有明确预先冻结的国家或冲突单元时间切分，估计未来事件数量或是否发生的概率，并与简单历史频率/季节性基线比较。E3历史预测目前为零，真实CSV行数和缺失尚未验证。
* 泄漏风险：source_article、code_status 和死亡数区间 best/high/low 可能包含事后修订信息。预测日期以前不可使用预测日期之后形成的字段或最终修订结果作输入。需要建立资料发布时间、事件发生时间、编码/修订时间的独立界限，留出时间段与地理/冲突聚类评估。
* 不能用本历史事件数据充当R073冻结的真人双人百轮重复博弈。R073适用性=NO。历史E3的评估协议须在查看未来事件标签前另行冻结。
* 许可：官方明确CC BY 4.0，具体引用和版本声明为必要条件。原始CSV未下载/再分发。
* 可获得性：官网免费CSV/Excel/codebook确认列出，实际文件字节、CSV表头、版本SHA、真实事件数、完整字段类型、缺失率均 NOT_VERIFIED。官网API需要token，未访问，也无收费服务调用。

## 下一步可执行复现准备

在免费资源允许时，下载固定26.1官方CSV和codebook，保存SHA256及获取时间；核验事件唯一性、时间精度、冲突/国家连接键、死亡估计上下界、来源发布时间；建立不跨未来信息的按年滚动训练/测试协议及基线。若官方CSV无法获取，登记BLOCKED，不改用付费API。不得把官方API文档示例总行数当作真实下载核验。

本轮新增E1模型结果0、真人E2=0、历史E3=0。无数据采购、无新增收费操作。此记录仅是数据候选来源与复现准备增量，不构成历史事件预测验收。
