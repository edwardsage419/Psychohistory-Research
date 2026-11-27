# 自主认知：预算受限多来源故障搜索与共享区间参数
2026-11-27。RESEARCH_CANDIDATE / FINITE_SYNTHETIC_EXHAUSTIVE_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线和范围
起点及写前 main ba898a214af620164474387136beff85f1aac142；目标新文件写前404。读取 v3.2 及研究同步规程全文、最近30提交、上一轮多来源派生故障预算报告（最新commit差分）、开放PR、唯一产品交接末9000字符（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07），检索 hitting、fault budget、interval evidence、branch bound；非全库查重。PR #63 仍open，作者描述语言数值单位7/23、条件0/5、他人主体1/4、修订链0/10，未复跑。直接补上一轮搜索预算及区间观察缺口；不重复源资格、原文语言生成或账本执行。原创有限数学推导，无外部数据或第三方AI运行时。

## 数学合同
沿用上一轮充分派生路径语义。每个违反观察的候选世界产生待命中非空根集合族P。所有用户已确认硬约束、根身份、来源和路径资格、预算k及候选域覆盖均为外部可信合同；未知资格不得通过计算自行补足。每个故障集合大小不超过k。搜索目标是存在可命中全部路径的故障集合。重复超边与含其他超边的严格超集可删除。互不相交的路径数是命中数下界；贪心逐次选覆盖最多剩余路径的根得到可行命中集合及其大小上界。下界超过k可拒绝；上界不超过k可保留。其他情况选一条最短路径，分别假定其中一个根故障，删除被该根命中的路径并递减k，分支逻辑为存在量词。全分支否定才拒绝；任一分支肯定可保留；无肯定且有未完成分支则UNKNOWN。完整性由对路径任一命中集合必含至少一个路径根归纳证明。节点上限仅限制展开次数，不是总工作、时间或内存上限；预处理、递归和贪心仍有成本。实现只支持非空合法位掩码、n≤4的主要测试（通用位掩码仍受JS位宽约束），生产需输入验证、可取消预处理、资源计量、证书及快照绑定，不得把未完成当拒绝。
 
三值候选集合：YES为有一致性见证，NO为已排除，UNKNOWN为未完成。对确定布尔硬门，只有至少一个YES且YES与UNKNOWN并集上硬门恒定才输出条件PASS/FAIL；全NO为CONFLICT，否则UNKNOWN。即使YES也仅是必要一致性可行，非事实证明、非账本写权限；所有authority NONE。若候选覆盖失败、错误预算失实或路径资格错误，保证失效。 

联合区间：将语义候选h与共享参数t联合为世界(h,t)，先在同一t上计算不符路径集合，再对故障预算求存在性。对于有限t域，h的状态为各t的三值存在合取规则（任一YES则YES；全NO则NO；否则UNKNOWN）。禁止把不同观察各自存在某个t当成共同t存在。例：t∈{0,1,2,3,4}，h∈{0,2}，观察t=0和t+h∈[1,2]，k=0。逐观察独立存在会保留h=0；共享t要求h=2，故硬门h≤1条件FAIL。连续参数域、无界参数、多维相关区间、单位及时间换算尚未解决。硬门若也依赖t，须在联合世界上判断，不能仅投影h。没有任何概率假定。

## 实验范围与结果
四个合成根，全部32768种非空路径族的子集（含空族），k=0..3；对照16个故障子集穷举。四种展开预算0/1/3/100分别测试，共524288次求解。三值门枚举4个候选的状态、硬门及全部兼容真实可行子集。区间实验枚举15个整数闭区间各两项、两个独立单根、k=0/1、h三个值的所有非空子域；枚举(h,t,F)生成合格配置，以所有非故障根的谓词必须成立为条件，检查真h保留及硬门。所有数值、根数、阈值、预算和基线均为研究者选定，未拟合。计数为相互依赖的有限配置，非独立样本、真实错误率或性能基准。两个版本在当前工具执行，归档以下扩展版（区间实验显式枚举故障集合及真参数）。未执行真实设备时间/内存、连续区间、原生入口、真实语料、独立留出、用户、竞品、训练、主动CI、合并、部署。零新增费用。下一责任：模型轨进一步研究可中断证书及连续线性域，数据轨核对来源路径资格，独立轨保留未见案例，经授权版本接入。保留唯一产品交接及冻结协议不变。

