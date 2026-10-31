"use strict";
/* F009 phase38: toy retrospective compromise-window policy, not PKI verification. */
function requireTrue(ok, label) { if (!ok) throw new Error(label); }
const PUBLIC_REVOCATION = 12;
const INTERVALS = {known:[5,8],unknown:null,contradictory:[9,4]};
function strict(s) {
  const interval = INTERVALS[s.interval];
  if (!interval || interval[0] > interval[1]) return "UNKNOWN";
  if (!s.crl_fresh || !s.anchor_verified) return "UNKNOWN";
  if (s.signature_time >= PUBLIC_REVOCATION || s.signature_time >= interval[1]) return "REJECT";
  if (s.signature_time >= interval[0]) return "UNKNOWN";
  if (s.timestamp_attested && s.independent_recovery) return "REVIEW";
  return "UNKNOWN";
}
function loose(s) { return s.signature_time < PUBLIC_REVOCATION && s.timestamp_attested && s.anchor_verified; }
function main() {
  const counts={REVIEW:0,UNKNOWN:0,REJECT:0}, looseAccepted={total:0,withoutReview:0}, states=[];
  for (const interval of Object.keys(INTERVALS))
    for (let signature_time=0;signature_time<16;signature_time++)
      for(let bits=0;bits<16;bits++){
        const s={interval,signature_time,crl_fresh:!!(bits&1),anchor_verified:!!(bits&2),timestamp_attested:!!(bits&4),independent_recovery:!!(bits&8)};
        const outcome=strict(s);counts[outcome]++;if(loose(s)){looseAccepted.total++;if(outcome!=="REVIEW")looseAccepted.withoutReview++;}
        states.push(s);
      }
  requireTrue(states.length===768,"universe");
  requireTrue(Object.values(counts).reduce((a,b)=>a+b,0)===768,"partition");
  const base={interval:"known",signature_time:4,crl_fresh:true,anchor_verified:true,timestamp_attested:true,independent_recovery:true};
  for (const [name,edit,expected] of [
    ["early documented",{}, "REVIEW"],
    ["within uncertain window",{signature_time:6},"UNKNOWN"],
    ["after latest possible compromise",{signature_time:9},"REJECT"],
    ["after publication",{signature_time:13},"REJECT"],
    ["missing attestation",{timestamp_attested:false},"UNKNOWN"],
    ["missing independent recovery",{independent_recovery:false},"UNKNOWN"],
    ["stale revocation list",{crl_fresh:false},"UNKNOWN"],
    ["untrusted anchor",{anchor_verified:false},"UNKNOWN"],
    ["unknown compromise interval",{interval:"unknown"},"UNKNOWN"],
    ["contradictory interval",{interval:"contradictory"},"UNKNOWN"]
  ]) requireTrue(strict({...base,...edit})===expected,name);
  for(let t=0;t<16;t++){
    const s={...base,signature_time:t};
    if(strict({...s,crl_fresh:false})==="REVIEW"||strict({...s,anchor_verified:false})==="REVIEW")throw new Error("downgrade monotonicity");
  }
  return {states:states.length,counts,looseAccepted,controls:10,downgrade_checks:32,compromise_possible_start:5,compromise_possible_end:8,public_revocation_time:12};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));
