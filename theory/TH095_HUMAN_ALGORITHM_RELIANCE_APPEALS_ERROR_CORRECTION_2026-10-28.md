# TH095 算法建议与人类裁量的依赖、申诉权、错误纠正及政策事后评价

研究日期与英文来源检索日期：2026-10-28（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。起始远端 main HEAD 核验为 `48f35dbbdb72c39b7b43c35dd4bcbe18001e083c`；写入前 TH095 同名文件不存在。理论储备研究，R 系列优先；C005 今日、D002 本周保持只读。未接入个人敏感资料，未开展行政干预，未调用收费服务或主动触发 CI。

## 一、原始文献与实际访问等级

A 表示本轮直接审读作者开放原文的指定章节；B 表示只核验原始摘要、原刊页面或机构原始书目。以下来源均为英文，检索日期同上。

1. [A] Dietvorst, Berkeley J., Joseph P. Simmons & Cade Massey (2018). “Overcoming Algorithm Aversion: People Will Use Imperfect Algorithms If They Can (Even Slightly) Modify Them.” *Management Science* 64(3):1155–1170. DOI https://doi.org/10.1287/mnsc.2016.2643 。作者机构原刊 PDF https://faculty.wharton.upenn.edu/wp-content/uploads/2016/08/Dietvorst-Simmons-Massey-2018.pdf 。直接审读摘要、Study 1–3、Study 2 Figure 4、讨论。Study 2 的选择模型比例为不允许调整 47%，允许调整10、5、2个百分位时分别为71%、71%、68%；实验为激励性学生成绩预测任务，外推到行政裁量需独立检验。
2. [A] Buçinca, Zana, Maja Barbara Malaya & Krzysztof Z. Gajos (2021). “To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-Assisted Decision-Making.” *Proceedings of the ACM on Human-Computer Interaction* 5(CSCW1), article 188. DOI https://doi.org/10.1145/3449287 。作者开放原刊 PDF https://www.eecs.harvard.edu/~kgajos/papers/2021/bucinca21trust.pdf 。直接审读设计、Table 2/3、结果、讨论。N=199，作者报告在错误AI建议上认知强制减少部分过度依赖；整体团队准确率相较普通解释界面无显著改善，接受度及认知动机存在异质性。
3. [A] Green, Ben & Yiling Chen (2019). “Disparate Interactions: An Algorithm-in-the-Loop Analysis of Fairness in Risk Assessments.” *FAT* 2019*:90–99. DOI https://doi.org/10.1145/3287560.3287563 。作者开放原刊 PDF https://www.benzevgreen.com/wp-content/uploads/2019/02/19-fat.pdf 。直接审读摘要、引言、实验框架及主要发现。受试者为众包普通参与者，并非法官；种族差异互动是该实验情景中的结果。
4. [A] Green, Ben & Yiling Chen (2021). “Algorithmic Risk Assessments Can Alter Human Decision-Making Processes in High-Stakes Government Contexts.” *Proceedings of the ACM on Human-Computer Interaction* 5(CSCW2), article 418. DOI https://doi.org/10.1145/3479562 。作者开放全文 https://arxiv.org/abs/2012.05370 。直接审读研究设计、引言、结果与局限。2140名众包参与者模拟两个公共决策情景；作者报告实验中预审羁押种族差异增加1.9%，政府贷款援助减少8.3%，不等于真实行政政策因果效果。
5. [A] Binns, Reuben (2018). “Fairness in Machine Learning: Lessons from Political Philosophy.” *Proceedings of Machine Learning Research* 81:149–159. 原刊 https://proceedings.mlr.press/v81/binns18a.html ，PDF https://proceedings.mlr.press/v81/binns18a/binns18a.pdf 。直接审读平等主义、歧视理论与多种公平目标的章节；规范理论，不是某一种公平指标的实证证明。
6. [A] Wachter, Sandra, Brent Mittelstadt & Chris Russell (2018). “Counterfactual Explanations without Opening the Black Box: Automated Decisions and the GDPR.” *Harvard Journal of Law & Technology* 31(2):841–887. 作者开放稿 v3 https://arxiv.org/pdf/1711.00399 ，DOI（预印本）https://doi.org/10.48550/arXiv.1711.00399 。审读原文有关解释目的、反事实建议及法律讨论的指定章节。其关于救济的建议属于作者法律论证，不能概括为所有司法辖区既有的申诉权。
7. [B] Kroll, Joshua A. et al. (2017). “Accountable Algorithms.” *University of Pennsylvania Law Review* 165(3). 原刊页面 https://pennlawreview.com/2017/02/23/accountable-algorithms/ 。仅核验作者原始摘要，全文访问重定向受阻。提出程序化核验与问责工具的规范主张。
8. [B] Kim, Pauline T. (2017). “Auditing Algorithms for Discrimination.” *University of Pennsylvania Law Review* 166(1). 原刊页面 https://pennlawreview.com/2017/12/12/auditing-algorithms-for-discrimination/ 。直接阅读出版页的详细作者论述，未通读 PDF。强调结果审计和社会背景，作为 Kroll 等偏重技术核验的竞争观点。
9. [B] Dietvorst, Berkeley J., Joseph P. Simmons & Cade Massey (2015). “Algorithm Aversion: People Erroneously Avoid Algorithms After Seeing Them Err.” *Journal of Experimental Psychology: General* 144(1):114–126. DOI https://doi.org/10.1037/xge0000033 。原刊摘要 https://doi.org/10.1037/xge0000033 及 PubMed https://pubmed.ncbi.nlm.nih.gov/25401381/ ，未审读完整正文。

