# TH074 原著增补：Cox 等 2009 工作论文与 2010 正式刊文分母及证据单位审计

track: theory
run_date: 2026-11-07 (Asia/Singapore)
target_key: (theory,Cox-Arnold-VillamayorTomas,2009-WP09MC1-vs-2010-ES03704,study-case-denominator-and-selection)
observed_main_head_before_write: 168b9bcf56cae2afdae02771c74edf98351c0c85
status: PRIMARY_VERSION_COMPARISON_BOUNDED
parent: theory/TH074_SES_ROBUSTNESS_CROSS_SCALE_FEEDBACK_ADAPTIVE_GOVERNANCE_2026-10-27.md

## 直接审读的原始版本

[A] Michael Cox, Gwen Arnold, Sergio Villamayor Tomás (2009), *Design Principles are not Blue Prints, but are They Robust? A Meta-analysis of 112 Studies*, Lincoln Institute of Land Policy Working Paper WP09MC1. 原始开放PDF：https://www.lincolninst.edu/app/uploads/legacy-files/pubfiles/1707_925_Cox%20Final.pdf 。直接审读封面摘要、目录、§3.3样本分布与§4总结果、结论段。无DOI核实。

[B] 同三位作者 (2010), *A Review of Design Principles for Community-based Natural Resource Management*, *Ecology and Society* 15(4):38, DOI:10.5751/ES-03704-150438。Indiana University Digital Library of the Commons保存的正式刊文PDF：https://dlc.dlib.indiana.edu/dlcrest/api/core/bitstreams/fe453645-ec0f-4a71-91ad-19abd9634dbc/content 。直接审读Introduction、Methods中的Data collection and coding、Coding of cases、Analytical methods、Results的样本和方法统计段及Table 1附近、Discussion开头。未逐项审读全部设计原则论证、附录和底层逐案数据。

## 版本差异与真正新增的方法事实

1. 2009工作论文标题及§3.3明示分析112项研究，按资源领域分为森林23、牧场7、灌溉28、渔业23、多个领域19、其他12，合计112。2010正式刊文Results明示91项study和77个case；研究单位有明确区分。91和112分别属于不同出版版本，不能混写为同一正式刊文的样本数。两版是否严格共享样本框、删去哪些研究、是否存在重编码，当前仍UNKNOWN；不可从112减91=21推断确切排除原因。
2. 正式刊文将study定义为被编码的论文、著作等作品；case为详细研究中涉及特定地理区域及共同资源的经验单位。统计型研究中的观测对象不被重复纳入case数据集。某些同一共同体的不同时期可以作为不同case，条件是发生实质变化。因此91 study和77 case既不等价，也不能合并为168个独立观测。
3. 正式刊文的study级评价是1至5的有序等级。91项中详细研究46、统计研究8、综合研究28、抽象研究9；总体均值3.73。原作者报告研究方法类型间Kruskal-Wallis P=0.004，排除抽象研究后P=0.122。抽象研究的中位数2.0，提示“理论批评较强、经验研究相对支持”部分取决于证据类型构成，不能将3.73解释成资源治理成功概率。
4. case级按原则分别编码成功与原则条件是否存在，缺乏信息时留空。作者明确因缺失量大而按原则分开分析；Fisher精确检验用于2×2关联，phi用于关联强度。每条原则使用的case子集可能不同，跨原则显著性无法直接当作同一完整样本上的联合制度因果效果。作者报告原则8仅在10%阈值显著，其余在5%阈值显著；这些是原文报告，未独立复算。
5. 正式刊文对study级评价采用双人编码，冲突时取更保守值；case级变量没有全部双人编码。编码优先尊重原研究作者自己的结论。故存在发表选择、研究者解释偏差、跨研究可比性和非随机缺失问题。关联也可能由资源条件、治理能力、外部制度或先前成功经验共同驱动。

## 竞争解释与可证伪边界

竞争A：设计原则有助于维持集体行动。竞争B：较有治理能力的共同体更容易建立这些原则并保持成功。竞争C：研究发表、编码和选择机制让支持性案例更易进入可观察样本。原刊的分层关联不能单独识别A、B、C。

可观测量：原始study唯一ID、case唯一ID及年代、资源领域、各原则是否有可编码资料、成功判据、作者结论、编码者分歧、研究选择与发表年份。后续若获得两版逐条名单，按稳定ID做交集、差集和重编码审计，方能解释112到91的变化。若有独立样本或前瞻制度变化数据，可预注册比较规则变化前后的资源状态，控制生态及外部冲击；本轮没有执行。

适用范围：群体合作、制度治理及历史资源环境的条件性解释。不得推出个人价值权重、跨文化普适制度配方或确定未来事件。

## 项目状态及执行

main已存在TH074 Ostrom2009指定页审读与TH197相关制度条目，故沿用TH074作版本审计，不新增TH编号。C子流程2026-11-07 PARTIAL，已知C012完成于2026-11-06；D子流程2026-W45 COMPLETE，D003完成于2026-11-02。R073、PESEN v0.1及证据等级保持不变。独立复算NOT_RUN，真人实验NOT_RUN，历史因果估计NOT_RUN，CI NOT_RUN。未使用新增收费服务；实际计费NOT_VERIFIED。
