# TH169 Smartcards公开复现目录、独立复现与选择性采用的因果边界

研究日期及英文来源检索日期：2026-10-31（Asia/Singapore）。
目标键：(theory,MURALIDHARAN_NIEHAUS_SUKHTANKAR_SMARTCARDS,TH169-theory-v1,archive_inventory_independent_replication_and_adoption_selection)。
状态：THEORY_NOTE_BOUNDED；ARCHIVE_INVENTORY_PARTIAL；INDEPENDENT_PUBLISHED_REPLICATION_RECOVERED；RAW_DATA_NOT_DOWNLOADED。
承接TH166至TH168；此笔记为非盲态文献与数学审计，未开展R系列拟合、真人数据复算或历史预测。

## 1. 原始来源、实际读取范围及可访问性

S1 [原作者正式出版信息与摘要，A] Muralidharan K, Niehaus P, Sukhtankar S (2016), Building State Capacity: Evidence from Biometric Smartcards in India, American Economic Review 106(10):2895–2929, DOI 10.1257/aer.20141346, https://pubs.aeaweb.org/doi/10.1257/aer.20141346 。本轮重新核对正式摘要；TH168已直接审读作者托管的正式排版全文，本轮未重新逐页阅读全部正文。
S2 [原作者开放工作论文元数据，B] 同作者，NBER Working Paper 19999 (2014), DOI 10.3386/w19999, https://www.nber.org/papers/w19999 。页面列出2014年10月修订，但本轮未恢复该修订全文。2014原稿与2016稿的353/296单位差异沿用TH167的原文审计。
S3 [原始复现档案官方目录，A：实际逐层打开目录，未取得文件内容] Muralidharan, Niehaus, Sukhtankar, Replication data for: Building State Capacity, openICPSR V1, 2019-10-12, DOI 10.3886/E113012V1, https://www.openicpsr.org/openicpsr/project/113012/version/V1/view 。本轮打开根目录、20141346_data、analysis_code、data及LICENSE.txt/20141346_ReadME.pdf文件详情页。LICENSE.txt 14.6 KB；ReadME.pdf 172.3 KB；master_analysis.do 11.2 KB；analysis_code目录显示37条（35个Stata do、2个R）；data目录显示62条Stata数据文件（本轮只看到首10项）。尝试下载LICENSE与README时分别重定向登录/403，未取得许可正文、README正文或数据字节。公开可浏览目录不自动意味着可免认证下载或无限制再分发。
S4 [第三方独立复现原报告，A：直接审读摘要、第2至6节及附录A1/A2/A3的部分表格] Atanda AA, Biometric Smartcards and payment disbursement: a replication study of a state capacity-building experiment in India, 3ie Replication Paper 23, March 2019, DOI 10.23846/RPS0023, https://www.3ieimpact.org/sites/default/files/2019-06/RPS23_Biometric_Smartcards_and_payment_disbursement_India_3.pdf 。原报告封面为2019年3月，版权/建议引用另有2018标记；按封面标注报告日期并记录版本差异。
S5 [同行评审复现论文摘要，B] Atanda AA (2019), Biometric Smartcards and payment disbursement: a replication study of building state capacity in India, Journal of Development Effectiveness 11(4):360–372, DOI 10.1080/19439342.2019.1646782, https://www.tandfonline.com/doi/abs/10.1080/19439342.2019.1646782 。仅审读可公开摘要，未购买收费正文；不将2019期刊全文等同于3ie报告逐字版本。
S6 [复现者公开代码归档元数据，B] Harvard Dataverse, DOI 10.7910/DVN/JQWCZH, https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/JQWCZH 。3ie官网明确指向该地址，访问出现JavaScript/机器人检查；代码文件身份与执行未核验。
S7 [3ie发布页，B] https://www.3ieimpact.org/evidence-hub/publications/replication-papers/biometric-smartcards-and-payment-disbursement 。报告为已完成的第三方同数据复现；不自动构成新地区独立实验。

## 2. 十二项条件性理论命题

TH169-01 [S3] 可检索归档与可执行复现是不同证据层次。目录存在仅证明元数据可发现；运行要求实际代码、数据、版本、软件环境和授权条件。
TH169-02 [S3,S4] 原始分析流程为多个Stata文件、两个R文件及master入口的组合。表格复算的完整依赖图必须覆盖data、analysis_code、utilities与compile_tables_figures，不能只检查单张表脚本。
TH169-03 [S4] 第三方在同一数据上报告原始代码可直接执行、主要表格可复现，增强计算可重复性证据；同源样本选择、历史行政总体、处理定义及因果外推仍需单独核查。
TH169-04 [S4] 第三方逐行检查发现某些Smartcard使用变量缺失值被改为零，作者报告未改变所检结果。缺失为零需要明确测量语义；缺失是否代表没有使用、未提问或未记录属于竞争机制。
TH169-05 [S4] 第三方报告对照组非零转卡暴露：NREGS对照村级单位中0.5%已转换、0.2%卡交易；SSP对应官方值为0%。行政交叉暴露、记录误差和处理扩散均是待分辨解释。
TH169-06 [S4] 原作者的随机分配对象为行政地区；实际持卡者与未持卡者的组内比较存在选择进入。第三方明确提醒该TOT式分解的选择非随机；不能由组间差异直接识别持卡者因果效应。
TH169-07 [S4] 第三方称所作非随机持卡者对比有助于建立上界。该上界需要额外单调选择或潜在结果限制；仅凭随机化行政区和组内持卡状态不足以保证上界方向。
TH169-08 [S4] 第三方报告约90%的稳健性比较与原结果相近，少数GLMM规格显著性与原OLS不同。该比例是作者按其检查集合形成的描述，不应作为所有政策估计目标90%可运输的概率。
TH169-09 [S4] 第三方未识别可解释地区效果异质性的调节变量，并说明社会经济变量缺失及内生性障碍。未检出异质性不能推导各地区真实效应完全相同。
TH169-10 [S2,S3,S4] 第三方以2016年296行政单位版本进行同源复现。其报告不能解释2014年353到2016年296的57单位差额；需要两个版本的行政身份与剔除时间链。
TH169-11 [S1,S4] 政策的意向处理效应、地区实际转卡覆盖率、个体持卡的选择效应、支付技术本身效应和整体推广政策效果是不同估计对象。
TH169-12 [研究方法推断] 第三方复现可以提升计算可靠性；独立来源、外部地区、长期追踪与事前冻结评估分别检验样本选择、可运输性和预测能力。不得混为单一科学验收等级。

