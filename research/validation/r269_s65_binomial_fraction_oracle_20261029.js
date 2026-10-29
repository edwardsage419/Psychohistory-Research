/* R269 S65 independent E1 binomial oracle. Node.js standard library only.
   Prescore freeze: protocols/R269_S65_POSTSELECTION_NEW_GROUP_BRIER_PRESCORE_FREEZE_2026-10-29.md
   This route never reads the R269 row-fold prediction generator. */
function runR269S65() {
  const abs=x=>x<0n?-x:x;
  const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b){let t=a%b;a=b;b=t;}return a;};
  class Q {
    constructor(n,d=1n) {n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
    add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
    neg(){return new Q(-this.n,this.d);}
    sub(b){return this.add(b.neg());}
    mul(b){return new Q(this.n*b.n,this.d*b.d);}
    div(b){return new Q(this.n*b.d,this.d*b.n);}
    pow(k){return new Q(this.n**BigInt(k),this.d**BigInt(k));}
    lt(b){return this.n*b.d<b.n*this.d;}
    eq(b){return this.n===b.n&&this.d===b.d;}
    toString(){return this.d===1n?String(this.n):String(this.n)+"/"+String(this.d);}
  }
  const f=(a,b=1)=>new Q(a,b),zero=f(0),one=f(1),quarter=f(1,4),half=f(1,2);
  const models=["GROUP_ID_MEMORIZER","GLOBAL_LAPLACE","CONSTANT_HALF"];
  const choose=(scores)=>{let m=scores[0];for(let j=1;j<scores.length;j++)if(scores[j].lt(m))m=scores[j];let ties=scores.map((v,j)=>v.eq(m)?j:-1).filter(j=>j>=0);return {index:ties[0],best:m,tie:ties.length>1};};
  const C=(n,k)=>{let x=1n;for(let i=1;i<=k;i++)x=x*BigInt(n-i+1)/BigInt(i);return f(x);};
  const out={research:"R269_S65",evidence:"E1_ARTIFICIAL",
    protocol:"R269_S65_POSTSELECTION_NEW_GROUP_BRIER_PRESCORE_FREEZE_2026-10-29.md",worlds:{}};
  for (const p of [f(1,4),f(1,2),f(3,4)]) {
    const bucket={LOOR:{risk:zero,cv:zero,ties:zero,counts:[zero,zero,zero]},
                  LOGO:{risk:zero,cv:zero,ties:zero,counts:[zero,zero,zero]}};
    let fixed=[zero,zero,zero],mass=zero;
    for(let k=0;k<=6;k++){
      const w=C(6,k).mul(p.pow(k)).mul(one.sub(p).pow(6-k));
      mass=mass.add(w);
      let logo=zero,loor=zero;
      for(let b=0;b<=1;b++){
        let count=b?k:6-k;if(!count)continue;
        let s=k-b;
        let qGroup=f(2*s+1,12),qRow=f(2*s+b+1,13);
        logo=logo.add(f(count,6).mul(qGroup.sub(f(b)).pow(2)));
        loor=loor.add(f(count,6).mul(qRow.sub(f(b)).pow(2)));
      }
      const q=f(2*k+1,14);
      const future=one.sub(p).mul(q.pow(2)).add(p.mul(one.sub(q).pow(2)));
      const risks=[quarter,future,quarter];
      for(let j=0;j<3;j++)fixed[j]=fixed[j].add(w.mul(risks[j]));
      for(const pol of ["LOOR","LOGO"]){
        const scores=pol==="LOOR"?[zero,loor,quarter]:[quarter,logo,quarter];
        const selected=choose(scores),b=bucket[pol];
        b.risk=b.risk.add(w.mul(risks[selected.index]));
        b.cv=b.cv.add(w.mul(selected.best));
        b.counts[selected.index]=b.counts[selected.index].add(w);
        if(selected.tie)b.ties=b.ties.add(w);
      }
    }
    if(!mass.eq(one))throw Error("source mass");
    let obj={};
    for(const pol of ["LOOR","LOGO"]){
      const b=bucket[pol];
      const sm=Object.fromEntries(models.map((m,i)=>[m,b.counts[i].toString()]));
      if(!b.counts.reduce((a,v)=>a.add(v),zero).eq(one))throw Error("selection mass");
      obj[pol]={expected_new_group_brier:b.risk.toString(),
        expected_selected_cv_brier:b.cv.toString(),
        cv_minus_new_group:b.cv.sub(b.risk).toString(),
        selection_mass:sm,tie_mass:b.ties.toString()};
    }
    obj.LOGO_minus_LOOR_future_risk=bucket.LOGO.risk.sub(bucket.LOOR.risk).toString();
    obj.fixed_model_new_group_risk=Object.fromEntries(models.map((m,i)=>[m,fixed[i].toString()]));
    out.worlds[p.toString()]=obj;
  }
  const expected={
    "1/4":["3209/14336","-375/14336","1103/2048"],
    "1/2":["425/1568","33/1568","7/32"],
    "3/4":["3209/14336","-375/14336","1103/2048"]};
  for(const [p,a] of Object.entries(expected)){
    let w=out.worlds[p];
    if(w.LOGO.expected_new_group_brier!==a[0]||
       w.LOGO_minus_LOOR_future_risk!==a[1]||
       w.LOGO.selection_mass.GLOBAL_LAPLACE!==a[2])throw Error("independent Python Fraction comparison failed");
  }
  return out;
}
if(typeof module!=="undefined"&&require.main===module)
  process.stdout.write(JSON.stringify(runR269S65(),null,2)+"\n");
