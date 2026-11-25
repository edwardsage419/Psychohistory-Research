# 自主认知专项累计第96轮候选：二维共享资源可行域、严格线性消元及联合决策

2026-11-25。RESEARCH_CANDIDATE / EXACT_TWO_VARIABLE_ELIMINATION_EXECUTED / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main d452a4f1c3605a3e95fb7601569a2096b64bed42。核对近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R95首19行、R63首18行。区别于R63矩形域、R94相关解释中的独立区间、R95单共享变量：本轮实际执行二维线性相关域中的联合真值可行性消元，不重复原生C028实验。未调用原生源码、注册表或API，不宣称原生支持二维依赖。无外部资料，基础傅里叶莫茨金消元和线排列不是原创定理。

## 合同与推导
人工夹具：两个共享连续量x,y∈[0,4]，三域为方形、附加x+y≤5、附加x+y=4。可视为同口径资源分配或两期共用额度的抽象例子，不等于真实资金和时间可以直接相加；若异单位必须先有经确认的系数及资源约束。本轮不模拟动态状态、跨期贴现、概率或真实用户。四个硬约束原子分别选5种仿射不等式，A、B各需两个原子成立；两种语义解释为全非严格或第1/4原子严格。B>A为人工固定序位。无候选域概率，不把可行掩码比例当现实概率。给定闭合有限解释及可信资源域才可做条件计算，资格/覆盖由人工布尔给定。每原子真值掩码的可达性由原域、真原子和假原子的严格互补约束求可行性；a*x+b*y≤c的否定为-a*x-b*y<-c，严格原子的否定则非严格。先消y再消x：将正负系数行按正倍数相加消元，若任一原行严格则新行严格。零系数行保留；一侧无界时无对应配对。有限线性约束的上/下界相容性保证投影充要（严格端点相等时排除）；最终常数行0≤c或0<c判断。BigInt全程精确，不用浮点投影。16掩码逐一判断；独立参照由所有边界直线交点和垂直线生成x切分，临界值与开区间中点，再按该x处所有y边界采样；直线顺序在各开x区间保持，覆盖域内全部真值组合，包括等式低维域。参照同研究者编写，非独立科学验收。仅有限二维夹具验证，不主张高维消元的资源可承受；行数可能乘积增长。预算仅计消元行与配对、最终检查，不是设备内存时间或完整请求资源；超限无掩码输出，缺覆盖UNKNOWN，空域CONFLICT，authority NONE，outside true。无真实语义解析、知识资格、写入或实际决策权限。

## 实验
5^4原子组合×3资源域×2严格解释=3750世界，逐一核对16原子掩码的完整集合及方案可行掩码；每组合域的两个解释取3种非空子集，共5625联合解释域、22500端口。独立原子基线分别取各原子可能真假再自由组合，矩形外包基线忽略共享资源域约束但保留同变量原子关系（精确在方形上计算），均为人为对照，非C028实际行为或产品错误率。端口为A/B可行状态、完整联合掩码、固定序位可能优选；稳定仅指给定域内单元素，不代表实际用户推荐。6预算与6覆盖检查、6严格边界控制及11总控制。无真实设备、真人、独立留出、训练、Codex、CI、生产修改、合并PR、部署、费用或冻结协议变更。形式、域、语义解释、偏好与预算均研究者选定。保留既有完整版本范围及正式验收门。

