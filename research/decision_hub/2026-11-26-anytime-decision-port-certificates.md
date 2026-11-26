# 自主认知：未完成联合搜索的决策端口区间证书
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线与去重
固定main 4fa7b55a0269b2f14b3ca684bc9e0e1d475c524f，读取20近期提交、15开放Draft PR、正式v3.2、同步规程、唯一产品交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07的前段。#63仍Draft，head 734686980b19da9291bdd08b67d4e2519c011acf，未重跑。直接前序研究 joint-semantic-support-and-search-completeness.md blob d827adc15f983c9c66c4f9fb989d2d911b92a9c6 研究有限图多义务支持及截断未知；interpretation-effect-equivalence-and-ledger-boundary.md 18ae7920f9ca317da66d1d50ba7f0fc3d8951c26研究完整域只读与持久效果；adaptive-clarification-port-guarantees.md 9178ff491047925e17f88fb1ab82f843bd254285研究完整域澄清策略；v08-durable-budgeted-join-transaction.md 1367026835d896b6c1cddd5734d38624822376ed研究持久执行权、预约及原子发布。本轮专注未完成语义搜索的数值端口证书与内存分段续算，不重复SQLite事务或完整域澄清，不声称全库无重复。
## 形式合同
有限图非负整数有向边，起点0终点n，必须按组各选一个候选。候选附必经点与三个整数贡献，分别为已定义硬门余量、A相对B的效用差、A相对C的效用差。三者单位/意义由合成夹具预设，不表示统一人生分数。硬门余量>=0为真，两个严格比较差>0为真。三端口均为条件只读查询，不推出行动可执行或正式建议。效用比较不得覆盖硬门。任意高阶禁配集合及必经点预算沿用上一轮有限合同。缺失参数、未覆盖义务、非加性模型及真实资格未接入，任何现实外域仍UNKNOWN。数据全部原创合成，无训练、个人数据或第三方运行时依赖。
对前缀p，已选贡献v(p)，剩余组G。逐端口计算 L(p)=v(p)+sum_g min_{c∈g} d(c)，U(p)=v(p)+sum_g max_{c∈g} d(c)。忽略未来联合约束只扩大包络；每个真实可行后继都落在此区间。已找到的世界精确值与尚未处理的DFS前缀区间取全局最小/最大；被单调预算或禁配剪掉的子树无可行世界。由前缀覆盖和归纳，所有有限可行世界均在全局界内。存在已发现可行见证且整个包络跨不过相应阈值时可证ALL_TRUE或ALL_FALSE。见证同时存在真假时可证MIXED；未发现可行见证不得从空域或包络推出全称结论；完整搜索无世界时EMPTY。其余UNKNOWN。随着合法搜索前进，已证明状态不会反转；边界可以缩紧，搜索完整后达到真实最小最大。注意MIXED为确定存在两种结果，不是概率。若宿主的语义域覆盖、数据、资格、版本或模型发生改变，证书全部按依赖失效。证书没有授权能力。数学比较与未来账本修订仍分离。
## 实验设计及执行
连接器标准JS实际执行下列完整源码，使用固定LCG seed 20261127、4个控制、600个随机有限结构（图4至9步、2至5候选组、每组2至3项、非负整数路径成本、0至6预算、显式禁配及带符号整数贡献）；0/1/4/12/32/96累计节点预算。直接参照枚举全部路径和候选笛卡尔积，独立于最短路及剪枝实现；逐前缀检查区间包络、真假/混合/空域、无见证不得全称、证书单调、分段与单次同预算状态完全一致，完整搜索与参照世界相同。已找到世界一致即发布的故意错误基线用于反例，不代表现有v0.8生产错误。计数按案例×节点帽×端口，重复前缀不作为独立样本。早期证书指尚有未处理前缀时得到的有限条件结论；完整域真实资格需另行核实。
## 结果
```json
{
  "seed": 20261127,
  "cases": 604,
  "controls": 4,
  "worlds": 9351,
  "emptyCases": 109,
  "prefixChecks": 3624,
  "portChecks": 10872,
  "earlyCertified": 466,
  "earlyMixed": 997,
  "earlyCertifiedCases": 228,
  "unanimityFalseCertificates": 655,
  "unanimityFalseCases": 319,
  "noWitnessControls": 4995,
  "boundChecks": 8910,
  "resumeChecks": 3624,
  "nodes": 23588,
  "pruned": 5712,
  "byBudget": {
    "0": {
      "cases": 604,
      "complete": 0,
      "nonempty": 0,
      "earlyUniversalPorts": 0,
      "earlyMixedPorts": 0,
      "wrongUnanimityPorts": 0
    },
    "1": {
      "cases": 604,
      "complete": 0,
      "nonempty": 0,
      "earlyUniversalPorts": 0,
      "earlyMixedPorts": 0,
      "wrongUnanimityPorts": 0
    },
    "4": {
      "cases": 604,
      "complete": 35,
      "nonempty": 168,
      "earlyUniversalPorts": 148,
      "earlyMixedPorts": 33,
      "wrongUnanimityPorts": 242
    },
    "12": {
      "cases": 604,
      "complete": 188,
      "nonempty": 481,
      "earlyUniversalPorts": 221,
      "earlyMixedPorts": 435,
      "wrongUnanimityPorts": 315
    },
    "32": {
      "cases": 604,
      "complete": 399,
      "nonempty": 494,
      "earlyUniversalPorts": 71,
      "earlyMixedPorts": 354,
      "wrongUnanimityPorts": 92
    },
    "96": {
      "cases": 604,
      "complete": 533,
      "nonempty": 495,
      "earlyUniversalPorts": 26,
      "earlyMixedPorts": 175,
      "wrongUnanimityPorts": 6
    }
  },
  "examples": [
    {
      "case": 0,
      "cap": 12,
      "port": 0,
      "seen": true,
      "interval": [
        -2,
        4
      ],
      "actual": [
        -2,
        4
      ]
    },
    {
      "case": 0,
      "cap": 12,
      "port": 1,
      "seen": true,
      "interval": [
        -2,
        4
      ],
      "actual": [
        -2,
        4
      ]
    },
    {
      "case": 0,
      "cap": 12,
      "port": 2,
      "seen": true,
      "interval": [
        -2,
        4
      ],
      "actual": [
        -2,
        4
      ]
    }
  ]
}
```
## 资源、边界及下一责任
最短路O(nE)/O(n²)，每端口后缀界线性预计算，栈内搜索最坏指数，当前存储已找到的所有世界，未测实际设备资源、时间、内存、持久化、恶意检查点、跨端一致性或真实自然语言。此版续算仅内存中的可信对象分段推进，不是安全序列化或断电恢复。状态、源与决策参数绑定必须由宿主实施；无真实语义覆盖时不得宣称全称事实。可进一步研究同一世界的相关差值而非独立边际区间、非加性安全包络、压缩见证、受限前沿及真实原文多字段接入，独立轨保管未见语料。研究者自行选择随机参数、三端口与严格比较、节点帽。未修改生产代码或唯一交接，未启动Codex新任务、训练、合并PR、部署、主动CI、费用或冻结/证据等级变更。
## 完整可执行复算
Node标准JS，无依赖。运行输出JSON；本轮实际执行为连接器JS，未单独调用Node命令行。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)},seed=20261127;let rng=seed>>>0;const rnd=n=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%n},range=n=>Array.from({length:n},(_,i)=>i);
 const cases=[];
 // Each candidate: [id, required lattice positions, contributions to slack and two utility differences].
 const controls=[
 {g:[[[1,1],[2,0]],[[2,0]],[[3,1],[4,0]],[[4,0]],[[5,1],[6,0]],[[6,0]]],groups:range(3).map(i=>[[2*i,[2*i+1],[2,2,2]],[2*i+1,[],[-1,-1,-1]]]),forbid:[],budget:2,base:[1,1,1]},
 {g:[[[1,0]]],groups:[[[0,[],[1,1,1]],[1,[],[-2,-2,-2]]]],forbid:[],budget:0,base:[0,0,0]},
 {g:[[[1,0]]],groups:[[[0,[],[1,1,1]],[1,[],[2,2,2]]]],forbid:[[0],[1]],budget:0,base:[0,0,0]},
 {g:[[[1,0]]],groups:[[[0,[],[1,2,-2]],[1,[],[3,1,-1]]],[[2,[],[0,1,-1]],[3,[],[1,0,0]]]],forbid:[],budget:0,base:[0,0,0]}];
 cases.push(...controls);
 for(let t=0;t<600;t++){const n=4+rnd(6),g=range(n).map(i=>range(Math.min(3,n-i)).filter(j=>j===0||rnd(3)>0).map(j=>[i+j+1,rnd(5)]));let id=0;const groups=range(2+rnd(4)).map(()=>range(2+rnd(2)).map(()=>[id++,range(n-1).map(i=>i+1).filter(()=>rnd(5)===0),range(3).map(()=>rnd(9)-4)]));const forbid=range(rnd(4)).map(()=>[...new Set(range(2+rnd(3)).map(()=>rnd(id)))].sort((a,b)=>a-b));cases.push({g,groups,forbid,budget:rnd(7),base:range(3).map(()=>rnd(11)-5)})}
 const sum=(a,b)=>a.map((x,i)=>x+b[i]),threshold=[0,1,1],truth=(v,p)=>v>=threshold[p],sort=(a,b)=>a-b;
 function reference(c){const paths=[];function walk(i,cost,points){if(i===c.g.length){paths.push({cost,points});return}for(const [j,w] of c.g[i])walk(j,cost+w,[...points,j])}walk(0,0,[0]);const opt=Math.min(...paths.map(x=>x.cost)),out=[];function visit(k,ids,pts,v){if(k===c.groups.length){if(c.forbid.some(f=>f.every(x=>ids.includes(x))))return;if(paths.some(p=>p.cost<=opt+c.budget&&pts.every(x=>p.points.includes(x))))out.push({ids,v});return}for(const [id,p,d] of c.groups[k])visit(k+1,[...ids,id],[...pts,...p],sum(v,d))}visit(0,[],[],c.base);return out}
 function init(c){const n=c.g.length,d=range(n+1).map(()=>Array(n+1).fill(Infinity));for(let s=0;s<=n;s++){d[s][s]=0;for(let i=s;i<n;i++)for(const [j,w] of c.g[i])d[s][j]=Math.min(d[s][j],d[s][i]+w)}const bound=(pts)=>{const a=[...new Set([0,n,...pts])].sort(sort);return a.slice(1).reduce((z,x,i)=>z+d[a[i]][x],0)-d[0][n]};const lo=range(c.groups.length+1).map(()=>[0,0,0]),hi=range(c.groups.length+1).map(()=>[0,0,0]);for(let k=c.groups.length-1;k>=0;k--)for(let p=0;p<3;p++){lo[k][p]=lo[k+1][p]+Math.min(...c.groups[k].map(x=>x[2][p]));hi[k][p]=hi[k+1][p]+Math.max(...c.groups[k].map(x=>x[2][p]))}return {c,bound,lo,hi,front:[{k:0,ids:[],pts:[],v:c.base}],found:[],nodes:0,pruned:0}}
 function step(s,cap){for(let i=0;i<cap&&s.front.length;i++){const a=s.front.pop();s.nodes++;if(s.bound(a.pts)>s.c.budget||s.c.forbid.some(f=>f.every(x=>a.ids.includes(x)))){s.pruned++;continue}if(a.k===s.c.groups.length){s.found.push({ids:a.ids,v:a.v});continue}for(const [id,p,d] of [...s.c.groups[a.k]].reverse())s.front.push({k:a.k+1,ids:[...a.ids,id],pts:[...new Set([...a.pts,...p])].sort(sort),v:sum(a.v,d)})}}
 function cert(s){const complete=!s.front.length,possible=s.found.length>0;const port=range(3).map(p=>{const vals=s.found.map(x=>x.v[p]),l=[...vals,...s.front.map(x=>x.v[p]+s.lo[x.k][p])],u=[...vals,...s.front.map(x=>x.v[p]+s.hi[x.k][p])];const low=l.length?Math.min(...l):null,high=u.length?Math.max(...u):null;let status="UNKNOWN";if(complete&&!possible)status="EMPTY";else if(possible){if(truth(low,p))status="ALL_TRUE";else if(!truth(high,p))status="ALL_FALSE";else if(vals.some(v=>truth(v,p))&&vals.some(v=>!truth(v,p)))status="MIXED"}return {low,high,status}});return {complete,possible,port,authority:"NONE"}}
 const out={seed,cases:cases.length,controls:controls.length,worlds:0,emptyCases:0,prefixChecks:0,portChecks:0,earlyCertified:0,earlyMixed:0,earlyCertifiedCases:0,unanimityFalseCertificates:0,unanimityFalseCases:0,noWitnessControls:0,boundChecks:0,resumeChecks:0,nodes:0,pruned:0,byBudget:{},examples:[]};
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),caps=[0,1,4,12,32,96];for(let i=0;i<cases.length;i++){const c=cases[i],oracle=reference(c),s=init(c);out.worlds+=oracle.length;out.emptyCases+=!oracle.length;let early=false,wrong=false,previous=0,prevCert=null;for(const cap of caps){step(s,cap-previous);previous=cap;let q=cert(s);const b=out.byBudget[cap]??={cases:0,complete:0,nonempty:0,earlyUniversalPorts:0,earlyMixedPorts:0,wrongUnanimityPorts:0};b.cases++;b.complete+=q.complete;b.nonempty+=q.possible;out.prefixChecks++;check(q.authority==="NONE","authority");check(!q.possible||oracle.length>0,"witness");for(let p=0;p<3;p++){out.portChecks++;const v=oracle.map(x=>x.v[p]),z=q.port[p],yes=v.some(x=>truth(x,p)),no=v.some(x=>!truth(x,p));if(v.length){check(z.low!==null&&z.low<=Math.min(...v)&&z.high>=Math.max(...v),"bound");out.boundChecks++}if(z.status==="ALL_TRUE")check(yes&&!no,"true");if(z.status==="ALL_FALSE")check(no&&!yes,"false");if(z.status==="MIXED")check(yes&&no,"mixed");if(z.status==="EMPTY")check(!v.length&&q.complete,"empty");if(!q.possible&&!q.complete){check(z.status==="UNKNOWN","vacuous");out.noWitnessControls++}if(q.complete)check(z.status===(!v.length?"EMPTY":yes&&no?"MIXED":yes?"ALL_TRUE":"ALL_FALSE"),"complete");if(prevCert&&prevCert.port[p].status!=="UNKNOWN")check(z.status===prevCert.port[p].status,"certificate changed");if(!q.complete){if(z.status==="ALL_TRUE"||z.status==="ALL_FALSE"){out.earlyCertified++;b.earlyUniversalPorts++;early=true}if(z.status==="MIXED"){out.earlyMixed++;b.earlyMixedPorts++}const seen=s.found.map(x=>truth(x.v[p],p));if(seen.length&&seen.every(x=>x===seen[0])&&(seen[0]?no:yes)){out.unanimityFalseCertificates++;b.wrongUnanimityPorts++;wrong=true;if(out.examples.length<3)out.examples.push({case:i,cap,port:p,seen:seen[0],interval:[z.low,z.high],actual:[Math.min(...v),Math.max(...v)]})}}}prevCert=q;const fresh=init(c);step(fresh,cap);check(eq(cert(fresh),q)&&eq(fresh.front,s.front)&&eq(fresh.found,s.found),"resume");out.resumeChecks++}
 step(s,1000000);check(!s.front.length&&eq(s.found,oracle),"oracle worlds");const q=cert(s);for(let p=0;p<3;p++){const v=oracle.map(x=>x.v[p]);check(v.length? q.port[p].low===Math.min(...v)&&q.port[p].high===Math.max(...v):q.port[p].status==="EMPTY","final exact")}out.earlyCertifiedCases+=early;out.unanimityFalseCases+=wrong;out.nodes+=s.nodes;out.pruned+=s.pruned}
 return out
}
console.log(JSON.stringify(experiment(),null,2));
```
