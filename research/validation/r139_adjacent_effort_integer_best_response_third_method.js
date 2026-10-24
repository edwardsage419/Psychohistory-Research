"use strict";
// R139 third method. Node or V8. No dependencies and no original R139 imports.
// Project-created 3-player finite common-pool game, synthetic E1 only.
const actions=[0,2,4,6,8,10,12,14,16];
function cmp(n1,d1,n2,d2){return Math.sign(n1*d2-n2*d1)}
function utility(e,s){return [e*(32-s-e),4+s+e]}
function welfare(S){return [S*(32-S),4+S]}
function bestResponses(s){
  const K=4+s,signs=[];
  for(let e=0;e<16;e+=2){
    const numerator=36*K-(K+e)*(K+e+2);
    signs.push(Math.sign(numerator));
  }
  for(let j=1;j<signs.length;j++)if(signs[j]>signs[j-1])throw Error("non-monotone adjacent sign");
  const first=signs.findIndex(x=>x<=0);
  const br=first<0?[16]:signs[first]===0?[2*first,2*first+2]:[2*first];
  // Independent full nine-action rational maximum cross-check.
  const values=actions.map(e=>utility(e,s));
  const brute=actions.filter((e,j)=>values.every(([n,d])=>cmp(values[j][0],values[j][1],n,d)>=0));
  if(JSON.stringify(br)!==JSON.stringify(brute))throw Error("BR disagreement at "+s);
  return {s,adjacent_signs:signs,best:br};
}
function main(){
  const br=actions.concat([18,20,22,24,26,28,30,32]).map(bestResponses);
  let worlds=0,deviations=0,disagreements=0;
  const equilibria=[];
  const optimumProfiles=[];
  const socialValues=[];
  for(let S=0;S<=48;S+=2)socialValues.push({S,value:welfare(S)});
  const bestW=socialValues.reduce((a,b)=>cmp(a.value[0],a.value[1],b.value[0],b.value[1])>=0?a:b);
  for(const a of actions)for(const b of actions)for(const c of actions){
    worlds++;
    const profile=[a,b,c],S=a+b+c;
    const byBR=profile.every((e,i)=>br[(S-e)/2].best.includes(e));
    let byDeviation=true;
    for(let i=0;i<3;i++){
      const s=S-profile[i],truth=utility(profile[i],s);
      for(const candidate of actions){
        if(candidate===profile[i])continue;
        const alt=utility(candidate,s);
        if(cmp(alt[0],alt[1],truth[0],truth[1])>0)byDeviation=false;
        deviations++;
      }
    }
    if(byBR!==byDeviation)disagreements++;
    if(byBR)equilibria.push(profile);
    const value=welfare(S);
    if(cmp(value[0],value[1],bestW.value[0],bestW.value[1])===0)optimumProfiles.push(profile);
  }
  const noCostBest=(s)=>actions.reduce((best,e)=>e*36/(4+s+e)>best*36/(4+s+best)?e:best,0);
  const negatives={no_cost_s0:noCostBest(0),no_cost_s32:noCostBest(32),true_s0:br[0].best,true_s32:br[16].best};
  const result={method:"integer_adjacent_effort_best_response",opponent_sum_conditions:br.length,adjacent_sign_checks:br.length*8,worlds,deviations,disagreements,equilibria,optimum_total_effort:bestW.S,optimum_profile_count:optimumProfiles.length,optimum_welfare:bestW.value,ne_welfare:welfare(22),negative_controls:negatives,br_table:br,evidence:"internal_E1_only"};
  const expected=[[6,8,8],[8,6,8],[8,8,6]];
  if(worlds!==729||deviations!==17496||disagreements||JSON.stringify(equilibria)!==JSON.stringify(expected)||bestW.S!==8||optimumProfiles.length!==15||noCostBest(0)!==16||noCostBest(32)!==16||JSON.stringify(br[0].best)!=="[8]"||JSON.stringify(br[16].best)!=="[0]")throw Error(JSON.stringify(result));
  return result;
}
const result=main();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
