import { useCallback, useEffect, useRef, useState } from 'react';
import { flushSync } from 'react-dom';
import { MechanismWorkflow } from './MechanismWorkflow';
import { ResearchWorkflow } from './ResearchWorkflow';
import { DecisionWorkbench } from './DecisionWorkbench';
import { DecisionConversation } from './DecisionConversation';
import { DecisionApiError } from './decisionTypes';

type Run={id:string;status:string;created_at:number;logs:string[];error:string|null;result_hash:string|null;kind?:string;protocol:string;code_sha256:string;config:Record<string,number>};
type Model={model_id:string;version:string;capabilities:string[];source_sha256:string;assumptions:string[];scale:string;input:string;output:string;evidence:string;permission:string};
type Asset={path:string;sha256:string;permission:string;scientific_status:{namespace:string;original_record:unknown}};
type History={tick:number;prevalence:number;exposure_used:number;group_updated:boolean;snapshot_hash:string};
type Result={scientific_status:string;versions:Record<string,string>;input:Record<string,number>;uncertainty:{kind:string};logs:string[];branches:Record<string,{parent_hash:string;history:History[];final_snapshot:{content_hash:string}}> ;comparison:{scenario_minus_baseline:number;interpretation:string}};
const sections=['研究看板','研究工作流','机制实验','模型注册','实验工作台','情景历史','审批与证据','个人决策工作台'] as const;
const labels:Record<string,string>={PENDING:'待审批',APPROVED:'已批准',RUNNING:'运行中',COMPLETED:'已完成',FAILED:'失败',CANCELED:'已取消',BLOCKED:'已阻塞'};

