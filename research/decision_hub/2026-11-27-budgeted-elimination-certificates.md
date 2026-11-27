# 预算受限线性消元、矛盾证书与撤回复用
2026-11-27。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
基线 93d6346053cfdfc655ef65778542faf4b632d6ec，写前HEAD一致，目标404。读取最近20提交、开放PR、上一轮消元全文、正式规程及同步规程（本轮工具获取全文，输出末2000字符）、唯一交接末2000字符。局部去重。经典消元直接推导，未核对原论文。
每行保存原始行的非负整数权重向量，初始单位向量，消元按相同正倍数合并。严格标志当且仅当某正权重原始行严格。若合成系数全零且常数负或常数零且严格，则不可行。验证器直接从原始行及权重复算，拒绝负权重、全零权重及长度错误。每次正负行配对消耗一单位预算；达到上限且尚无矛盾则UNKNOWN，完整消元才可YES。仅限制配对次数，非总时间、内存或位长上限；无可行性见证输出。撤回原始行时若其证书权重为零，剩余原始行不变且快照重新绑定，则旧证书仍有效；非零权重须重新求证，不能推断必然可行。生产需可信快照绑定、输入验证、资源限制、证书权限隔离，当前未实现。共享故障预算下需对所有允许故障集合分别证明不可行，本轮仅单固定集合求解器，未接入上一轮故障外层。authority NONE。
实验：研究者选定二维[0,4]^2、40条候选观察、三条可重复组合、配对上限0/4/16/1000。参照为闭包顶点枚举及严格行松弛判定，非独立人员验收。撤回检查计数含非零权重行（仅零权重行执行复用断言）。负权重及零证书变异实际验证。合成配置非独立样本。未验证真实语言、设备、任意维、独立留出、训练、CI、合并或部署。零新增费用。下一责任模型轨可行见证与快照绑定，独立轨留出，产品轨解释交互。冻结及交接不变。
复算（置于函数内执行并打印返回值）：
```js
const row=(a,b,c,s=false)=>({v:[BigInt(a),BigInt(b)],c:BigInt(c),s});
function verify(rs,w){if(!Array.isArray(w)||w.length!==rs.length||w.some(x=>typeof x!=="bigint"||x<0n))return false;let v=[0n,0n],c=0n,s=false;rs.forEach((r,i)=>{for(let j=0;j<2;j++)v[j]+=w[i]*r.v[j];c+=w[i]*r.c;s ||= w[i]>0n&&r.s});return v.every(x=>x===0n)&&(c<0n||c===0n&&s)}
function solve(rs,cap){let z=rs.map((r,i)=>({...r,w:rs.map((_,j)=>BigInt(i===j))})),used=0;
const bad=r=>r.v.every(x=>x===0n)&&(r.c<0n||r.c===0n&&r.s);
for(let j=0;j<=2;j++){let b=z.find(bad);if(b)return {state:0,w:b.w,used};if(j===2)return {state:1,used};
let p=z.filter(r=>r.v[0]>0n),n=z.filter(r=>r.v[0]<0n),q=z.filter(r=>r.v[0]===0n).map(r=>({...r,v:r.v.slice(1)}));
for(const a of p)for(const b of n){if(used>=cap)return {state:-1,used};used++;let u=-b.v[0],v=a.v[0],r={v:a.v.slice(1).map((x,i)=>u*x+v*b.v[i+1]),c:u*a.c+v*b.c,s:a.s||b.s,w:a.w.map((x,i)=>u*x+v*b.w[i])};if(bad(r))return {state:0,w:r.w,used};q.push(r)}z=q}}
function oracle(rs){let vertices=[];for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){let a=rs[i],b=rs[j],d=a.v[0]*b.v[1]-b.v[0]*a.v[1];if(!d)continue;let x=a.c*b.v[1]-b.c*a.v[1],y=a.v[0]*b.c-b.v[0]*a.c;if(d<0n){d=-d;x=-x;y=-y}if(rs.every(r=>r.v[0]*x+r.v[1]*y<=r.c*d))vertices.push([x,y,d])}return vertices.length>0&&rs.filter(r=>r.s).every(r=>vertices.some(([x,y,d])=>r.v[0]*x+r.v[1]*y<r.c*d))}
const box=[row(-1,0,0),row(1,0,4),row(0,-1,0),row(0,1,4)],pool=[];for(const [a,b] of [[1,1],[1,-1],[-1,1],[-1,-1]])for(const c of [-2,0,2,4,6])for(const s of [false,true])pool.push(row(a,b,c,s));
let out={cases:0,wrong:0,invalidCertificate:0,zeroCertificateAccepted:0,negativeCertificateAccepted:0,withdrawChecks:0,withdrawWrong:0,limits:{}};
for(const cap of [0,4,16,1000])out.limits[cap]={yes:0,no:0,unknown:0,maxPairs:0};
for(let i=0;i<pool.length;i++)for(let j=i;j<pool.length;j++)for(let k=j;k<pool.length;k++){let rs=box.concat(pool[i],pool[j],pool[k]),truth=oracle(rs);out.cases++;for(const cap of [0,4,16,1000]){let z=solve(rs,cap),o=out.limits[cap];o[z.state===1?"yes":z.state===0?"no":"unknown"]++;o.maxPairs=Math.max(o.maxPairs,z.used);if(z.state!==-1&&Boolean(z.state)!==truth||z.used>cap||cap===1000&&z.state===-1)out.wrong++;if(z.state===0){if(!verify(rs,z.w))out.invalidCertificate++;if(verify(rs,z.w.map(()=>0n)))out.zeroCertificateAccepted++;if(verify(rs,z.w.map((x,i)=>i===0?-1n:x)))out.negativeCertificateAccepted++;if(cap===1000)for(let t=4;t<7;t++){out.withdrawChecks++;let reduced=rs.filter((_,i)=>i!==t),w=z.w.filter((_,i)=>i!==t);if(z.w[t]===0n&&!verify(reduced,w))out.withdrawWrong++;if(z.w[t]===0n&&oracle(reduced))out.withdrawWrong++}}}}
if(out.wrong||out.invalidCertificate||out.zeroCertificateAccepted||out.negativeCertificateAccepted||out.withdrawWrong)throw Error("failed");return out;
```
```json
{
  "cases": 11480,
  "wrong": 0,
  "invalidCertificate": 0,
  "zeroCertificateAccepted": 0,
  "negativeCertificateAccepted": 0,
  "withdrawChecks": 10794,
  "withdrawWrong": 0,
  "limits": {
    "0": {
      "yes": 0,
      "no": 0,
      "unknown": 11480,
      "maxPairs": 0
    },
    "4": {
      "yes": 0,
      "no": 554,
      "unknown": 10926,
      "maxPairs": 4
    },
    "16": {
      "yes": 7882,
      "no": 3598,
      "unknown": 0,
      "maxPairs": 14
    },
    "1000": {
      "yes": 7882,
      "no": 3598,
      "unknown": 0,
      "maxPairs": 14
    }
  }
}
```