## 3. 十项公开数字、目录及人工识别审计

E169-01 [S3] 官方归档V1日期2019-10-12；根目录显示LICENSE.txt、20141346_data，后者含四子目录、README及master入口。目录清单的文件名与大小已读，文件正文未读。
E169-02 [S3,S4] analysis_code显示37条，3ie报告记载35个Stata do文件加2个R文件，35+2=37一致。此一致性只覆盖文件数量，不证明哈希、版本或代码正确性。
E169-03 [S3,S4] data目录官方显示62条；3ie报告同样记载62个Stata数据文件。当前仅浏览目录首页10项，未遍历全部62项的名字和文件内容。
E169-04 [S4] 2016版本296=112处理+139缓冲+45对照；157=112+45。第三方独立报告同一分组口径；这不解决2014年113+195+45=353的版本差。
E169-05 [S4] 2016样本880个村级单位，NREGS官方GP结果880条，问卷GP结果818条；SSP官方880条，问卷878条。分别缺62、2条；结果表对应不同测量来源与可观测单位，不应把880当全部结局共同分母。
E169-06 [S4] 对照官方NREGS已转换GP约0.5%，交易比例约0.2%；该量级不能直接解释为随机化失效。需要个体及行政区时间戳、地区间传播与数据定义。
E169-07 [S4] 3ie报告表A2 NREGS支付领取时间处理系数在两规格为-22分钟，标准误9.2/8.7，p=0.019/0.014；SSP对应-6.1/-3.5，p=0.24/0.521。不同结局、模型与样本不可混为统一“22分钟效果”。
E169-08 [S4] 第三方报告2016政策效果与其同源重算相同，稳健性规格约90%可比。这个“约90%”的分母是作者选择的分析集合，本轮未独立逐表计数或复算。
E169-09 [人工反例] 在已转换村庄内，持卡者观察Y=0.9、未持卡者观察Y=0.5，两组各半，观察差=0.4。世界A设持卡者Y(0)=0.8、未持卡者Y(1)=0.6，平均真实采用效应=0.1；世界B设0和1，真实效应=0.7；世界C设1和0，真实效应=-0.3。三世界观察值完全一致，观察差0.4既可能高于也可能低于真实平均效应。纯人工，不代表Smartcards数据。
E169-10 [人工尖锐界] 仅给定E169-09两组观察结果、各占一半、潜在结局在[0,1]，整体采用平均效应的可达区间为[-0.3,0.7]。端点由E169-09世界C/B达到；无外部识别假设不能宣称观察差为上界。原报告“upper bound”属于作者的解释性主张，需要更强条件才能形式化。

## 4. 竞争机制、四层联系与验证清单

个体层：持卡者的实际可用性、缺失值、领取时间和选择采用；反例包括非持卡者具有不同初始能力或政治关系。
群体层：村级同伴传播、对照区少量转卡和行政区间支付网络；反例包括共同的记录规则变化。
制度层：支付链、行政容量、问责、腐败适应与技术故障；反例包括改革同时改变支付组织与身份验证，单项机制难以拆分。
历史层：2014与2016随机化总体口径、2019复现版本及地区跨期政策环境；外推需要身份对应、制度版本和共同支持。

验证优先级：1）在许可允许且无需新增费用时读取LICENSE/README的原始字节；2）确认master_analysis.do与37个脚本的路径依赖和运行环境；3）查找行政区随机化ID、Nalgonda单位身份、2014年10月修订稿；4）逐表复核3ie“约90%”稳健性分母；5）先冻结估计对象、原始分母和测量缺失语义，再考虑真实数据复算。遇登录、收费、隐私限制则记录阻塞，不规避访问控制。

## 5. 证据等级与协作边界

已直接读取：openICPSR官方可浏览目录、3ie公开报告指定章节和部分附录表；已读摘要：原作者2016正式摘要、2019期刊复现摘要；未读：openICPSR LICENSE与README正文、全部原始数据字节、Dataverse代码、2014年10月修订稿。人工精确计算独立于真实数据。
2019第三方复现是既有文献成果，本轮仅发现、审读、比较；不得把其执行归为本项目新E1/E2/E3科学验收。
REAL_DATA_REPLAY=NOT_RUN；ORIGINAL_UNIT_ID_MATCH=UNKNOWN；ARCHIVE_LICENSE=UNREAD；ARCHIVE_README=UNREAD；E1/E2/E3新增=0。R系列既定顺序及冻结协议不变。C008已满足2026-10-31，D002已满足2026-W44，均保持只读。
下一专题TH170：3ie附录的真实表格对照与失访/缺失重编码可识别性；如能合法读取原始README，再优先恢复2014/2016行政区身份流转。
