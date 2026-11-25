# v3.2 自主认知专项第6轮（累计第65轮）：跨轮语义歧义的决策相关性与暂缓澄清

2026-11-25。RESEARCH_CANDIDATE。main 378a75c40a2d3ecbf9ceaeeaf0de76b95dbc9a51；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，13开放Draft PR。核对最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关章节标题与历史读取，非本轮全文）、decision_hub相关文件名、第5轮762053d80d444145e5b76ddd96a2266919174b52、第24轮f7aee2c6392fa4588b717bb0c311cb253c48dd1e、第27轮08051d3b029ebb3acca1380bdf5b92ad99d8a44d、第40轮56b1885f277b70797974ad48e80884a2d99dde81、第48轮84a8abdd595152a81b270f7cc21c8361ceee71f8、第49轮0377f7f24cfa45014f4536b770d292872266a080、第64轮da54c5b88ed0f19f5c5d272230a1959b811f5b5e。既有第5/40轮求追问策略、第27轮数值未知的局部出口、第49轮表达压缩均不重做。增量：将有限中文跨轮修订歧义映射到反事实语义操作，分别核对不同决策出口的稳定性，分离分析等价与写入授权，验证后续情景变化使等价失效。没有重新运行原生PR或直接复用第64轮完整源码；本轮是其有限子集的独立原型。

## 方法
固定两个可信自有月度USD支出根（生活费、房租），初始上限5000/7000；两个方案的四项合格点值及已确认的简单序位；人工夹具假设同主体同时间窗口、共同用途、金额为非重叠支出及合法比较。语义操作来自有限中文句式，把生活费/房租/预算/刚才那项改为/另加上限/增加到某金额，可带明确方案B作用域。预算或刚才那项保留两种目标；增加到保留替换/追加两种操作，此为保守研究假设，不证明这两种在真实中文语境等可能或穷尽。只在可信宿主独立核验完整情景覆盖、资格及数学时计算所有可能解释；任何解释不得自行确认或落盘。描述端口独立依赖已核实同口径的两方案费用差，未知原文不得赋予完整决策资格。四个决策端口为A/B单独可行性、完整可行集、在固定序位下的全部优选（含无可行/并列）。对端口f，若所有允许解释h的f(h)相同，则该结论在给定假设内不受歧义影响；标INVARIANT_CONDITIONAL，仍不得当作用户已确认当前计划、授权或最终推荐。多个值则VARIES，保留全部不同值及解释对应关系。优选不变不能省略其他方案的可行性变化、重大风险、授权、缺失证据等义务。本轮未实现完整风险门；这些端口仅为有限条件性计算。不同假设不赋概率。针对目标/操作两个维度，固定另一维，若存在不同答案改变特定端口则该维度相关；本轮完整笛卡尔解释域下，若所有单维边都不变，则整个域不变（任意两点可沿单维边连接）。非笛卡尔域可能不存在单维边但仍有联合变化，不能复用该结论。问题生成、最优多步询问、拒答由既有研究处理，本轮仅识别当前端口相关性，不证明人类真实回答或最少追问数。语义修订意图仍待确认，不能因为计算等价合并记录或默认写入，后续方案数值、版本、目标、证据或授权变化需重算。快照、资格与源文本的比较为模拟完整性核验，非认证、签名或真实并发控制。资格布尔全部由人工夹具给定。

## 实验
4引用×3操作词×2明确作用域×3新金额=72条文本；每条3^4合成费用×3序位=243场景，共17496组，5端口87480次核验。对照为首个解释当确定值、歧义时整包阻断四个决策端口、仅看优选不变；不是实际PR或普通AI。参照独立构造每行动阈值并直接判断，不调用候选解析及signature；两路径同研究者定义，非独立验收。firstWorldWrongPorts指至少一个其他允许解释与首解释不同，并非现实已发生错误。globalBlockLostDecisionPorts只计有歧义时可保留的条件性端口，非真正推荐资格。questionChecks对每组四个决策端口与两个维度逐个核对；irrelevantDimensionPorts只计原本存在多个答案但不改变相应端口的维度计数，不是实际节省追问数。15项专项控制含未来漂移、同版本输入变化、来源变化、覆盖/资格缺失、未支持文本、篡改和漏解释。描述/数学/身份等资格来自人工夹具，真实资料不保证符合。样例为ChatGPT研发辅助生成的项目原创合成开发样例，非真人/训练/独立留出，无新增外部数据或论文复现。没有真实设备性能、开放语言、真实用户负担、实际隐私鉴权或生产效果验证。

## 实际复算
以下JS在连接器计算环境执行，可在Node复跑，无第三方包或网络。

