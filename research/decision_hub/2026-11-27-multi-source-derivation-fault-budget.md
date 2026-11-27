# 自主认知：多来源派生的联合故障预算与条件硬门
2026-11-27。RESEARCH_CANDIDATE / FINITE_SYNTHETIC_EXHAUSTIVE_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线与去重
起点及写前main 5dd9170ec4e5433f30d6cb39eb976367a2016370；目标新文件写前404。核对25近期提交、开放PR列表、v3.2全文、同步规程全文、产品唯一交接 research/coordination/DECISION_WORKBENCH_PRODUCT_PRIVACY_HANDOFF_2026-11-19.md（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07，末9500字符）。PR #63作者描述候选head 734686980b19da9291bdd08b67d4e2519c011acf，公开开发集正确数值单位7/23、条件0/5、他人主体1/4、修订链0/10；未复跑工程。阅读上一轮 research/decision_hub/2026-11-27-source-group-robust-quantity-disambiguation.md 全文及 provenance、hitting 提交搜索；局部查重而非全库证明。新增多来源派生故障集合，直接补上一轮明确未实现的多源派生问题。不重复单根分组、语义候选生成、账本执行、来源鉴别或独立语言验收。原创有限推导，无外部论文、数据或模型依赖。

## 条件合同与推导
令每项外部合格观察r具有至少一个非空的充分派生路径P（根集合），且每条路径内所有根均正确时，路径能够保证该观察谓词为真。多个路径是替代性充分依据；不是把多个引用合并成一个证据，也不假定统计独立。路径资格须包括变换本身、单位、时间、主体、来源版本及适用条件。未知来源、变换或覆盖不可由本算法自行认证；相应条件门UNKNOWN，不允许写入账本。由候选自身计算出的数字不能反过来支持候选。真实故障根集合F未知，预设上界e不是概率。用户已确认硬底线不参加错误容忍。

对于候选世界h，将所有不符合观察的r的全部充分路径收集为超边集合L(h)。若任一不符观察仍有一条全正确路径，则h与假设不相容。因此可行的故障集合必须与L(h)中每条路径相交。定义c(h)=min{|F|: 对所有P∈L(h)，F∩P非空}，空超边集合的成本为0。保留c(h)≤e的候选。真解释在域、路径合同真实、实际错误根数≤e时，真实故障集合就是一个可行见证，所以真解释必保留。非空保留域上硬门恒定时，可输出该假设下的只读结论；其他情况UNKNOWN，空域CONFLICT，任何输出authority NONE。此为必要一致性筛选，不声称某故障集合一定产生全部实际观察，也不证明唯一候选真实。

实现逐路径扩张极小故障集合前沿：初始{∅}，若现集合命中该路径则保留，否则分别加入路径中一个根，去重并删除严格超集。归纳：任一全局命中集合含一个前沿子集，未来路径命中保持单调，故删除超集安全。复制同一路径不改变结果；新增同口径合格路径只能维持或提高c，撤销路径只能维持或降低c，更新时重新核对候选域及证据快照。单根观察时退化为上一轮不同坏根计数。将替代路径取并集只保留一条弱约束，产生超集候选；按报告条数计算则可能重复计算共享根故障。复杂度最坏指数级（前沿为根集合反链，至多二项式系数C(n,floor(n/2))），大域预算耗尽必须标UNKNOWN，不能把截断当完整。没有测量真实设备时间/内存。未实现原始来源自动识别、DAG循环检查、实际路径资格、区间谓词或生产接入。

## 有限实验
三个合成根A/B/C，以位掩码1/2/4表示；枚举其全部18个非空路径反链；两个观察各取一个反链及0/1/2值，构成2916结构。三个角色各分配不同数值0/1/2，六个排列；两观察约束前两个角色。每个结构对六世界执行最小前沿和8个故障子集穷举参照，重复路径再次检查。对全部63个非空候选子域、e=0/1/2及六个指定真解释执行比较。硬门为第一角色≤1。基线A合并每条观察的全部路径为一个并集；基线B按不符报告数计数。枚举参照与候选共享数学夹具，不是独立科学复现。合格817152配置由真实解释在域且其最小不符路径命中成本≤预算定义；每个合格配置至少存在一个与不符观察相容的故障集合，未另外模拟具体错误生成过程。所有计数高度相关、不是统计样本量、置信率或现实误判率。研究者自行选定角色、根数、预算、硬门、结构和基线，未拟合参数。
结果：3306744个配置，817152合格，17496个算法成本/枚举参照核对与同数复制检查；合格真值排除0，确定硬门302700，错误硬门0。并集基线额外候选148890，丢失确定硬门94044；报告计数排除真值49152，错误确定硬门17152。1627128真值不在域，其中482370仍得到唯一候选；862464真值在域但超预算。两个基线作用不同，不能声称同覆盖率产品优势。例：r0支持路径{A}、r1有替代路径{A}及{B}，两观察均为0，预算1，域{(0,1,2),(2,0,1)}。第一个世界违背r1须同时故障A/B，故排除；第二个世界只违背r0需A故障，条件硬门FAIL。并集基线错误允许第一个世界，无法确定硬门。该例也说明不同路径的共同变换错误必须显式建根，否则路径合同不成立。

