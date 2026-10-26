const fs=require('fs');
function audit(data){
  function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let c=a%b;a=b;b=c;}return a;}
  class Q{constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}let g=gcd(a,b);this.a=a/g;this.b=b/g;}add(x){return new Q(this.a*x.b+x.a*this.b,this.b*x.b)}sub(x){return new Q(this.a*x.b-x.a*this.b,this.b*x.b)}mul(x){return new Q(this.a*x.a,this.b*x.b)}abs(){return new Q(this.a<0n?-this.a:this.a,this.b)}str(){return this.b===1n?String(this.a):this.a+"/"+this.b;}}
  const z=new Q(0),one=new Q(1),q=(s)=>{let a=String(s).split("/");return new Q(a[0],a[1]||1);};
  const E={star:[[0,1],[0,2],[0,3]],path:[[0,1],[1,2],[2,3]],cycle:[[0,1],[1,2],[2,3],[3,0]],complete:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]};
  function bits(s){return s.toString(2).padStart(4,"0");}
  function pop(s){return [0,1,2,3].reduce((a,i)=>a+((s>>i)&1),0);}
  function pmf(c,mutate=false){
    const seed=1<<c.seed,a=q(c.rate),mu=c.mechanism==="diffusion"?z:c.mechanism==="mixed"?q("1/4"):a,beta=c.mechanism==="invention"?z:a;
    const prob=[];
    for(let i=0;i<4;i++){if((seed>>i)&1){prob.push([z,one]);continue;}
      const nbr=E[c.graph].filter(([u,v])=>u===i?((seed>>v)&1):v===i?((seed>>u)&1):false).length;
      let coins=[mutate&&nbr===0?z:mu,...Array(nbr).fill(beta)],no=z,yes=z;
      for(let mask=0;mask<(1<<coins.length);mask++){let pr=one,success=false;for(let j=0;j<coins.length;j++){const hit=(mask>>j)&1;pr=pr.mul(hit?coins[j]:one.sub(coins[j]));if(hit)success=true;}if(success)yes=yes.add(pr);else no=no.add(pr);}
      if(no.add(yes).str()!=="1")throw Error("coin normalization");prob.push([no,yes]);
    }
    let out={};for(let s=0;s<16;s++){let p=one;for(let i=0;i<4;i++)p=p.mul(prob[i][(s>>i)&1]);out[bits(s)]=p;}return out;
  }
  function countPMF(dist){let out={};for(const [k,v] of Object.entries(dist)){let n=pop(parseInt(k,2));out[n]=(out[n]||z).add(v);}return out;}
  function tv(a,b){let sum=z;for(const k of Object.keys(a))sum=sum.add(a[k].sub(b[k]).abs());return new Q(sum.a,2n*sum.b).str();}
  let comparisons=0,countComparisons=0,errors=[],mutated=null;
  for(const c of data.cases){let actual=pmf(c),source=c.time_distributions[1];for(let k of Object.keys(source)){comparisons++;if(actual[k].str()!==q(source[k]).str())errors.push([c.graph,c.seed,c.rate,c.mechanism,k,actual[k].str(),source[k]]);}
    const a=countPMF(actual),b=countPMF(Object.fromEntries(Object.entries(source).map(([k,v])=>[k,q(v)])));
    for(let n=0;n<=4;n++){countComparisons++;if((a[n]||z).str()!==(b[n]||z).str())errors.push(["count",c.graph,c.seed,c.rate,c.mechanism,n]);}
    if(c.graph==="path"&&c.seed===1&&c.rate==="1/4"&&c.mechanism==="invention"){let m=pmf(c,true);mutated={world:"path|seed1|rate1/4|invention",first_step_full_TV:tv(actual,m),original_unexposed_node3_probability:"1/4",mutated_unexposed_node3_probability:"0"};}
  }
  if(errors.length)throw Error(JSON.stringify(errors.slice(0,3)));
  if(mutated.first_step_full_TV==="0")throw Error("mutant undetected");
  return {research:"R174",date:"2026-10-26",source_git_blob_sha1:"084a6783cdf495e5fb06390a481e38c1efe396b6",algorithm:"independent per-node innovation and exposed-edge Bernoulli event enumeration",worlds:data.cases.length,first_step_full_state_cells_exact:comparisons,first_step_count_cells_exact:countComparisons,errors:errors.length,mutant:mutated,external_team_replication:false};
}
if(require.main===module){console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));}
module.exports={audit};
