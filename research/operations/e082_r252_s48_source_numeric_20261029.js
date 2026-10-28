'use strict';
// E082 independent source-first numeric audit, artificial R252 S48.
// node e082_r252_s48_source_numeric_20261029.js original.csv receipt.json
function audit(csvText, receiptText) {
 const lines=csvText.trim().split(/\r?\n/).map(line=>line.split(','));
 const header=lines.shift(), source=new Map(), receipt=JSON.parse(receiptText);
 const col=name=>{const k=header.indexOf(name);if(k<0)throw Error('missing '+name);return k};
 const wi=col('world'), bi='UABCDE'.split('').map(c=>col('oracle_original_'+c));
 const oi='XYZ'.split('').map(c=>col('observed_'+c)), pi=col('original_sixbit_source_probability');
 let checks=0;
 function verify(cond,msg){checks++;if(!cond)throw Error(msg)}
 for(const row of lines){const w=row[wi];if(!source.has(w))source.set(w,[]);
   source.get(w).push({bits:bi.map(i=>Number(row[i])),obs:oi.map(i=>Number(row[i]))});
   verify(row[pi]==='1/64','probability');}
 verify(lines.length===576,'576 source atoms');
 for(const [world,rows] of source){verify(rows.length===64,'64 atoms '+world);
   for(let i=0;i<64;i++)verify(rows[i].bits.join('')===i.toString(2).padStart(6,'0'),'ordering');}
 verify(receipt.records.length===288&&receipt.n_records===288,'288 cells');
 function perm(rep){let a=Array.from({length:64},(_,i)=>i),s=(0x51A80000+7919*rep)>>>0;
   for(let i=63;i>0;i--){s^=s<<13;s^=s>>>17;s^=s<<5;s>>>=0;
     const j=s%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
 function entropy(rows,fields){const c=new Map();for(const r of rows){
   const key=fields.map(i=>r[i]).join(',');c.set(key,(c.get(key)||0)+1);}
   const n=rows.length;return [...c.values()].reduce((sum,count)=>sum-(count/n)*Math.log2(count/n),0);}
 function metrics(rows){const H=cols=>entropy(rows,cols),x=H([0]),y=H([1]),z=H([2]),
   xy=H([0,1]),xz=H([0,2]),yz=H([1,2]),xyz=H([0,1,2]);
   return {H_Y:y,I_XY:x+y-xy,I_XY_given_Z:xz+yz-z-xyz,H_Y_given_XZ:xyz-xz};}
 const seen=new Set(), perWorld=new Map();let metricChecks=0,indexChecks=0,countChecks=0,maxError=0;
 for(const rec of receipt.records){const key=[rec.world,rec.replicate,rec.n].join('|');
   verify(!seen.has(key),'duplicate cell');seen.add(key);
   const ids=perm(rec.replicate).slice(0,rec.n);
   verify(JSON.stringify(ids)===JSON.stringify(rec.source_indices),'sample indices');indexChecks++;
   const observations=ids.map(i=>source.get(rec.world)[i].obs),counts={};
   for(const triple of observations){const k=triple.join(',');counts[k]=(counts[k]||0)+1;}
   verify(Object.keys(counts).length===Object.keys(rec.xyz_integer_counts).length,'cell count size');
   for(const [k,v] of Object.entries(counts))verify(rec.xyz_integer_counts[k]===v,'cell mass');
   countChecks++;
   for(const [name,value] of Object.entries(metrics(observations))){const err=Math.abs(value-rec.metrics[name].approx_bits);
     maxError=Math.max(maxError,err);verify(err<1e-10,'numeric '+key+' '+name);metricChecks++;}
   perWorld.set(rec.world,(perWorld.get(rec.world)||0)+1);
 }
 verify(seen.size===288,'unique cells');
 for(const [world,n] of perWorld)verify(n===32,'world count '+world);
 const positives=receipt.records.filter(r=>r.world==='INDEPENDENT_BITS'&&r.n<64&&r.metrics.I_XY.approx_bits>1e-10).length;
 verify(positives===21,'positive independent-bit subsamples');
 const mutated=JSON.parse(JSON.stringify(receipt.records[0]));mutated.metrics.I_XY.approx_bits=999;
 const obs=perm(mutated.replicate).slice(0,mutated.n).map(i=>source.get(mutated.world)[i].obs);
 verify(Math.abs(metrics(obs).I_XY-mutated.metrics.I_XY.approx_bits)>1,'mutant rejected');
 return {study:'E082_R252_S48',source_rows:lines.length,records:seen.size,
   metric_checks:metricChecks,index_checks:indexChecks,count_record_checks:countChecks,
   assertions:checks,max_absolute_error:maxError,independent_bits_positive_subsamples:positives,
   mutant_rejected:true,evidence:'E1_ARTIFICIAL_ONLY'};
}
if(typeof require!=='undefined'&&require.main===module){
 const fs=require('fs'),crypto=require('crypto');
 if(process.argv.length!==4)throw Error('usage: node script.js original.csv receipt.json');
 const bytes=fs.readFileSync(process.argv[2]);
 const sha=crypto.createHash('sha256').update(bytes).digest('hex');
 if(sha!=='febd739ed17cbdac2dff13e32429e8250bfc13f067b31bf641c9679c241d3061')throw Error('source SHA256');
 console.log(JSON.stringify(audit(bytes.toString('utf8'),fs.readFileSync(process.argv[3],'utf8'))));
}
