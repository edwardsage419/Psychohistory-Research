/* F009 phase24: fictional re-enrollment and restore-scope safety policy. Run: node <this file>. */
function run(){let checks=0,states=0,naive=0,strict=0,over=0;
function check(v,m){checks++;if(!v)throw Error(m)}
function gate(B,R,A,I,T){return {loose:A&&B!=="OFFLINE",strict:A&&B==="REJOIN_CURRENT"&&I&&T&&R!=="OLD_SCOPE"}}
for(const B of ["OFFLINE","REJOIN_OLD","REJOIN_CURRENT"])for(const R of ["NONE","OLD_SCOPE","CURRENT_SCOPE"])
for(const A of [false,true])for(const I of [false,true])for(const T of [false,true]){
states++;const x=gate(B,R,A,I,T);if(x.loose)naive++;if(x.strict)strict++;if(x.loose&&!x.strict)over++;
check(!x.strict||x.loose,"strict implies loose");}
check(!gate("REJOIN_OLD","OLD_SCOPE",true,true,true).strict,"old rejoin");
check(gate("REJOIN_CURRENT","CURRENT_SCOPE",true,true,true).strict,"fresh rejoin");
check(!gate("OFFLINE","NONE",true,true,true).strict,"offline");
check(!gate("REJOIN_CURRENT","OLD_SCOPE",true,true,true).strict,"old scope");
check(!gate("REJOIN_CURRENT","NONE",true,false,true).strict,"unknown inventory");
check(!gate("REJOIN_CURRENT","NONE",true,true,false).strict,"no tombstone");
check(states===72&&naive===24&&strict===2&&over===22,"counts");
return {states,assertions:checks,naive,strict,over};}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));
