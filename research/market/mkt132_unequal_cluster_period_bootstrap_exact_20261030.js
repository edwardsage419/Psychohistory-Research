'use strict';
// Exact finite-world row and cluster percentile bootstrap; no external packages.
function gcd(a,b){while(b!==0n){let t=b;b=a%b;a=t;}return a;}

function frac(a,b){a=BigInt(a);b=BigInt(b);if(b<=0n)throw Error("bad denominator");let g=gcd(a,b);return [a/g,b/g];}

function cmp(a,b){let x=a[0]*b[1]-b[0]*a[1];return x<0n?-1:x>0n?1:0;}

function choose(n,k){let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-i+1)/BigInt(i);return v;}

function quantile(vals,weights,num,den){if(!vals.length||vals.length!==weights.length)throw Error("bad distribution");let total=weights.reduce((a,b)=>a+b,0n),sum=0n;if(total<=0n)throw Error("empty distribution");for(let i=0;i<vals.length;i++){sum+=weights[i];if(sum*BigInt(den)>=BigInt(num)*total)return vals[i];}throw Error("bad quantile");}

function rowInterval(ns,ys){let N=ns.reduce((a,b)=>a+b,0),K=ns.reduce((a,n,i)=>a+n*ys[i],0),vals=[],weights=[];for(let k=0;k<=N;k++){vals.push(frac(k,N));weights.push(choose(N,k)*BigInt(K)**BigInt(k)*BigInt(N-K)**BigInt(N-k));}return [quantile(vals,weights,1,40),quantile(vals,weights,39,40)];}

function clusterInterval(ns,ys){let G=ns.length,m=new Map();for(let draw=0;draw<G**G;draw++){let v=draw,num=0,den=0;for(let j=0;j<G;j++){let i=v%G;v=Math.floor(v/G);num+=ns[i]*ys[i];den+=ns[i];}let f=frac(num,den),key=f[0]+"/"+f[1];m.set(key,(m.get(key)||0n)+1n);}let sorted=[...m].map(([key,w])=>[key.split("/").map(BigInt),w]).sort((a,b)=>cmp(a[0],b[0]));return [quantile(sorted.map(x=>x[0]),sorted.map(x=>x[1]),1,40),quantile(sorted.map(x=>x[0]),sorted.map(x=>x[1]),39,40)];}

function study(ns){if(!Array.isArray(ns)||ns.length!==4||ns.some(n=>!Number.isSafeInteger(n)||n<=0))throw Error("four positive integer clusters required");let row=0,group=0,missRow=[],missGroup=[];for(let mask=0;mask<16;mask++){let ys=[0,1,2,3].map(i=>(mask>>i)&1),r=rowInterval(ns,ys),c=clusterInterval(ns,ys),half=frac(1,2),okR=cmp(r[0],half)<=0&&cmp(half,r[1])<=0,okC=cmp(c[0],half)<=0&&cmp(half,c[1])<=0;row+=Number(okR);group+=Number(okC);if(!okR)missRow.push(mask);if(!okC)missGroup.push(mask);}let N=ns.reduce((a,b)=>a+b,0),s=ns.reduce((a,n)=>a+n*n,0),v=frac(s,4*N*N),eff=frac(N*N,s);return {sizes:ns,worlds:16,row_covered:row,cluster_covered:group,true_variance:v[0]+"/"+v[1],effective_clusters:eff[0]+"/"+eff[1],row_misses:missRow,cluster_misses:missGroup};}

function selftest(){let a=study([3,3,3,3]),b=study([1,1,2,8]),c=study([2,2,4,16]);let tests=[[a.row_covered,14],[a.cluster_covered,14],[a.true_variance,"1/16"],[b.row_covered,6],[b.cluster_covered,14],[b.true_variance,"35/288"],[b.effective_clusters,"72/35"],[c.row_covered,2],[c.cluster_covered,14],[c.true_variance,b.true_variance],[b.cluster_misses.join(","),"0,15"],[c.cluster_misses.join(","),"0,15"]];for(let [x,y] of tests)if(x!==y)throw Error("assertion failed "+x+" != "+y);let invalid=0;for(let x of [[1,1,0,8],[1,1,8],null]){try{study(x);}catch(e){invalid++;}}if(invalid!==3)throw Error("invalid input accepted");return {status:"PASS",worlds:48,assertions:15,negative_controls:3,balanced:a,unequal:b,two_period_same_cluster:c};}

if(typeof process!=='undefined'&&process.argv&&process.argv[1]&&process.argv[1].endsWith('mkt132_unequal_cluster_period_bootstrap_exact_20261030.js')){if(process.argv[2]&&process.argv[2]!=='--selftest')throw Error('use --selftest');console.log(JSON.stringify(selftest(),null,2));}
