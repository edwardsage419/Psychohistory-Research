#!/usr/bin/env node
'use strict';
// R127 source-bounded partial identification. No person-level transitions are imputed.
// Source: Van Huyck, Battalio, Beil (1990), AER 80(1), printed Table 2 pp.240-241.
// Published counts visually crosschecked; source snapshot pinned below.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const SOURCE_BLOB='6964fa57e291e719e8cc071cc3a70d73836363e4';
const TABLE2={
  "1": {
    "n": 16,
    "first": [
      8,
      3,
      2,
      1,
      1,
      1,
      0
    ],
    "last": [
      1,
      0,
      0,
      0,
      1,
      1,
      13
    ]
  },
  "2": {
    "n": 16,
    "first": [
      4,
      1,
      3,
      4,
      1,
      3,
      0
    ],
    "last": [
      1,
      0,
      1,
      0,
      0,
      1,
      13
    ]
  },
  "3": {
    "n": 14,
    "first": [
      4,
      2,
      5,
      3,
      0,
      0,
      0
    ],
    "last": [
      2,
      0,
      0,
      1,
      0,
      2,
      9
    ]
  },
  "4": {
    "n": 15,
    "first": [
      6,
      0,
      8,
      1,
      0,
      0,
      0
    ],
    "last": [
      0,
      0,
      0,
      0,
      0,
      2,
      13
    ]
  },
  "5": {
    "n": 16,
    "first": [
      2,
      1,
      9,
      3,
      1,
      0,
      0
    ],
    "last": [
      0,
      0,
      0,
      1,
      1,
      3,
      11
    ]
  },
  "6": {
    "n": 16,
    "first": [
      5,
      2,
      5,
      2,
      1,
      0,
      1
    ],
    "last": [
      3,
      0,
      0,
      0,
      0,
      5,
      8
    ]
  },
  "7": {
    "n": 14,
    "first": [
      4,
      1,
      2,
      4,
      1,
      1,
      1
    ],
    "last": [
      1,
      0,
      0,
      0,
      0,
      3,
      10
    ]
  }
};
function requireExact(ok,message){if(!ok)throw new Error(message)}

function objective(kind,i,j,k){if(kind==="changed")return Number(i!==j);if(kind==="seven_to_one")return Number(i===0&&j===k-1);if(kind==="new_one")return Number(i!==k-1&&j===k-1);throw Error("unknown objective")}

function transport(a,b,kind,maximize){
const k=a.length,n=a.reduce((x,y)=>x+y,0);
requireExact(k===b.length&&a.every(x=>Number.isInteger(x)&&x>=0)&&b.every(x=>Number.isInteger(x)&&x>=0)&&b.reduce((x,y)=>x+y,0)===n,"invalid marginals");
const V=2*k+2,S=0,T=V-1,g=Array.from({length:V},()=>[]),arcs=[];
function edge(u,v,cap,cost){const f={to:v,rev:g[v].length,cap,cost},rr={to:u,rev:g[u].length,cap:0,cost:-cost};g[u].push(f);g[v].push(rr);return f}
for(let i=0;i<k;i++)edge(S,1+i,a[i],0);
for(let j=0;j<k;j++)edge(1+k+j,T,b[j],0);
for(let i=0;i<k;i++)for(let j=0;j<k;j++)arcs.push([i,j,edge(1+i,1+k+j,n,(maximize?-1:1)*objective(kind,i,j,k))]);
let flow=0;
while(flow<n){
const dist=Array(V).fill(Infinity),prev=Array(V).fill(null);dist[S]=0;
for(let iter=0;iter<V-1;iter++){let changed=false;for(let u=0;u<V;u++){if(!Number.isFinite(dist[u]))continue;for(let z=0;z<g[u].length;z++){const e=g[u][z];if(e.cap>0&&dist[u]+e.cost<dist[e.to]){dist[e.to]=dist[u]+e.cost;prev[e.to]=[u,z];changed=true}}}if(!changed)break}
requireExact(prev[T]!==null,"transport flow infeasible");
let d=n-flow;for(let v=T;v!==S;){const [u,z]=prev[v];d=Math.min(d,g[u][z].cap);v=u}
for(let v=T;v!==S;){const [u,z]=prev[v],e=g[u][z];e.cap-=d;g[v][e.rev].cap+=d;v=u}flow+=d
}
const mat=Array.from({length:k},()=>Array(k).fill(0));
for(const [i,j,e] of arcs)mat[i][j]=n-e.cap;
for(let i=0;i<k;i++)requireExact(mat[i].reduce((x,y)=>x+y,0)===a[i],"row conservation");
for(let j=0;j<k;j++)requireExact(mat.reduce((x,row)=>x+row[j],0)===b[j],"column conservation");
const value=mat.reduce((s,row,i)=>s+row.reduce((t,v,j)=>t+v*objective(kind,i,j,k),0),0);
return {value,matrix:mat}
}