## 可执行复算
保存为JS后以外层函数执行（例如将代码放入 function experiment(){ ... }，再console.log(experiment())）。仅标准JS。
```js
const pc=x=>{let n=0;while(x){x&=x-1;n++}return n};
function solve(paths,k,limit,n=4){
 let nodes=0;const roots=Array.from({length:n},(_,i)=>1<<i);
 function rec(p,k){
  if(!p.length)return 1;
  if(k===0)return 0;
  p=[...new Set(p)].filter(x=>!p.some(y=>x!==y&&(x&y)===y)).sort((a,b)=>pc(a)-pc(b)||a-b);
  let union=0,lower=0;
  for(const x of p)if(!(x&union)){union|=x;lower++}
  if(lower>k)return 0;
  let q=p.slice(),upper=0;
  while(q.length){let b=roots.slice().sort((a,b)=>q.filter(x=>x&b).length-q.filter(x=>x&a).length||a-b)[0];q=q.filter(x=>!(x&b));upper++}
  if(upper<=k)return 1;
  if(nodes>=limit)return -1;
  nodes++;let unknown=false;
  for(const b of roots.filter(b=>b&p[0])){const z=rec(p.filter(x=>!(x&b)),k-1);if(z===1)return 1;if(z===-1)unknown=true}
  return unknown?-1:0;
 }
 return [rec(paths,k),nodes];
}
function gate(status,pass){const possible=status.map((s,i)=>s!==0?i:-1).filter(i=>i>=0);if(!possible.length)return "conflict";if(!status.includes(1)||!possible.every(i=>pass[i]===pass[possible[0]]))return "unknown";return pass[possible[0]]?"pass":"fail"}
const out={graphs:0,cases:0,fullWrong:0,limitedWrong:0,limits:{},hard:{cases:0,known:0,wrong:0,empty:0,unknown:0},joint:{cases:0,truthExcluded:0,exactKnown:0,wrong:0,relaxedLost:0,relaxedExtra:0,witness:null}};
for(const l of [0,1,3,100])out.limits[l]={yes:0,no:0,unknown:0,nodes:0};
for(let mask=0;mask<32768;mask++){
 const p=Array.from({length:15},(_,i)=>i+1).filter((_,i)=>mask&(1<<i));out.graphs++;
 for(let k=0;k<4;k++){
 const t=Array.from({length:16},(_,i)=>i).some(f=>pc(f)<=k&&p.every(x=>x&f));out.cases++;
 for(const l of [0,1,3,100]){const [z,n]=solve(p,k,l),s=out.limits[l];s[z===1?"yes":z===0?"no":"unknown"]++;s.nodes+=n;if(z!==-1&&Boolean(z)!==t)out.limitedWrong++;if(l===100&&z!==Number(t))out.fullWrong++;}
 }
}
for(let s=0;s<81;s++){let status=Array.from({length:4},(_,i)=>Math.floor(s/3**i)%3-1);for(let b=0;b<16;b++){let pass=Array.from({length:4},(_,i)=>!!(b&(1<<i)));let g=gate(status,pass);for(let m=0;m<16;m++){const actual=Array.from({length:4},(_,i)=>!!(m&(1<<i)));if(status.some((z,i)=>z!==-1&&Boolean(z)!==actual[i]))continue;out.hard.cases++;if(g==="unknown")out.hard.unknown++;else if(g==="conflict"){out.hard.empty++;if(actual.some(Boolean))out.hard.wrong++}else{out.hard.known++;if(!actual.some(Boolean)||actual.some((a,i)=>a&&pass[i] !== (g==="pass")))out.hard.wrong++}}}}
const intervals=[];for(let a=0;a<=4;a++)for(let b=a;b<=4;b++)intervals.push([a,b]);
const inI=(x,I)=>I[0]<=x&&x<=I[1], T=[0,1,2,3,4];
for(const I of intervals)for(const J of intervals)for(let k=0;k<=1;k++)for(let mask=1;mask<8;mask++){
 const d=[0,1,2].filter(h=>mask&(1<<h));
 const status=d.map(h=>{let z=T.map(t=>solve([...(inI(t,I)?[]:[1]),...(inI(t+h,J)?[]:[2])],k,100)[0]);return z.includes(1)?1:z.includes(-1)?-1:0});
 const a=d.filter((h,i)=>status[i]===1), b=d.filter(h=>Number(!T.some(t=>inI(t,I)))+Number(!T.some(t=>inI(t+h,J)))<=k);
 const g=gate(status,d.map(h=>h<=1)),r=gate(d.map(h=>Number(b.includes(h))),d.map(h=>h<=1));
 for(const truth of d)for(const t of T)for(let f=0;f<4;f++){
 if(pc(f)>k||(!(f&1)&&!inI(t,I))||(!(f&2)&&!inI(t+truth,J)))continue;
 out.joint.cases++;if(!a.includes(truth))out.joint.truthExcluded++;if(g==="pass"||g==="fail"){out.joint.exactKnown++;if((g==="pass")!==(truth<=1))out.joint.wrong++}if(b.length>a.length)out.joint.relaxedExtra++;if((g==="pass"||g==="fail")&&r==="unknown"){out.joint.relaxedLost++;if(!out.joint.witness)out.joint.witness={I,J,k,d,a,b,truth,t,f}}
 }
}
if(out.fullWrong||out.limitedWrong||out.hard.wrong||out.joint.truthExcluded||out.joint.wrong)throw Error("validation failed");
return out;
```
```json
{
  "graphs": 32768,
  "cases": 131072,
  "fullWrong": 0,
  "limitedWrong": 0,
  "limits": {
    "0": {
      "yes": 46991,
      "no": 82303,
      "unknown": 1778,
      "nodes": 0
    },
    "1": {
      "yes": 46991,
      "no": 83025,
      "unknown": 1056,
      "nodes": 1778
    },
    "3": {
      "yes": 46991,
      "no": 84081,
      "unknown": 0,
      "nodes": 2866
    },
    "100": {
      "yes": 46991,
      "no": 84081,
      "unknown": 0,
      "nodes": 2866
    }
  },
  "hard": {
    "cases": 4096,
    "known": 738,
    "wrong": 0,
    "empty": 16,
    "unknown": 3342
  },
  "joint": {
    "cases": 16616,
    "truthExcluded": 0,
    "exactKnown": 7473,
    "wrong": 0,
    "relaxedLost": 256,
    "relaxedExtra": 351,
    "witness": {
      "I": [
        0,
        0
      ],
      "J": [
        1,
        2
      ],
      "k": 0,
      "d": [
        0,
        2
      ],
      "a": [
        2
      ],
      "b": [
        0,
        2
      ],
      "truth": 2,
      "t": 0,
      "f": 0
    }
  }
}
```
