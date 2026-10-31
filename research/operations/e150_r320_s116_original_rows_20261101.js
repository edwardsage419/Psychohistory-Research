#!/usr/bin/env node
"use strict";
const fs=require("node:fs");
const csv=fs.readFileSync("research/R320/R320_ALL_384_ORIGINAL_SIX_STEP_PATHS.csv","utf8");
const original=JSON.parse(fs.readFileSync("research/R320/R320_EXACT_6_FIRST_HIT_WORLDS.json","utf8"));
const extended=JSON.parse(fs.readFileSync("research/validation/R320_S116_EXACT_EVENTUAL_RESULTS.json","utf8"));
const result=(function(csv,original,extended){
const lines=csv.trimEnd().split(/\r?\n/),cols=lines.shift().split(",");
const required="world_id,upper_bound,start,p_up,path_bits,up_steps,down_steps,full_path_probability,first_hit_time,first_hit_side,censored".split(",");
if(cols.join()!==required.join())throw Error("header mismatch");
let checks=0;const worlds=new Map();
function eq(actual,expected,label){checks++;if(actual!==expected)throw Error(label+": "+actual+" expected "+expected);}
function scaled(s){const [n,d="1"]=s.split("/");const top=BigInt(n)*4096n,bot=BigInt(d);if(top%bot!==0n)throw Error("unrepresentable fraction");return Number(top/bot);}
for(let i=0;i<lines.length;i++){
 const c=lines[i].split(",");eq(c.length,11,"columns");const [widS,aS,zS,p,bits,upS,downS,prob,tS,side,censored]=c;
 const wid=Number(widS),a=Number(aS),z=Number(zS),up=[...bits].filter(b=>b==="1").length,down=6-up;
 eq(bits.length,6,"bits length");if(!/^[01]{6}$/.test(bits))throw Error("invalid bits");
 eq(up,Number(upS),"up count");eq(down,Number(downS),"down count");
 const params=[[4,"1/4"],[4,"1/2"],[4,"3/4"],[6,"1/4"],[6,"1/2"],[6,"3/4"]][wid];
 if(!params)throw Error("invalid world");
 eq(a,params[0],"bound");eq(z,a/2,"start");eq(p,params[1],"p");
 let x=z,hit=0,hitSide="none";
 for(let j=0;j<6;j++){x+=bits[j]==="1"?1:-1;if(x===0||x===a){hit=j+1;hitSide=x===a?"upper":"lower";break;}}
 eq(tS,hit?String(hit):"","first hit time");eq(side,hitSide,"first hit side");eq(censored,hit?"false":"true","censored");
 const pn=p==="1/4"?3**down:p==="3/4"?3**up:64;eq(scaled(prob),pn,"path probability");
 if(!worlds.has(wid))worlds.set(wid,{paths:new Set(),sum:0,hit:{},surv:0,weighted:0,hitWeighted:0,hitTotal:0});
 const w=worlds.get(wid);if(w.paths.has(bits))throw Error("duplicate path");
 w.paths.add(bits);w.sum+=pn;w.weighted+=pn*(hit||6);
 if(hit){const key=hit+"_"+hitSide;w.hit[key]=(w.hit[key]||0)+pn;w.hitWeighted+=pn*hit;w.hitTotal+=pn;}else w.surv+=pn;
}
eq(worlds.size,6,"world count");eq(lines.length,384,"row count");
for(let wid=0;wid<6;wid++){
 const w=worlds.get(wid),o=original.worlds[wid],e=extended.worlds[wid];
 if(!w)throw Error("missing world");
 eq(w.paths.size,64,"paths per world");eq(w.sum,4096,"probability total");
 eq(w.surv,scaled(o.survival),"original survival");eq(w.surv,scaled(e.six_step_survival),"extended survival");
 eq(w.weighted,scaled(o.expected_truncated_steps),"original truncated mean");
 eq(w.weighted,scaled(e.expected_truncated_six_steps),"extended truncated mean");
 for(let t=1;t<=6;t++)for(const s of ["lower","upper"]){
  const value=w.hit[t+"_"+s]||0;
  eq(value,scaled(o.hit_by_time_and_side[t-1][s]),"original hit cell");
  eq(value,scaled(e.six_step_cells[t-1][s]),"extended hit cell");
 }
 eq(w.hitTotal,scaled(o.hit_total),"original hit total");
 const [n,d="1"]=o.conditional_mean_decision_steps_among_hits.split("/");
 eq(BigInt(w.hitWeighted)*BigInt(d),BigInt(w.hitTotal)*BigInt(n),"conditional hit mean");
}
return {rows:lines.length,worlds:worlds.size,checks};

})(csv,original,extended);
console.log(JSON.stringify(result,null,2));
