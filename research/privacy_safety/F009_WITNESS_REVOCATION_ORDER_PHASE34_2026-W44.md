# F009 第三十四阶段：撤销传播顺序与旧回执
UTC 2026-10-31T07:18:57Z，2026-W44。目标键 (privacy_safety,F009,phase34,revocation-order-old-receipt)。仅虚构数据，不接入真实用户资料、设备或收费 TSA。

RFC 3161 定义可信时间戳 nonce、genTime、accuracy、ordering；缺少明确排序证明时不能从相近时间直接认定先后。RFC 5280 规定 CRL thisUpdate、nextUpdate 和撤销日期。两份标准均未直接规定本项目的人生决策授权，以下为候选人工状态机。

假设 epoch1 授权、epoch2 撤销、epoch3 再授权。枚举9个二元变量：回执是否epoch3，见证A/B/C是否epoch3，设备缓存是否epoch3，是否有独立根证据，签名是否有效，排序证明是否充分，撤销状态是否已知。512种人工状态，1543项断言全部通过。宽松规则只检查签名及至少两个见证与回执版本一致，接受128种，其中64种旧回执、64种无独立根。严格候选规则：签名无效或已知撤销且回执仍旧则REJECT，其他缺证据为UNKNOWN，仅九条件齐备时REVIEW。结果 REVIEW=1、UNKNOWN=191、REJECT=320。宽松接受的128种中127种不达REVIEW。

REVIEW仅代表可进入人工复核，绝非自动授权。epoch3重新授权为人工假设，真实再授权必须由合法主体决定。没有真实签名、撤销服务、设备或安全审计；状态计数不代表现实概率。

零费用候选控制：本地保存单调授权版本、签发身份、事件类型、撤销版本、见证依赖和时间不确定度。旧回执不得覆盖较新撤销。证据缺失、离线、乱序或冲突时保持UNKNOWN并暂停高影响自动执行，保留申诉和人工复核。坚持最小数据采集与本地优先。无个人决策产品开发。新增E2=0、E3=0。

来源：https://www.rfc-editor.org/rfc/rfc3161.html
https://www.rfc-editor.org/rfc/rfc5280.html

可复算程序：research/privacy_safety/f009_phase34_witness_revocation_order_20261031.js。下一项phase35多设备乱序撤销的持久化恢复。
