# 第54轮：共享事实参数、精确线性推导与跨模型依赖身份
2026-11-25。固定main 9702d42453b022a10100d2db9935a8a2a869ab85；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第11/39/47/53轮。关键词 unit conversion/parameter derivation/shared facts/dimensional analysis 检索，parameter derivation命中第11轮e140dda93ebb6065312baa69b44f16c2c1050b2f，已读报告，其他无结果；未声称全库无重复。原生decision_state.py 0840855431fbc88fe212785584277aa01be74d93 Quantity/Option/Scenario分离 measurements/scores/utilities；decision_feasibility.py 6181d6c578c7ef251e9708d0ffcf65e95d35f88f 检查单位、时域及同指标不一致；decision_scoring.py 7832116703246bafc98831a6039d14c0d691cdd1 _score_gap/_objective_horizons；decision_regret.py e56689a54897d95eaa126540c23fca51cc0eede7 _validate；decision_extensions.py a9f96ca5979329c9de77498b34acd153ba4594a6 EvidenceItem。源级审阅未运行完整入口，不声称生产缺陷。与C034共同偏移误差已有专门研究、R39差分约束、R47共享计算、R53义务映射区别，本轮专注可追溯共享原始参数的有限线性组合接口；共同误差抵消非原创数学定理，增量为跨字段数据绑定与资格隔离。无新增外部事实。
## 合同
单个可复用事实绑定主体、数量语义（税前/税后、总量/速率、成本/收益、事实/假设/政策）、单位与币种、时间窗口及聚合定义、情景/行动条件、来源与版本、决策会话及修订、授权范围与代次。相同名称、数值或来源不证明相同随机变量或实际量；不同记录只有经过可信同一性核实才能合并。事实可投影至同一含义的多个原生字段；货币不能未经用户确认的效用函数直接充当总体效用。单位换算须可信精确关系；例如同币种KRW与千KRW，保留时间和聚合语义，不能把月收入自动乘12充当实际年总收入（需明确覆盖每月、奖金、合同期限等假设）；外汇换算需有时点/来源的汇率及不确定性；本轮不执行汇率、时间折算或效用变换。经确认的估计不自动升级为事实，条件假设的计算结果保持条件，政策阈值不作为现实测量证据。派生数据不扩大授权范围。不同用途的复用需要实际许可，原型只测试完全相同purpose的保守情形。
## 数学
原始合格参数x_i在有限闭区间[l_i,h_i]，联合可行域确认为矩形；同一x_i被多个公式重复引用仍是同一变量。线性输出 f(x)=c+Σ a_i x_i；对每个i按符号取端点给出紧界，零系数抵消。f-g=(c_f-c_g)+Σ(a_i-b_i)x_i，直接对差求界保留共享依赖；分别计算f、g的边际区间再相减只能给保守外界，可能丢失确定比较。证明：矩形内各变量可独立取端点，因此每个贡献的极值能联合达到；相关域时矩形只是有效外包（若边际是可靠硬界），不可称精确或自造独立性；统计置信区间不能直接当硬界。模型原生输入若不支持联合依赖，应保留条件性差界及保守边际、不要伪造独立性证据；只能按适用准则解释结果。即使数值抵消，原始来源和合同仍应记录以支持审计和更正，撤回后的重新使用需单独授权；本轮保守地使所有依赖输出失效，不尝试证明消除私有影响。一般非线性、概率、动态时间与相关联合域未覆盖。
## 实际实验
三原始量，6种闭整数区间0..2，27种三元系数向量(-1/0/1)，两个线性表达式全组合，216×729组；逐整数世界直接计算f-g核对符号端点公式，整数盒端点也是连续域精确极值见证。边际外界对照按不同变量处理输出（保守，非错误现实概率），统计严格收紧、由未决变成严格胜出或全域并列。仅比较差的符号，非任意多目标排序；合成权重与单位非用户真实值。另人工可信身份字段变异、撤权、无效区间、比例单位转换、同值不同变量、依赖修订控制；不能将此布尔模拟当真实鉴权或加密校验。两路径同研究者编写，非独立验收。
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 // All quantities in a qualified common additive unit and horizon. Integer coefficients are illustrative.
 const I=[[0,0],[0,1],[0,2],[1,1],[1,2],[2,2]];
 const forms=[];for(let a=-1;a<=1;a++)for(let b=-1;b<=1;b++)for(let c=-1;c<=1;c++)forms.push([a,b,c]);
 const sub=(a,b)=>a.map((v,i)=>v-b[i]);
 const bound=(f,box)=>f.reduce(([l,h],a,i)=>[l+Math.min(a*box[i][0],a*box[i][1]),h+Math.max(a*box[i][0],a*box[i][1])],[0,0]);
 const val=(f,x)=>f.reduce((s,a,i)=>s+a*x[i],0);
 const status=(l,h)=>l>0?"A":h<0?"B":l===0&&h===0?"TIE":"UNRESOLVED";
 let cases=0,worlds=0,exact=0,strictTightening=0,decisiveGain=0,strictWinnerGain=0,tieGain=0,baselineDecisive=0,sharedDecisive=0,controls=0,witness=null,tieWitness=null;
 for(const a of I)for(const b of I)for(const c of I){
  const box=[a,b,c],pts=[];
  for(let x=a[0];x<=a[1];x++)for(let y=b[0];y<=b[1];y++)for(let z=c[0];z<=c[1];z++)pts.push([x,y,z]);
  for(const f of forms)for(const g of forms){
   cases++;const diff=sub(f,g),[l,h]=bound(diff,box),[al,ah]=bound(f,box),[bl,bh]=bound(g,box),old=[al-bh,ah-bl];
   const vs=pts.map(x=>val(f,x)-val(g,x));worlds+=pts.length;ck(l===Math.min(...vs)&&h===Math.max(...vs),"bound");exact++;
   ck(old[0]<=l&&h<=old[1],"outer");
   if(old[0]<l||h<old[1])strictTightening++;
   const s=status(l,h),o=status(...old);if(o!=="UNRESOLVED"){baselineDecisive++;ck(s===o,"old decisive");}if(s!=="UNRESOLVED")sharedDecisive++;
   if(s!=="UNRESOLVED"&&o==="UNRESOLVED"){decisiveGain++;if(s==="TIE"){tieGain++;if(!tieWitness)tieWitness={box,f,g,old,shared:[l,h]};}else{strictWinnerGain++;if(!witness)witness={box,f,g,old,shared:[l,h],winner:s};}}
  }
 }
 // Exact semantic identity: no matching via label or equal numeric value. Trusted fixture, not real authentication.
 const root={id:"x",revision:1,session:"S",generation:1,subject:"person",metric:"net_income",currency:"KRW",unit:"KRW",period:"2027-01",aggregation:"total",scenario:"base",role:"fact",source:"source1",purpose:"decision",authorized:true,lo:1000,hi:2000};
 const keys=["id","revision","session","generation","subject","metric","currency","unit","period","aggregation","scenario","role","source","purpose"];
 const use=(r,t)=>r.authorized===true&&t.authorized===true&&keys.every(k=>r[k]===t[k])&&Number.isSafeInteger(r.lo)&&Number.isSafeInteger(r.hi)&&r.lo<=r.hi;
 ck(use(root,{...root}),"positive");controls++;
 for(const k of keys){ck(!use(root,{...root,[k]:typeof root[k]==="number"?root[k]+1:root[k]+"_changed"}),"identity "+k);controls++;}
 ck(!use({...root,authorized:false},root),"revoked");controls++;
 ck(!use({...root,lo:3000},root),"bounds");controls++;
 // Exact scale conversion does not change role, horizon, or dependence. Separate explicit conversion receipt.
 const scale=(v,num,den)=>{if(!Number.isSafeInteger(num)||!Number.isSafeInteger(den)||num<=0||den<=0)throw Error("scale");return {loNum:v.lo*num,hiNum:v.hi*num,den};};
 ck(JSON.stringify(scale(root,1,1000))===JSON.stringify({loNum:1000,hiNum:2000,den:1000}),"scale");controls++;
 // Same numeric interval from distinct variables cannot be merged; same source alone does not establish equality.
 ck(JSON.stringify(bound([1,-1,0],[[0,2],[0,2],[0,0]]))==="[-2,2]","distinct");controls++;
 ck(JSON.stringify(bound([0,0,0],[[0,2],[0,2],[0,0]]))==="[0,0]","shared");controls++;
 // Recompute all dependent nodes, not just outputs with changed numerical values.
 const dep={x:[],y:[],z:[],A:["x","y"],B:["x","z"],D:["A","B"],note:["y"]};
 function affected(changed){let set=new Set(changed),n;do{n=set.size;for(const [k,ds] of Object.entries(dep))if(ds.some(d=>set.has(d)))set.add(k);}while(set.size!==n);return [...set].sort();}
 ck(affected(["x"]).join()==="A,B,D,x","revision");controls++;
 ck(affected(["y"]).join()==="A,D,note,y","selective");controls++;
 return {cases,worlds,exact,strictTightening,decisiveGain,strictWinnerGain,tieGain,baselineDecisive,sharedDecisive,controls,witness,tieWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "cases": 157464,
  "worlds": 729000,
  "exact": 157464,
  "strictTightening": 46872,
  "decisiveGain": 21000,
  "strictWinnerGain": 12504,
  "tieGain": 8496,
  "baselineDecisive": 75534,
  "sharedDecisive": 96534,
  "controls": 22,
  "witness": {
    "box": [
      [
        0,
        0
      ],
      [
        0,
        1
      ],
      [
        1,
        1
      ]
    ],
    "f": [
      -1,
      -1,
      -1
    ],
    "g": [
      -1,
      -1,
      0
    ],
    "old": [
      -2,
      0
    ],
    "shared": [
      -1,
      -1
    ],
    "winner": "B"
  },
  "tieWitness": {
    "box": [
      [
        0,
        0
      ],
      [
        0,
        0
      ],
      [
        0,
        1
      ]
    ],
    "f": [
      -1,
      -1,
      -1
    ],
    "g": [
      -1,
      -1,
      -1
    ],
    "old": [
      -1,
      1
    ],
    "shared": [
      0,
      0
    ]
  }
}
```
## 接入
B02/B05/B06/B07/B08/B09/B10/B11候选增量。建立共享事实引用及可信派生收据（源ID、完整语义身份、单位换算关系、公式/版本、依赖、条件、授权、输出区间及联合结构），将同一用户确认数据在硬约束、目标比较、情景分析之间按要求投影，避免重复询问；有歧义仍需确认，关键参数未知保留未知。事实或授权修改后依赖收据失效，原有计算不能仅凭数值一致复用。生产端需复用现有state/validator而非改写数学核心，保留C034及其他已知依赖机制，不将候选方法自动上线。独立轨预留税前/后、个人/家庭、月/年、货币、场景、同源异量、不同来源同量、权重、过期、撤回、线性误差和相关域反例；真实自然语言、单位注册、原生投影、完整环境、隐私和真人体验尚未验证。未修改生产代码、Codex、CI、训练、合并、部署或冻结协议，零新增费用。