## 二、16项条件性理论命题、机制与反例

P01【A1】看到算法犯错后，部分人在实验中更愿意选择人工预测。依赖水平受任务、错误展示、参与者经验和激励影响；不能将算法厌恶视为普遍常数。
P02【A1】允许少量人工修正可以提高参与者采用算法的比例。Study 2 不同修正幅度差异较小；更高采用率本身不证明更高公平性。
P03【A2】算法错误时，简单解释界面可能仍促使参与者照单全收；认知强制有助于识别部分错误。需同时报告错误建议采纳率、正确建议拒绝率及总效用。
P04【A2】认知强制增加认知负担并影响主观接受度，且效果受认知动机调节。任务时长、教育程度、工作压力可能改变干预效果，后者为待检推断。
P05【A3】算法风险分数经人工解释后可能引入新的群体差异。实验中对黑人被告的风险上调响应更强；不得将众包实验直接推广为法官普遍行为。
P06【A4】预测精度提高仍可能改变决策者对风险与其他目标的权重。实验中的羁押与援助变化需要同时考察自由、资源分配和程序保障。
P07【A5】公平目标包含不同规范立场，可能强调机会、结果、最弱势者或历史不公。指标选取必须显式登记价值判断和利益相关者。
P08【A6】反事实解释可帮助说明改变哪些输入可能改变系统输出，但仅凭模型边界无法保证建议现实可执行、合法或符合个人利益。
P09【A6/B7】申诉与解释应区分：告知原始输入、纠正事实错误、质疑规则、要求人工复核、获得实际救济。作者提出的制度设计须按司法辖区另行核验法律效力。
P10【B7与B8竞争】技术合规证明可以核验预设规则；外部结果审计可能发现规则之外的系统性伤害。两者目标不同，技术核验不足以确定规范规则本身正当。
P11【研究推断】行政纠错应追踪受理、审查、撤销、重新决定、实际执行及后续伤害，避免只报告申诉成功率。各阶段受选择和失访影响。
P12【研究推断】人工覆盖建议的比例需要区分正确纠偏与错误覆盖；覆盖率为零或很高均不能单独说明治理质量。
P13【研究推断】事后评价需记录政策前后的选择性标签、申诉可达性和干预引发的行为反馈；既有 TH094 行政记录偏差问题延续存在。
P14【研究推断】评价单位应包含个体结果、群体分布、机构规则执行及长期制度信任，不能以单一准确率替代完整政策目标。
P15【研究推断】申诉资格、材料门槛、语言与时间成本可能影响谁进入可观察申诉样本。若仅观察成功申诉者，无法推断全部错误率。
P16【研究推断】长期部署可能改变工作人员对建议的学习、抵抗、责任归属及公众行为，短期随机实验的平均效应不能自动迁移至多年制度变化。

## 三、八项人工数学与识别审计

