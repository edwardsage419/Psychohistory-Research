# 第36轮：首次对话关闭与未返回会话的生命周期
2026-11-24。main c95c6e61137c9e45d8aa87298371ad1de831f22e；PR #61 固定 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核查 v3.1、AGENTS、同步规程、近期提交及开放 PR、唯一产品交接（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）、第34/35轮、V06_INDEPENDENT_HANDOFF、两份最新修复报告。第35轮后PR已修复全局clear期间start重新发布的竞态，见 V06_SESSION_INVALIDATION_REPAIR_2026-11-24.md；本轮不重复该竞态，专门分析没有已知session_id时的单客户端关闭。关联B09/B12，补充原交接的共享设备退出与临时会话要求，不改交接清单。无新模型准入。
## 源码审查
固定四个源码blob及锚点（实际连接器文本子串检查，不是原始字节哈希复算）：
```json
[
  {
    "blob": "c0ca9a82863359eefbdc8611ca6abd4a71c910bd",
    "anchors": [
      {
        "text": "if(token&&session_id)void fetch",
        "found": true
      },
      {
        "text": "conversationId.current=null;",
        "found": true
      },
      {
        "text": "signal.throwIfAborted();",
        "found": true
      }
    ]
  },
  {
    "blob": "443b6141aeb1aa3c52595dace7a5726d7d6667eb",
    "anchors": [
      {
        "text": "return () => active.abort();",
        "found": true
      },
      {
        "text": "registerConversation(next.session_id);",
        "found": true
      },
      {
        "text": "const next = await api<ConversationView>",
        "found": true
      }
    ]
  },
  {
    "blob": "f505aeab2d9e5e0a9c8957ce6e039dea174918a7",
    "anchors": [
      {
        "text": "generation = self._generation",
        "found": true
      },
      {
        "text": "row = Conversation(uuid4().hex",
        "found": true
      },
      {
        "text": "if generation != self._generation:",
        "found": true
      },
      {
        "text": "self._sessions[row.session_id] = row",
        "found": true
      },
      {
        "text": "SESSION_TTL = 45 * 60",
        "found": true
      }
    ]
  },
  {
    "blob": "85ff09e20483211deec434ac252047f2c0265ef1",
    "anchors": [
      {
        "text": "class StartInput(InputModel):",
        "found": true
      },
      {
        "text": "question: Original",
        "found": true
      },
      {
        "text": "class EndInput(InputModel):",
        "found": true
      },
      {
        "text": "session_id: Identity",
        "found": true
      }
    ]
  }
]
```
App.closeConversation只有已获session_id才调用end；结束本地会话或离开工作台会触发关闭/abort。DecisionConversation仅在收到start响应后登记session_id；App API在读取响应后检查abort。StartInput没有客户端预先可知的会话身份；服务端start自己生成uuid，在_ingest完成后检查全局generation并发布。单页面关闭在未登记ID时并未调用clear/end；如果请求已抵达且继续在服务端执行，浏览器取消等待本身不能证明后端停止。故存在关闭早于收到响应且服务端继续完成时的孤儿会话路径。服务端TTL为2700秒，_expire由后续操作调用；没有后续清理调用的闲置路径上，45分钟是访问时的过期阈值，不能据此宣称45分钟必定从内存主动删除。实际ASGI取消语义、真实浏览器及provider运行未执行；不能认定真实事故或泄露。当前同源本地bearer保护及不默认持久保存仍有效。
## 候选设计与有限状态复算
先取得仅含随机身份的短期reservation，再提交自然语言；关闭时使用已知租约身份取消。只有尚有效的reserved能原子进入running；完成时仅同一仍有效的running租约可原子发布，取消/到期删除后不得重新创建。单租约关闭不能误伤别的会话。所有开始、完成、取消、到期、容量回收在同一锁/事务语义下验证身份及代次；保留全局clear防护。预约不得携带问题或隐私；预约响应丢失时不提交问题。身份不复用，重复start拒绝或幂等，关闭幂等。需限制租约数、寿命和内存；客户端响应仍按视图修订拒绝过期结果。
有限模型枚举B(服务端开始)、F(完成)、R(客户端收到结果)、C(关闭)，B<F<R且C可在任意位置。假定取消可送达，旧基线3/4顺序产生服务端孤儿，新租约候选0/4；这是序列计数，绝非实际风险概率。取消丢失的4/4反例要求主动有界清理：若有效期T且可靠调度最大间隔d，则活租约对象最迟在T+d从会话表移除（假定单调时钟及调度锁延迟计入d）；非会话表中运行线程/模型上下文、备份、已送达响应不在此保证。示例d=5秒仅为假设，未设产品参数。进程挂起、调度失败、网络丢包时不能承诺即时清除。比较更简单的全局clear，单租约避免取消无关会话；取消全局授权仍须全局invalidate。增加一次自动本地握手，不增加用户必填项，真实延迟待测。
### 可复算 JS（Node，普通模式；本轮实际执行同一函数）
```js
function experiment(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 // B: server accepts start, F: finishes, R: response reaches browser, C: client closes.
 // Reserve candidate assumes acknowledged non-sensitive reservation before B, and delivered C.
 const orders=["CBFR","BCFR","BFCR","BFRC"];
 function simulate(order,mode,delivered=true){
  let closed=false, known=mode==="lease", phase=mode==="lease"?"reserved":"absent",working=false,visible=false;
  for(const e of order){
   if(e==="B"){working=mode==="old"||phase==="reserved";if(mode==="lease"&&working)phase="running";}
   if(e==="F"&&working){if(mode==="old"||phase==="running")phase="active";working=false;}
   if(e==="R"&&!closed&&phase==="active"){known=true;visible=true;}
   if(e==="C"){closed=true;visible=false;if(delivered&&known)phase="absent";}
  }
  return {order,mode,delivered,orphan:closed&&phase==="active",visible,phase};
 }
 const matrix=orders.flatMap(o=>["old","lease"].map(m=>simulate(o,m)));
 const lost=orders.map(o=>simulate(o,"lease",false));
 check(matrix.filter(x=>x.mode==="old"&&x.orphan).length===3,"old witness");
 check(matrix.filter(x=>x.mode==="lease"&&x.orphan).length===0,"lease guarantee");
 check(matrix.every(x=>!x.visible),"no client display after close");
 check(lost.every(x=>x.orphan),"lost close counterexample");
 // Multi-session: deletion of A is scoped, unlike global clear.
 const sessions=new Map([["a","running"],["b","active"]]);sessions.delete("a");
 const canPublishA=sessions.get("a")==="running";check(!canPublishA&&sessions.get("b")==="active","scoped cancellation");
 // Candidate must not accept a second start or late completion after a removed/expired lease.
 const states=["absent","reserved","running","active"];
 const eligibleStart=states.filter(x=>x==="reserved"),eligibleFinish=states.filter(x=>x==="running");
 check(eligibleStart.length===1&&eligibleFinish.length===1,"transition admission");
 // Native lazy expiry does not run while idle; conceptual bounded timer sweeps at expiry+delta.
 const ttl=2700,delta=5,elapsed=3600;
 const lazyIdleRetains=elapsed>ttl;const scheduledRemoves=elapsed>=ttl+delta;
 check(lazyIdleRetains&&scheduledRemoves,"expiry distinction");
 return {matrix,lost,oldOrphans:3,leaseOrphans:0,deliveredSchedules:4,lostCancelOrphans:4,scopedCancelPreservesOther:true,eligibleStart,eligibleFinish,ttlSeconds:ttl,illustrativeSweepSeconds:delta,lazyIdleRetains,scheduledRemoves,scope:"finite abstract transition model; no browser, HTTP, server or provider execution"};
}
console.log(JSON.stringify(experiment(),null,2));
```
### 实际输出
```json
{
  "matrix": [
    {
      "order": "CBFR",
      "mode": "old",
      "delivered": true,
      "orphan": true,
      "visible": false,
      "phase": "active"
    },
    {
      "order": "CBFR",
      "mode": "lease",
      "delivered": true,
      "orphan": false,
      "visible": false,
      "phase": "absent"
    },
    {
      "order": "BCFR",
      "mode": "old",
      "delivered": true,
      "orphan": true,
      "visible": false,
      "phase": "active"
    },
    {
      "order": "BCFR",
      "mode": "lease",
      "delivered": true,
      "orphan": false,
      "visible": false,
      "phase": "absent"
    },
    {
      "order": "BFCR",
      "mode": "old",
      "delivered": true,
      "orphan": true,
      "visible": false,
      "phase": "active"
    },
    {
      "order": "BFCR",
      "mode": "lease",
      "delivered": true,
      "orphan": false,
      "visible": false,
      "phase": "absent"
    },
    {
      "order": "BFRC",
      "mode": "old",
      "delivered": true,
      "orphan": false,
      "visible": false,
      "phase": "absent"
    },
    {
      "order": "BFRC",
      "mode": "lease",
      "delivered": true,
      "orphan": false,
      "visible": false,
      "phase": "absent"
    }
  ],
  "lost": [
    {
      "order": "CBFR",
      "mode": "lease",
      "delivered": false,
      "orphan": true,
      "visible": false,
      "phase": "active"
    },
    {
      "order": "BCFR",
      "mode": "lease",
      "delivered": false,
      "orphan": true,
      "visible": false,
      "phase": "active"
    },
    {
      "order": "BFCR",
      "mode": "lease",
      "delivered": false,
      "orphan": true,
      "visible": false,
      "phase": "active"
    },
    {
      "order": "BFRC",
      "mode": "lease",
      "delivered": false,
      "orphan": true,
      "visible": false,
      "phase": "active"
    }
  ],
  "oldOrphans": 3,
  "leaseOrphans": 0,
  "deliveredSchedules": 4,
  "lostCancelOrphans": 4,
  "scopedCancelPreservesOther": true,
  "eligibleStart": [
    "reserved"
  ],
  "eligibleFinish": [
    "running"
  ],
  "ttlSeconds": 2700,
  "illustrativeSweepSeconds": 5,
  "lazyIdleRetains": true,
  "scheduledRemoves": true,
  "scope": "finite abstract transition model; no browser, HTTP, server or provider execution"
}
```
## 独立验收与下一责任方
独立轨冻结新情节：首次start尚未到达/正在推理/已发布未返回时关闭，已收到后关闭，关闭消息丢失、重复关闭、重试、租约超时、容量回收、同时打开另一标签页、全局撤回、过期返回、真实provider停止能力和浏览器卸载。验证服务器会话表、客户端视图、保存记录及日志分别无越权残留；区分正常可达、请求取消、服务端对象清理及实际内存/外部副本删除。候选属B09/B12一体化规格，非单独Codex任务，不自动修改API。真实浏览器/HTTP/线程、受支持Python、Mac Qwen、iPhone、独立验收、实际用户效果均NOT_RUN。只证明有限状态模型和固定源码锚点。无正式开发、CI、训练、PR合并、部署、冻结改动和新增费用。
