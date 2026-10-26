// A track: audit public OpenNeuro ds007822 decision event TSVs, no raw rows in output.
// Usage: node research/data_scout/a_openneuro_ds007822_decision_gate_20261027.js /path/to/ds007822
"use strict";
function audit(load){let subjects=[],byGroup={},total=0,derived=0,valid=0,files=0;
for(let g=1;g<=11;g++)for(let s=1;s<=3;s++){const group="G"+String(g).padStart(2,"0"),subject="S0"+s,id=group+subject;
const path="sub-"+id+"/eeg/sub-"+id+"_task-pddecision_events.tsv";
const lines=load(path).trim().split(/\r?\n/),cols=lines.shift().split("\t");
const required=["onset","duration","trial_type","trial","group","subject","choice","triad_outcome"];
if(required.some(x=>!cols.includes(x)))throw Error("schema "+id);
const rows=lines.map(line=>Object.fromEntries(line.split("\t").map((v,i)=>[cols[i],v])));
if(rows.length!==40)throw Error("round count "+id);
const seq=[];for(let i=0;i<rows.length;i++){let r=rows[i];if(r.group!==group||r.subject!==subject||r.trial_type!=="decision"||Number(r.trial)!==i+1||Number(r.onset)!==i*4||Number(r.duration)!==4||!["1","2"].includes(r.choice))throw Error("identity or time "+id);
const inferred=r.choice==="1"?"coop":"def";if(r.triad_outcome===inferred)derived++;else throw Error("outcome mapping "+id);
seq.push(r.choice);total++;valid++;}
subjects.push({id,sequence:seq.join("")});(byGroup[group]??=[]).push(seq);files++;}
let mixed=0;for(let [g,arr] of Object.entries(byGroup)){if(arr.length!==3)throw Error("triad "+g);for(let t=0;t<40;t++)if(new Set(arr.map(a=>a[t])).size>1)mixed++;}
let duplicates=[];for(let [g,arr] of Object.entries(byGroup))for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(arr[i].join("")===arr[j].join(""))duplicates.push([g+"S0"+(i+1),g+"S0"+(j+1)]);
return {dataset:"OpenNeuroDatasets/ds007822",files,subjects:subjects.length,triads:Object.keys(byGroup).length,rounds_per_subject:40,decision_rows:total,valid_rows:valid,triad_outcome_equal_own_choice:derived,triad_rounds:440,triad_rounds_with_mixed_choices:mixed,within_triad_duplicate_sequences:duplicates,source_license_conflict:"LICENSE unspecified; dataset_description.json CC0",R073_direct_transfer:"BLOCKED",E2_prediction_scores:0};}
if(typeof require!=="undefined"&&require.main===module){const fs=require("node:fs"),path=require("node:path"),root=process.argv[2];if(!root)throw Error("dataset root required");console.log(JSON.stringify(audit(p=>fs.readFileSync(path.join(root,p),"utf8")),null,2));}
if(typeof module!=="undefined")module.exports={audit};
