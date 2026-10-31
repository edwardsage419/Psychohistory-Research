// MKT183 synthetic note retention and conflict, no service access.
function mkt183(){
 const revisions=[-100,-70,-20],retention=(settings)=>({days:settings,retained:revisions.filter(x=>x>=-Math.min(...settings)),purged:revisions.filter(x=>x< -Math.min(...settings))});
 const a=retention([90,90]),b=retention([90,30]),c=retention([30,100]),d=retention([90]);
 const conflict=(base,left,right)=>left!==base&&right!==base&&left!==right;
 const tests=[a.retained.join(",")==="-70,-20",b.retained.join(",")==="-20",b.purged.includes(-70),c.retained.length===1,d.retained.includes(-70),conflict("old","editA","editB"),!conflict("old","editA","old")];
 if(tests.some(x=>!x))throw Error("synthetic retention failure");
 return {scope:"synthetic; Joplin runtime not executed",revisions,a,b,c,d,offline_conflict:true,assertions:tests.length};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(mkt183(),null,2));
