# 自主引擎：有界精确数值协议、共享参数调度与结果收据
2026-11-26。RESEARCH_CANDIDATE / PYTHON_NODE_PARITY / VERIFIED_NATIVE_SLICE / SYNTHETIC_DEVELOPMENT / INDEPENDENT_NOT_RUN。手动科研增量，非正式产品或科学验收。起始main d73bf7e3ad4032d2c94346953ba7ebe14f4a0757；固定v0.7 Draft #62 e61bbad10932edabc9a87483e5407fdae6c751cc。实际核对18近期提交、14开放PR、v3.2及同步规程前18行、唯一交接 research/coordination/DECISION_WORKBENCH_PRODUCT_PRIVACY_HANDOFF_2026-11-19.md 前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、前轮数值与活动版本报告9c8ea98d61646f481d65193486169de5f6362b54前18行及前轮实际研究包。检索serialization/rational/canonical/shared parameter/budget；已有R54共享参数谱系、R4类型调度、R111结果信封、近期预算续算及来源资格等不重复计为新研究。本轮新增数值线协议的严格有界解码、跨语言实测、有限算术预算下共享转换与硬门连接、认证结果收据负向控制；全库去重不保证。不修改唯一产品交接、已定v0.8任务或生产代码。
## A 数值线协议与资源约束
研究合同：数值端口只接受ASCII已约分有理数n/d，分母为正、零唯一0/1、禁止前导零、空白、指数、浮点JSON值、非ASCII数字和非规范别名。分子绝对值及分母最多38位十进制，字符串长度最多78；先检查长度及语法，再转换整数和gcd。不能用于任意精度宣称。原文和显示精度仍另保留。原始用户输入解析、单位资格及科学证据由独立宿主确认；不能由语法合格推导事实真实或许可。
计算支持有限加法和乘法。对输入n/d,p/q定义b(z)=max(1,bit_length(abs(z)))；令A=b(n), B=b(d), C=b(p), D=b(q)。加法未约分分子位宽上界W=max(A+D,C+B)+1，分母B+D；乘法上界A+C及B+D。计算前限制位宽≤256且结构成本不超过剩余额度：add成本A*D+C*B+B*D+W，mul成本A*C+B*D。计算完成后若规范输出超过38位则拒绝输出但仍扣已计算成本。未进入算术步骤时不扣该步骤成本；链式计算逐步扣款，中途失败不发布完整链结果。上述成本是研究者选定的确定性结构代理，仅覆盖所列算术步骤，不是CPU、内存、GCD、JSON解析、认证、调度或全请求资源上限；真实运行仍需独立长度、请求、时间、内存控制。此有界输入集最大位宽不足以系统测任意长度输入，位宽门主要为后续扩展保留。非线性变换、仿射单位、汇率及概率模型未执行。
实际Python3.13.5 Fraction与Node22.16.0 BigInt两套实现，无网络、第三方包或训练。521个合法规范量包括2^53附近及38位边界，32个负例全部拒绝；972算术配置（9量×9量×2算子×6预算），319成功、601预算限制、52输出限制。两运行时逐项完全一致1525/1525。1715条两次加法链，498完整、1217阻断，所有完整链与Fraction直接总和一致。跨端这里只是Python与Node，不声称Swift/iPhone。
## B 真实C028片段连接
复用前轮固定全文 decision_feasibility.py，实际重算Git blob SHA1 6181d6c578c7ef251e9708d0ffcf65e95d35f88f，通过AST仅执行原始check_constraint函数。使用人工结构对象，非完整DecisionState/Pydantic/Hub/API。5费用×4阈值×3比例×4比较符×7资格状态×3额度=5040场景，其中720资格匹配、4320未资格、320合格但计算受限、400完成有理数换算及硬门；0错误确定判定。独立时间约束在5040场景均以另外固定夹具保留，不代表完整决策通过。400已完成中若采用浮点比较有8错误（非当前产品错误率）。具体来源、参数身份、用途、时间范围、活动版本及代次来自人工可信合同；元数据完全一致才准备，四个内容摘要/缺授权/非规范别名负例额外拒绝。主实验以每案例的已知数值为可信输入，额外控制核对旧内容摘要不能授权新数值；未实现生产授权服务。
## C 共享转换及预算
同一可信请求中的两个硬约束共享一次同一参数的精确换算结果；比较成本以交叉乘法的位长乘积和计。相同完整输入合同、来源、用途、代次、活动版本、预算策略且在可信进程内才复用。972配置（4量×3比例×3下界×3上界×9预算），与重复执行转换的基线使用相同逐步额度及顺序。共享403完整，重复377完整，26仅共享完整、0仅重复完整；尝试调用1305与1944；累计已收费结构成本94482与112288（不同完成数且非耗时测量），两者均0错误确定判定。对x=1/3、比例1/3、下界0、上界1/3、额度16，共享两门均确定通过，重复转换第二门LIMIT。两门分别覆盖不等于全局决策资格。
7项版本、代次、预算策略、来源、用途、数值和比例变化，旧收据7/7拒绝、旧生产请求7/7拒绝，新收据7/7通过。重要反例：输入摘要相同但把输出1/3替换为2/1，输入摘要校验仍能改变硬门判断。此反例针对研究夹具，不是已证实平台漏洞；普通哈希不能认证输出来源，客户端不得自行提交可信结果。
## D 认证收据及回退边界
单独Python标准库HMAC-SHA256研究原型，每次运行生成临时测试密钥（不持久化、不入库）。固定ASCII字段数组绑定会话、修订、授权代次、活动方法精确版本、预算策略、来源、用途、原始规范数值和比例、初始额度、输出值、成本及RESEARCH_ONLY权威状态。14合格收据通过，4计算失败不发收据；56处输出、成本、权威状态或认证码篡改全部拒绝；140旧上下文核验全部拒绝；14新代次重新计算通过。14同一上下文重复验证仍通过，明确未提供同上下文防重放；正式系统须以事务、幂等操作身份、当前代次和可信发布边界控制，不把认证等同数学正确或授权。密钥托管、跨设备信任、完整输出schema、严格有界外层解码和原子事务未实现。研究夹具不是安全产品。
## E 实际资产、复算和边界
本轮会话包 psychohistory_wire_shared_research_2026-11-26.zip，SHA256 3143505769cdf09f48de2519d15eaa4275ef923ddb97e16f91bb7477b0f24c93。包含wire.py、wire.js、probe.py、shared.py、receipt.py、固定C028原文件、逐项输入cases.json、三个结果JSON、README和SHA256SUMS。实际11个受校验文件全部通过，ZIP完整性检查通过，三个结果文件连续两次运行逐字节相同。完整包在研究会话提供，不声称ZIP已上传至仓库。下列独立实现的核心JS在连接器标准计算环境实际再次执行，输出与Python/Node研究包摘要一致；它不执行C028原生片段、不运行HMAC或真实授权，不能代替完整包。所有样例为ChatGPT辅助产生的原创虚构开发夹具，同一研究者、非独立留出、非真实用户或现实频率。
```js
function replay(){
 const abs=n=>n<0n?-n:n,gcd=(a,b)=>{a=abs(a);while(b)[a,b]=[b,a%b];return a},F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);const g=gcd(n,d);return [n/g,d/g]},str=([n,d])=>`${n}/${d}`,bits=n=>abs(n).toString(2).length;
 const check=(b,m)=>{if(!b)throw Error(m)};
 function parse(s){if(typeof s!=="string"||s.length>78)throw Error("WIRE");const m=/^(0|-?[1-9][0-9]{0,37})\/([1-9][0-9]{0,37})$/.exec(s);if(!m||m[0]!==s)throw Error("WIRE");let n=BigInt(m[1]),d=BigInt(m[2]);if(gcd(n,d)!==1n)throw Error("NONCANONICAL");return [n,d]}
 function exact(op,[n,d],[p,q]){return op==="add"?F(n*q+p*d,d*q):F(n*p,d*q)}
 function calc(op,a,b,budget){let [n,d]=a,[p,q]=b,[A,B,C,D]=[n,d,p,q].map(bits),w=op==="add"?Math.max(A+D,C+B)+1:A+C,cost=op==="add"?A*D+C*B+B*D+w:A*C+B*D;if(Math.max(w,B+D)>256||cost>budget)return ["LIMIT",null,0];let v=exact(op,a,b);if(abs(v[0]).toString().length>38||v[1].toString().length>38)return ["OUTPUT_LIMIT",null,cost];return ["OK",v,cost]}
 function cmp([n,d],[p,q],op){let a=n*q,b=p*d;return op===">="?a>=b:op===">"?a>b:op==="<="?a<=b:a<b}
 let valid=new Set();for(let n=-20;n<=20;n++)for(let d=1;d<=20;d++)valid.add(str(F(n,d)));for(let i=-2n;i<=4n;i++)valid.add(str(F(2n**53n+i)));for(let x of [F(10n**37n+1n,10n**37n-1n),F(10n**38n-1n),F(1,10n**38n-1n)])valid.add(str(x));
 for(let s of valid)check(str(parse(s))===s,"wire");
 let invalid=["-0/1","00/1","01/1","1/01","+1/1","1/-1","1/0","2/2","0/2","2/4","1/1\n","1/1\r"," 1/1","1/1 ","1 /1","1.0/1","1e2/1","١/1","１/1","−1/1","1/１","1/1\u0000","9".repeat(39)+"/1","1/"+"9".repeat(39),"9".repeat(10000)+"/1","1/1/1","",null,false,1,{},["1/1"]];
 for(let s of invalid){let rejected=false;try{parse(s)}catch(e){rejected=true}check(rejected,"malformed")}
 let a=[F(-3,7),F(0),F(1,3),F(2,9),F(1,10n**37n-1n),F(1,10n**37n-3n),F(10n**37n+1n),F(2n**53n+1n),F(10n**38n-1n)];
 let arithmetic={LIMIT:0,OK:0,OUTPUT_LIMIT:0};
 for(let op of ["add","mul"])for(let x of a)for(let y of a)for(let budget of [0,1,16,128,4096,65536]){let [s,v,c]=calc(op,x,y,budget);check(c<=budget,"budget");arithmetic[s]++;if(s==="OK")check(str(v)===str(exact(op,x,y)),"exact")}
 let chains={complete:0,blocked:0};for(let x of a.slice(0,7))for(let y of a.slice(0,7))for(let z of a.slice(0,7))for(let budget of [0,16,128,4096,65536]){let [s,v,c]=calc("add",x,y,budget);if(s==="OK"){let [t,w,k]=calc("add",v,z,budget-c);if(t==="OK"){check(str(w)===str(exact("add",exact("add",x,y),z)),"chain");chains.complete++;continue}}chains.blocked++}
 let g={cases:0,qualified:0,unqualified:0,limit:0,exact_gate:0};for(let x of [F(0),F(1,3),F(2n**53n),F(2n**53n+1n),F(10n**37n+1n)])for(let t of [F(0),F(1,3),F(2n**53n),F(2n**53n+1n)])for(let s of [F(1),F(1,3),F(3,2)])for(let op of [">=",">","<=","<"])for(let ctx=0;ctx<7;ctx++)for(let budget of [0,64,65536]){g.cases++;if(ctx){g.unqualified++;continue}g.qualified++;let [status,v]=calc("mul",x,s,budget);if(status!=="OK"){g.limit++;continue}check(cmp(v,t,op)===cmp(exact("mul",x,s),t,op),"gate");g.exact_gate++}
 function solve(x,s,ts,budget,share){let left=budget,results=[],v=null,calls=0;for(let [t,op] of ts){if(v===null||!share){let [status,val,cost]=calc("mul",x,s,left);calls++;left-=cost;v=val;if(status!=="OK"){results.push(status);continue}}let [n,d]=v,[p,q]=t,cost=bits(n)*bits(q)+bits(p)*bits(d);if(cost>left){results.push("LIMIT");continue}left-=cost;results.push(cmp(v,t,op)?"CERTAIN_PASS":"CERTAIN_FAIL");if(!share)v=null}return [results,budget-left,calls]}
 const complete=r=>r.every(x=>x==="CERTAIN_PASS"||x==="CERTAIN_FAIL");let shared={cases:0,shared_complete:0,duplicate_complete:0,shared_only_complete:0,duplicate_only_complete:0,shared_compute_calls:0,duplicate_compute_calls:0,shared_cost:0,duplicate_cost:0};
 for(let x of [F(1,3),F(2,9),F(2n**53n+1n),F(10n**37n+1n)])for(let s of [F(1),F(1,3),F(3,2)])for(let lo of [F(0),F(1,3),F(2n**53n)])for(let hi of [F(1,3),F(1),F(2n**53n+1n)])for(let budget of [0,8,16,32,64,128,512,4096,65536]){let ts=[[lo,">="],[hi,"<="]],[a,c,na]=solve(x,s,ts,budget,true),[b,d,nb]=solve(x,s,ts,budget,false);shared.cases++;shared.shared_complete+=+complete(a);shared.duplicate_complete+=+complete(b);shared.shared_only_complete+=+(complete(a)&&!complete(b));shared.duplicate_only_complete+=+(complete(b)&&!complete(a));shared.shared_compute_calls+=na;shared.duplicate_compute_calls+=nb;shared.shared_cost+=c;shared.duplicate_cost+=d;check(c<=budget&&d<=budget,"fanout budget");for(let row of [a,b])row.forEach((v,i)=>{if(v.startsWith("CERTAIN"))check(v===(cmp(exact("mul",x,s),ts[i][0],ts[i][1])?"CERTAIN_PASS":"CERTAIN_FAIL"),"fanout")})}
 return {valid:valid.size,invalid:invalid.length,arithmetic,chains,gate:g,shared};
}
console.log(JSON.stringify(replay(),null,2));
```
实测核心复算输出：
```json
{
  "valid": 521,
  "invalid": 32,
  "arithmetic": {
    "LIMIT": 601,
    "OK": 319,
    "OUTPUT_LIMIT": 52
  },
  "chains": {
    "complete": 498,
    "blocked": 1217
  },
  "gate": {
    "cases": 5040,
    "qualified": 720,
    "unqualified": 4320,
    "limit": 320,
    "exact_gate": 400
  },
  "shared": {
    "cases": 972,
    "shared_complete": 403,
    "duplicate_complete": 377,
    "shared_only_complete": 26,
    "duplicate_only_complete": 0,
    "shared_compute_calls": 1305,
    "duplicate_compute_calls": 1944,
    "shared_cost": 94482,
    "duplicate_cost": 112288
  }
}
```
## F 接入建议与下一责任
NumericPort沿用上轮精确量合同，新增可验证的规范编码、长度上限、受控算术策略和不确定状态；预算策略版本与活动方法及结果绑定。共享参数调度按真正相同输入合同去重，完整上下文才可复用；不同权限、时域、来源、预算策略或活动版本不共享。ResultPort记录完整输入输出及计算状态、来源和代次，并由可信宿主完成认证及发布事务。受限设备降级使用前轮保守区间，不能把UNKNOWN/LIMIT当成0或确定违反。对应v0.8 G01/G03/G04/G08/G09，不新增独立Codex任务或扩大已定范围。手动窗口后续优先研究跨阶段联合情景中精确量的完整计算及预算资源的真正计量；模型轨、产品轨与独立轨分别负责科学合同、唯一交接和独立测试。所有历史冻结、R073、PESEN及证据等级不变。无个人数据、生产源码修改、训练、外部AI运行时、合并、部署、计费资源或主动CI运行。
