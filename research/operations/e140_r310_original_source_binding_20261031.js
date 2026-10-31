// E140: original R310 416 directed source events versus S106 48-world receipt.
// Run: node e140_r310_original_source_binding_20261031.js SOURCE.csv S106.csv
// All source records are artificial. No paid API, user data or external dependencies.
function csvParse(text){
  const lines=text.trim().split(/\r?\n/);const parse=line=>{let a=[],v="",q=false;
    for(let i=0;i<line.length;i++){let c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){v+='"';i++;}else q=!q;}
    else if(c===','&&!q){a.push(v);v="";}else v+=c;}
    if(q)throw Error("unclosed CSV quote");a.push(v);return a;};
  const header=parse(lines.shift());return lines.map(line=>{const v=parse(line);if(v.length!==header.length)throw Error("column count");return Object.fromEntries(header.map((h,i)=>[h,v[i]]));});
}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let c=a%b;a=b;b=c;}return a||1n;}
function f(v){let p=String(v).split("/"),n=BigInt(p[0]),d=BigInt(p[1]||1);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return f((a[0]*b[1]+b[0]*a[1])+"/"+(a[1]*b[1]));}
function mul(a,b){return f((a[0]*b[0])+"/"+(a[1]*b[1]));}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1];}
function auditRows(src,ext){
 const edges={PATH4:[[0,1],[1,2],[2,3]],CYCLE4:[[0,1],[1,2],[2,3],[0,3]],
 COMPLETE4:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]};
 if(src.length!==416||ext.length!==48)throw Error("row universe");
 const ex=new Map();for(const r of ext){if(Object.keys(r).sort().join(",")!=="bits,expected_steps,graph,p_absorb_ones")throw Error("extension fields");
 const key=r.graph+"|"+r.bits;if(ex.has(key))throw Error("duplicate extension");
 ex.set(key,{q:f(r.p_absorb_ones),t:f(r.expected_steps)});}
 if(ex.size!==48)throw Error("extension size");
 let events=new Map(),seen=new Set(),sourceChecks=0;
 for(const r of src){
 const e=edges[r.graph];if(!e)throw Error("unknown graph");
 const bits=r.initial_bits.split(";").join("");const next=r.next_bits.split(";").join("");
 if(!/^[01]{4}$/.test(bits)||!/^[01]{4}$/.test(next))throw Error("bad bits");
 if(r.world!==r.graph+"|bits="+bits.split("").join(","))throw Error("source world mismatch");
 const deg=[0,0,0,0];for(const [i,j] of e){deg[i]++;deg[j]++;}
 if(r.degree_vector!==deg.join(";"))throw Error("degree vector");
 if(r.undirected_edges!==e.map(z=>z.join("-")).join(";"))throw Error("edge identity");
 const i=Number(r.target_node),j=Number(r.copied_neighbor_node);
 if(!Number.isInteger(i)||!Number.isInteger(j)||!e.some(([a,b])=>(a===i&&b===j)||(a===j&&b===i)))throw Error("neighbor identity");
 const id=r.graph+"|"+bits+"|"+i+"|"+j;
 if(seen.has(id))throw Error("duplicate directed event");seen.add(id);
 if(Number(r.neighbor_prior_bit)!==Number(bits[j])||Number(r.original_target_bit)!==Number(bits[i]))throw Error("bit metadata");
 const arr=bits.split("");arr[i]=bits[j];if(arr.join("")!==next)throw Error("next state");
 if(r.target_opinion_changed!==String(bits[i]!==bits[j]).replace("true","True").replace("false","False"))throw Error("change marker");
 const prob=f(r.directed_update_probability),expected=f("1/"+(4*deg[i]));
 if(!eq(prob,expected))throw Error("event probability");
 const density=f(bits.split("").filter(z=>z==="1").length+"/4");
 const weighted=f(bits.split("").reduce((a,z,k)=>a+Number(z)*deg[k],0)+"/"+deg.reduce((a,b)=>a+b,0));
 const nextDensity=f(next.split("").filter(z=>z==="1").length+"/4");
 const nextWeighted=f(next.split("").reduce((a,z,k)=>a+Number(z)*deg[k],0)+"/"+deg.reduce((a,b)=>a+b,0));
 if(!eq(f(r.initial_unweighted_density),density)||!eq(f(r.next_unweighted_density),nextDensity)||
 !eq(f(r.initial_degree_weighted_density),weighted)||!eq(f(r.next_degree_weighted_density),nextWeighted))throw Error("density metadata");
 const key=r.graph+"|"+bits, nxt=r.graph+"|"+next;
 if(!ex.has(key)||!ex.has(nxt))throw Error("unknown extension state");
 let v=events.get(key)||{prob:f(0),qnext:f(0),tnext:f(0),count:0};
 v.prob=add(v.prob,prob);v.qnext=add(v.qnext,mul(prob,ex.get(nxt).q));
 v.tnext=add(v.tnext,mul(prob,ex.get(nxt).t));v.count++;events.set(key,v);
 sourceChecks+=9;
 }
 if(seen.size!==416||events.size!==48)throw Error("event coverage");
 let transient=0,boundary=0,graphCounts={PATH4:0,CYCLE4:0,COMPLETE4:0};
 for(const [key,row] of ex){const [graph,bits]=key.split("|");if(!edges[graph])throw Error("extra graph");
 const v=events.get(key);if(!v||!eq(v.prob,f(1)))throw Error("probability normalization");
 graphCounts[graph]+=v.count;
 if(bits==="0000"||bits==="1111"){
   boundary++;if(!eq(row.q,f(bits==="1111"?1:0))||!eq(row.t,f(0)))throw Error("absorbing boundary");
 }else{transient++;if(!eq(row.q,v.qnext)||!eq(row.t,add(f(1),v.tnext)))throw Error("Bellman equation");}
 }
 if(transient!==42||boundary!==6||graphCounts.PATH4!==96||graphCounts.CYCLE4!==128||graphCounts.COMPLETE4!==192)throw Error("counts");
 return {source_rows:src.length,extension_worlds:ext.length,source_checks:sourceChecks,
  transient_equations:transient,boundaries:boundary,graph_event_counts:graphCounts};
}
function run(original,extension){
 const src=csvParse(original),ext=csvParse(extension),result=auditRows(src,ext);
 let mutants=0;const tries=[
 [0,r=>r[0].directed_update_probability="1/3"],
 [0,r=>r[0].next_bits="1;0;0;0"],
 [0,r=>r[0].target_node="99"],
 [0,r=>r[1]={...r[0]}],
 [0,r=>r.pop()],
 [1,r=>r[8].p_absorb_ones="1/3"],
 [1,r=>r[8].expected_steps="99"],
 [1,r=>r[8].bits="2222"]
 ];
 for(const [side,fn] of tries){const a=src.map(x=>({...x})),b=ext.map(x=>({...x}));fn(side?b:a);
  try{auditRows(a,b);throw Error("MUTANT_FALSE_ACCEPT");}catch(e){if(e.message==="MUTANT_FALSE_ACCEPT")throw e;mutants++;}}
 return {...result,mutations_rejected:mutants,status:"PASS",evidence:"NONBLIND_INTERNAL_E1",native_python_cli:"NOT_RUN"};
}
if (typeof require !== "undefined" && require.main === module) {
  const fs = require("node:fs");
  if (process.argv.length !== 4) throw Error("Usage: node script SOURCE.csv S106.csv");
  const result = run(fs.readFileSync(process.argv[2], "utf8"),
                     fs.readFileSync(process.argv[3], "utf8"));
  process.stdout.write(JSON.stringify(result) + "\n");
}
