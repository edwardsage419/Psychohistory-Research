# 自主认知：外部真实开发集的联合词边界与依存关系端点候选
2026-11-26。RESEARCH_CANDIDATE / EXTERNAL_DEVELOPMENT_BYTES_VERIFIED / REUSED_RESEARCH_CODE_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与去重
固定main dd30e2d3eed3b458dba632d06f904d7d92221669，核对20近期提交、15开放Draft PR、v3.2、同步规程、唯一交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）及完整目录树相关题名。#63仍Draft，head 734686980b19da9291bdd08b67d4e2519c011acf，未重跑。读取R134结构审计 db9cc100d96d49832fe32879a706f63830301773、R137非投射解码 0218ff41ee8fd68e5df1b2886cdfbee3368c8426、原文格 86dcd5387b89c5302b1c139ad57a17b22f5d5a1d、静态词典 6eb499cc01f023f352167cbe886d2f3144136cc7、联合分词预算 cee6b6f8d759b6aa33ec4f2863232a6583f8ae07。R136/137在金标分词及UPOS上解码，前轮联合分词研究整句覆盖，已有角色跨度联合预算。本轮新增无金标输入的分词边依存关系端点对、同路径可行性及给定依存词跨度的候选头排名诊断；不重新计整句分词或声称依存树解析。未做全库无重复证明。
## 来源及许可
UD Chinese GSDSimp固定commit b79a1c2f7ba7f9b264808d91c6886a67b7f847a3，dev blob af8cc878e7934b38ce3c1a266053100e7c47de6f。CC-CEDICT镜像 rhcarvalho/cedict固定commit 6317ff202e14be60365c826f62e45fc9fa71d19e，blob d7fee8237f26524b38eee220647e4c5d79f00de9。实际重新读取两blob并用R134已审阅Git SHA1实现独立复算两者字节长度及身份一致。许可沿用既有英文官方来源及固定README/LICENSE记录（本轮未重读许可全文）：https://universaldependencies.org/treebanks/zh_gsdsimp/ ，https://www.mdbg.net/chinese/dictionary?page=cc-cedict 。CC BY-SA 4.0许可与wiki原始文本权利分离；词典及语料衍生分发须另审。只做已见公开dev聚合非训练诊断，未读取train/test、复制第三方词条/正文、训练或派生权重。不是用户决策对话或独立留出。连接器返回项目源码blob与固定值匹配；仅执行自有已审阅固定JS，外部文本按数据解析。
## 数学与方法
复用前轮expanded原文词边界格（词典头词和结构边、单字兜底、未知跨度成本1+8*长度、Unicode标量、最大16，空白跳过），不输入FORM/UPOS/HEAD。全点对前向DAG最短路D(i,j)，原最优D(0,n)。对两不重叠词边 a=(i,j), b=(k,l), j<=k，共同包含的最低路径成本恰为D(0,i)+c(a)+D(j,k)+c(b)+D(l,n)。证明：任一共同路径分解为这五部分，分别不低于最短路；拼接对应最短路可取得下界。减原最优得到联合松弛，必不小于各边单独松弛。先枚举单边松弛<=32，再按预算0/2/8/32枚举两方向依存端点假设；联合不合格丢弃。没有POS或语义关系分类，方向均保留；两端点同一路径可行不意味着所有弧共树可行，无单根、无环、全树兼容性或语言解析证明。评分按依存词跨度条件比较候选头：gap为两边间字符距离，cost为联合松弛，两个排序为gap优先及cost后gap优先；同分字符串顺序。K=1/3/5/10；不是概率、完整原生预测或自动理解。给定金标依存词跨度仅用于评估对应候选头排名，明确oracle诊断。所有候选先生成再对照gold端点及原标注关系nsubj/obj/advcl（按冒号前缀）与全部非根弧；advcl不必然条件，不测主体语义/条件方向、角色分类或精度。边对计数包含两方向，重叠边不进入边际对统计；同一原文多种边和重复预算非独立样本。所有候选无操作权。实际完整构造候选后排序，最短路矩阵及二次边对空间开销未测设备性能，不能当生产预算。
## 实际结果
标准JS连接器执行。500句12665词元全部严格对齐。短串直接枚举完整路径核对共同端点最小成本，所有候选核对联合不低于边际；报告每预算的端点边际覆盖、联合覆盖、给定正确依存词的候选头排名。计数聚合，无第三方原文或词条。
```json
{
  "sentences": 500,
  "tokens": 12665,
  "words": 121696,
  "sourceBytes": 1195378,
  "dictBytes": 9881659,
  "metrics": {
    "0": {
      "marginalPairs": 409976,
      "jointPairs": 409540,
      "overBudgetPairs": 436,
      "relation": {
        "nsubj": {
          "targets": 956,
          "endpointCoverage": 615,
          "jointCoverage": 615,
          "rankedGap": {
            "1": 29,
            "3": 236,
            "5": 322,
            "10": 457
          },
          "rankedCost": {
            "1": 29,
            "3": 236,
            "5": 322,
            "10": 457
          }
        },
        "obj": {
          "targets": 818,
          "endpointCoverage": 560,
          "jointCoverage": 560,
          "rankedGap": {
            "1": 134,
            "3": 198,
            "5": 340,
            "10": 490
          },
          "rankedCost": {
            "1": 134,
            "3": 198,
            "5": 340,
            "10": 490
          }
        },
        "advcl": {
          "targets": 446,
          "endpointCoverage": 324,
          "jointCoverage": 324,
          "rankedGap": {
            "1": 3,
            "3": 39,
            "5": 66,
            "10": 162
          },
          "rankedCost": {
            "1": 3,
            "3": 39,
            "5": 66,
            "10": 162
          }
        },
        "all": {
          "targets": 12165,
          "endpointCoverage": 8343,
          "jointCoverage": 8338,
          "rankedGap": {
            "1": 1458,
            "3": 4040,
            "5": 5240,
            "10": 6775
          },
          "rankedCost": {
            "1": 1458,
            "3": 4040,
            "5": 5240,
            "10": 6775
          }
        }
      }
    },
    "2": {
      "marginalPairs": 1573730,
      "jointPairs": 1479328,
      "overBudgetPairs": 94402,
      "relation": {
        "nsubj": {
          "targets": 956,
          "endpointCoverage": 819,
          "jointCoverage": 819,
          "rankedGap": {
            "1": 11,
            "3": 195,
            "5": 296,
            "10": 448
          },
          "rankedCost": {
            "1": 33,
            "3": 293,
            "5": 395,
            "10": 553
          }
        },
        "obj": {
          "targets": 818,
          "endpointCoverage": 730,
          "jointCoverage": 729,
          "rankedGap": {
            "1": 140,
            "3": 194,
            "5": 245,
            "10": 467
          },
          "rankedCost": {
            "1": 140,
            "3": 223,
            "5": 389,
            "10": 572
          }
        },
        "advcl": {
          "targets": 446,
          "endpointCoverage": 404,
          "jointCoverage": 400,
          "rankedGap": {
            "1": 1,
            "3": 19,
            "5": 41,
            "10": 86
          },
          "rankedCost": {
            "1": 3,
            "3": 39,
            "5": 70,
            "10": 175
          }
        },
        "all": {
          "targets": 12165,
          "endpointCoverage": 10893,
          "jointCoverage": 10877,
          "rankedGap": {
            "1": 1530,
            "3": 3986,
            "5": 5239,
            "10": 7097
          },
          "rankedCost": {
            "1": 1711,
            "3": 5018,
            "5": 6362,
            "10": 8083
          }
        }
      }
    },
    "8": {
      "marginalPairs": 1640518,
      "jointPairs": 1636490,
      "overBudgetPairs": 4028,
      "relation": {
        "nsubj": {
          "targets": 956,
          "endpointCoverage": 821,
          "jointCoverage": 821,
          "rankedGap": {
            "1": 11,
            "3": 191,
            "5": 294,
            "10": 443
          },
          "rankedCost": {
            "1": 33,
            "3": 294,
            "5": 396,
            "10": 554
          }
        },
        "obj": {
          "targets": 818,
          "endpointCoverage": 731,
          "jointCoverage": 731,
          "rankedGap": {
            "1": 140,
            "3": 192,
            "5": 244,
            "10": 462
          },
          "rankedCost": {
            "1": 140,
            "3": 223,
            "5": 390,
            "10": 573
          }
        },
        "advcl": {
          "targets": 446,
          "endpointCoverage": 404,
          "jointCoverage": 404,
          "rankedGap": {
            "1": 1,
            "3": 19,
            "5": 40,
            "10": 86
          },
          "rankedCost": {
            "1": 3,
            "3": 39,
            "5": 70,
            "10": 175
          }
        },
        "all": {
          "targets": 12165,
          "endpointCoverage": 10940,
          "jointCoverage": 10940,
          "rankedGap": {
            "1": 1495,
            "3": 3950,
            "5": 5207,
            "10": 7077
          },
          "rankedCost": {
            "1": 1712,
            "3": 5037,
            "5": 6382,
            "10": 8106
          }
        }
      }
    },
    "32": {
      "marginalPairs": 12736750,
      "jointPairs": 7516950,
      "overBudgetPairs": 5219800,
      "relation": {
        "nsubj": {
          "targets": 956,
          "endpointCoverage": 952,
          "jointCoverage": 951,
          "rankedGap": {
            "1": 17,
            "3": 71,
            "5": 162,
            "10": 322
          },
          "rankedCost": {
            "1": 41,
            "3": 313,
            "5": 422,
            "10": 599
          }
        },
        "obj": {
          "targets": 818,
          "endpointCoverage": 816,
          "jointCoverage": 816,
          "rankedGap": {
            "1": 23,
            "3": 134,
            "5": 181,
            "10": 228
          },
          "rankedCost": {
            "1": 159,
            "3": 247,
            "5": 421,
            "10": 611
          }
        },
        "advcl": {
          "targets": 446,
          "endpointCoverage": 446,
          "jointCoverage": 446,
          "rankedGap": {
            "1": 0,
            "3": 4,
            "5": 18,
            "10": 42
          },
          "rankedCost": {
            "1": 4,
            "3": 45,
            "5": 79,
            "10": 190
          }
        },
        "all": {
          "targets": 12165,
          "endpointCoverage": 12103,
          "jointCoverage": 12092,
          "rankedGap": {
            "1": 462,
            "3": 1987,
            "5": 3576,
            "10": 5456
          },
          "rankedCost": {
            "1": 1844,
            "3": 5395,
            "5": 6798,
            "10": 8604
          }
        }
      }
    }
  },
  "controls": 51,
  "distChecks": 6368375
}
```
## 局限及下游
研究者选定预算、词典代价、关系类别、排序和评价口径。若排序无明显改善，保留负面结果，后续研究全树共同分词及结构候选、真实主体与条件义务、独立开发来源及原生入口，不能继续把候选覆盖称为理解准确率。实际未执行训练、原生产品、真实用户、独立留出、设备、CI、生产修改、唯一交接修改、PR合并、部署或新增费用；未启动Codex或变更历史证据等级/冻结协议。
## 完整复算
固定R134与前轮联合分词报告全文首个js代码块作为ac/gc，固定语料/词典UTF8作为raw/dict。Node标准JS。核心实际连接器运行；下面文件读取包装未另跑。
```js
const fs=require("node:fs");
const [raw,dict,auditDoc,graphDoc]=process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"));
const code=s=>s.split("\x60\x60\x60js\n")[1].split("\n\x60\x60\x60")[0];
function experiment(raw,dict,ac,gc){
 const ck=(x,m)=>{if(!x)throw Error(m)},audit=Function(ac.split("console.log(JSON.stringify(audit(raw)")[0]+"\nreturn audit;")();let verified=audit(raw);
 const G=Function("dict","const ck=(x,m)=>{if(!x)throw Error(m)};\n"+gc.slice(gc.indexOf("const words=new Set()"),gc.indexOf("function analyze(g)"))+"\nreturn {graph,cls,words};")(dict);
 const hash=Function(ac.slice(ac.indexOf(" function utf("),ac.indexOf(" const bytes=utf(raw)"))+"\nreturn s=>{let b=utf(s);return {bytes:b.length,sha:sha1(utf('blob '+b.length+'\\0').concat(b))}};")();
 let dh=hash(dict);ck(dh.sha==="d7fee8237f26524b38eee220647e4c5d79f00de9"&&dh.bytes===9881659,"dict bytes");
 const budgets=[0,2,8,32],kvals=[1,3,5,10],rels=["nsubj","obj","advcl","all"],blank=()=>({targets:0,endpointCoverage:0,jointCoverage:0,rankedGap:Object.fromEntries(kvals.map(k=>[k,0])),rankedCost:Object.fromEntries(kvals.map(k=>[k,0]))});
 let out={sentences:0,tokens:0,words:G.words.size,sourceBytes:verified.bytes,dictBytes:dh.bytes,metrics:Object.fromEntries(budgets.map(b=>[b,{marginalPairs:0,jointPairs:0,overBudgetPairs:0,relation:Object.fromEntries(rels.map(r=>[r,blank()]))}])),controls:0,distChecks:0};
 function distances(g){let n=g.length,ds=Array.from({length:n+1},()=>Array(n+1).fill(Infinity));for(let a=0;a<=n;a++){ds[a][a]=0;for(let i=a;i<n;i++)if(Number.isFinite(ds[a][i]))for(let e of g[i])ds[a][e.j]=Math.min(ds[a][e.j],ds[a][i]+e.c)}return ds}
 const key=e=>e.i+":"+e.j;
 function evaluate(c,rows,gold){
  let g=G.graph(c,true),n=c.length,ds=distances(g),base=ds[0][n];let es=g.flatMap((v,i)=>v.filter(e=>!e.skip).map(e=>({i,j:e.j,c:e.c,m:ds[0][i]+e.c+ds[e.j][n]-base}))).filter(e=>e.m<=32),m=new Map(es.map(e=>[key(e),e]));
  const joint=(a,b)=>{if(a.i>b.i)[a,b]=[b,a];if(a.j>b.i)return Infinity;return ds[0][a.i]+a.c+ds[a.j][b.i]+b.c+ds[b.j][n]-base};
  let per=Object.fromEntries(budgets.map(b=>[b,new Map()]));
  // Generate from raw text and fixed lexicon only. Undirected geometric pairs become both directed hypotheses.
  for(let a of es)for(let b of es){if(a.j>b.i)continue;let v=joint(a,b);ck(v>=Math.max(a.m,b.m),"joint dominance");out.distChecks++;
    for(let B of budgets){if(a.m>B||b.m>B)continue;let q=out.metrics[B];q.marginalPairs+=2;if(v>B){q.overBudgetPairs+=2;continue}q.jointPairs+=2;
      for(let [d,h] of [[a,b],[b,a]]){let map=per[B],id=key(d);if(!map.has(id))map.set(id,[]);map.get(id).push({h:key(h),gap:Math.max(a.i-b.j,b.i-a.j,0),cost:v})}
    }
  }
  for(let B of budgets)for(let a of per[B].values()){a.sort((x,y)=>x.gap-y.gap||x.h.localeCompare(y.h));a.forEach((x,i)=>x.rg=i+1);a.sort((x,y)=>x.cost-y.cost||x.gap-y.gap||x.h.localeCompare(y.h));a.forEach((x,i)=>x.rc=i+1)}
  for(let i=0;i<rows.length;i++){let r=rows[i],head=Number(r[6]),rel=r[7].split(":")[0];if(!head)continue;let d=gold[i],h=gold[head-1],a=m.get(key(d)),b=m.get(key(h));let kinds=rels.includes(rel)&&rel!=="all"?[rel,"all"]:["all"];
   for(let B of budgets){let rr=per[B].get(key(d))?.find(x=>x.h===key(h));for(let k of kinds){let q=out.metrics[B].relation[k];q.targets++;q.endpointCoverage+=+(!!a&&!!b&&a.m<=B&&b.m<=B);q.jointCoverage+=+!!rr;if(rr)for(let k of kvals){q.rankedGap[k]+=+(rr.rg<=k);q.rankedCost[k]+=+(rr.rc<=k)}}if(rr)ck(a&&b&&joint(a,b)<=B,"gold joint")}
  }
 }
 for(let block of raw.trimEnd().split(/\n\n+/)){let lines=block.split("\n"),c=[...lines.find(l=>l.startsWith("# text = ")).slice(9)],rows=lines.filter(l=>!l.startsWith("#")).map(l=>l.split("\t")).filter(x=>/^[1-9]\d*$/.test(x[0])),gold=[],i=0;
  for(let r of rows){while(G.cls(c[i]??"")==="s")i++;let a=[...r[1]];ck(a.every((v,k)=>v===c[i+k]),"align");gold.push({i,j:i+a.length});i+=a.length}while(G.cls(c[i]??"")==="s")i++;ck(i===c.length,"end");out.sentences++;out.tokens+=rows.length;evaluate(c,rows,gold)
 }
 // direct exhaustive path oracle for small graphs and every nonoverlapping pair.
 for(let s of ["研究生命","南京市长","甲 乙","12.5","A𠀀B"]){let g=G.graph([...s],true),ds=distances(g),n=g.length,paths=[];function walk(i,c,es){if(i===n){paths.push({c,es});return}for(let e of g[i])walk(e.j,c+e.c,[...es,key({i,j:e.j})])}walk(0,0,[]);let edges=g.flatMap((a,i)=>a.filter(e=>!e.skip).map(e=>({i,...e})));for(let a of edges)for(let b of edges)if(a.j<=b.i){let expected=Math.min(...paths.filter(p=>p.es.includes(key(a))&&p.es.includes(key(b))).map(p=>p.c));ck(expected===ds[0][a.i]+a.c+ds[a.j][b.i]+b.c+ds[b.j][n],"joint brute");out.controls++}}
 ck(out.sentences===500&&out.tokens===12665,"totals");for(let B of budgets){let q=out.metrics[B];ck(q.jointPairs+q.overBudgetPairs===q.marginalPairs,"pair partition");for(let r of Object.values(q.relation))ck(r.jointCoverage<=r.endpointCoverage&&r.endpointCoverage<=r.targets,"coverage");}
 return out
}
console.log(JSON.stringify(experiment(raw,dict,code(auditDoc),code(graphDoc)),null,2));
```