function analyze(table){
const ids=Object.keys(table).sort(),sessions=[];requireExact(ids.join(",")==="1,2,3,4,5,6,7","seven sessions");
for(const id of ids){const {n,first:a,last:b}=table[id];requireExact(a.length===7&&b.length===7&&a.every(x=>Number.isInteger(x)&&x>=0)&&b.every(x=>Number.isInteger(x)&&x>=0)&&a.reduce((s,x)=>s+x,0)===n&&b.reduce((s,x)=>s+x,0)===n,"invalid session "+id);
const changed=[transport(a,b,"changed",false).value,transport(a,b,"changed",true).value];
const sevenToOne=[transport(a,b,"seven_to_one",false).value,transport(a,b,"seven_to_one",true).value];
const newOne=[transport(a,b,"new_one",false).value,transport(a,b,"new_one",true).value];
requireExact(changed[0]===n-a.reduce((s,x,i)=>s+Math.min(x,b[i]),0),"TV lower "+id);
requireExact(changed[1]===n-Math.max(0,...a.map((x,i)=>x+b[i]-n)),"Hall upper "+id);
requireExact(sevenToOne[0]===Math.max(0,a[0]+b[6]-n)&&sevenToOne[1]===Math.min(a[0],b[6]),"Frechet 7 to 1 "+id);
requireExact(newOne[0]===Math.max(0,b[6]-a[6])&&newOne[1]===Math.min(b[6],n-a[6]),"new 1 bounds "+id);
sessions.push({session:Number(id),n,changed,seven_to_one:sevenToOne,new_one:newOne})
}
const sum=(key,i)=>sessions.reduce((s,z)=>s+z[key][i],0);
const total={n:sessions.reduce((s,z)=>s+z.n,0),changed:[sum("changed",0),sum("changed",1)],seven_to_one:[sum("seven_to_one",0),sum("seven_to_one",1)],new_one:[sum("new_one",0),sum("new_one",1)]};
requireExact(total.n===107&&total.changed[0]===89&&total.changed[1]===107&&total.seven_to_one[0]===10&&total.seven_to_one[1]===33&&total.new_one[0]===75&&total.new_one[1]===77,"unexpected aggregate bounds");
return {status:"PASS_SHARP_MARGINAL_BOUNDS_INTERNAL_NONBLIND_PUBLISHED_AGGREGATES_ONLY",sessions,total,individual_identities:"NOT_AVAILABLE",new_E2_predictions:0,new_E3_predictions:0}
}

function compositions(n,k){if(k===1)return [[n]];const out=[];for(let x=0;x<=n;x++)for(const z of compositions(n-x,k-1))out.push([x,...z]);return out}

function brute(a,b,kind){const k=a.length,col=b.slice();let min=Infinity,max=-Infinity;function row(i,score){if(i===k){if(col.every(x=>x===0)){min=Math.min(min,score);max=Math.max(max,score)}return}function assign(j,left,delta){if(j===k){if(left===0)row(i+1,score+delta);return}for(let x=0;x<=Math.min(left,col[j]);x++){col[j]-=x;assign(j+1,left-x,delta+x*objective(kind,i,j,k));col[j]+=x}}assign(0,a[i],0)}row(0,0);requireExact(min!==Infinity,"brute infeasible");return [min,max]}

function selftest(){let cases=0;for(let n=1;n<=4;n++){const cc=compositions(n,3);for(const a of cc)for(const b of cc)for(const kind of ["changed","seven_to_one","new_one"]){const want=brute(a,b,kind),got=[transport(a,b,kind,false).value,transport(a,b,kind,true).value];requireExact(want[0]===got[0]&&want[1]===got[1],"brute disagreement "+JSON.stringify({a,b,kind,want,got}));cases++}}const result=analyze(TABLE2);for(const [id] of Object.entries(TABLE2)){const tampered=JSON.parse(JSON.stringify(TABLE2));tampered[id].last[0]+=1;let rejected=false;try{analyze(tampered)}catch(e){rejected=true}requireExact(rejected,"invalid session accepted "+id)}return {brute_force_small_margin_cases:cases,invalid_session_rejections:7,result}}
if(require.main===module){
 try{
  const args=process.argv.slice(2);
  requireExact(args.length===0||(args.length===1&&args[0]==='--selftest')||(args.length===2&&args[0]==='--repo-root'),'usage: [--selftest | --repo-root PATH]');
  const test=selftest();
  if(args[0]==='--selftest'){console.log(JSON.stringify({status:'PASS_SYNTHETIC_SELFTEST',cases:test.brute_force_small_margin_cases,negative_controls:test.invalid_session_rejections,bounds:test.result.total}));}
  else{
   const root=args.length===2?path.resolve(args[1]):path.resolve(__dirname,'..','..');
   const file=path.join(root,'research','R127','r127_van_huyck_1990_min_effort_coordination_selection_exact.py');
   const st=fs.lstatSync(file);requireExact(st.isFile()&&!st.isSymbolicLink(),'unsafe R127 source');
   const b=fs.readFileSync(file);
   const blob=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\\0')).update(b).digest('hex');
   requireExact(blob===SOURCE_BLOB,'R127 source Git blob mismatch');
   console.log(JSON.stringify({...test.result,source_blob:SOURCE_BLOB,small_margin_exhaustive_cases:test.brute_force_small_margin_cases,negative_controls:test.invalid_session_rejections}));
  }
 }catch(e){console.error('R127_MARGINAL_BOUND_FAIL: '+e.message);process.exitCode=1}
}
module.exports={analyze,transport,selftest,TABLE2,SOURCE_BLOB};
