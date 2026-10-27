"use strict";
// MKT076 offline synthetic OAuth transport and deauthorization callback contract.
// Run: node mkt076_oauth_deauth_synthetic_20261027.js (Node 18+).
// All tokens are fictional. No HTTP requests, account creation, or charges.
function run(){
 let checks=0;const failures=[];
 const ok=(value,label)=>{checks++;if(!value)failures.push(label)};
 const token="FAKE_TOKEN_MKT076_DO_NOT_USE";
 const callback="https://client.example/callback?access_token="+token+"&username=synthetic";
 const apiUrl="https://www.beeminder.com/api/v1/users/me.json";
 const bearer={url:apiUrl,headers:{Authorization:"Bearer "+token}};
 const query={url:apiUrl+"?access_token="+token,headers:{}};
 const redact=s=>s.replace(/(access_token|auth_token)=([^&#\s]+)/g,"$1=[REDACTED]").replace(/Bearer\s+[^\s]+/g,"Bearer [REDACTED]");
 const form=s=>Object.fromEntries(s.split("&").map(p=>p.split("=").map(decodeURIComponent)));
 ok(callback.includes("access_token="+token),"documented redirect has token in query");
 ok(callback.includes("username=synthetic"),"redirect includes username");
 ok(callback.startsWith("https://"),"synthetic redirect https");
 ok(!apiUrl.includes(token),"base api URL clean");
 ok(bearer.url===apiUrl,"bearer URL clean");
 ok(bearer.headers.Authorization==="Bearer "+token,"bearer header");
 ok(!bearer.url.includes(token),"bearer token absent from URL");
 ok(query.url.includes(token),"query variant contains token");
 ok(!query.headers.Authorization,"query variant no header");
 ok(redact(callback).includes("[REDACTED]"),"callback URL redacted");
 ok(!redact(callback).includes(token),"callback token removed");
 ok(!redact(query.url).includes(token),"query token removed");
 ok(!redact("Authorization: "+bearer.headers.Authorization).includes(token),"header token removed");
 ok(redact("auth_token="+token).includes("auth_token=[REDACTED]"),"personal token redacted");
 const parsed=form("access_token="+token);
 ok(parsed.access_token===token,"callback body parsed");
 ok(!("signature" in parsed),"documented minimal callback has no signature field");
 let state={generation:0,authorized:true,queue:["old"],derived:"valid",lastEvent:null};
 const accept=(body,validated)=>{
  const p=form(body);
  if(!validated||p.access_token!==token)return false;
  state.generation++;state.authorized=false;state.queue=[];state.derived="stale";state.lastEvent="revoked";return true;
 };
 ok(!accept("access_token="+token,false),"unverified callback rejected by candidate guard");
 ok(state.authorized,"unverified callback no state change");
 ok(!accept("access_token=OTHER",true),"wrong token rejected");
 ok(state.generation===0,"wrong token no generation change");
 ok(accept("access_token="+token,true),"verified synthetic callback accepted");
 ok(!state.authorized,"authorization closed");
 ok(state.queue.length===0,"queued work cancelled");
 ok(state.derived==="stale","derived output invalidated");
 ok(state.generation===1,"generation advanced");
 ok(state.lastEvent==="revoked","revocation event stored");
 const staleResponseGeneration=0;
 ok(staleResponseGeneration!==state.generation,"in-flight old response rejected");
 ok(!accept("access_token="+token,false),"duplicate unverified callback rejected");
 ok(state.generation===1,"rejected duplicate leaves generation");
 const sensitiveLog=JSON.stringify({url:callback,headers:bearer.headers});
 ok(sensitiveLog.includes(token),"raw debug record unsafe");
 ok(!redact(sensitiveLog).includes(token),"redacted debug record clean");
 return {checks,failures,source:"synthetic transport and consent state only",network_calls:0};
}
if(typeof require!=="undefined"&&require.main===module){const r=run();console.log(JSON.stringify(r));if(r.failures.length)process.exitCode=1}
if(typeof module!=="undefined")module.exports={run};
