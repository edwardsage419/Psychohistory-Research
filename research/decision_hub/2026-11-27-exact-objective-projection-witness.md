# 精确目标投影、可行见证与机会成本上界
2026-11-27。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
基线 53530a48a5c6664de9349944310a38a84ab3f7ac，写前HEAD一致，目标404。核查最近20提交、开放PR、上一轮证书全文、正式规程与同步规程及唯一交接（工具获取全文，输出末2500字符）。局部去重。经典线性消元直接推导，未核对原论文。
在二维有界线性域加入目标变量 t=ax+by，以两条非严格不等式表达等式。消去x,y得到精确目标区间；上端闭合则最大值可达，开放则仅上确界。取闭上端或区间中点，逆序代入消元阶段并取剩余变量区间中点，生成精确有理可行见证。BigInt交叉乘法，分母正，不约分。若上端开放，可取任意内部目标值趋近上界；本实现仅取中点，不声称近似最优。固定有界域保证各逆代区间有界。参照：闭包顶点枚举，严格行各有松弛顶点则其平均可行；在最优面重复松弛检查判断可达性。新增约束后上确界不得增加，差额是同一已确认线性目标下的上确界机会成本，不能当作实际收益差或跨目标总分。目标权重须用户确认；本实验研究者选定，authority NONE。
实验：[0,4]^2，40条观察，两条可重复组合，4种目标，追加x≥2检查上确界单调性。精确验证原约束、目标等式和可达性。合成配置非独立样本。未实现预算中断、证书绑定、任意维数、无界域、故障世界稳健优化、实际机会成本数据、原生入口、真机及独立留出。无训练、主动CI、合并、部署或新增费用。下一责任模型轨研究预算下上下界及稳健多情景，独立轨留出，产品轨目标确认。冻结与交接不变。
复算（置于函数内执行并打印返回值）：
```js
const R=(a,b,c,s=false)=>({v:[BigInt(a),BigInt(b)],c:BigInt(c),s});
const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
const add=(a,b)=>[a[0]*b[1]+b[0]*a[1],a[1]*b[1]];
const mid=(a,b)=>{let z=add(a,b);return [z[0],2n*z[1]]};
function eliminate(z){let p=z.filter(r=>r.v[0]>0n),n=z.filter(r=>r.v[0]<0n),q=z.filter(r=>r.v[0]===0n).map(r=>({...r,v:r.v.slice(1)}));for(const a of p)for(const b of n){let u=-b.v[0],v=a.v[0];q.push({v:a.v.slice(1).map((x,i)=>u*x+v*b.v[i+1]),c:u*a.c+v*b.c,s:a.s||b.s})}return q}
function bounds(z){let l=null,u=null,ls=false,us=false;for(const r of z){let a=r.v[0];if(!a){if(r.c<0n||r.c===0n&&r.s)return null;continue}let t=a>0n?[r.c,a]:[-r.c,-a];if(a>0n){if(!u||cmp(t,u)<0n){u=t;us=r.s}else if(cmp(t,u)===0n)us ||= r.s}else{if(!l||cmp(t,l)>0n){l=t;ls=r.s}else if(cmp(t,l)===0n)ls ||= r.s}}if(l&&u&&(cmp(l,u)>0n||cmp(l,u)===0n&&(ls||us)))return null;return {l,u,ls,us}}
function optimize(rs,a,b){let z=rs.map(r=>({...r,v:[...r.v,0n]}));z.push({v:[a,b,-1n],c:0n,s:false},{v:[-a,-b,1n],c:0n,s:false});let y=eliminate(z),t=eliminate(y),B=bounds(t);if(!B)return null;let value=B.us?mid(B.l,B.u):B.u;
function fix(rows,q){return rows.map(r=>({v:r.v.slice(0,-1).map(x=>x*q[1]),c:r.c*q[1]-r.v[r.v.length-1]*q[0],s:r.s}))}
let Y=bounds(fix(y,value)),yv=mid(Y.l,Y.u),X=bounds(fix(fix(z,value),yv)),xv=mid(X.l,X.u);return {upper:B.u,attained:!B.us,value,xv,yv}}
function oracle(rs,a,b){let V=[];for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){let [p,q]=[rs[i],rs[j]],d=p.v[0]*q.v[1]-q.v[0]*p.v[1];if(!d)continue;let x=p.c*q.v[1]-q.c*p.v[1],y=p.v[0]*q.c-q.v[0]*p.c;if(d<0n){d=-d;x=-x;y=-y}if(rs.every(r=>r.v[0]*x+r.v[1]*y<=r.c*d))V.push({x,y,d,t:[a*x+b*y,d]})}const ok=W=>W.length&&rs.filter(r=>r.s).every(r=>W.some(v=>r.v[0]*v.x+r.v[1]*v.y<r.c*v.d));if(!ok(V))return null;let u=V.reduce((m,v)=>cmp(v.t,m)>0n?v.t:m,V[0].t);return {upper:u,attained:!!ok(V.filter(v=>cmp(v.t,u)===0n))}}
const box=[R(-1,0,0),R(1,0,4),R(0,-1,0),R(0,1,4)],pool=[];for(const [a,b] of [[1,1],[1,-1],[-1,1],[-1,-1]])for(const c of [-2,0,2,4,6])for(const s of [false,true])pool.push(R(a,b,c,s));
let out={cases:0,wrong:0,witnessWrong:0,attained:0,unattained:0,infeasible:0,opportunityChecks:0,opportunityWrong:0};
for(let i=0;i<pool.length;i++)for(let j=i;j<pool.length;j++)for(const [a,b] of [[1n,1n],[2n,1n],[-1n,2n],[0n,0n]]){let rs=box.concat(pool[i],pool[j]),z=optimize(rs,a,b),o=oracle(rs,a,b);out.cases++;if(!z!==!o||z&& (cmp(z.upper,o.upper)!==0n||z.attained!==o.attained))out.wrong++;if(!z){out.infeasible++;continue}out[z.attained?"attained":"unattained"]++;let [x,xd]=z.xv,[y,yd]=z.yv;if(rs.some(r=>{let v=r.v[0]*x*yd+r.v[1]*y*xd-r.c*xd*yd;return v>0n||v===0n&&r.s})||cmp([a*x*yd+b*y*xd,xd*yd],z.value)!==0n||z.attained&&cmp(z.value,z.upper)!==0n)out.witnessWrong++;let restricted=optimize(rs.concat(R(-1,0,-2)),a,b);if(restricted){out.opportunityChecks++;if(cmp(restricted.upper,z.upper)>0n)out.opportunityWrong++}}
if(out.wrong||out.witnessWrong||out.opportunityWrong)throw Error("failed");return out;
```
```json
{
  "cases": 3280,
  "wrong": 0,
  "witnessWrong": 0,
  "attained": 2083,
  "unattained": 573,
  "infeasible": 624,
  "opportunityChecks": 2272,
  "opportunityWrong": 0
}
```
