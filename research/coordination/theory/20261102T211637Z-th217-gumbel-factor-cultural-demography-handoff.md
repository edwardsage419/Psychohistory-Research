# TH217 文化人口与Gumbel公式校勘交接

track: theory
subflow: main
target_key: (theory,Henrich2004+Vaesen2016+HenrichEtAl2016+Fay2019,2004-original+2016-published+2016-author-accepted+2019-published,Gumbel-A3-normalization-vs-effective-learners-and-empirical-counterevidence)
utc_record: 2026-11-02T21:16:37Z
observed_main_before_write: fdf51d0ae145b9d8f6710b048110d18f454b0e97
evidence: Henrich2004原刊p210式A3/A7扫描图像；正文pp197至205；Vaesen2016 E2241至E2245正式版；Henrich等2016作者接收稿2页；Fay2019正式版pp6726至6729
finding: Henrich2004原刊A3/A7积分缺1/β，iid Gumbel下A4精确；β=2、N=100、a=4原印刷积分28.7295434而A4为14.3647717。2016竞争考古与2019纸飞机真人实验表明人口效应有条件，未作R轨实证复算。
outputs: theory/TH217_HENRICH_2004_GUMBEL_A3_FACTOR_AND_CULTURAL_DEMOGRAPHY_COMPETITION_2026-11-03.md; theory/th217_gumbel_integral_audit.py; theory/INDEX.md
tests: Python标准库4组参数8积分断言及3条件扩展断言PASS；正式勘误、原始真人/历史复算、CI NOT_RUN
C_D: C011 COMPLETE 2026-11-03；D003 COMPLETE 2026-W45实际2026-11-02；只读
frozen: R073; PESEN v0.1; R E1/E2/E3; MARKET
cost: 新增收费操作0，账户账单及免费CI额度NOT_VERIFIED
next: 查正式勘误及2016双方回复，Fay2019 SI与原始任务经验；随后跨学科轮换
coordination: 可选2小时提示性认领；不是原子锁；Codex开放PR未合并不算main成果