E01【原刊数字核算】Dietvorst 等 Study 2 的允许调整10/5/2百分位模型采用率分别71%、71%、68%，对照47%；差值24、24、21个百分点。原刊图表数字核算，不是原始个体数据复算。
E02【人工】AI独立正确率0.8；人工在AI正确时有20%概率错误覆盖，在AI错误时有50%概率正确纠偏。最终正确率=0.8×0.8+0.2×0.5=0.74，低于直接采用AI的0.8；是否覆盖与错误条件相关，不能以平均覆盖率替代。
E03【人工】同样80% AI准确率，若人工只在AI错误时纠偏50%且从不破坏正确建议，最终准确率=0.8+0.2×0.5=0.9。E02与E03说明人工协作成败取决于条件纠偏能力。
E04【人工】100件行政拒绝中20件申诉、10件成功撤销。即使假定成功撤销均纠正真实错误，未申诉80件及未撤销10件的错误状态未知，总错误数可处于10至100；10/20申诉成功率无法识别总体错误率。
E05【人工】两个群体各100人，模型原始建议拒绝率均20%；人工额外分别拒绝5人与15人且均从原建议通过者中选取，最终拒绝率25%和35%。原始建议相同不保证最终结果平等。
E06【人工】算法只建议改变不可控制的历史变量，形式上可使输出从拒绝变批准；现实中变量无法改变，反事实建议的可行性为零。反事实距离小不等于实际救济成本小。
E07【人工】政策A正确率0.90、每100人错误10件；政策B正确率0.88、每100人错误12件。若A错误的平均损害为10单位、B为1单位，则期望总损害A=100、B=12；准确率排序与损害排序反转。损害权重属于规范选择。
E08【人工】在仅观察获批准者后续违约时，100人中50人批准，已知其中10人违约；另50人拒绝且其潜在违约未知，总潜在违约数的粗界为10至60。拒绝组若永不暴露于贷款，其“获得贷款时违约”是反事实，需要额外识别假设。

## 四、跨四层框架及竞争解释

个体层：算法厌恶、自动化依赖、认知努力、权利意识、解释理解和申诉成本。实验参与者偏好变化可能来自控制感，也可能来自预测任务的奖励结构。

群体层：不同人群的错误覆盖、申诉进入率和后果差异；群体结果差异可能来自数据分布、人工偏差、制度约束或共同环境。

制度层：模型采购、人工覆盖权限、申诉程序、复核记录、审计责任和规范权重。Kroll等强调技术核验能力，Kim强调社会影响的外部审计，两种方法可互补，仍存在资源与合法性争议。

历史层：制度引入前后的决策规则、纠错渠道、政策反馈及公众信任变化。必须区分同期改革、执行差异、档案保存与算法引入本身的效果。

## 五、候选验证清单与未决问题

1. 明确评价目标：准确率、错误损害、可解释性、申诉可达性、群体公平、财政成本及时间窗口，登记各目标的规范权重。
2. 预先记录原始建议、人工初始判断、覆盖理由、最终决定、复核过程、纠错结果及执行结果，避免覆盖后只保留最终标签。
3. 区分人工与AI的条件正确率，针对AI正确和错误的样本分别测量采纳、拒绝和纠偏。
4. 检查结果只在获批准或被执法群体可见时的选择性标签，必要时给出部分识别区间。
5. 比较无AI、纯建议、可小幅修正、认知强制和可申诉等方案；先做伦理和合法性审查，禁止未经授权的真实高风险随机试验。
6. 申诉审计需要分母：有资格者、知晓者、提出者、受理者、复核者、成功者、实际获救济者。
7. 对制度变化进行时间对齐、处理前趋势、共同改革、溢出与长期反馈检查；不可将短期众包实验视为真实政策净效果。
8. 未来优先研究 TH096：行政申诉的可达性、选择性进入、复核误差及纠错后长期后果。保持 R 系列完成后再分类与熔炼。

证据边界：本轮六份开放原文或作者稿指定章节直接审读，两份原刊页面及一份原刊摘要核验；八项算术或人工反例。真实行政微观数据复算0，独立因果估计0，前瞻性政策评价0，模型熔炼0。未检验的跨时代解释仅作研究假设。