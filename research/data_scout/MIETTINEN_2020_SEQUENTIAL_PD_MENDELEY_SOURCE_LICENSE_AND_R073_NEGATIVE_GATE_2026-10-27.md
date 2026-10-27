# A轨：Miettinen等2020顺序囚徒困境真人数据来源与R073负资格审查

日期：2026-10-27（Asia/Singapore）。结论：`PUBLIC_DATASET_METADATA_AND_LICENSE_CONFIRMED; ROWS_UNVERIFIED; R073_REPEATED_ROUND_INELIGIBLE`。性质：公开英文来源的元数据审计，无新增真人模型评分。

## 1. 论文和数据来源的实际核验

Miettinen、Kosfeld、Fehr、Weibull，2020，*Revealed preferences in a sequential prisoners’ dilemma: a horse-race between six utility functions*，Journal of Economic Behavior & Organization 173:1–25，论文 DOI `10.1016/j.jebo.2020.02.018`。作者所在机构的公开论文元数据确认该实验要求每名受试者分别报告先手行动、后手条件行动以及对其他人后手选择的信念。官方来源：
https://research.hhs.se/esploro/outputs/journalArticle/Revealed-preferences-in-a-sequential-prisoners/991001480258606056

原作者关联Mendeley Data归档：
https://data.mendeley.com/datasets/87nz7v9s98/1
数据 DOI `10.17632/87nz7v9s98.1`，版本1，公开日期2020-03-30，贡献者Topi Miettinen与Michael Kosfeld。实际打开公开数据页面，确认许可证标注 **CC BY 4.0**，页面存在“Download All”入口。页面明确写明变量名称解释需要向作者索取。当前读取界面没有呈现可独立核验的具体文件名、行数、字段字典或二进制内容。公开Mendeley API文档有列出文件的接口，但本轮工具未成功读取该数据集文件清单，故不得声称已下载原始记录或复算结果。API说明：
https://data.mendeley.com/api/docs/

本轮没有注册账户、请求作者提供私人数据、调用付费API或下载任何个体行记录。

## 2. 实验单位与R073适配门槛

根据作者机构论文摘要，核心观察是**顺序博弈的先手行动、后手条件策略和信念报告**。这与R073在每个双人重复博弈的t>=3轮使用过去两轮本人/对手实际行为预测下一轮C/D的任务不同。现有来源证据没有提供连续的t=1,2,3...真实轮次、对手逐轮配对身份、整实验场次编号和场次独立性。因此当前不得把此实验用于R073冻结评分，`R073_FROZEN_PROTOCOL_COMPATIBLE=NO`。

该来源可能在未来用于个人偏好与信念的横截面机制比较，前提是能实际获取合法数据文件、明确字段、实验单位、受试者独立性与缺失值；需另行预先冻结相容的研究问题和评分规则。当前未执行任何模型拟合、样本外预测或概率校准。

## 3. 来源去重与现有真人证据的项目级纠正

对本项目已有`research/SOURCE_PROVENANCE_DOI_DEDUP_REGISTRY_2026-10-18.json`的当前内容进行DOI及作者关键词检查，未找到该Mendeley数据DOI或Miettinen条目。该检查仅说明**已检查的旧注册表未收录**，不证明与全部239目录研究或所有真人实验完全无样本重合。不能计为第五项已验证独立真人重复博弈实验。

本轮还重新读取既有归档`research/data_scout/DF2011_FIXED_BLOB_ROW_DECODE_REPORT_2026-10-24.md`和`DF2011_R074_SAME_ORIGINAL_EXPERIMENT_DEDUP_2026-10-24.md`。确认DF2011 7358行六字段早在2026-10-24已完成实际解码，且来源与R074同为Dal Bó与Fréchette 2011原始实验。后续2026-10-27的DF2011来源登记若描述“尚未完成RDA解压”属于过时叙述，不能把它作为新独立实验。R074、R075和R077此前已分别归档第二、第三、第四项不同原始真人实验的有界研究。依据`research/operations/E006_R073_R077_STUDY_LINEAGE_EVIDENCE_TAXONOMY_AND_R167_E1_2026-10-26.md`，跨真人实验的旧版“E3”字段按当前统一口径仍归真人E2，历史社会演化E3仍未建立。该纠正不修改任何历史报告、R073冻结模型或旧机器收据。

## 4. 复现准备结果

`SOURCE_DOI_VERIFIED=YES`，`PAPER_DOI_VERIFIED=YES`，`LICENSE_PAGE_CC_BY_4_0=YES`，`DATA_BYTES_OBTAINED=NO`，`FIELD_DICTIONARY_VERIFIED=NO`，`ROW_COUNT_VERIFIED=NO`，`TIME_UNIT=SEQUENTIAL_ROLE_CONDITIONAL_ACTION_PER_PAPER_ABSTRACT`，`SESSION_ID_VERIFIED=NO`，`INDEPENDENT_ACTOR_SPLIT=NO`，`R073_COMPATIBLE=NO`，`NEW_E2_SCORES=0`，`NEW_E3_HISTORICAL=0`。

下一次A优先检查真正未评分的真人重复博弈数据的完整字节、明确场次身份、逐轮配对和许可；本Mendeley候选低于具有可复核完整纵向轮次的来源优先级。无新增费用；账户实际账单未核验。
