"use strict";
// Reconstruct the two-group logistic coefficient and participant cluster sandwich from public CSV.
function analyze(csv){
 let lines=csv.trimEnd().split(/\r?\n/),h=lines.shift().split(","),records=lines.map(s=>{let a=s.split(",");return Object.fromEntries(h.map((k,i)=>[k,a[i]]));}),pd=records.filter(x=>x.game==="PD");
 function calc(score,dropAnomaly){
  let groups={};for(let row of pd){if(dropAnomaly&&row.action==="0"&&row.score==="0")continue;let name=row.opponent,id=row.id;if(!groups[name])groups[name]={};if(!groups[name][id])groups[name][id]={n:0,y:0};groups[name][id].n++;groups[name][id].y+=+(row.score===String(score));}
  let g={};for(let [name,sub] of Object.entries(groups)){let s=Object.values(sub),G=s.length,N=s.reduce((a,x)=>a+x.n,0),Y=s.reduce((a,x)=>a+x.y,0),p=Y/N,res=s.reduce((a,x)=>a+(x.y-x.n*p)**2,0);g[name]={participants:G,N,Y,p,clusterVar:(G/(G-1))*res/(N*N*p*p*(1-p)**2),naiveVar:1/Y+1/(N-Y)};}
  let beta=Math.log(g.Prompted.Y/(g.Prompted.N-g.Prompted.Y))-Math.log(g.Base.Y/(g.Base.N-g.Base.Y)),se=Math.sqrt(g.Base.clusterVar+g.Prompted.clusterVar);
  return {score,dropAnomaly,Base:g.Base,Prompted:g.Prompted,logOddsContrast:beta,oddsRatio:Math.exp(beta),naiveSE:Math.sqrt(g.Base.naiveVar+g.Prompted.naiveVar),clusterSE:se,clusterOR95:[Math.exp(beta-1.96*se),Math.exp(beta+1.96*se)]};
 }
 let anomaly=pd.filter(x=>x.action==="0"&&x.score==="0");
 if(records.length!==3900||pd.length!==1950||anomaly.length!==1)throw Error("unexpected source shape");
 return {allRows:records.length,pdRows:pd.length,anomalyCount:anomaly.length,results:[calc(5,false),calc(8,false),calc(5,true),calc(8,true)]};
}
if(typeof require!=="undefined"&&require.main===module){let fs=require("fs");console.log(JSON.stringify(analyze(fs.readFileSync(process.argv[2],"utf8")),null,2));}
