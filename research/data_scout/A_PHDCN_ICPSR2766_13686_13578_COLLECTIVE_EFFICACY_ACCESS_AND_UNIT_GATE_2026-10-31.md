# A轨：PHDCN集体效能原始来源、权限与分析单位核验

核查日期：2026-10-31 UTC。任务键 (A,PHDCN_ICPSR_2766_13686_13578,metadata_v1,access_unit_license)。证据来源为ICPSR官方英文元数据；未下载任何受限记录，未注册账户或购买数据。

## 三套来源严格区分

1. ICPSR 2766 V4, Community Survey 1994–1995, DOI https://doi.org/10.3886/ICPSR02766.v4 ，版本日期2023-03-29。社区横截面成人居民访谈，问卷包括邻里社会凝聚、社会控制、感知暴力、资源、人口背景。Part 1个体问卷；Part 2邻里cluster聚合。343个邻里cluster。官方Restrictions明确要求Restricted Data Use Agreement及IRB批准或豁免说明，且“at present, only a restricted version ... available”。官方Notes又有公共使用文件的通用提示，不能据此忽略该项目具体限制。实际文件字段、逐行记录、独立个体ID、精确样本计数、数据许可与哈希：NOT_VERIFIED。当前复现门 BLOCKED_RESTRICTED。
2. ICPSR 13686 V1, Community Involvement and Collective Efficacy (Young Adult), Wave 3, 2000–2002, DOI https://doi.org/10.3886/ICPSR13686.v1 ，版本日期2007-02-06。面向Longitudinal Cohort Study的15和18岁组，问卷含社区参与、邻里凝聚、邻居干预可能性，单位为individual，访谈形式含面访和电话。该整体纵向项目在Wave 1/2/3分别有6228/5338/4850名受访者，这些数字不等于本具体问卷的样本量。官方明确Restricted Data Use Agreement和IRB要求，且说明目前仅有受限版本。实际个人跨波次连接键、逐行记录、文件级许可和哈希：NOT_VERIFIED。状态 BLOCKED_RESTRICTED。
3. ICPSR 13578 V1, Systematic Social Observation 1995, DOI https://doi.org/10.3886/ICPSR13578.v1 ，2005-07-18发布。官方目录列105 MB DS1及public-use访问说明。采集80个邻里cluster中街道block-face的视频和观察日志，分析单位是街道侧面/观察单元，与居民的自报集体效能问卷不同。原始字段、许可和本轮可下载性未实测。该公开候选只可作为潜在环境观察数据，不能充当2766或13686的居民问卷，也不能未经核验将两者匹配为因果复现。

## 与R主线及R073的适配门

R308当前只验证原创E1人工公式 B*c*w*r。上述真实研究并未估计或支持该乘法公式。ICPSR 2766及13686当前受限，不启动数据获取；13578公开说明尚不足以建立B、c、w、r与真实干预结果的一一对应。

R073冻结协议要求具有合法前序自身/对手行动及独立双人重复博弈场次。三套PHDCN来源均不符合其博弈设计。R073_VALIDATION_ELIGIBLE=NO。

## 复现准备结果

已核实发布者、版本、调查时间范围、主要问卷内容、调查单位、受限状态与跨来源不可互换风险。未核实文件级字段编码、缺失值、身份键、实际逐行数量、许可、下载SHA或真人样本外评分。只记录官方公开元数据，零私人数据处理。下次如公开可用版本出现，先确认具体文件及授权，再冻结真实目标和分组方案。不得为了R308 E2追求绕过访问限制。

来源： https://www.icpsr.umich.edu/web/NACJD/studies/2766 ; https://www.icpsr.umich.edu/web/NACJD/studies/13686 ; https://doi.org/10.3886/ICPSR13578.v1 。原作者背景：Sampson et al. 1997 DOI 10.1126/science.277.5328.918。无中文网站来源。
