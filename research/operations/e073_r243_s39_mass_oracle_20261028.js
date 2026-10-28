"use strict";
// E073: independent prefix mass route. Usage: node e073_r243_s39_mass_oracle_20261028.js original.csv receipt.json
const fs=require("fs");
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a;}
function frac(a,b=1n){a=BigInt(a);b=BigInt(b);let g=gcd(a<0n?-a:a,b);return [a/g,b/g];}
function plus(x,y){return frac(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function str(x){return x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);}
function parse(x){let [a,b="1"]=String(x).split("/");return frac(a,b);}
function audit(csv,receipt){
  let lines=csv.trim().split(/\r?\n/),head=lines.shift().split(",");
  let rows=lines.map(line=>Object.fromEntries(line.split(",").map((v,i)=>[head[i],v])));
  let worlds=[...new Set(rows.map(x=>x.world))],checks=0,errors=[];
  function test(ok,msg){checks++;if(!ok)errors.push(msg);}
  test(rows.length===144,"source rows");test(worlds.length===9,"worlds");
  for(const world of worlds){
    const a=rows.filter(x=>x.world===world),seen=new Set(),labels=[];
    test(a.length===16,world+" row count");
    for(const x of a){
      test(x.original_path_probability==="1/16",world+" mass");
      const eps=[1,2,3,4].map(i=>x["oracle_original_epsilon_"+i]);seen.add(eps.join(","));
      for(const e of eps)test(e==="1"||e==="-1",world+" epsilon");
      const y3=parse(x.observed_y3),y4=parse(x.observed_y4);
      const delta=plus(y4,frac(-y3[0],y3[1]));
      test(str(delta)===x.observed_increment4,world+" increment");
      labels.push(delta[0]>0n?1:0);
    }
    test(seen.size===16,world+" full epsilon universe");
    test(labels.reduce((s,x)=>s+x,0)===8,world+" balanced event");
    for(let n=0;n<=4;n++){
      const groups=new Map();
      a.forEach((x,i)=>{
        const key=Array.from({length:n+1},(_,k)=>x["observed_y"+k]).join("|");
        if(!groups.has(key))groups.set(key,{p:0,m:0});
        groups.get(key)[labels[i]?"p":"m"]++;
      });
      let risk=frac(0n),probs=new Set();
      for(const g of groups.values()){
        const total=g.p+g.m;test(total>0,world+" nonempty prefix");
        probs.add(str(frac(g.p,total)));
        risk=plus(risk,frac(g.p*g.m,16*total));
      }
      if(n===4){test(risk[0]===0n,world+" invalid Y4 leakage");continue;}
      const row=receipt.rows.find(x=>x.world===world&&x.n===n);
      test(Boolean(row),world+" receipt condition "+n);
      if(row){
        test(row.prefix_support===groups.size,world+" prefix support "+n);
        test(row.oracle_brier===str(risk),world+" risk "+n);
        test(row.baseline_brier==="1/4",world+" baseline "+n);
        const gain=plus(frac(1n,4n),frac(-risk[0],risk[1]));
        test(row.gain===str(gain),world+" gain "+n);
        test(JSON.stringify(row.probabilities.slice().sort())===JSON.stringify([...probs].sort()),world+" probs "+n);
      }
    }
  }
  test(receipt.rows.length===36,"receipt conditions");
  return {checks,failures:errors.length,errors:errors.slice(0,12),rows:rows.length,worlds:worlds.length,conditions:receipt.rows.length};
}
if(require.main===module){
  if(process.argv.length!==4)throw Error("Usage: node script.js original.csv receipt.json");
  const out=audit(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8")));
  console.log(JSON.stringify(out,null,2));if(out.failures)process.exitCode=1;
}
module.exports={audit};
