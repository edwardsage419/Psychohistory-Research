/* R275 S71 exact finite noisy pair experiment. No dependencies; native Node --emit <directory>. */
function gcd(a,b){while(b!==0n){let t=a%b;a=b;b=t;}return a<0n?-a:a;}
function rat(a,b){if(b===0n)throw Error("zero denominator");let g=gcd(a,b);return (a/g).toString()+(b/g===1n?"":"/"+(b/g).toString());}
function pow(a,n){let p=1n;for(let i=0;i<n;i++)p*=a;return p;}
function run(){
const names=["IID_PAIR","COPY_PAIR","FLIP_PAIR"];
const eps=[[0n,1n],[1n,8n],[1n,4n],[1n,2n]];
const header="epsilon,true_mechanism,pair_code,equal_pair_count,true_source_probability,MAP_selected,correct,posterior_IID,posterior_COPY,posterior_FLIP\n";
let csv=header,summary=[],rows=0;
for(const [n,d] of eps){
 const en=rat(n,d),D=256n*pow(d,4);
 let conf=Array.from({length:3},()=>[0n,0n,0n]),counts=[0,0,0];
 function lik(k){return [pow(d,4),16n*pow(d-n,k)*pow(n,4-k),16n*pow(n,k)*pow(d-n,4-k)];}
 function argmax(p){let best=0;for(let i=1;i<3;i++)if(p[i]>p[best])best=i;return best;}
 const decisions=Array.from({length:5},(_,k)=>names[argmax(lik(k))]);
 for(let m=0;m<3;m++){
  let mass=0n;
  for(let z=0;z<256;z++){
   let code=z.toString(4).padStart(4,"0"),k=0;
   for(const ch of code)if(ch==="0"||ch==="3")k++;
   const p=lik(k),s=p[0]+p[1]+p[2],selected=argmax(p),correct=+(selected===m);
   if(s<=0n)throw Error("posterior zero");
   let row=[en,names[m],code,k,rat(p[m],D),names[selected],correct,...p.map(x=>rat(x,s))];
   csv+=row.join(",")+"\n";
   conf[m][selected]+=p[m];mass+=p[m];rows++;counts[m]++;
  }
  if(mass!==D||counts[m]!==256)throw Error("source normalization");
 }
 const diag=conf[0][0]+conf[1][1]+conf[2][2],avg=rat(diag,3n*D);
 summary.push({epsilon:en,average_MAP_correct:avg,confusion:Object.fromEntries(names.map((m,i)=>[m,Object.fromEntries(names.map((v,j)=>[v,rat(conf[i][j],D)]))])),K_decisions:decisions});
 if(n===0n&&avg!=="23/24")throw Error("original R275 control");
 if(2n*n===d&&avg!=="1/3")throw Error("uninformative noise control");
}
if(rows!==3072)throw Error("source count");
const obj={research_id:"R275_S71",evidence:"E1_ARTIFICIAL_NONBLIND",source_rows:rows,summary,new_E2:0,new_E3:0};
return {csv,json:JSON.stringify(obj,null,2)+"\n",summary,rows};
}
if(typeof process!=="undefined" && typeof require!=="undefined" && require.main===module){
 const fs=require("fs"),path=require("path"),out=process.argv[2]==="--emit"?process.argv[3]:null;
 const result=run();if(!out)throw Error("usage: node source.js --emit <existing-output-directory>");
 fs.writeFileSync(path.join(out,"R275_S71_ALL_3072_NOISY_PAIR_ROWS.csv"),result.csv);
 fs.writeFileSync(path.join(out,"R275_S71_EXACT_RESULTS.json"),result.json);
 console.log(JSON.stringify({rows:result.rows,summary:result.summary.map(x=>[x.epsilon,x.average_MAP_correct])}));
}