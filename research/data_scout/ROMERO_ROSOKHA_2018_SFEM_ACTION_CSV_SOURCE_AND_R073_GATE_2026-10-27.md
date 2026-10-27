# A轨：Romero与Rosokha 2018真人重复囚徒困境原始行动候选，来源、字段与独立验证门槛

日期：2026-10-27。状态：PUBLIC_GIT_BLOB_CONFIRMED / NOTEBOOK_SCHEMA_VERIFIED / FULL_ROW_AUDIT_BLOCKED / LICENSE_UNKNOWN / R073_FROZEN_E2_INELIGIBLE。

## 原始英文来源和去重
Romero, Julian and Yaroslav Rosokha (2018), *Constructing strategies in the indefinitely repeated prisoner's dilemma game*, European Economic Review 104, 185–219，DOI https://doi.org/10.1016/j.euroecorev.2018.02.008 。原文摘要说明真实实验的重复囚徒困境、继续概率0.95、每个实验session包含多个supergame，实验允许策略构造，具有明显的实验规则依赖。原作者研究页面 https://jnromero.com/research/strategyChoice 。本轮找到Yaroslav Rosokha公开GitHub仓库 https://github.com/yaroslavrosokha/sfem ，默认分支master。该数据来源与R073使用的Montero 2022双人100轮实验不同，不能将其与既有FRD2012、NV_games汇总数据自动视为完全独立；需要后续核验实际实验批次和样本重合。

## 本轮实际读取的材料
1. 通过GitHub仓库树确认 `input/action_data_RR2018.csv` 为公开普通Git blob，大小1,789,540字节，blob SHA1 `84ed4bc262757efe891683609063ca3ab00cca46`。文件存在并有确定版本；本轮读取大文件时连接器返回空文本，未取得全部CSV字节，因此未核验总行数、完整缺失、身份唯一性和所有行动镜像。
2. 实际读取 `sfem.ipynb`，blob `c18a3e4746db12c2e055c8ebd93808ba1a10b77e`。原有Notebook显示的已执行 `pd.read_csv` 输出可直接看到字段 `subject, supergame, period, action, opponentAction`，前五条记录为匿名 `T1S1S01` 的supergame 1、period 1至5，行动序列C,D,C,D,C，对手行动均为D。这是Notebook存档的示例输出，尚未独立复算原CSV。
3. Notebook明确筛选 `30 < supergame < 51` 且 `period < 21`，仅使用各supergame前20轮及第31至50场进行策略频率估计。不能把Notebook的策略估计样本当作完整原始数据，不能把这些supergame直接视为独立session。
4. Notebook包含20种策略和使用全部筛选行为拟合的混合模型，未看到独立场次留出评分协议；输出的策略占比只属于原研究拟合结果，不能当作样本外准确率。
5. 仓库树未发现LICENSE或COPYING文件。README请求引用论文，引用要求不能自动视为数据再分发许可。原论文的版权和公开GitHub可读性也不自动建立独立CSV的CC授权。原始CSV不复制进本项目仓库。

## 字段、单位与评分风险
`subject` 是匿名受试者键，`supergame` 是重复博弈编号，`period` 是轮次，`action` 与 `opponentAction` 是本轮双方行为。需从原始行检查 `subject` 是否跨session唯一、同一supergame的双人配对身份、每组轮数、session之间是否独立及同一受试者是否跨多个supergame。若在预测本轮行动时直接使用本轮 `opponentAction`，将造成同轮信息泄漏。正确时间特征只能使用已发生的对手历史行动，且应冻结具体允许信息。

实验使用不定长supergame及0.95继续概率，R073的双人100轮冻结评分不能直接迁移。若以后研究这项数据，先完成全CSV解码、许可证确认、独立session标识和训练测试分割，再另行冻结兼容的模型协议；R073原评分规则不得修改或事后调参。当前R073独立真人E2资格为NO，新增E2/E3均为0。

## 复现准备与阻塞
已取得固定Git blob、论文、README、Notebook已执行字段示例和筛选逻辑。下一步优先以免费工具完整读取固定CSV并做行数、类型、轮次连续性、行动互证、受试者跨session与实验批次核查。当前阻塞为1.79MB CSV读取工具限制、独立许可文本缺失及session身份未证实。没有访问私人数据、付费账户、收费API、GPU或GitHub Actions。主动新增费用0；账户实际账单未核验。