export function App(){
 const [workflow]=useState(()=>new URLSearchParams(window.location.search).get('workflow'));
 const legacy=workflow==='v04';
 const conversational=workflow!=='v04'&&workflow!=='v05'&&workflow!=='research';
 const [section,setSection]=useState<string>(conversational?'个人决策工作台':'研究看板');
 const [token,setToken]=useState('');const [connected,setConnected]=useState(false);
 const [visitedPersonal,setVisitedPersonal]=useState(false);
 const personal=section==='个人决策工作台';
 const conversationId=useRef<string|null>(null);
 const registerConversation=useCallback((id:string|null)=>{conversationId.current=id;},[]);
 const closeConversation=useCallback(()=>{
   const session_id=conversationId.current;
   conversationId.current=null;
   if(token&&session_id)void fetch('/api/v7/decisions/end',{method:'POST',cache:'no-store',keepalive:true,headers:{Authorization:`Bearer ${token}`,'Content-Type':'application/json'},body:JSON.stringify({session_id})}).catch(()=>{});
 },[token]);
 const [session,setSession] = useState(()=>new AbortController());
 const [runs,setRuns]=useState<Run[]>([]);const [models,setModels]=useState<Model[]>([]);const [assets,setAssets]=useState<Asset[]>([]);
 const [historyOffset,setHistoryOffset]=useState(0);const [moreHistory,setMoreHistory]=useState(false);const [selectedRun,setSelectedRun]=useState<Run|null>(null);const refreshSequence=useRef(0);
 const [selected,setSelected]=useState('');const [result,setResult]=useState<Result|null>(null);const [error,setError]=useState('');const [busy,setBusy]=useState(false);
 const [form,setForm]=useState({seed:7,rounds:8,population:24,intervention:0.2});const [source,setSource]=useState('research/R233/R233_FINAL_ACCEPTANCE_STATUS.json');
 const api=useCallback(async <T,>(path:string,body?:unknown,version:'v1'|'v2'|'v3'|'v4'|'v5'|'v6'|'v7'='v1',scope?:AbortSignal):Promise<T>=>{
   const signal=scope?AbortSignal.any([session.signal,scope]):session.signal;
   const response=await fetch(`/api/${version}/${path}`,{signal,cache:'no-store',method:body===undefined?'GET':'POST',headers:{Authorization:`Bearer ${token}`,...(body===undefined?{}:{'Content-Type':'application/json'})},...(body===undefined?{}:{body:JSON.stringify(body)})});
   const data=await response.json();
   signal.throwIfAborted();
   if(!response.ok){
     if(version==='v4'||version==='v5'||version==='v6'||version==='v7')throw new DecisionApiError(typeof data.detail==='string'?data.detail:data.detail?.[0]?.msg??'个人决策请求失败。',response.status);
     throw new Error(typeof data.detail==='string'?data.detail:JSON.stringify(data.detail));
   }
   return data as T;
 },[token,session]);
 const refresh=useCallback(async()=>{const seq=++refreshSequence.current;const [r,live,m,a,chosen]=await Promise.all([api<Run[]>(`runs?limit=50&offset=${historyOffset}`),api<Run[]>('runs/active'),api<Model[]>('models'),api<Asset[]>('assets'),selected?api<Run>(`runs/${selected}`):Promise.resolve(null)]);if(seq!==refreshSequence.current)return r;setRuns([...new Map([...live,...r].map(run=>[run.id,run])).values()]);setMoreHistory(r.length===50);setSelectedRun(chosen);setModels(m);setAssets(a);return r;},[api,historyOffset,selected]);
 async function action(work:()=>Promise<void>){const current=session;setBusy(true);setError('');try{await work();}catch(e){if(!current.signal.aborted)setError(String(e));}finally{if(!current.signal.aborted)setBusy(false);}}
 const endSession=useCallback(()=>{
   closeConversation();
   session.abort();
   setSession(new AbortController());
   refreshSequence.current+=1;
   setConnected(false);setToken('');setVisitedPersonal(false);setBusy(false);setError('');
   setRuns([]);setModels([]);setAssets([]);setSelectedRun(null);setSelected('');setResult(null);setHistoryOffset(0);setMoreHistory(false);
 },[session,closeConversation]);
 useEffect(()=>{
   const purge=()=>flushSync(endSession);
   const restore=(event:PageTransitionEvent)=>{if(event.persisted)purge();};
   window.addEventListener('pagehide',purge);
   window.addEventListener('pageshow',restore);
   return()=>{window.removeEventListener('pagehide',purge);window.removeEventListener('pageshow',restore);};
 },[endSession]);
 useEffect(()=>{if(!connected||(personal&&conversational))return;let active=true;refresh().catch(e=>{if(active)setError(String(e));});const interval=setInterval(()=>{refresh().catch(e=>{if(active)setError(String(e));});},700);return()=>{active=false;clearInterval(interval);};},[connected,refresh,personal,conversational]);
 const current=runs.find(r=>r.id===selected)||(selectedRun?.id===selected&&(!selectedRun.kind||selectedRun.kind==='legacy')?selectedRun:undefined);
 useEffect(()=>{let active=true;setResult(null);if(connected&&current?.status==='COMPLETED')api<Result>(`runs/${current.id}/result`).then(x=>{if(active)setResult(x);}).catch(e=>{if(active)setError(String(e));});return()=>{active=false;};},[connected,current?.id,current?.status,api]);
 const choose=(r:Run)=>{setSelected(r.id);setSection('实验工作台');};
 const status=(r:Run)=><span className={`status ${r.status.toLowerCase()}`}><span>{labels[r.status]}</span> <small>{r.status}</small></span>;
 const historyControls=<div className="actions" aria-label="实验历史分页"><button className="quiet" disabled={historyOffset===0||busy} onClick={()=>setHistoryOffset(Math.max(0,historyOffset-50))}>较新一页</button><span className="muted">历史第 {historyOffset/50+1} 页 · 活动任务始终显示</span><button className="quiet" disabled={!moreHistory||busy} onClick={()=>setHistoryOffset(historyOffset+50)}>较早一页</button></div>;
 const taskTable=<div className="table-wrap"><table><thead><tr><th>实验标识</th><th>种子 / 轮次</th><th>状态</th><th>操作</th></tr></thead><tbody>{runs.map(r=><tr key={r.id}><td><button className="text-button mono" onClick={()=>choose(r)}>{r.id.slice(0,12)}</button></td><td>{r.config.seed} / {r.config.rounds}</td><td>{status(r)}</td><td className="actions">{r.status==='PENDING'&&<button disabled={busy} onClick={()=>action(async()=>{await api(`runs/${r.id}/approve`,{});setSelected(r.id);await refresh();})}>批准合成执行</button>}{['PENDING','APPROVED','RUNNING'].includes(r.status)&&<button className="quiet" disabled={busy} onClick={()=>action(async()=>{await api(`runs/${r.id}/cancel`,{});setSelected(r.id);await refresh();})}>取消</button>}<button className="quiet" onClick={()=>choose(r)}>查看</button></td></tr>)}</tbody></table>{historyControls}{!runs.length&&<p className="empty">尚无实验。创建一个有版本、有种子、可复现的合成实验。</p>}</div>;
 const results=result&&<>
  <section className="card"><div className="section-heading"><div><span className="eyebrow">SCENARIO COMPARISON</span><h2>两条独立情景分支</h2></div><span className="pill">仅合成数据</span></div>
  <p className="muted">蓝色为基线，绿色为参数情景。分支使用相同随机种子；差异不代表真实因果效应。</p>
  <div className="chart" role="img" aria-label="两个合成情景的传播比例随轮次变化"><svg viewBox="0 0 720 210"><path d="M30 15V180H700 M30 97H700" stroke="#dce4e9" fill="none"/>{Object.entries(result.branches).map(([name,b])=><polyline key={name} points={b.history.map((x,i)=>`${30+(i/Math.max(1,b.history.length-1))*660},${180-x.prevalence*160}`).join(' ')} fill="none" stroke={name==='baseline'?'#5476c2':'#168b75'} strokeWidth="3"/>)}<text x="5" y="25">1</text><text x="5" y="184">0</text><text x="635" y="205">模拟轮次 →</text></svg></div>
  <div className="metric-grid compact"><div><span>情景 − 基线</span><strong>{result.comparison.scenario_minus_baseline.toFixed(4)}</strong></div><div><span>真实世界有效性</span><strong className="unknown">UNKNOWN</strong></div><div><span>运行性质</span><strong className="small-value">SYNTHETIC_ONLY</strong></div></div>
  </section>
  <div className="two-col">{Object.entries(result.branches).map(([name,b])=><section className="card" key={name}><span className="eyebrow">{name.toUpperCase()}</span><h3>{name==='baseline'?'基线情景':'参数变化情景'}</h3><p className="muted">共同根快照</p><code className="hash">{b.parent_hash}</code><p className="muted">最终不可变快照</p><code className="hash">{b.final_snapshot.content_hash}</code><table><thead><tr><th>轮次</th><th>传播比例</th><th>使用的暴露</th><th>群体更新</th></tr></thead><tbody>{b.history.map(h=><tr key={h.tick}><td>{h.tick}</td><td>{h.prevalence.toFixed(3)}</td><td>{h.exposure_used.toFixed(3)}</td><td>{h.group_updated?'更新':'保持'}</td></tr>)}</tbody></table></section>)}</div>
  <section className="card"><h3>版本锁定与完整运行日志</h3><div className="version-row">{Object.entries(result.versions).map(([k,v])=><code key={k}>{k}@{v}</code>)}</div><pre>{(current?.logs||result.logs).join('\n')}</pre></section>
 </>;
 return <div className="layout"><aside><a className="brand" href="#"><span className="brand-icon">Ψ</span><span>心理史学<small>RESEARCH PLATFORM</small></span></a><div className="workspace"><span className="dot"/>Psychohistory-Platform<small>云端科研工作空间 · v0.3</small></div><nav aria-label="平台导航">{sections.map((name,i)=><button key={name} className={section===name?'active':''} aria-current={section===name?'page':undefined} onClick={()=>{if(name==='个人决策工作台')setVisitedPersonal(true);else if(conversational)closeConversation();setSection(name);}}><span className="nav-number" aria-hidden="true">0{i+1}</span>{name}</button>)}</nav><div className="sidebar-note"><span className="eyebrow">SCIENTIFIC BOUNDARY</span><p>保留未知，保留分歧。<br/>工程成功 ≠ 科学验证。</p><small>R073 / PESEN v0.1 保持冻结<br/>不启动原创模型熔炼</small></div></aside>
 <main><header><div className="breadcrumb">{personal?'个人决策':'科研基础设施'} <span>/</span> {section}</div><div className="session-controls"><span className="session-state"><span className={connected?'dot':'dot offline'}/>{connected?'工作空间已连接':'本地会话未连接'}</span>{connected&&<button type="button" className="quiet" onClick={endSession}>结束本地会话</button>}</div></header><div className="content"><div className="page-title"><div><span className="eyebrow">{personal?(conversational?'个人决策 · V0.7':legacy?'个人决策 · V0.4':'个人决策 · V0.5'):'PSYCHOHISTORY RESEARCH · V0.3'}</span><h1>{section}</h1><p>{personal?'澄清现实选择，比较取舍，记录之后实际发生的事。':'从可追溯的机制，走向可重复的研究。'}</p></div><span className="pill outline">仅环回访问 · 零外部服务</span></div>
 {!connected&&<section className="card connection"><h2>{personal&&conversational?'连接本地工作空间':'连接本地科研会话'}</h2><p className="muted">使用服务启动时生成的本地令牌。令牌仅保留在当前页面内存，不写入浏览器存储。</p><form onSubmit={e=>{e.preventDefault();action(async()=>{const current=session;if(personal&&conversational)await api('decisions/status',undefined,'v7');else await refresh();if(!current.signal.aborted)setConnected(true);});}}><label>本地访问令牌<input type="password" autoComplete="off" value={token} onChange={e=>setToken(e.target.value)} required/></label><button type="submit" disabled={busy}>连接工作空间</button></form></section>}
 {error&&<div role="alert" className="error">操作未完成：{error}</div>}
 {section==='研究看板'&&<><div className="metric-grid"><section className="card"><span>已注册机制</span><strong>{models.length.toString().padStart(2,'0')}</strong><small>版本锁定 · 独立能力</small></section><section className="card"><span>本页及活动实验</span><strong>{runs.length.toString().padStart(2,'0')}</strong><small>{runs.filter(r=>r.status==='COMPLETED').length} 个完成 · 失败与取消均保留</small></section><section className="card"><span>来源记录</span><strong>{assets.length.toString().padStart(2,'0')}</strong><small>只读登记 · 不自动执行</small></section></div><section className="banner"><div><span className="eyebrow">REPRODUCIBLE BY DESIGN</span><h2>每一次运行，都有来处与版本。</h2><p>个体状态更新 → 版本化适配器 → 双时间尺度群体传播。<br/>独立情景分支、显式不确定性与完整来源记录。</p></div><button onClick={()=>setSection('实验工作台')}>进入实验工作台 →</button></section><section className="card"><h2>近期实验与真实状态</h2>{taskTable}</section></>}
 {connected&&personal&&conversational&&<DecisionConversation api={api} registerConversation={registerConversation} closeConversation={closeConversation}/>}
 {connected&&!conversational&&(personal||(legacy&&visitedPersonal))&&<div hidden={!personal}><DecisionWorkbench api={api} version={legacy?'v4':'v5'}/></div>}
 {section==='研究工作流'&&connected&&<ResearchWorkflow api={api}/>}
 {section==='机制实验'&&connected&&<MechanismWorkflow api={api}/>}
 {section==='模型注册'&&<div className="two-col">{models.map(m=><section className="card" key={m.model_id}><span className="eyebrow">VERSIONED MECHANISM</span><h2>{m.model_id}</h2><span className="pill">{m.version}</span><p>{m.scale}</p><dl><dt>输入</dt><dd>{m.input}</dd><dt>输出</dt><dd>{m.output}</dd><dt>证据边界</dt><dd>{m.evidence} / {m.permission}</dd></dl><h3>数学假设</h3><ul>{m.assumptions.map(a=><li key={a}>{a}</li>)}</ul><h3>声明能力</h3><p className="muted">{m.capabilities.join(' · ')}</p><h3>源码身份 SHA-256</h3><code className="hash">{m.source_sha256}</code></section>)}</div>}
 {section==='实验工作台'&&<><section className="card"><div className="section-heading"><div><span className="eyebrow">SYNTHETIC EXPERIMENT</span><h2>个体更新 × 群体传播</h2></div><span className="pill">协议 synthetic-paired-1.0.0</span></div><p className="muted">提交后需明确批准。群体每两轮更新，反馈在下一轮生效；不使用真实个体数据。</p><form onSubmit={e=>{e.preventDefault();action(async()=>{const r=await api<Run>('runs',{...form,permission:'SYNTHETIC_ONLY'});setSelected(r.id);await refresh();});}}><div className="form-grid">{([['seed','随机种子',0,4294967295,1],['rounds','模拟轮次',1,100,1],['population','合成人口',1,1000,1],['intervention','情景参数变化',0,1,.01]] as const).map(([key,label,min,max,step])=><label key={key}>{label}<input type="number" required min={min} max={max} step={step} value={form[key]} onChange={e=>setForm({...form,[key]:Number(e.target.value)})}/></label>)}</div><button disabled={!connected||busy}>提交合成实验</button></form></section><section className="card"><h2>任务与审批</h2>{taskTable}</section>{current&&<section className="card"><h3>所选实验 <code>{current.id.slice(0,12)}</code></h3>{status(current)}<p className="muted">代码身份</p><code className="hash">{current.code_sha256}</code>{current.error&&<p role="alert" className="error">{current.error}</p>}<pre>{current.logs.join('\n')}</pre></section>}{results}</>}
 {section==='情景历史'&&<><section className="card"><h2>选择已完成实验</h2><p className="muted">快照不可变；情景分支彼此隔离。选择实验查看两条时间线及版本记录。</p><select aria-label="历史实验" value={selected} onChange={e=>setSelected(e.target.value)}><option value="">选择实验</option>{[...runs,...(current?.status==='COMPLETED'&&!runs.some(r=>r.id===current.id)?[current]:[])].filter(r=>r.status==='COMPLETED').map(r=><option value={r.id} key={r.id}>{r.id.slice(0,12)} · seed {r.config.seed}</option>)}</select>{historyControls}</section>{results}</>}
 {section==='审批与证据'&&<><section className="card boundary"><h2>科学准入与冻结边界</h2><p>仅允许内置合成协议执行。发现来源只授予浏览权限；真人实验、冻结协议变更、科学升格、模型熔炼和部署均被阻止。</p><div className="version-row"><code>R 系列：保留原命名空间</code><code>MARKET：不映射证据等级</code><code>真实效度：UNKNOWN</code></div></section><section className="card"><h2>待审批与历史任务</h2>{taskTable}</section><section className="card"><h2>现有科研来源 · 只读登记</h2><form onSubmit={e=>{e.preventDefault();action(async()=>{await api('assets/discover',{path:source});await refresh();});}}><label>来源记录路径<input value={source} onChange={e=>setSource(e.target.value)} required/></label><button disabled={!connected||busy}>只读登记来源</button></form>{assets.map(a=><article className="asset" key={a.sha256}><h3>{a.path}</h3><p>{a.permission} · {a.scientific_status.namespace}</p><code className="hash">{a.sha256}</code><details><summary>查看保留原样的科研证据记录</summary><pre>{JSON.stringify(a.scientific_status.original_record,null,2)}</pre></details></article>)}</section></>}
 <footer>PSYCHOHISTORY PLATFORM <span>合成运行可复现 · 科研结论须独立验证</span></footer></div></main></div>;
}
