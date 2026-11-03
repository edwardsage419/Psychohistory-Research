# MKT240 Exist 手工追踪缺失值语义与相关性接口审查

track: market
run_date_utc: 2026-11-03
target_key: (market,Exist,manual-tracking-zero-default-and-correlation-API,missingness-semantics-and-effect-validity)
baseline_main: 00d1e5b6d81720a0569f89d7c72f1ea555054756
status: COMPLETE_BOUNDED_OFFICIAL_DOCUMENT_REVIEW
evidence: MARKET-E1_OFFICIAL_DOCUMENTATION
independent_human_effect: NOT_VERIFIED
native_execution: NOT_RUN
CI: NOT_RUN
billing: NOT_VERIFIED
R_E1_E2_E3: NO_CHANGE

## 直接核实的机制

Exist 手工记录支持 quantity、decimal、duration、1至9量表、时间和百分比，亦支持自定义标签及第三方同步。官方帮助文档明确规定：quantity 与 duration 若某日没有记录，默认写入零；其他数值类型未输入时不写值。官方称数周数据后可展示相关性及趋势。

官方 correlations API 返回近一周生成的相关结果，字段包含 period、offset、value、p、stars、文字解释，并允许按 confident、strong、attribute 筛选。API 示例中的相关系数、p值和星级仅为文档示例，不能视为真实独立实测样本。

官方帮助明确提示相关性不能识别因果，可能受反向因果、第三变量或偶然性影响。

## 具体风险与可证伪问题

在 quantity/duration 类型，未输入和真实零会在文档描述的默认规则下合并；在其他类型，未输入保持未观测。这意味着同一个人的追踪习惯改变，可能改变进入相关计算的序列及缺失机制。**此处只是由数据记录规则推导的潜在测量偏差，尚无生产相关性计算反例。** 若某日没有输入实际发生的活动，零默认会低估真实量。若真实零没有手动记录，则该默认值可能正确。无法从官方文档确定关联计算是否对默认零、停用属性、数据不足或时间滞后作特殊处理。

需要独立核验的高价值问题：
1. 数量类型未输入与显式零是否在导出中可区分。
2. 相关性计算是否保留观测掩码，是否处理序列自相关、多重检验与滞后。
3. 星级与p值的精确定义、校准及多次探索后的假阳性控制。
4. 是否存在独立随机研究证明看见Exist相关建议改善了客观长期决策结果。

上述均 UNKNOWN；没有账户、真实个人数据、API token或付费操作。

## 产品与F风险边界

实际输入：自动同步与手工数值/标签。状态表示：日级属性时间序列。反馈：相关系数、置信星级及自然语言说明。产品官方价格页面显示月费6.99美元、年费62.90美元；本轮未购买。官方2026-04-23发布PDF导出，支持CSV、JSON与PDF；其导出可用性不等于删除完成或本地优先。2023-10-06隐私政策为需继续单独审阅的云端数据边界。没有取得产品专属独立长期改善实验。

F已有本周F010完成登记，本轮仅提出最小采集与观测/缺失分离的后续方法问题，不升级F专题，不读取敏感资料。

## E只读状态

本轮查询main近期提交，baseline为上列SHA，较MKT239提交后增加TH220理论提交。开放PR查询返回12项，均为Draft，未合并；PR #8/#9存在历史身份依赖，R272生产写权限和强制前像验收缺口未见关闭证据。E168为当日既有审计；待核队列本轮未逐项重算，净变化UNKNOWN。R073及PESEN v0.1冻结保持。

## 原始公开来源（2026-11-03访问）

https://exist.io/page/help-manual-tracking/
https://developer.exist.io/reference/correlations/
https://kb.exist.io/article/37-what-are-correlations
https://exist.io/about/custom-tags/
https://exist.io/blog/pdf-export/
https://exist.io/privacy/

本轮没有运行原生代码、人工模拟、真实用户实验或CI。没有新增付费服务，GitHub实际账单与免费额度未验证。下一步优先寻找独立产品效果研究，或核实导出文件能否区分默认零和真实零；如无新来源，转向其他产品。