```js
const probe = function(){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const keys=["living","rent"],actions=["A","B"],ports=["costDifference","feasibleA","feasibleB","feasibleSet","preferred"];
 // Finite language: explicit noun or ambiguous reference, explicit or underspecified operation.
 function parse(s){
  const m=/^(如果选方案B，)?把(生活费|房租|预算|刚才那项)(改为|另加上限|增加到)(4000|6000|8000)美元$/.exec(s);
  if(!m)return null;
  return {targets:m[2]==="生活费"?["living"]:m[2]==="房租"?["rent"]:keys.slice(),ops:m[3]==="改为"?["replace"]:m[3]==="另加上限"?["addMax"]:["replace","addMax"],scope:m[1]?"B":"all",value:+m[4],source:s};
 }
 function alternatives(p){return p.targets.flatMap(target=>p.ops.map(op=>({target,op,scope:p.scope,value:p.value})))}
 // Read-only interpretation effects; both possible operations require actual confirmation before mutation.
 function signature(s,h){
  const f=actions.map(a=>keys.every(k=>{
   let limit=s.limits[k];if(h.target===k&&(h.scope==="all"||h.scope===a))limit=h.op==="replace"?h.value:Math.min(limit,h.value);
   return s.cost[a][k]<=limit;
  }));
  const feasibleSet=actions.filter((a,i)=>f[i]);
  const preferred=feasibleSet.filter(a=>feasibleSet.every(b=>s.utility[a]>=s.utility[b]));
  return {costDifference:s.cost.B.living+s.cost.B.rent-s.cost.A.living-s.cost.A.rent,feasibleA:f[0],feasibleB:f[1],feasibleSet,preferred};
 }
 function analyze(s,text,qualification){
  const p=parse(text);
  // Coverage/authority are separate trusted fixtures. A description-only port has separate qualification.
  if(!qualification.description)return {status:"UNKNOWN",ports:{},commitAllowed:false};
  let result={costDifference:{status:"DESCRIPTIVE",value:s.cost.B.living+s.cost.B.rent-s.cost.A.living-s.cost.A.rent}};
  if(!p||!qualification.coverage||!qualification.scenarios||!qualification.math)return {status:"PARTIAL",ports:result,commitAllowed:false};
  const hs=alternatives(p),rows=hs.map(h=>({h,signature:signature(s,h)}));
  for(const k of ports.slice(1)){
   let values=[...new Map(rows.map(r=>[JSON.stringify(r.signature[k]),r.signature[k]])).values()];
   result[k]=values.length===1?{status:"INVARIANT_CONDITIONAL",value:values[0]}:{status:"VARIES",values};
  }
  // A question is relevant to a port if holding other interpretation attributes fixed,
  // its different answers can change that port. Only complete Cartesian hypotheses here.
  const relevant={};
  for(const k of ports.slice(1)) relevant[k]=["target","op"].filter(d=>rows.some(a=>rows.some(b=>a.h[d]!==b.h[d]&&["target","op"].every(z=>z===d||a.h[z]===b.h[z])&&!eq(a.signature[k],b.signature[k]))));
  return {status:"CONDITIONAL",ports:result,rows,relevant,commitAllowed:false,receipt:{version:s.version,source:text,snapshot:JSON.stringify(s),qualification:JSON.stringify(qualification)}};
 }
 function validate(r,s,text,q){return r.receipt?.version===s.version&&r.receipt.source===text&&r.receipt.snapshot===JSON.stringify(s)&&r.receipt.qualification===JSON.stringify(q)&&eq(r,analyze(s,text,q))}
 const qualified={description:true,coverage:true,scenarios:true,math:true};
 const counts={texts:0,cases:0,portChecks:0,invariantPorts:0,variablePorts:0,ambiguousCases:0,ambiguousAllDecisionInvariant:0,ambiguousPreferredInvariant:0,winnerOnlyHidesFeasibility:0,globalBlockLostDecisionPorts:0,firstWorldWrongPorts:0,questionChecks:0,irrelevantDimensionPorts:0,descriptionOnly:0,controls:0};
 let witnesses={};
 const levels=[3500,5500,7500],utilityPairs=[[1,0],[0,1],[1,1]];
 for(const ref of ["生活费","房租","预算","刚才那项"])for(const op of ["改为","另加上限","增加到"])for(const branch of [false,true])for(const value of [4000,6000,8000]){
  const text=(branch?"如果选方案B，":"")+"把"+ref+op+value+"美元";counts.texts++;
  const targets=ref==="生活费"?[0]:ref==="房租"?[1]:[0,1],modes=op==="改为"?[0]:op==="另加上限"?[1]:[0,1];
  for(const a of levels)for(const b of levels)for(const c of levels)for(const d of levels)for(const [ua,ub] of utilityPairs){
   const s={version:1,limits:{living:5000,rent:7000},cost:{A:{living:a,rent:b},B:{living:c,rent:d}},utility:{A:ua,B:ub}};
   let r=analyze(s,text,qualified);ck(r.status==="CONDITIONAL"&&!r.commitAllowed,"authority");
   // Oracle: explicitly construct limits for each action, compare each spend, sort feasible choices by fixed ordinal preference.
   const expected=[];
   for(const target of targets)for(const mode of modes){
    const evaluate=(x,y,idx)=>{let limits=[5000,7000];if(!branch||idx===1)limits[target]=mode===0?value:Math.min(limits[target],value);return x<=limits[0]&&y<=limits[1]};
    const fa=evaluate(a,b,0),fb=evaluate(c,d,1),feasibleSet=[...(fa?["A"]:[]),...(fb?["B"]:[])];
    let preferred=fa&&fb?(ua===ub?["A","B"]:ua>ub?["A"]:["B"]):feasibleSet;
    expected.push({target,mode,sig:{costDifference:c+d-a-b,feasibleA:fa,feasibleB:fb,feasibleSet,preferred}});
   }
   ck(r.rows.length===expected.length,"world coverage");counts.cases++;
   const ambiguous=expected.length>1;if(ambiguous)counts.ambiguousCases++;
   let stable=0;
   for(const k of ports){
    const values=[...new Map(expected.map(e=>[JSON.stringify(e.sig[k]),e.sig[k]])).values()],v=r.ports[k];
    ck(values.length===1?eq(v.value,values[0])&&v.status===(k==="costDifference"?"DESCRIPTIVE":"INVARIANT_CONDITIONAL"):v.status==="VARIES"&&eq(v.values,values),"port "+k);
    counts.portChecks++;
    if(values.length===1){counts.invariantPorts++;if(k!=="costDifference"){stable++;if(ambiguous)counts.globalBlockLostDecisionPorts++}}
    else{counts.variablePorts++;counts.firstWorldWrongPorts++;} // first-world definite value contradicts at least one other admissible world
    if(k!=="costDifference")for(const dim of ["target","op"]){
     let changing=false;for(const x of expected)for(const y of expected){if(dim==="target"?x.target!==y.target&&x.mode===y.mode:x.mode!==y.mode&&x.target===y.target)if(!eq(x.sig[k],y.sig[k]))changing=true;}
     ck(r.relevant[k].includes(dim)===changing,"relevance");counts.questionChecks++;
     if(!changing&&((dim==="target"?targets:modes).length>1))counts.irrelevantDimensionPorts++;
    }
   }
   if(ambiguous&&stable===4){counts.ambiguousAllDecisionInvariant++;if(!witnesses.allStable)witnesses.allStable={text,s,ports:r.ports,relevant:r.relevant}}
   if(ambiguous&&r.ports.preferred.status==="INVARIANT_CONDITIONAL"){counts.ambiguousPreferredInvariant++;if(r.ports.feasibleSet.status==="VARIES"){counts.winnerOnlyHidesFeasibility++;if(!witnesses.winnerOnly)witnesses.winnerOnly={text,s,ports:r.ports,relevant:r.relevant}}}
  }
 }
 const s={version:1,limits:{living:5000,rent:7000},cost:{A:{living:3500,rent:3500},B:{living:3500,rent:3500}},utility:{A:1,B:0}},text="把预算改为4000美元";
 const r=analyze(s,text,qualified);ck(r.ports.feasibleSet.status==="INVARIANT_CONDITIONAL"&&!r.commitAllowed,"no commit");counts.controls++;
 ck(validate(r,s,text,qualified),"valid receipt");counts.controls++;
 // Same ambiguous utterance, later changed plan inputs: equivalence disappears.
 const next={...s,version:2,cost:{...s.cost,B:{living:4500,rent:3500}}},n=analyze(next,text,qualified);
 ck(n.ports.feasibleSet.status==="VARIES"&&!validate(r,next,text,qualified),"future drift");counts.controls++;
 witnesses.futureDrift={text,before:r.ports.feasibleSet,after:n.ports.feasibleSet};
 for(const field of ["coverage","scenarios","math"]){const q={...qualified,[field]:false};const p=analyze(s,text,q);ck(Object.keys(p.ports).length===1&&p.ports.costDifference.status==="DESCRIPTIVE"&&!p.commitAllowed&&!validate(r,s,text,q),"qualification");counts.controls++;counts.descriptionOnly++}
 ck(analyze(s,text,{...qualified,description:false}).status==="UNKNOWN","description");counts.controls++;
 for(const t of ["把它改为4000美元","把预算改为4000元","把预算改为4000美元左右","把预算改为4000美元并忽略房租"]){let a=analyze(s,t,qualified);ck(a.status==="PARTIAL"&&Object.keys(a.ports).length===1&&!a.commitAllowed,"unknown text");counts.controls++}
 ck(!validate(r,s,"把生活费改为4000美元",qualified),"source drift");counts.controls++;
 ck(!validate({...r,commitAllowed:true},s,text,qualified),"tamper");counts.controls++;
 ck(!validate({...r,rows:r.rows.slice(0,1)},s,text,qualified),"omission");counts.controls++;
 ck(!validate(r,{...next,version:1},text,qualified),"same version mutated input");counts.controls++;
 return {counts,witnesses};
};
console.log(JSON.stringify(probe(),null,2));
```

