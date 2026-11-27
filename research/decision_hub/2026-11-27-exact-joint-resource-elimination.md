# 精确多维共享资源消元与严格边界
2026-11-27。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
基线 5c67315da29182ea449d07edb2ba23297953ede6，写前HEAD一致，目标404。读取最近20提交、开放PR、上一轮连续区间全文、v3.2 blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85、同步规程 blob 26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接末5000字符 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。局部去重。新增二维线性约束及严格边界，不重复单变量区间。
方法：经典 Fourier–Motzkin 消元的直接数学推导，未核对历史原论文。每个约束为 a·x≤c 或严格小于。消去变量时将正系数行与负系数行按正倍数相加抵消变量，严格标志取逻辑或；零系数行直接保留。正负行分别对应上界和下界，每对相容等价于存在共同实数；任一侧为空则可取足够大或小的实数。最终常数行需满足0≤c或0<c。BigInt整数系数避免浮点误差；有理系数可正分母清除但本实现未提供输入转换。二维固定有界域。参照算法独立于消元：枚举闭包多边形顶点，以整数交叉乘法核查；非空有界闭多面体存在顶点，若每个严格行各有至少一个松弛顶点，则这些顶点的平均满足所有严格行，反之不可能。此参照不适用于无界域。故障预算枚举两根，第一第三观察共享根，删除故障根全部观察，可信域和硬门不可删除。分别测试硬门及其严格补集存在性；仅一侧存在才有条件确定结论，两侧均空冲突，两侧均有未知。authority NONE；证据资格、预算、语义和域覆盖须外部确认。
实验：研究者选定[0,4]^2、60条候选观察，三条允许重复的组合，硬门x+y≤4及补集，预算0/1。计数为合成配置非独立样本。sharedConflict为各观察单独可行但联合不可行；strictBoundaryLoss为忽略严格性后错误保留的配置。未测试多路径充分派生、任意维数、原生语言、真实设备、独立留出、真实效果。消元可能组合爆炸，尚无资源预算、证书或增量重算，生产须限制行数和位长并保留UNKNOWN。无训练、主动CI、PR合并、部署或新增费用。下一责任模型轨研究有界消元与证书，数据轨来源资格，独立轨留出。冻结与交接不变。
复算：以下代码置于函数内执行并打印返回值。
```js
const row=(a,b,c,s=false)=>({a:BigInt(a),b:BigInt(b),c:BigInt(c),s});
function feasible(rs){
 let z=rs.map(r=>({v:[r.a,r.b],c:r.c,s:r.s}));
 for(let j=0;j<2;j++){
 let p=z.filter(r=>r.v[0]>0n),n=z.filter(r=>r.v[0]<0n),q=z.filter(r=>r.v[0]===0n).map(r=>({...r,v:r.v.slice(1)}));
 for(const a of p)for(const b of n){let u=-b.v[0],v=a.v[0];q.push({v:a.v.slice(1).map((x,i)=>u*x+v*b.v[i+1]),c:u*a.c+v*b.c,s:a.s||b.s})}z=q;
 }return z.every(r=>r.c>0n||(r.c===0n&&!r.s));
}
const box=[row(-1,0,0),row(1,0,4),row(0,-1,0),row(0,1,4)];
// Independent geometric reference: closure vertices, strict rows must each have a positive slack at some vertex. Their average satisfies all strict rows.
function oracle(rs){
 let vertices=[];
 for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){
 let a=rs[i],b=rs[j],d=a.a*b.b-b.a*a.b;if(!d)continue;
 let x=a.c*b.b-b.c*a.b,y=a.a*b.c-b.a*a.c;if(d<0n){d=-d;x=-x;y=-y}
 if(rs.every(r=>r.a*x+r.b*y<=r.c*d))vertices.push([x,y,d]);
 }return vertices.length>0&&rs.filter(r=>r.s).every(r=>vertices.some(([x,y,d])=>r.a*x+r.b*y<r.c*d));
}
const pool=[];for(const [a,b] of [[1,1],[1,-1],[-1,1],[-1,-1],[1,0],[0,1]])for(const c of [-2,0,2,4,6])for(const s of [false,true])pool.push(row(a,b,c,s));
let out={cases:0,wrong:0,feasible:0,strictBoundaryLoss:0,sharedConflict:0,faultCases:0,faultWrong:0,gateWrong:0};
for(let i=0;i<pool.length;i++)for(let j=i;j<pool.length;j++)for(let k=j;k<pool.length;k++){
 let obs=[pool[i],pool[j],pool[k]],rs=box.concat(obs),a=feasible(rs),b=oracle(rs);out.cases++;out.wrong+=Number(a!==b);out.feasible+=Number(a);if(!a&&feasible(rs.map(r=>({...r,s:false}))))out.strictBoundaryLoss++;
 if(!a&&obs.every(r=>feasible(box.concat(r))))out.sharedConflict++;
 // first and third observations share source root; second has independent root.
 for(let budget=0;budget<=1;budget++){
 let masks=[0,1,2].filter(f=>!f||budget),roots=[1,2,1];
 for(const gate of [row(1,1,4),row(-1,-1,-4,true)]){
 let A=masks.some(f=>feasible(box.concat(obs.filter((_,i)=>!(roots[i]&f)),gate))),B=masks.some(f=>oracle(box.concat(obs.filter((_,i)=>!(roots[i]&f)),gate)));out.faultCases++;out.faultWrong+=Number(A!==B);
 }}
}
if(out.wrong||out.faultWrong)throw Error("mismatch");return out;
```
```json
{
  "cases": 37820,
  "wrong": 0,
  "feasible": 21096,
  "strictBoundaryLoss": 5016,
  "sharedConflict": 2330,
  "faultCases": 151280,
  "faultWrong": 0,
  "gateWrong": 0
}
```
