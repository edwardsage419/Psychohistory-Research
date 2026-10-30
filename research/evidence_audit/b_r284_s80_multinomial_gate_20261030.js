"use strict";
const POLICIES=["COMPLETE_REGISTRY","POSITIVE_ONLY","POSITIVE_PREFERRED"],UNITS=[[2,2,0],[2,0,2],[2,1,1]];
const HEADER="policy,source8,Ybits,Rbits,included4,K,J,T,published_alarm,registry_alarm,mass,evidence";
function f(n){let a=1;for(let i=2;i<=n;i++)a*=i;return a;}
function die(s){throw Error("B_GATE_FAIL "+s);}
function oracle(ix){
 let [a,b,c]=UNITS[ix],z={eligible:0,alarm:0,registry:0,false_alarm:0,miss_alarm:0,none:0,cell00:0,cell01:0,cell10:0,cell11:0};
 for(let i=0;i<=4;i++)for(let j=0;j<=4-i;j++){let l=4-i-j,w=f(4)/(f(i)*f(j)*f(l))*a**i*b**j*c**l,K=i+j,pa=+(K>=2&&4*i>=3*K),ra=+(i>=3);
  z.eligible+=w*+(K>=2);z.none+=w*+(K===0);z.alarm+=w*pa;z.registry+=w*ra;z.false_alarm+=w*pa*(1-ra);z.miss_alarm+=w*(1-pa)*ra;z["cell"+pa+ra]+=w;
 }
 if(z.cell00+z.cell01+z.cell10+z.cell11!==256)die("oracle mass");return z;
}
function fraction(a,b){function gcd(x,y){while(y){let t=x%y;x=y;y=t;}return x;}let g=gcd(a,b);return b/g===1?String(a/g):String(a/g)+"/"+String(b/g);}
function audit(csv,json){
 let j=JSON.parse(json);if(j.protocol_freeze_commit!=="dd478613b265823f620db2affb69ef94ffb7a955"||j.evidence!=="E1_ARTIFICIAL_NONBLIND"||j.extension!=="S80-v1"||j.source_count!==768||j.real_human_E2_prediction!==0||j.real_historical_E3_prediction!==0||j.R073!=="FROZEN"||j.PESEN_v0_1!=="FROZEN")die("grade/freeze");
 let lines=csv.trimEnd().split(/\r?\n/);if(lines.shift()!==HEADER||lines.length!==768)die("header/count");
 let seen=new Set(),rows=POLICIES.map(()=>({eligible:0,alarm:0,registry:0,false_alarm:0,miss_alarm:0,none:0,cell00:0,cell01:0,cell10:0,cell11:0}));
 for(let line of lines){
  let v=line.split(",");if(v.length!==12)die("width");
  let [p,s,ys,rs,fs,ks,js,ts,pas,ras,mass,grade]=v,ix=POLICIES.indexOf(p);
  if(ix<0||!/^[01]{8}$/.test(s)||mass!=="1/256"||grade!=="E1_ARTIFICIAL")die("identity/mass");
  let key=p+":"+s;if(seen.has(key))die("duplicate");seen.add(key);
  let Y=[0,2,4,6].map(i=>+s[i]),R=[1,3,5,7].map(i=>+s[i]),inc=Y.map((y,i)=>ix===0?1:ix===1?y:+Boolean(y||R[i]));
  let K=inc.reduce((a,b)=>a+b,0),J=Y.reduce((a,y,i)=>a+y*inc[i],0),T=Y.reduce((a,b)=>a+b,0),pa=+(K>=2&&4*J>=3*K),ra=+(T>=3);
  if(ys!==Y.join("")||rs!==R.join("")||fs!==inc.join("")||ks!==String(K)||js!==String(J)||ts!==String(T)||pas!==String(pa)||ras!==String(ra))die("row/alarm");
  let z=rows[ix];z.eligible+=+(K>=2);z.none+=+(K===0);z.alarm+=pa;z.registry+=ra;z.false_alarm+=pa*(1-ra);z.miss_alarm+=(1-pa)*ra;z["cell"+pa+ra]++;
 }
 if(seen.size!==768||j.policy_worlds.length!==3)die("universe");
 for(let ix=0;ix<3;ix++){
  let a=oracle(ix),b=rows[ix],w=j.policy_worlds[ix];if(w.policy!==POLICIES[ix]||w.original_source_types!==256)die("world");
  for(let k of Object.keys(a))if(a[k]!==b[k]||a[k]!==w.counts[k])die("multinomial "+k);
  let probs={eligible:fraction(a.eligible,256),published_alarm:fraction(a.alarm,256),published_alarm_given_eligible:fraction(a.alarm,a.eligible),registry_alarm:fraction(a.registry,256),published_only_false_alarm:fraction(a.false_alarm,256),registry_only_missed_alarm:fraction(a.miss_alarm,256),no_publication:fraction(a.none,256)};
  for(let k of Object.keys(probs))if(w.probabilities[k]!==probs[k])die("probability "+k);
 }
 return {pass:true,source_rows:768,independent_category_cells:45};
}
function mutations(csv,json){
 let l=csv.trimEnd().split(/\r?\n/),passed=[];
 function reject(name,c,j){let failed=false;try{audit(c,j);}catch(e){failed=true;}if(!failed)die("mutation accepted "+name);passed.push(name);}
 let x=l.slice();x[2]=x[1];reject("duplicate",x.join("\n")+"\n",json);
 x=l.slice(0,-1);reject("missing",x.join("\n")+"\n",json);
 x=l.slice();x[1]=x[1].replace(",1/256,E1_ARTIFICIAL",",1/255,E1_ARTIFICIAL");reject("mass",x.join("\n")+"\n",json);
 x=l.slice();let q=x[1].split(",");q[8]=q[8]==="0"?"1":"0";x[1]=q.join(",");reject("alarm",x.join("\n")+"\n",json);
 let z=JSON.parse(json);z.evidence="E3_REAL";reject("grade",csv,JSON.stringify(z));
 z=JSON.parse(json);z.policy_worlds[0].counts.alarm++;reject("receipt",csv,JSON.stringify(z));return passed;
}
if(typeof require!=="undefined"&&require.main===module){let fs=require("fs"),c=fs.readFileSync(process.argv[2],"utf8"),j=fs.readFileSync(process.argv[3],"utf8");console.log(JSON.stringify({audit:audit(c,j),mutations:mutations(c,j)}));}
