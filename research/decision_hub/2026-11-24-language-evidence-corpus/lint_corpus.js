/* Node >=18. Dataset integrity only; no LLM or natural language extraction. */
const fs=require('node:fs');
function lint(corpus){
 const ids=new Set(),sourceIds=new Set(corpus.sources.map(x=>x.id)),seenClaims=new Map(),domains={},kinds={},statuses={},rows=[],questions={count:0};
 for(const episode of corpus.cases){
  if(ids.has(episode.id)||episode.turns.length!==2||episode.sources.some(s=>!sourceIds.has(s)))throw Error("episode");
  ids.add(episode.id);domains[episode.domain]=(domains[episode.domain]||0)+1;
  for(let i=0;i<episode.turns.length;i++){
   const t=episode.turns[i];if(!t.text||!t.expected||!t.forbid.length)throw Error("turn");
   statuses[t.expected]=(statuses[t.expected]||0)+1;if(t.question)questions.count++;
   for(const c of t.claims){
    const start=t.text.indexOf(c.span);if(start<0||t.text.indexOf(c.span,start+c.span.length)>=0)throw Error("span "+episode.id+" "+c.span);
    if(c.supersedes&&!seenClaims.has(c.supersedes))throw Error("revision "+c.supersedes);
    if(c.op&& !["<","<=",">",">=","=="].includes(c.op))throw Error("operator");
    if(c.lo!==undefined&&(c.hi===undefined||c.lo>c.hi||!c.unit))throw Error("interval");
    if(c.kind==="ESTIMATE"&&c.field==="forecast"&&(c.value<0||c.value>1))throw Error("forecast");
    const key=episode.id+":t"+i+":"+c.field;seenClaims.set(key,c);kinds[c.kind]=(kinds[c.kind]||0)+1;
    rows.push({episode:episode.id,turn:i,field:c.field,kind:c.kind,start,end:start+c.span.length});
   }
  }
 }
 // Mutations test lint rejects unsupported quote, dangling revision and malformed interval. Isolate fixture copy.
 return {episodes:ids.size,turns:corpus.cases.reduce((s,x)=>s+x.turns.length,0),claims:rows.length,domains,kinds,statuses,questions:questions.count,rows};
}
const c=JSON.parse(fs.readFileSync(require('node:path').join(__dirname,'language_corpus.json'),'utf8'));console.log(JSON.stringify(lint(c),null,2));
