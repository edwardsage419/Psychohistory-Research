const fs=require('fs');
function compute(data){
  function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let c=a%b;a=b;b=c;}return a;}
  class Q{constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(b===0n)throw Error("zero denominator");let g=gcd(a,b);this.a=a/g;this.b=b/g;}add(x){return new Q(this.a*x.b+x.a*this.b,this.b*x.b)}sub(x){return new Q(this.a*x.b-x.a*this.b,this.b*x.b)}abs(){return new Q(this.a<0n?-this.a:this.a,this.b)}half(){return new Q(this.a,2n*this.b)}str(){return this.b===1n?String(this.a):this.a+"/"+this.b;}}
  const z=new Q(0n);
  function q(s){const a=String(s).split("/");return new Q(a[0],a[1]||1);}
  const edges={star:[[0,1],[0,2],[0,3]],path:[[0,1],[1,2],[2,3]],cycle:[[0,1],[1,2],[2,3],[3,0]],complete:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]};
  const pop=(v)=>{let n=0;while(v){n+=v&1;v>>=1;}return n;};
  const cut=(g,s)=>edges[g].reduce((n,[a,b])=>n+(((s>>a)&1)!==((s>>b)&1)?1:0),0);
  function proj(c,g,mode){let out={};for(const [bits,v] of Object.entries(c)){const s=parseInt(bits,2),key=mode==="O1"?String(pop(s)):mode==="O2"?pop(s)+":"+cut(g,s):bits;out[key]=(out[key]||z).add(q(v));}return out;}
  function sig(p){return Object.entries(p).filter(([,v])=>v.a!==0n).sort((a,b)=>a[0].localeCompare(b[0])).map(([k,v])=>k+"="+v.str()).join("|");}
  function tv(a,b){let keys=new Set([...Object.keys(a),...Object.keys(b)]),s=z;for(let k of keys)s=s.add((a[k]||z).sub(b[k]||z).abs());return s.half().str();}
  if(data.cases.length!==72)throw Error("wrong number of worlds");
  const cases=data.cases.map((c)=>{if(!edges[c.graph]||![0,1].includes(c.seed)||c.time_distributions.length!==5)throw Error("invalid world");
    let projections={O1:[],O2:[],O3:[]};for(let t=0;t<5;t++){let dist=c.time_distributions[t];if(Object.keys(dist).length!==16)throw Error("16 states");let sum=Object.values(dist).reduce((a,v)=>a.add(q(v)),z);if(sum.str()!=="1")throw Error("normalization");for(let o of Object.keys(projections))projections[o].push(proj(dist,c.graph,o));}
    return {graph:c.graph,seed:c.seed,rate:c.rate,mechanism:c.mechanism,projections};});
  const groups={};for(const c of cases){const k=c.graph+"|"+c.seed;(groups[k]??=[]).push(c);}if(Object.keys(groups).length!==8)throw Error("group count");
  const levels=["O1","O2","O3"],by_time={},cumulative={},detail=[];
  function classify(items,lev,t,cum){const map={};for(const c of items){const s=(cum?Array.from({length:t},(_,i)=>sig(c.projections[lev][i+1])).join("~"):sig(c.projections[lev][t]));(map[s]??=[]).push(c.rate+":"+c.mechanism);}return Object.values(map).map(v=>v.sort()).sort((a,b)=>a.join().localeCompare(b.join()));}
  for(let t=1;t<=4;t++){by_time[t]={};cumulative[t]={};for(const lev of levels){let n=0,uniq=0,cumN=0,cumUniq=0;for(const [group,items] of Object.entries(groups)){let cl=classify(items,lev,t,false),cc=classify(items,lev,t,true);n+=cl.length;uniq+=cl.filter(x=>x.length===1).length;cumN+=cc.length;cumUniq+=cc.filter(x=>x.length===1).length;detail.push({group,t,observation:lev,classes:cl.length,unique_worlds:cl.filter(x=>x.length===1).length,largest_class:Math.max(...cl.map(x=>x.length)),cumulative_classes:cc.length,cumulative_unique_worlds:cc.filter(x=>x.length===1).length});}by_time[t][lev]={classes:n,unique_worlds:uniq};cumulative[t][lev]={classes:cumN,unique_worlds:cumUniq};}}
  for(let t=1;t<=4;t++){if(by_time[t].O1.classes>by_time[t].O2.classes||by_time[t].O2.classes>by_time[t].O3.classes)throw Error("information monotonicity");for(let lev of levels)if(cumulative[t][lev].classes<by_time[t][lev].classes)throw Error("cumulative monotonicity");}
  const pairs=[];for(const [group,items] of Object.entries(groups)){for(const rate of ["1/4","1/2","3/4"]){const i=items.find(x=>x.rate===rate&&x.mechanism==="invention"),d=items.find(x=>x.rate===rate&&x.mechanism==="diffusion");if(!i||!d)throw Error("missing pair");let p={group,rate,TV:{}};for(const lev of levels){p.TV[lev]=Array.from({length:4},(_,k)=>tv(i.projections[lev][k+1],d.projections[lev][k+1]));}pairs.push(p);}}
  for(const p of pairs){if(p.group==="star|0"&&levels.some(l=>p.TV[l].some(v=>v!=="0")))throw Error("star negative control");if(p.group==="path|1"&&p.TV.O3[0]==="0")throw Error("path positive control");}
  return {research:"R174",date:"2026-10-26",source_git_blob_sha1:"084a6783cdf495e5fb06390a481e38c1efe396b6",input_worlds:cases.length,groups:Object.keys(groups).length,observation_levels:levels,by_time,cumulative,per_group:detail,paired_I_D_TV:pairs,checks:{source_72x5_normalized:true,observation_information_monotone:true,star_center_negative_control:true,path_seed1_positive_control:true}};
}
if(require.main===module){const input=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(compute(input),null,2));}
module.exports={compute};
