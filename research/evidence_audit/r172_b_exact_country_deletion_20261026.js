"use strict";
// B independent rational arithmetic audit. Run: node r172_b_exact_country_deletion_20261026.js research/R172/R172_REAL_HELDOUT_PREDICTIONS.csv
// No external libraries. Distinct arithmetic route from R172 floating country bootstrap.
function check(b,m){if(!b)throw new Error(m);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function q(a,b=1n){check(b!==0n,"zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
function add(x,y){return q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function sub(x,y){return q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
function mul(x,y){return q(x[0]*y[0],x[1]*y[1]);}
function div(x,n){return q(x[0],x[1]*BigInt(n));}
function equal(x,y){return x[0]===y[0]&&x[1]===y[1];}
function parse(s){const t=s.split("/");check(t.length<=2&&/^\d+$/.test(t[0])&&(t.length===1||/^\d+$/.test(t[1])),"bad rational");const r=q(BigInt(t[0]),BigInt(t[1]||"1"));check(r[0]>0n&&r[0]<r[1],"p out of range");return r;}
function decimal(x){return Number(x[0])/Number(x[1]);}
function signature(x){const prime=1000000007n;return {numerator_digits:x[0].toString().length,denominator_digits:x[1].toString().length,num_mod:String((x[0]%prime+prime)%prime),den_mod:String(x[1]%prime)};}
function analyze(csv){
 const lines=csv.trimEnd().split(/\r?\n/),header=lines.shift().split(",");
 const col=Object.fromEntries(header.map((h,i)=>[h,i]));for(const h of ["episode_id","country_id","year","recorded_breakdown_event","M0_constant_exact","M1_duration_exact","M2_duration_baseline_exact"])check(h in col,"missing "+h);
 const rows=lines.map((line,i)=>{const z=line.split(",");check(z.length===header.length,"CSV columns "+i);const ep=z[col.episode_id],country=z[col.country_id],year=Number(z[col.year]),y=Number(z[col.recorded_breakdown_event]);check((y===0||y===1)&&year>=2000&&year<=2017,"bad event/year");const ps=[col.M0_constant_exact,col.M1_duration_exact,col.M2_duration_baseline_exact].map(k=>parse(z[k]));const sq=ps.map(p=>{const e=sub(p,q(BigInt(y)));return mul(e,e);});return {ep,country,year,y,ps,sq};});
 check(rows.length===319,"row count");const country=new Map(),episode=new Map(),seen=new Set();let events=0;
 for(const r of rows){check(r.ep&&r.country,"missing ids");const k=r.ep+"|"+r.year;check(!seen.has(k),"duplicate episode year");seen.add(k);if(!episode.has(r.ep))episode.set(r.ep,{country:r.country,events:0});check(episode.get(r.ep).country===r.country,"episode country mismatch");episode.get(r.ep).events+=r.y;check(episode.get(r.ep).events<=1,"repeated event");events+=r.y;if(!country.has(r.country))country.set(r.country,[]);country.get(r.country).push(r);}
 check(country.size===32&&episode.size===35&&events===18,"counts");
 const zero=q(0n),tot=[zero,zero,zero];for(const r of rows)for(let i=0;i<3;i++)tot[i]=add(tot[i],r.sq[i]);
 const exactMean=tot.map(x=>div(x,rows.length)),means=exactMean.map(decimal);
 const expected=[.054407113235,.054667027894,.054105271593];for(let i=0;i<3;i++)check(Math.abs(means[i]-expected[i])<1e-10,"original brier mismatch");
 const bins=[[0,.02],[.02,.05],[.05,1]],calibration=[0,1,2].map(m=>bins.map(([lo,hi])=>{let n=0,obs=0;for(const r of rows){const p=decimal(r.ps[m]);if(p>=lo&&p<hi){n++;obs+=r.y;}}return {n,obs};}));
 const names=[...country.keys()].sort(),perCountry=names.map(name=>{const rr=country.get(name),s=[zero,zero,zero];for(const r of rr)for(let i=0;i<3;i++)s[i]=add(s[i],r.sq[i]);return {country:name,n:rr.length,episodes:new Set(rr.map(r=>r.ep)).size,s};});
 const loco=perCountry.map(g=>{const remain=rows.filter(r=>r.country!==g.country);const direct=[zero,zero,zero];for(const r of remain)for(let i=0;i<3;i++)direct[i]=add(direct[i],r.sq[i]);const bySub=tot.map((x,i)=>sub(x,g.s[i]));for(let i=0;i<3;i++)check(equal(direct[i],bySub[i]),"country deletion exact mismatch "+g.country+"/"+i);return {country:g.country,n:remain.length,brier_delta:[1,2].map(i=>decimal(div(sub(bySub[i],bySub[0]),remain.length)))};});
 const originalCountryCount=country.size;const changed=rows.map((r,i)=>i? r:{...r,country:"ZZZ_SENTINEL"});const mutatedCountries=new Set(changed.map(r=>r.country)).size;check(mutatedCountries===originalCountryCount+1,"label negative control");
 const before=tot[2],replacement=mul(sub(q(1n,2n),q(BigInt(rows[0].y))),sub(q(1n,2n),q(BigInt(rows[0].y))));const changedTotal=add(sub(before,rows[0].sq[2]),replacement);check(!equal(changedTotal,before),"probability negative control");
 const signatures=exactMean.map(signature);
 return {status:"PASS_INTERNAL_EXACT_COUNTRY_DELETE",rows:rows.length,episodes:episode.size,countries:country.size,events,means,signatures,country_multi_episode:perCountry.filter(g=>g.episodes>1).map(g=>({country:g.country,episodes:g.episodes})),calibration,loco,exact_deletion_checks:perCountry.length*3,controls:{label_mutation_changes_country_count:mutatedCountries===originalCountryCount+1,probability_mutation_changes_exact_brier:!equal(changedTotal,before)}};
}
module.exports={analyze};
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");const p=process.argv[2]||"research/R172/R172_REAL_HELDOUT_PREDICTIONS.csv";console.log(JSON.stringify(analyze(fs.readFileSync(p,"utf8")),null,2));}
