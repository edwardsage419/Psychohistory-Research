/* Node.js >=18; replay identity audit against archived snapshot, no runtime model authorization. */
const fs=require('node:fs');
function audit(index){
 const linked=new Map(index.methods.map(m=>[m.key,m]));
 const rows=[];
 function eligible(key,path,blob){const m=linked.get(key);return !!m&&m.sources.some(s=>s.status==="MATCH"&&s.path===path&&s.baselineBlob===blob)}
 for(const m of index.methods)for(const s of m.sources){
  for(const [kind,key,path,blob] of [["exact",m.key,s.path,s.currentBlob],["version",m.key.replace("@1.0.0","@9.0.0"),s.path,s.currentBlob],["hash",m.key,s.path,"0".repeat(40)],["path",m.key,s.path+".wrong",s.currentBlob]]){
   const actual=eligible(key,path,blob),expected=kind==="exact"&&s.status==="MATCH";if(actual!==expected)throw Error("identity");
   rows.push({key:m.key,path:s.path,kind,actual,expected});
  }
 }
 const groups={};for(const a of index.assets)if(a.shortId)(groups[a.shortId]??=[]).push(a);
 const collisions=Object.entries(groups).filter(([,a])=>a.length>1).map(([shortId,a])=>({shortId,paths:a.map(x=>x.path)}));
 // Compare deliberately unsafe short-ID lookup to exact source relation on actual C-number documents.
 const aliases=[];
 for(const m of index.methods)for(const s of m.sources){
  const source=index.assets.find(a=>a.path===s.path);if(!source?.shortId)continue;
  for(const a of groups[source.shortId]){
   const exact=eligible(m.key,a.path,a.blob);
   aliases.push({key:m.key,source:s.path,proposed:a.path,shortId:a.shortId,naive:true,exact});
  }
 }
 return {summary:{assets:index.assets.length,registeredMethods:index.methods.length,linkedAssets:index.assets.filter(x=>x.linkedMethods.length).length,unmappedAssets:index.assets.filter(x=>!x.linkedMethods.length).length,declaredSourceEdges:index.methods.reduce((s,m)=>s+m.sources.length,0),matchingEdges:index.methods.flatMap(x=>x.sources).filter(s=>s.status==="MATCH").length,missingEdges:index.methods.flatMap(x=>x.sources).filter(s=>s.status==="MISSING").length,changedEdges:index.methods.flatMap(x=>x.sources).filter(s=>s.status==="CHANGED").length,numberedGroups:Object.keys(groups).length,multiFileNumberGroups:collisions.length,identityControls:rows.length,shortIdComparisons:aliases.length,shortIdUnsupported:aliases.filter(a=>!a.exact).length,excerptReviewed:index.assets.filter(a=>a.contentReview==="EXCERPT_REVIEW").length,relations:index.relations.length},collisions,identityRows:rows,aliasRows:aliases};
}
console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'corpus_index.json'),'utf8'))),null,2));
