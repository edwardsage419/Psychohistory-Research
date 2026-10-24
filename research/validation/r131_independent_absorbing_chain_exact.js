"use strict";
// R131 independent finite Moran audit. Node.js 18+; no dependencies.
// Uses exact rational absorbing-chain linear algebra; original R131 Python is not imported.
function rat(a,b=1n) {
  a=BigInt(a); b=BigInt(b);
  if(b===0n) throw Error("zero denominator");
  if(b<0n){a=-a;b=-b;}
  function gcd(x,y){x=x<0n?-x:x;while(y){let t=x%y;x=y;y=t;}return x;}
  const g=gcd(a,b);return [a/g,b/g];
}
const plus=(x,y)=>rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const minus=(x,y)=>rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const times=(x,y)=>rat(x[0]*y[0],x[1]*y[1]);
const divide=(x,y)=>rat(x[0]*y[1],x[1]*y[0]);
const equal=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const less=(x,y)=>x[0]*y[1]<y[0]*x[1];
const show=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
const ZERO=rat(0),ONE=rat(1);
function transitionMatrix(N,fa,fb){
  const out=[];
  for(let i=0;i<=N;i++){
    const row=Array.from({length:N+1},()=>ZERO);
    if(i===0||i===N){row[i]=ONE;out.push(row);continue;}
    const denom=(N-i)*fa+i*fb;
    const births=[["A",rat((N-i)*fa,denom)],["B",rat(i*fb,denom)]];
    const deaths=[["A",rat(N-i,N)],["B",rat(i,N)]];
    for(const [bt,bp] of births) for(const [dt,dp] of deaths){
      const j=i+(bt==="B"?1:0)-(dt==="B"?1:0);
      row[j]=plus(row[j],times(bp,dp));
    }
    out.push(row);
  }
  return out;
}
function solve(A,b){
  const n=b.length;
  const aug=A.map((row,i)=>[...row,b[i]]);
  for(let c=0;c<n;c++){
    let pivot=c;
    while(pivot<n&&equal(aug[pivot][c],ZERO))pivot++;
    if(pivot===n)throw Error("singular absorption system");
    [aug[c],aug[pivot]]=[aug[pivot],aug[c]];
    const p=aug[c][c];
    for(let k=c;k<=n;k++)aug[c][k]=divide(aug[c][k],p);
    for(let j=0;j<n;j++)if(j!==c){
      const f=aug[j][c];
      for(let k=c;k<=n;k++)aug[j][k]=minus(aug[j][k],times(f,aug[c][k]));
    }
  }
  return aug.map(row=>row[n]);
}
function absorbingProbabilities(P,rightBoundary=ONE){
  const N=P.length-1;
  const A=[],b=[];
  for(let i=1;i<N;i++){
    A.push(Array.from({length:N-1},(_,k)=>minus(i===k+1?ONE:ZERO,P[i][k+1])));
    b.push(times(P[i][N],rightBoundary));
  }
  return [ZERO,...solve(A,b),rightBoundary];
}
function sourceRecurrenceFirst(N,fa,fb){
  // Comparator transcribed from R131's forward-difference ratio; not executed from its Python file.
  let product=ONE,total=ONE;
  for(let i=1;i<N;i++){
    const down=rat((N-i)*fa*i,((N-i)*fa+i*fb)*N);
    const up=rat(i*fb*(N-i),((N-i)*fa+i*fb)*N);
    product=times(product,divide(down,up));
    total=plus(total,product);
  }
  return divide(ONE,total);
}
function runAudit(){
  let rows=0,transitionRows=0,residuals=0,comparisons=0;
  const output=[];
  for(let N=2;N<=8;N++)for(const [fa,fb] of [[3,2],[1,1],[2,3]]){
    const P=transitionMatrix(N,fa,fb),h=absorbingProbabilities(P);
    for(let i=0;i<=N;i++){
      const total=P[i].reduce(plus,ZERO);
      if(!equal(total,ONE))throw Error("transition row not stochastic");
      transitionRows++;
    }
    if(!equal(h[0],ZERO)||!equal(h[N],ONE))throw Error("wrong boundaries");
    for(let i=1;i<N;i++){
      const expected=P[i].reduce((sum,prob,j)=>plus(sum,times(prob,h[j])),ZERO);
      if(!equal(h[i],expected))throw Error("Dirichlet residual");
      if(!less(h[i-1],h[i])||!less(h[i],h[i+1]))throw Error("nonmonotone fixation");
      output.push([N,fa,fb,i,show(h[i])]);
      rows++;residuals++;
    }
    if(!equal(h[1],sourceRecurrenceFirst(N,fa,fb)))throw Error("recurrence disagreement");
    comparisons++;
    if(N===5){
      const target=fa===3?rat(16,211):fa===fb?rat(1,5):rat(81,211);
      if(!equal(h[1],target))throw Error("N5 frozen anchor mismatch");
    }
    if(N===5&&fa===3&&fb===2){
      if(equal(h[1],rat(1,N)))throw Error("negative control: false neutral probability");
      const changed=absorbingProbabilities(P,ZERO);
      if(equal(changed[1],h[1]))throw Error("negative control: false boundary");
    }
  }
  if(rows!==84||transitionRows!==126||residuals!==84||comparisons!==21)
    throw Error("case count mismatch");
  return {status:"PASS_LOCAL_EXACT_E1",interior_cases:rows,transition_rows:transitionRows,
    zero_residuals:residuals,recurrence_formula_checks:comparisons,negative_controls:2,
    anchors:{N5_disadvantaged:"16/211",N5_neutral:"1/5",N5_advantaged:"81/211"},
    csv:"N,fitness_A,fitness_B,initial_mutant_B_count,fixation_probability\n"+
      output.map(x=>x.join(",")).join("\n")+"\n"};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module){
  const result=runAudit();
  process.stdout.write(JSON.stringify({...result,csv:undefined})+"\n");
}
