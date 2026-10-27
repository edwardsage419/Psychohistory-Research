# A轨：Shirado 2020 真人网络公共物品博弈来源与原始记录访问资格

日期：2026年10月28日。审计状态：PUBLIC_DATASET_METADATA_AND_LICENSE_VERIFIED / RAW_JSON_NOT_RETRIEVED / E2_REPLAY_BLOCKED。

## 公开来源及独立性

一手数据存档：Hirokazu Shirado，*Bot Cooperation Experiment Dataset*，Mendeley Data，2020年7月21日发布，版本1，DOI 10.17632/t963ktp6ft.1。固定公开入口：https://data.mendeley.com/datasets/t963ktp6ft/1 。

原作者及 Christakis 2020 年研究 *Network Engineering Using Autonomous Agents Increases Cooperation in Human Groups*，iScience 23(9), 101438，DOI 10.1016/j.isci.2020.101438；原作者研究机构英文页面：https://humannaturelab.net/paper/network-engineering-using-autonomous-agents-increases-cooperation-in-human-groups 。

存档说明明确：1024名真人，64个网络，网络公共物品博弈；部分实验加入基于局部信息重新配置网络连接的自动代理。研究单位主要是网络，不能把1024人当作1024个独立网络。公开说明将原始每场次JSON放在 `data/raw`，另有个人级和网络级分析R代码；exp1包含6种bot处理及1种可见性处理，exp2包含单bot五条连接的补充实验。以上数量均是原作者元数据声明，**本轮没有逐行读取JSON，因此没有独立确认实际记录、轮次、字段和场次完整性**。

## 许可及访问尝试

Mendeley Data版本1公开页面明确标记 CC BY 4.0。许可为该存档页面的声明，若后续重用文件仍需核对具体文件和第三方材料的适用条款。页面显示 Download All，但当前网页读取接口只返回HTML元数据，无法取得嵌套原始JSON目录或文件字节。尝试访问官方公开数据API `https://api.data.mendeley.com/datasets/t963ktp6ft?version=1` 和 `.../files?version=1` 均返回读取环境不可访问错误。没有绕过访问限制、注册账户或下载个人级原始数据。

## 复现资格矩阵

来源与作者：VERIFIED_METADATA；公开许可：CC_BY_4_0_PAGE_VERIFIED；逐轮行为记录：NOT_VERIFIED；时间单位及轮次：UNKNOWN；参与者匿名ID与网络ID：UNKNOWN_AT_RAW_LEVEL；网络间独立性：64_NETWORKS_CLAIM_ONLY；行为变量及bot动作编码：UNKNOWN；实际JSON下载：BLOCKED；代码可执行性：NOT_TESTED；复现难度：MEDIUM_TO_HIGH，需解析会话JSON、动态边、bot与真人身份及网络聚类。

此数据可能支持未来网络干预、社会合作和群体动态的真人E2探索，但实验为网络公共物品博弈，**R073冻结的双人100轮囚徒困境直接复评分资格=NO**。当前新增E2评分=0。需取得公开原始JSON字节、固定SHA256，核对场次、轮次、匿名ID、动态网络和许可后再设计预冻结的独立留出评分。不得混用 E1、E2、E3。

## 与已有登记的区别及下一步

本轮读取项目main递归文件树，未发现此前的 SHIRADO 或此DOI数据登记路径。此项与先前Fudenberg公共物品博弈、OpenNeuro三人囚徒困境及Montero 2022固定/轮换配对实验分开登记；同源性仍应在真正下载后用论文与样本时间再次检查。

下一轮可优先尝试Mendeley公开归档的无需登录下载入口，检查raw JSON与R脚本的文件清单和哈希。若继续受限，保持BLOCKED并转向明确开放的其他独立真人长轮次实验。无新增费用。
