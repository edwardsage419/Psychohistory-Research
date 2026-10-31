# A轨数据登记：Values Interact with Psychological Distance and Eco-Anxiety to Promote Climate Engagement

日期：2026-11-01（UTC+8）。目标键：(A,hanwzhang_valuesAndClimateEngagement,public_GitHub_schema,R323_measurement_relevance_privacy_gate)。

## 已实读英文官方来源
原作者公开仓库：https://github.com/hanwzhang/valuesAndClimateEngagement 。README 明确说明包含论文《Values Interact with Psychological Distance and Eco-Anxiety to Promote Climate Engagement: Insights from Two Experimental Studies》分析所用的两套清洗数据。

实际通过 GitHub 连接器读取仓库目录、README、LICENSE 文件开头及两份 CSV 表头，未开展逐行数据处理：
* study1CleanedData.csv，210088 字节，Git blob 7bc3033ef3cbdbb853a14a79d0bbfd53a9ee4176。
* study2CleanedData.csv，305027 字节，Git blob f15e655707506394cbffea86cc7f970416b89ee8。
* README.md Git blob 39485fb3ccabffce83bb51f5123e84958bd992ad。
* LICENSE Git blob f288702d2fa16d3cdf0035b15a9fcbc552cd88e7，文件开头为 GNU GPL v3。数据文件自身是否单独授予 GPL v3 或其他再利用许可，未找到明确声明，须单独确认。

## 可见字段与任务匹配
Study 1 表头含 value_1 至 value_15、efficacy_1 至 efficacy_4、mitigation_intention_1 至 7、policy_support_1 至 4、PD_1 至 PD_8、condition、start_date 等。Study 2 表头含 SELFTRANSCD、CONSERV、OPENNESS、ECOANX、RISK_PERCEP、WEPT_Behavior、POL_SUPPORT、condition、responseId 等。可用于后续探索价值、风险感知与环境行为自报指标的测量关系，但没有验证完整 VBN 的个人规范中介指标，也没有验证客观行为结果。

Study 1 有日期字符串字段，Study 2 有任务时长字段；两个研究是否有同一人纵向重复测量、样本独立性、实际样本量、完整字段缺失率、干预随机化和行为计量单位仍 UNKNOWN。文件大小与 Git blob 是远端元数据核验，尚未本地完整解析或独立 SHA256。

## 隐私和许可阻塞
表头存在 zip_code、political_party、gender_text、自由文本 description；Study 2 还含 responseId、textResponse、ethnicity 和 zipcode。仅核对表头，不复制、保存或分析参与者具体回答，也不上传原始 CSV。后续研究必须先进行最小化字段筛选、去标识化与许可审核，避免将政治倾向、地理细节、个人自由文本纳入公共研究包。

数据访问：公开 GitHub CSV 入口可见；合法再利用范围：DATA_LICENSE_UNCONFIRMED；R323 实证复现：NOT_READY；R073 资格：HARD_NO_BY_TASK_TYPE，非双人百轮重复博弈。真人 E2 新评分 0，历史 E3 新评分 0。未购买数据、注册付费账户或使用中文网站。

## 复现准备
后续若许可和隐私审核通过，优先只提取匿名研究条件、价值与风险量表、规范测量候选、环境行为结果字段，按参与者与研究分组避免泄漏。预先冻结测量模型、缺失处理、外部验证与校准指标。R073 冻结模型及评分规则不变。