## 复算
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)},row=(a,b,c,s=false)=>({a:BigInt(a),b:BigInt(b),c:BigInt(c),s}),neg=q=>({a:-q.a,b:-q.b,c:-q.c,s:!q.s});
 // a*x+b*y <= c, s=true means strict.
 const box=[row(-1,0,0),row(1,0,4),row(0,-1,0),row(0,1,4)];
 const domains=[box,[...box,row(1,1,5)],[...box,row(1,1,4),row(-1,-1,-4)]];
 const forms=[[1,0,2],[0,1,2],[1,1,4],[-1,1,0],[1,-1,0]];
 function elim(rows,key,tick){
  let p=[],n=[],z=[];for(let q of rows){tick();(q[key]>0n?p:q[key]<0n?n:z).push(q)}
  for(let u of p)for(let v of n){tick();let x=-v[key],y=u[key];z.push({a:x*u.a+y*v.a,b:x*u.b+y*v.b,c:x*u.c+y*v.c,s:u.s||v.s})}return z
 }
 function feasible(rows,tick){let v=elim(elim(rows,"b",tick),"a",tick);return v.every(q=>{tick();return q.c>0n||q.c===0n&&!q.s})}
 function solve(D,A,covered=true,cap=100000){
  if(!covered)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  let used=0,tick=()=>{if(used>=cap)throw Error("LIMIT");used++};
  try{if(!feasible(D,tick))return {status:"CONFLICT",authority:"NONE",used};
   let masks=[];for(let i=0;i<16;i++)if(feasible(D.concat(A.map((a,j)=>i&(1<<j)?a:neg(a))),tick))masks.push(i);
   return {status:"EXACT_CONDITIONAL",authority:"NONE",outside:true,masks,used}
  }catch(e){if(e.message!=="LIMIT")throw e;return {status:"LIMIT",authority:"NONE",used}}
 }
 // Independent arrangement sweep: critical x from every pair of lines or
 // vertical line; test critical x and open slab midpoint, then y cuts/midpoints.
 const F=(n,d=1n)=>d<0n?[-n,-d]:[n,d],cmp=(a,b)=>a[0]*b[1]<b[0]*a[1]?-1:a[0]*b[1]>b[0]*a[1]?1:0;
 const mid=(a,b)=>F(a[0]*b[1]+b[0]*a[1],2n*a[1]*b[1]);
 function samples(a){let v=a.sort(cmp).filter((x,i,s)=>!i||cmp(x,s[i-1])!==0);return v.concat(v.slice(1).map((x,i)=>mid(v[i],x)))}
 function truth(q,x,y){let a=q.a*x[0]*y[1]+q.b*y[0]*x[1],b=q.c*x[1]*y[1];return q.s?a<b:a<=b}
 function sweep(D,A){
  let lines=D.concat(A),X=[F(0n),F(4n)],masks=new Set(),points=0;
  for(let q of lines)if(!q.b&&q.a)X.push(F(q.c,q.a));
  for(let i=0;i<lines.length;i++)for(let j=i+1;j<lines.length;j++){
   let u=lines[i],v=lines[j],d=u.a*v.b-v.a*u.b;if(d)X.push(F(u.c*v.b-v.c*u.b,d))
  }
  for(let x of samples(X.filter(x=>cmp(x,F(0n))>=0&&cmp(x,F(4n))<=0))){
   let Y=[F(0n),F(4n)];for(let q of lines)if(q.b)Y.push(F(q.c*x[1]-q.a*x[0],q.b*x[1]));
   for(let y of samples(Y.filter(y=>cmp(y,F(0n))>=0&&cmp(y,F(4n))<=0))){
    points++;if(D.every(q=>truth(q,x,y)))masks.add(A.reduce((m,q,i)=>m|(truth(q,x,y)?1<<i:0),0))
   }
  }return {masks:[...masks].sort((a,b)=>a-b),points}
 }
 const same=(a,b)=>a.length===b.length&&a.every((x,i)=>x===b[i]),option=m=>((m&3)===3?1:0)+((m&12)===12?2:0),uniq=a=>[...new Set(a)].sort(),pref=m=>m&2?"B":m&1?"A":"NONE",ports=m=>[uniq(m.map(x=>x&1)),uniq(m.map(x=>x>>1)),uniq(m),uniq(m.map(pref))];
 let out={worlds:0,truthChecks:0,optionChecks:0,oraclePoints:0,maxWork:0,extraIndependentAtoms:0,extraIndependentOptions:0,extraIndependentPreferred:0,extraRectangleOptions:0,extraRectanglePreferred:0,rectangleLostStablePorts:0,rectangleWrongCertain:0,domains:0,ports:0,stablePorts:0,unionExtraOptions:0,unionExtraPreferred:0,budgetChecks:0,coverageChecks:0,strictBoundaryControls:0,controls:0,witnesses:{},byDomain:[{worlds:0,extraRect:0},{worlds:0,extraRect:0},{worlds:0,extraRect:0}]};
 for(let a of forms)for(let b of forms)for(let c of forms)for(let d of forms){
  let fs=[a,b,c,d], cached=[];
  for(let s of [false,true]){let A=fs.map((f,i)=>row(...f,s&&(i===0||i===3)));cached.push({A,rect:sweep(box,A).masks})}
  for(let k=0;k<3;k++){
   let worlds=[],rects=[];
   for(let {A,rect} of cached){let D=domains[k],v=solve(D,A),o=sweep(D,A);ck(v.status==="EXACT_CONDITIONAL"&&same(v.masks,o.masks),"exact");out.worlds++;out.truthChecks+=16;out.oraclePoints+=o.points;out.maxWork=Math.max(out.maxWork,v.used);out.byDomain[k].worlds++;
    let m=uniq(v.masks.map(option)),g=uniq(o.masks.map(option)),outer=uniq(rect.map(option));ck(same(m,g),"options");out.optionChecks++;ck(m.every(x=>outer.includes(x)),"outer");
    let independent=Array.from({length:16},(_,i)=>i).filter(i=>A.every((_,j)=>v.masks.some(t=>(t&(1<<j))===(i&(1<<j))))),ip=uniq(independent.map(option));ck(v.masks.every(x=>independent.includes(x)),"atom outer");
    out.extraIndependentAtoms+=+!same(independent,v.masks);out.extraIndependentOptions+=+!same(ip,m);out.extraIndependentPreferred+=+!same(uniq(ip.map(pref)),uniq(m.map(pref)));
    if(!same(m,outer)){out.extraRectangleOptions++;out.byDomain[k].extraRect++;out.witnesses.rectangle??={domain:k,forms:fs,strict:A.map(q=>q.s),exact:m,outer}}
    out.extraRectanglePreferred+=+!same(uniq(m.map(pref)),uniq(outer.map(pref)));
    let p=ports(m),q=ports(outer);for(let i=0;i<4;i++){ck(p[i].every(x=>q[i].includes(x)),"port outer");out.rectangleLostStablePorts+=+(p[i].length===1&&q[i].length>1);out.rectangleWrongCertain+=+(q[i].length===1&&!same(p[i],q[i]))}
    worlds.push(m);rects.push(outer)
   }
   for(let i=1;i<4;i++){let m=uniq(worlds.flatMap((x,j)=>i&(1<<j)?x:[])),q=uniq(rects.flatMap((x,j)=>i&(1<<j)?x:[]));out.domains++;out.unionExtraOptions+=+!same(m,q);out.unionExtraPreferred+=+!same(uniq(m.map(pref)),uniq(q.map(pref)));for(let p of ports(m)){out.ports++;out.stablePorts+=+(p.length===1)}}
  }
 }
 for(let D of domains)for(let s of [false,true]){let A=forms.slice(0,4).map(f=>row(...f,s)),v=solve(D,A);ck(solve(D,A,false).status==="UNKNOWN_COVERAGE","coverage");out.coverageChecks++;let t=solve(D,A,true,v.used-1);ck(t.status==="LIMIT"&&!Object.hasOwn(t,"masks")&&same(solve(D,A,true,v.used).masks,v.masks),"budget");out.budgetChecks++}
 let tick=()=>{};for(let [D,ok] of [[[row(1,0,0,true),row(-1,0,0)],false],[[row(1,0,0),row(-1,0,0)],true],[[row(0,0,0,true)],false],[[row(0,0,0)],true],[[row(1,1,4,true),row(-1,-1,-4)],false],[[row(1,1,4),row(-1,-1,-4)],true]]){ck(feasible(D,tick)===ok,"strict");out.strictBoundaryControls++}
 for(let t of [()=>out.worlds===3750,()=>out.truthChecks===60000,()=>out.optionChecks===3750,()=>out.domains===5625,()=>out.ports===22500,()=>out.byDomain[0].extraRect===0,()=>out.extraRectangleOptions>0,()=>out.rectangleWrongCertain===0,()=>out.budgetChecks===6&&out.coverageChecks===6,()=>solve([...box,row(1,1,-1)],forms.slice(0,4).map(f=>row(...f))).status==="CONFLICT",()=>out.strictBoundaryControls===6]){ck(t(),"control");out.controls++}
 return out;
}
console.log(experiment())
```

## 实测
```json
{
  "worlds": 3750,
  "truthChecks": 60000,
  "optionChecks": 3750,
  "oraclePoints": 163046,
  "maxWork": 1486,
  "extraIndependentAtoms": 3716,
  "extraIndependentOptions": 2348,
  "extraIndependentPreferred": 1588,
  "extraRectangleOptions": 990,
  "extraRectanglePreferred": 788,
  "rectangleLostStablePorts": 956,
  "rectangleWrongCertain": 0,
  "domains": 5625,
  "ports": 22500,
  "stablePorts": 1280,
  "unionExtraOptions": 1312,
  "unionExtraPreferred": 984,
  "budgetChecks": 6,
  "coverageChecks": 6,
  "strictBoundaryControls": 6,
  "controls": 11,
  "witnesses": {
    "rectangle": {
      "domain": 2,
      "forms": [
        [
          1,
          0,
          2
        ],
        [
          1,
          0,
          2
        ],
        [
          1,
          0,
          2
        ],
        [
          0,
          1,
          2
        ]
      ],
      "strict": [
        true,
        false,
        false,
        true
      ],
      "exact": [
        0,
        1
      ],
      "outer": [
        0,
        1,
        2,
        3
      ]
    }
  },
  "byDomain": [
    {
      "worlds": 1250,
      "extraRect": 0
    },
    {
      "worlds": 1250,
      "extraRect": 0
    },
    {
      "worlds": 1250,
      "extraRect": 990
    }
  ]
}
```

## 下一步
将经证据确认的资源变量身份、单位系数、跨期资源状态与现有数学方法接口整合；先验证真实原文义务和覆盖，再考虑实际长期动态规划。独立轨负责未见样本，数据轨负责合法真实来源，产品轨维护唯一交接。正式工程及训练另获授权。
