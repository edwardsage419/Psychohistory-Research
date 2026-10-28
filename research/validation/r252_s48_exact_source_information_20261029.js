#!/usr/bin/env node
'use strict';
// Frozen R252 S48 artificial E1 sensitivity; Node 18+.
const WORLDS=["INDEPENDENT_BITS","DIRECT_COPY","HIDDEN_COMMON_CAUSE_ALIAS","XOR_SYNERGY","ERASURE_HALF","BINARY_SYMMETRIC_QUARTER","COLLIDER_AND","XOR_MASK_REPARAM","CONSTANT_REPORTER"];
const ORIGINAL_SHA='febd739ed17cbdac2dff13e32429e8250bfc13f067b31bf641c9679c241d3061';
const FREEZE='c57653fe521b9c2bad4da8fce95fa794050e320a';
const NS=[8,16,32,64];
function check(ok,msg){if(!ok)throw Error(msg);}

function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b){let t=a%b;a=b;b=t;}return a||1;}

function frac(a,n){let g=gcd(a,n);return n/g===1?String(a/g):String(a/g)+'/'+String(n/g);}

function factor(n){let d={},p=2;while(p*p<=n){while(n%p===0){d[p]=(d[p]||0)+1;n/=p;}p++;}if(n>1)d[n]=(d[n]||0)+1;return d;}

function entropy(rows,axes){
 let counts={};for(const row of rows){let k=axes.map(i=>row[i]).join(',');counts[k]=(counts[k]||0)+1;}
 let n=rows.length;check(Object.values(counts).reduce((a,b)=>a+b,0)===n,'count mass');
 let v={'1':n*Math.log2(n)};
 for(const c of Object.values(counts)){for(const [p,e] of Object.entries(factor(c))){let k=p==='2'?'1':'log2_'+p;v[k]=(v[k]||0)-c*e;}}
 return v;
}

function add(...signed){let d={};for(const [sgn,v] of signed){for(const [k,a] of Object.entries(v))d[k]=(d[k]||0)+sgn*a;}return Object.fromEntries(Object.entries(d).filter(([k,v])=>v!==0).sort());}

function metrics(rows){
 let hx=entropy(rows,[0]),hy=entropy(rows,[1]),hz=entropy(rows,[2]),hxy=entropy(rows,[0,1]),hxz=entropy(rows,[0,2]),hyz=entropy(rows,[1,2]),hxyz=entropy(rows,[0,1,2]);
 return {H_Y:hy,I_XY:add([1,hx],[1,hy],[-1,hxy]),I_XY_given_Z:add([1,hxz],[1,hyz],[-1,hz],[-1,hxyz]),H_Y_given_XZ:add([1,hxyz],[-1,hxz])};
}

function approx(e,n){return Object.entries(e).reduce((a,[k,v])=>a+(v/n)*(k==='1'?1:Math.log2(Number(k.slice(5)))),0);}

function format(e,n){let prime={};for(const [k,v] of Object.entries(e))if(k!=='1')prime[k.slice(5)]=frac(v,n);
 return {rational:frac(e['1']||0,n),prime_log2:prime,approx_bits:Number(approx(e,n).toFixed(12))};}

function perm(rep){let state=(0x51A80000+7919*rep)>>>0,arr=Array.from({length:64},(_,i)=>i);
 for(let i=63;i>0;i--){state=(state^(state<<13))>>>0;state=(state^(state>>>17))>>>0;state=(state^(state<<5))>>>0;
 let j=state%(i+1);[arr[i],arr[j]]=[arr[j],arr[i]];}check(new Set(arr).size===64,'permutation');return arr;}

function parse(csv){
 let lines=csv.trimEnd().split(/\r?\n/),h=lines.shift().split(',');
 check(lines.length===576,'source rows must be 576');
 const col=k=>{let j=h.indexOf(k);check(j>=0,'missing column '+k);return j;};
 const iw=col('world'),ib='UABCDE'.split('').map(k=>col('oracle_original_'+k)),ix='XYZ'.split('').map(k=>col('observed_'+k)),ip=col('original_sixbit_source_probability');
 let out=Object.fromEntries(WORLDS.map(w=>[w,[]]));
 for(let line of lines){let a=line.split(','),w=a[iw];check(out[w]!==undefined,'unfrozen world');check(a[ip]==='1/64','source mass');
 let bits=ib.map(j=>Number(a[j])),obs=ix.map(j=>Number(a[j]));check(bits.every(x=>x===0||x===1),'invalid bits');
 out[w].push({bits,obs});}
 for(let w of WORLDS){check(out[w].length===64,'source group size');check(new Set(out[w].map(x=>x.bits.join(''))).size===64,'source uniqueness');
 for(let i=0;i<64;i++){let a=out[w][i].bits.join(''),b=i.toString(2).padStart(6,'0');check(a===b,'original source ordering');}}
 for(let i=0;i<64;i++)check(JSON.stringify(out.DIRECT_COPY[i])===JSON.stringify(out.HIDDEN_COMMON_CAUSE_ALIAS[i]),'sourcewise alias');
 return out;
}

