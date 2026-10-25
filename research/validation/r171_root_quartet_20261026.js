// R171 exact source tree root/quartet audit. node r171_root_quartet_20261026.js path/to/summary.trees
const fs=require("fs");
function audit(source){
 const err=s=>{throw Error(s)};if(!source.startsWith("#NEXUS\nBEGIN TREES;\ntree summary = [&R] "))err("header");
 const t=source.slice(source.indexOf("[&R] ")+5,source.indexOf(";\nEND;")).trim();let p=0;const nodes=[],edges=[],names=new Map();
 function parse(parent=-1){const id=nodes.length;nodes.push({parent,name:null,w:0});if(t[p]==="("){p++;while(true){parse(id);if(t[p]===","){p++;continue}if(t[p]===")"){p++;break}err("separator at "+p)}}else{let a=p;while(p<t.length&&!":,()".includes(t[p]))p++;let n=t.slice(a,p);if(!n||names.has(n))err("leaf "+n);names.set(n,id);nodes[id].name=n}
 if(t[p]===":"){p++;let a=p;while(p<t.length&&/[0-9.eE+-]/.test(t[p]))p++;let raw=t.slice(a,p),v=Number(raw)*1000000;if(!/^\d+(\.\d+)?([eE][+-]?\d+)?$/.test(raw)||!Number.isSafeInteger(Math.round(v))||Math.abs(v-Math.round(v))>1e-7||v<0)err("edge "+raw);nodes[id].w=Math.round(v)}if(parent>=0)edges.push([parent,id,nodes[id].w]);return id}
 const root=parse();if(p!==t.length)err("trailing "+t.slice(p,p+30));
 const tips=[...names.keys()].sort(),adj=nodes.map(()=>[]);for(const [u,v,w] of edges){adj[u].push([v,w]);adj[v].push([u,w])}
 if(tips.length!==400||nodes.length!==756||edges.length!==755||edges.filter(x=>x[2]===0).length!==52)err("source structure "+[tips.length,nodes.length,edges.length]);
 function rooted(r){const parent=Array(nodes.length).fill(-1),depth=Array(nodes.length).fill(0),level=Array(nodes.length).fill(0),seen=new Set([r]),stack=[r];while(stack.length){const u=stack.pop();for(const [v,w] of adj[u])if(!seen.has(v)){seen.add(v);parent[v]=u;depth[v]=depth[u]+w;level[v]=level[u]+1;stack.push(v)}}if(seen.size!==nodes.length)err("disconnected");
 const up=[parent];for(let k=1;(1<<k)<=nodes.length;k++)up[k]=up[k-1].map(v=>v<0?-1:up[k-1][v]);
 function lca(a,b){if(level[a]<level[b])[a,b]=[b,a];let dif=level[a]-level[b],k=0;while(dif){if(dif&1)a=up[k][a];dif>>=1;k++}if(a===b)return a;for(k=up.length-1;k>=0;k--)if(up[k][a]!==up[k][b]){a=up[k][a];b=up[k][b]}return parent[a]}
 return {depth,dist:(a,b)=>depth[a]+depth[b]-2*depth[lca(a,b)]}}
 const r0=rooted(root),r1=rooted(names.get(tips[0])),d=Array.from({length:400},()=>Array(400).fill(0));let equal=0;
 for(let i=0;i<400;i++)for(let j=i+1;j<400;j++){const a=names.get(tips[i]),b=names.get(tips[j]),v=r0.dist(a,b);if(v!==r1.dist(a,b))err("reroot mismatch");d[i][j]=d[j][i]=v;equal++}
 const pair=(a,b)=>d[tips.indexOf(a)][tips.indexOf(b)];
 const frozen=[["SquliqAtayal","CiuliAtayal",2644574],["SquliqAtayal","Sediq",5947138],["Saisiat","Pazeh",5992084],["Pazeh","Thao",5992084],["Bali","Sasak",3795798],["MalayBahasaIndonesia","Melayu",344650],["Kanakanabu","Saaroa",10696],["Rukai","Tsou",3471426],["OldChinese","Buyang",6345432]];
 for(const [a,b,v] of frozen)if(pair(a,b)!==v)err("frozen pair "+a+" "+b+" "+pair(a,b));
 const depth=tips.map(x=>r0.depth[names.get(x)]).sort((a,b)=>a-b);
 let skip=0,res=0,unres=0,example=null;for(let k=0;k<1024;k++){const ix=[(k*37+3)%400,(k*71+19)%400,(k*113+41)%400,(k*157+67)%400];if(new Set(ix).size!==4){skip++;continue}const [a,b,c,e]=ix;const sums=[d[a][b]+d[c][e],d[a][c]+d[b][e],d[a][e]+d[b][c]],sorted=[...sums].sort((x,y)=>x-y);if(sorted[1]!==sorted[2])err("fourpoint "+k);if(sorted[0]===sorted[2])unres++;else{res++;if(!example)example={k,labels:ix.map(i=>tips[i]),sums}}}
 if(!example)err("no resolved quartet");
 const uf=Array.from({length:400},(_,i)=>i),find=x=>uf[x]===x?x:(uf[x]=find(uf[x]));let zero=0;for(let i=0;i<400;i++)for(let j=i+1;j<400;j++)if(d[i][j]===0){zero++;let a=find(i),b=find(j);if(a!==b)uf[b]=a}const g=new Map();for(let i=0;i<400;i++){const a=find(i);g.set(a,(g.get(a)||0)+1)}const groups=[...g.values()].filter(x=>x>1).sort((a,b)=>b-a);
 const edge=edges.find(e=>e[2]>0),[eu,ev,ew]=edge,comp=new Set([eu]),stack=[eu];while(stack.length){const u=stack.pop();for(const [v] of adj[u])if(!((u===eu&&v===ev)||(u===ev&&v===eu))&&!comp.has(v)){comp.add(v);stack.push(v)}}
 const x=tips.find(a=>comp.has(names.get(a))),y=tips.find(a=>!comp.has(names.get(a)));if(!x||!y)err("mutant no crossing tips");const old=pair(x,y);let sum=0,seen=new Set([names.get(x)]),q=[[names.get(x),0]];while(q.length){const [u,dd]=q.pop();if(u===names.get(y)){sum=dd;break}for(const [v,w] of adj[u])if(!seen.has(v)){seen.add(v);q.push([v,dd+w+((u===eu&&v===ev)||(u===ev&&v===eu)?1:0)])}}if(sum-old!==1)err("edge mutant");
 const sm=[...example.sums],mx=Math.max(...sm);sm[sm.indexOf(mx)]++;sm.sort((a,b)=>a-b);if(sm[1]===sm[2])err("quartet mutant");
 return {source_chars:source.length,tree_tips:tips.length,nodes:nodes.length,edges:edges.length,zero_length_edges:52,reroot_label:tips[0],root_tip_depth_micro:{min:depth[0],median_lower:depth[199],median_upper:depth[200],max:depth[399],range:depth[399]-depth[0]},reroot_tip_depth_micro:{min:Math.min(...tips.map(x=>r1.depth[names.get(x)])),max:Math.max(...tips.map(x=>r1.depth[names.get(x)]))},exact_equal_unordered_pair_distances:equal,nine_frozen_pairs_exact_equal:true,quartets:{attempts:1024,skipped:skip,valid:1024-skip,resolved:res,unresolved:unres,first_resolved:example},zero_distance_distinct_tip_pairs:zero,zero_distance_group_sizes:groups,negative_controls:{one_micro_positive_edge_mutation_detected:true,mutated_edge:edge,crossing_pair:[x,y],original_distance_micro:old,mutated_distance_micro:sum,one_micro_quartet_sum_mutation_detected:true},source_parser_note:"scientific notation e-06 handled exactly at integer micro-millennia",scientific_grade:"E1_SOURCE_DESCRIPTIVE_INTERNAL",new_E2:0,new_E3:0,external_replications:0}
}
if(!process.argv[2])throw Error("Specify archived source summary.trees");
console.log(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8")),null,2));