## 可执行复算
标准JS、无外部依赖。下列同一程序在当前工具中运行两次，第二次在归档前重新运行，实际关键计数见JSON。
```js
const W=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]], M=[1,2,3,4,5,6,7], pc=x=>((x&1)>0)+((x&2)>0)+((x&4)>0), ck=(b,m)=>{if(!b)throw Error(m)};
const fam=[];for(let s=1;s<128;s++){const f=M.filter((_,i)=>s&(1<<i));if(!f.some(a=>f.some(b=>a!==b&&(a&b)===a)))fam.push(f)}
function minimal(xs){return [...new Set(xs)].filter(x=>!xs.some(y=>x!==y&&(x&y)===y)).sort((a,b)=>a-b)}
function frontier(paths){let f=[0];for(const p of paths)f=minimal(f.flatMap(x=>(x&p)?[x]:[1,2,4].filter(b=>b&p).map(b=>x|b)));return f}
function minCost(paths){return Math.min(...frontier(paths).map(pc))}
const counts={families:fam.length,structures:0,solverChecks:0,cases:0,eligible:0,excludedTruth:0,known:0,wrongKnown:0,flatExtra:0,flatKnownLost:0,reportExcludes:0,reportWrongKnown:0,missingTruth:0,missingUnique:0,violated:0,duplicateChecks:0,witness:null};
const port=i=>W[i][0]<=1?1:0, inv=ids=>ids.length&&ids.every(i=>port(i)===port(ids[0]))?port(ids[0]):-1;
for(const a of fam)for(const b of fam)for(let x=0;x<3;x++)for(let y=0;y<3;y++){
 counts.structures++;
 const costs=W.map(w=>{const paths=[...(w[0]!==x?a:[]),...(w[1]!==y?b:[])];const f=frontier(paths),c=Math.min(...f.map(pc));const oracle=Math.min(...[0,...M].filter(z=>paths.every(p=>z&p)).map(pc));ck(c===oracle,"oracle");ck(JSON.stringify(f)===JSON.stringify(frontier([...paths,...paths])),"duplicate");counts.solverChecks++;counts.duplicateChecks++;
 return [c,minCost([...(w[0]!==x?[a.reduce((u,v)=>u|v,0)]:[]),...(w[1]!==y?[b.reduce((u,v)=>u|v,0)]:[])]),Number(w[0]!==x)+Number(w[1]!==y)]});
 for(let e=0;e<=2;e++)for(let d=1;d<64;d++){
 const domain=W.map((_,i)=>i).filter(i=>d&(1<<i)), exact=domain.filter(i=>costs[i][0]<=e),flat=domain.filter(i=>costs[i][1]<=e),report=domain.filter(i=>costs[i][2]<=e),p=inv(exact),q=inv(flat),r=inv(report);
 ck(exact.every(i=>flat.includes(i)),"relaxation");
 for(let t=0;t<6;t++){counts.cases++;if(!domain.includes(t)){counts.missingTruth++;if(exact.length===1)counts.missingUnique++;continue}if(costs[t][0]>e){counts.violated++;continue}
 counts.eligible++;if(!exact.includes(t))counts.excludedTruth++;if(p!==-1){counts.known++;if(p!==port(t))counts.wrongKnown++}if(flat.length>exact.length)counts.flatExtra++;if(p!==-1&&q===-1)counts.flatKnownLost++;if(!report.includes(t))counts.reportExcludes++;if(r!==-1&&r!==port(t))counts.reportWrongKnown++;
 if(!counts.witness&&p!==-1&&q===-1)counts.witness={a,b,x,y,e,domain:domain.map(i=>W[i]),truth:W[t],exact:exact.map(i=>W[i]),flat:flat.map(i=>W[i])};
 }
 }
}
ck(counts.cases===counts.eligible+counts.missingTruth+counts.violated,"partition");ck(counts.excludedTruth===0&&counts.wrongKnown===0,"safety");
console.log(JSON.stringify(counts,null,2));
```
```json
{
  "families": 18,
  "structures": 2916,
  "solverChecks": 17496,
  "cases": 3306744,
  "eligible": 817152,
  "excludedTruth": 0,
  "known": 302700,
  "wrongKnown": 0,
  "flatExtra": 148890,
  "flatKnownLost": 94044,
  "reportExcludes": 49152,
  "reportWrongKnown": 17152,
  "missingTruth": 1627128,
  "missingUnique": 482370,
  "violated": 862464,
  "duplicateChecks": 17496,
  "witness": {
    "a": [
      1
    ],
    "b": [
      1,
      2
    ],
    "x": 0,
    "y": 0,
    "e": 1,
    "domain": [
      [
        0,
        1,
        2
      ],
      [
        2,
        0,
        1
      ]
    ],
    "truth": [
      2,
      0,
      1
    ],
    "exact": [
      [
        2,
        0,
        1
      ]
    ],
    "flat": [
      [
        0,
        1,
        2
      ],
      [
        2,
        0,
        1
      ]
    ]
  }
}
```

## 接入边界
下一责任：模型轨研究预算受限搜索、区间观察和不完整路径；数据轨验证根身份与充分派生路径的来源资格；独立轨保管未见案例并测试错误放行、拒绝与版本回退；后续经授权版本才接入原生数学准备合同。未执行原生入口、真实语料、新独立留出、真人、竞品、设备、训练、主动CI、PR合并或部署；不改变唯一产品交接、历史冻结、正式证据等级。零新增费用。