function run(csv){
 const source=parse(csv),pop={},records=[];
 for(let w of WORLDS){let e=metrics(source[w].map(x=>x.obs));pop[w]=Object.fromEntries(Object.entries(e).map(([k,v])=>[k,format(v,64)]));}
 for(let rep=0;rep<8;rep++){let order=perm(rep);
 for(let n of NS){let indices=order.slice(0,n);
 for(let w of WORLDS){
 let rows=indices.map(i=>source[w][i].obs),e=metrics(rows),m=Object.fromEntries(Object.entries(e).map(([k,v])=>[k,format(v,n)]));
 for(let v of Object.values(m))check(v.approx_bits>=-1e-10,'negative entropy or information');
 let counts={};for(let row of rows){let k=row.join(',');counts[k]=(counts[k]||0)+1;}
 let abs1=Math.abs(m.I_XY.approx_bits-pop[w].I_XY.approx_bits),abs2=Math.abs(m.I_XY_given_Z.approx_bits-pop[w].I_XY_given_Z.approx_bits);
 if(n===64)check(JSON.stringify(m)===JSON.stringify(pop[w]),'full source exact population mismatch');
 records.push({world:w,replicate:rep,n,source_indices:indices,xyz_integer_counts:Object.fromEntries(Object.entries(counts).sort()),metrics:m,abs_error_I_XY_bits:Number(abs1.toFixed(12)),abs_error_I_XY_given_Z_bits:Number(abs2.toFixed(12))});
 }}}check(records.length===288,'288 records required');
 let by=Object.fromEntries(records.map(x=>[[x.world,x.replicate,x.n].join('|'),x]));
 for(let rep=0;rep<8;rep++)for(let n of NS){
 let a=by[['DIRECT_COPY',rep,n].join('|')],b=by[['HIDDEN_COMMON_CAUSE_ALIAS',rep,n].join('|')];
 check(JSON.stringify(a.xyz_integer_counts)===JSON.stringify(b.xyz_integer_counts),'alias counts');
 check(JSON.stringify(a.metrics)===JSON.stringify(b.metrics),'alias metrics');
 }
 check(JSON.stringify(by['XOR_SYNERGY|0|64'].xyz_integer_counts)===JSON.stringify(by['XOR_MASK_REPARAM|0|64'].xyz_integer_counts),'XOR population alias');
 check(pop.INDEPENDENT_BITS.I_XY.rational==='0'&&pop.XOR_SYNERGY.I_XY.rational==='0'&&pop.XOR_SYNERGY.I_XY_given_Z.rational==='1','population controls');
 let positive=records.filter(x=>x.world==='INDEPENDENT_BITS'&&x.n<64&&x.metrics.I_XY.approx_bits>1e-10).length;
 check(positive>0,'positive sample control absent');
 let summaries=[];
 for(let n of NS)for(let w of WORLDS){let a=records.filter(x=>x.n===n&&x.world===w);
 let mean=k=>Number((a.reduce((s,r)=>s+r[k],0)/8).toFixed(12));
 summaries.push({n,world:w,mean_abs_error_I_XY_bits:mean('abs_error_I_XY_bits'),mean_abs_error_I_XY_given_Z_bits:mean('abs_error_I_XY_given_Z_bits'),positive_empirical_I_XY_replicates:a.filter(x=>x.metrics.I_XY.approx_bits>1e-10).length});}
 return {study:'R252_S48',prescore_protocol_commit:FREEZE,original_source_sha256:ORIGINAL_SHA,evidence:'E1_ARTIFICIAL_ONLY',n_worlds:9,n_replicates:8,sample_sizes:NS,n_records:288,independent_bits_positive_sample_I_count_n_below64:positive,target_leakage_H_Y_given_XZ_and_Y_zero_by_identity_checks:288,population:pop,summaries,records,new_human_E2:0,new_historical_E3:0,external_independent_replications:0,R073:'FROZEN',PESEN_v0_1:'FROZEN'};
}

if(require.main===module){
 const fs=require('fs'),crypto=require('crypto');
 if(process.argv.length!==4)throw Error('usage: node script.js original.csv receipt.json');
 const bytes=fs.readFileSync(process.argv[2]);
 check(crypto.createHash('sha256').update(bytes).digest('hex')===ORIGINAL_SHA,'original SHA256 mismatch');
 const result=run(bytes.toString('utf8'));
 fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2)+'\n','utf8');
 console.log(JSON.stringify({study:result.study,n_records:result.n_records,positive:result.independent_bits_positive_sample_I_count_n_below64}));
}
