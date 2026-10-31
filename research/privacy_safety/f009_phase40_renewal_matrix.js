function evaluate() {
  const fields=["old_tsa_compromised","old_hash_weak","time_renewal","hash_tree_renewal","chain_intact","new_tsa_valid","independent_witness","renewal_precedes_break"];
  const count={REVIEW:0,UNKNOWN:0,REJECT:0};
  const review=[];
  for(let mask=0;mask<256;mask++){
    const x=Object.fromEntries(fields.map((f,i)=>[f,Boolean(mask&(1<<i))]));
    let state;
    if(!x.chain_intact||!x.new_tsa_valid)state="REJECT";
    else if(x.old_hash_weak&&!x.hash_tree_renewal)state="UNKNOWN";
    else if(x.old_tsa_compromised&&!x.time_renewal)state="UNKNOWN";
    else if(!x.renewal_precedes_break||!x.independent_witness)state="UNKNOWN";
    else if(!x.old_hash_weak&&!x.time_renewal)state="UNKNOWN";
    else state="REVIEW";
    count[state]++;
    if(state==="REVIEW"){
      if(!x.chain_intact||!x.new_tsa_valid||!x.independent_witness||!x.renewal_precedes_break||
         (x.old_hash_weak&&!x.hash_tree_renewal)||(x.old_tsa_compromised&&!x.time_renewal))throw Error("unsafe REVIEW");
      review.push(mask);
    }
  }
  if(count.REVIEW!==7||count.UNKNOWN!==57||count.REJECT!==192)throw Error("matrix changed");
  return {states:256,count,review_masks:review,automatic_execution:0};
}

if(require.main===module)process.stdout.write(JSON.stringify(evaluate(),null,2)+"\n");
module.exports={evaluate};
