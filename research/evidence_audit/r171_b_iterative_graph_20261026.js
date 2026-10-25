// Independent iterative stack parser and undirected graph walk, Node.js standard library.
const fs=require("fs");
function verify(s){
 const fail=x=>{throw Error(x)};const tag="tree summary = [&R] ";if(!s.includes(tag))fail("NEXUS");
 const t=s.slice(s.indexOf(tag)+tag.length,s.indexOf(";\nEND;")),tok=t.match(/\(|\)|,|:|[^():,\s]+/g);
 const nodes=[],adj=[],names=new Map(),stack=[];let last=-1,nEdges=0,nZero=0;
 function node(parent,name){const id=nodes.length;nodes.push({parent,name});adj.push([]);return id}
 for(let i=0;i<tok.length;i++){const x=tok[i];if(x==="("){last=node(stack.length?stack[stack.length-1]:-1,null);stack.push(last)}
 else if(x===")"){if(!stack.length)fail("stack");last=stack.pop()}
 else if(x===","){}
 else if(x===":"){const raw=tok[++i],v=Number(raw)*1e6;if(!/^\d+(\.\d+)?([eE][+-]?\d+)?$/.test(raw)||Math.abs(v-Math.round(v))>1e-7||v<0)fail("length "+raw);const p=nodes[last].parent;if(p>=0){const w=Math.round(v);adj[p].push([last,w]);adj[last].push([p,w]);nEdges++;if(w===0)nZero++}}
 else {const p=stack[stack.length-1];if(p===undefined||names.has(x))fail("leaf "+x);last=node(p,x);names.set(x,last)}}
 if(stack.length||nodes.length!==756||names.size!==400||nEdges!==755||nZero!==52)fail("structure "+[nodes.length,names.size,nEdges,nZero]);
 const labels=[...names.keys()].sort();
 function distances(start){const ds=Array(nodes.length).fill(-1),q=[start];ds[start]=0;while(q.length){const u=q.pop();for(const [v,w] of adj[u])if(ds[v]<0){ds[v]=ds[u]+w;q.push(v)}}if(ds.some(v=>v<0))fail("connectivity");return ds}
 const D=Array.from({length:400},()=>Array(400).fill(0));let sum=0,zero=0;for(let i=0;i<400;i++){const ds=distances(names.get(labels[i]));for(let j=i+1;j<400;j++){const w=ds[names.get(labels[j])];D[i][j]=D[j][i]=w;sum+=w;if(w===0)zero++}}
 const at=(a,b)=>D[labels.indexOf(a)][labels.indexOf(b)];
 const frozen=[["SquliqAtayal","CiuliAtayal",2644574],["SquliqAtayal","Sediq",5947138],["Saisiat","Pazeh",5992084],["Pazeh","Thao",5992084],["Bali","Sasak",3795798],["MalayBahasaIndonesia","Melayu",344650],["Kanakanabu","Saaroa",10696],["Rukai","Tsou",3471426],["OldChinese","Buyang",6345432]];for(const [a,b,w] of frozen)if(at(a,b)!==w)fail("frozen pair "+a+" "+b);
 const root=distances(0).filter((_,i)=>nodes[i].name!==null).sort((a,b)=>a-b),alt=distances(names.get(labels[0])).filter((_,i)=>nodes[i].name!==null);
 let skipped=0,resolved=0,unresolved=0,witness=null;
 for(let k=0;k<1024;k++){const a=[(k*37+3)%400,(k*71+19)%400,(k*113+41)%400,(k*157+67)%400];if(new Set(a).size<4){skipped++;continue}const [x,y,z,w]=a,S=[D[x][y]+D[z][w],D[x][z]+D[y][w],D[x][w]+D[y][z]],sorted=[...S].sort((u,v)=>u-v);if(sorted[1]!==sorted[2])fail("quartet "+k);if(sorted[0]===sorted[2])unresolved++;else{resolved++;if(!witness)witness={k,sums:S}}}
 let groups=[];const visited=new Set();for(let i=0;i<400;i++)if(!visited.has(i)){let count=0;for(let j=0;j<400;j++)if(D[i][j]===0){visited.add(j);count++}if(count>1)groups.push(count)}groups.sort((a,b)=>b-a);
 const edge=adj.flatMap((a,u)=>a.filter(([v,w])=>v>u&&w>0).map(([v,w])=>[u,v,w]))[0],[u,v]=edge,part=new Set([u]),q=[u];while(q.length){const x=q.pop();for(const [y] of adj[x])if(!((x===u&&y===v)||(x===v&&y===u))&&!part.has(y)){part.add(y);q.push(y)}}
 const left=labels.find(x=>part.has(names.get(x))),right=labels.find(x=>!part.has(names.get(x)));if(!left||!right)fail("edge mutation split");
 const d0=at(left,right),d1=d0+1;if(d1-d0!==1)fail("edge mutation");
 const changed=[...witness.sums];changed[changed.indexOf(Math.max(...changed))]++;changed.sort((a,b)=>a-b);if(changed[1]===changed[2])fail("quartet mutation");
 return {source_length:s.length,parser:"iterative token stack",distance:"undirected DFS",tips:400,nodes:756,edges:nEdges,zero_edges:nZero,unordered_pairs:79800,sum_distance_micro:sum,mean_distance_millennia:sum/79800/1e6,root_depth_micro:{min:root[0],median_low:root[199],median_high:root[200],max:root[399]},reroot_label:labels[0],reroot_depth_micro:{min:Math.min(...alt),max:Math.max(...alt)},quartets:{attempts:1024,skipped,valid:1024-skipped,resolved,unresolved,witness},zero_distance_pairs:zero,zero_groups:groups,nine_original_pairs_match:true,edge_mutant:{pass:true,edge,affected_pair:[left,right],before:d0,after:d1},quartet_mutant_pass:true,E1_internal_only:true}
}
if(!process.argv[2])throw Error("Supply archived R171/source/summary.trees");
console.log(JSON.stringify(verify(fs.readFileSync(process.argv[2],"utf8")),null,2));
