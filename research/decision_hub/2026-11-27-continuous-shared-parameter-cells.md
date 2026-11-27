# 连续共享参数的精确端点划分与撤回单调性
2026-11-27，RESEARCH_CANDIDATE / FINITE_SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
基线 3dd1c45feb6db07d462adb4312da176d3bce76ca，写前同HEAD，目标404。读取最近20提交、开放PR和上一轮预算搜索全文；v3.2、同步规程及唯一交接沿用紧邻上一轮已读版本，本轮未重新读取，局部去重。新增单连续参数的精确分区，不重复离散故障搜索。
数学：有界实数t，合格观察为闭区间[l,u]（可由单变量非零线性不等式换算，负系数翻转方向；本代码仅接受已换算的整数端点），每条观察单根，允许共享根。硬门t≤H。将所有区间端点、域端点、H排序去重；每个端点单独作为点单元，相邻端点间为开区间单元。所有观察和硬门在每单元内恒定，任意内部代表点足以判定；端点不能合并进开区间。对每单元计数不同不符根，≤k则保留。条件门在非空可行域恒真或恒假才确定，空域冲突。所有结论依赖来源资格、预算、候选覆盖，authority NONE。独立计算参照为枚举故障根集合，对未故障观察求区间交集并直接检查硬门两侧是否存在。撤回观察仅移除约束，因此固定域、预算和根身份下可行域只能扩大；原确定结论可能失效。生产应绑定版本及重新验证，当前仅全量重算，未实现增量缓存或证书。
实验：域[0,12]，15个闭区间，3观察、2根，第三观察根可选，预算0/1，5个硬门阈值。对照固定网格0/4/8/12。所有参数研究者选定，合成配置非独立样本。整数端点和半整数中点在本范围JS精确表示，任意实数输入需有理数或可靠区间算术；未验证多维、严格输入不等式、无界域、多路径派生、设备资源、真实语言、独立验收。未训练、合并、部署或主动CI，零新增费用。下一责任模型轨扩展有理数与多维，独立轨留出，数据轨来源资格。冻结及交接不变。
复算（放入函数内执行并打印返回值）：
```js
function solve(rows,k,hard){
 const cuts=[0,12,...rows.flatMap(r=>[r.l,r.u]),hard].filter(x=>x>=0&&x<=12).sort((a,b)=>a-b);
 const p=[...new Set(cuts)], cells=p.flatMap((x,i)=>i+1<p.length?[[x,x],[x,p[i+1]]]:[[x,x]]);
 const pc=x=>((x&1)>0)+((x&2)>0);
 return cells.filter(([a,b])=>{const t=(a+b)/2;let f=0;for(const r of rows)if(t<r.l||t>r.u)f|=r.root;return pc(f)<=k}).map(([a,b])=>({a,b,point:a===b,pass:(a+b)/2<=hard}));
}
function oracle(rows,k,hard){
 let yes=false,no=false;
 for(let f=0;f<4;f++){if(((f&1)>0)+((f&2)>0)>k)continue;
 let l=0,u=12;for(const r of rows)if(!(r.root&f)){l=Math.max(l,r.l);u=Math.min(u,r.u)}
 if(l<=u){yes ||= l<=hard;no ||= u>hard}}
 return [yes,no];
}
const state=c=>[c.some(x=>x.pass),c.some(x=>!x.pass)];
const eq=(a,b)=>String(a)===String(b);
const I=[];for(let l=0;l<=12;l+=3)for(let u=l;u<=12;u+=3)I.push([l,u]);
let out={cases:0,mismatch:0,gridMiss:0,gridWrongGate:0,withdrawChecks:0,withdrawWrong:0,pointOnly:0};
for(const a of I)for(const b of I)for(const c of I)for(const root of [1,2])for(let k=0;k<=1;k++)for(let hard=0;hard<=12;hard+=3){
 const rows=[{l:a[0],u:a[1],root:1},{l:b[0],u:b[1],root:2},{l:c[0],u:c[1],root}];
 const cells=solve(rows,k,hard),s=state(cells),o=oracle(rows,k,hard);out.cases++;if(!eq(s,o))out.mismatch++;
 const grid=[0,4,8,12].filter(t=>{let f=0;for(const r of rows)if(t<r.l||t>r.u)f|=r.root;return ((f&1)>0)+((f&2)>0)<=k});
 const g=[grid.some(t=>t<=hard),grid.some(t=>t>hard)];if(cells.length&&!grid.length)out.gridMiss++;if(g[0]!==g[1]&&s[0]&&s[1])out.gridWrongGate++;
 if(cells.length&&cells.every(x=>x.point))out.pointOnly++;
 for(let i=0;i<3;i++){let w=state(solve(rows.filter((_,j)=>i!==j),k,hard));out.withdrawChecks++;if(s.some((v,j)=>v&&!w[j]))out.withdrawWrong++}
}
if(out.mismatch||out.withdrawWrong)throw Error("failed");return out;
```
```json
{
  "cases": 67500,
  "mismatch": 0,
  "gridMiss": 12900,
  "gridWrongGate": 5376,
  "withdrawChecks": 202500,
  "withdrawWrong": 0,
  "pointOnly": 17760
}
```