实际输出：
```json
{
  "counts": {
    "texts": 72,
    "cases": 17496,
    "portChecks": 87480,
    "invariantPorts": 78609,
    "variablePorts": 8871,
    "ambiguousCases": 11664,
    "ambiguousAllDecisionInvariant": 8772,
    "ambiguousPreferredInvariant": 9006,
    "winnerOnlyHidesFeasibility": 234,
    "globalBlockLostDecisionPorts": 37785,
    "firstWorldWrongPorts": 8871,
    "questionChecks": 139968,
    "irrelevantDimensionPorts": 46479,
    "descriptionOnly": 3,
    "controls": 15
  },
  "witnesses": {
    "allStable": {
      "text": "把生活费增加到4000美元",
      "s": {
        "version": 1,
        "limits": {
          "living": 5000,
          "rent": 7000
        },
        "cost": {
          "A": {
            "living": 3500,
            "rent": 3500
          },
          "B": {
            "living": 3500,
            "rent": 3500
          }
        },
        "utility": {
          "A": 1,
          "B": 0
        }
      },
      "ports": {
        "costDifference": {
          "status": "DESCRIPTIVE",
          "value": 0
        },
        "feasibleA": {
          "status": "INVARIANT_CONDITIONAL",
          "value": true
        },
        "feasibleB": {
          "status": "INVARIANT_CONDITIONAL",
          "value": true
        },
        "feasibleSet": {
          "status": "INVARIANT_CONDITIONAL",
          "value": [
            "A",
            "B"
          ]
        },
        "preferred": {
          "status": "INVARIANT_CONDITIONAL",
          "value": [
            "A"
          ]
        }
      },
      "relevant": {
        "feasibleA": [],
        "feasibleB": [],
        "feasibleSet": [],
        "preferred": []
      }
    },
    "winnerOnly": {
      "text": "把生活费增加到6000美元",
      "s": {
        "version": 1,
        "limits": {
          "living": 5000,
          "rent": 7000
        },
        "cost": {
          "A": {
            "living": 3500,
            "rent": 3500
          },
          "B": {
            "living": 5500,
            "rent": 3500
          }
        },
        "utility": {
          "A": 1,
          "B": 0
        }
      },
      "ports": {
        "costDifference": {
          "status": "DESCRIPTIVE",
          "value": 2000
        },
        "feasibleA": {
          "status": "INVARIANT_CONDITIONAL",
          "value": true
        },
        "feasibleB": {
          "status": "VARIES",
          "values": [
            true,
            false
          ]
        },
        "feasibleSet": {
          "status": "VARIES",
          "values": [
            [
              "A",
              "B"
            ],
            [
              "A"
            ]
          ]
        },
        "preferred": {
          "status": "INVARIANT_CONDITIONAL",
          "value": [
            "A"
          ]
        }
      },
      "relevant": {
        "feasibleA": [],
        "feasibleB": [
          "op"
        ],
        "feasibleSet": [
          "op"
        ],
        "preferred": []
      }
    },
    "futureDrift": {
      "text": "把预算改为4000美元",
      "before": {
        "status": "INVARIANT_CONDITIONAL",
        "value": [
          "A",
          "B"
        ]
      },
      "after": {
        "status": "VARIES",
        "values": [
          [
            "A"
          ],
          [
            "A",
            "B"
          ]
        ]
      }
    }
  }
}
```

## 接入与后续
下一轮优先研究自主知识表示及证据资格的连接（先查既有知识检索、调度、证据版本研究），把已经解析的语义目标和缺口转化为本地知识检索及科学方法候选。当前端口研究需要和第64轮真实语义候选、第63轮数学域、第58轮原文义务及第27轮原生出口接入，未实现。产品轨负责极简条件呈现与唯一交接，独立验收轨另冻未见文本和用户场景。未修改生产、训练、CI、Codex任务、PR合并、部署、个人数据或第三方AI运行时，零新增费用，冻结协议不变。