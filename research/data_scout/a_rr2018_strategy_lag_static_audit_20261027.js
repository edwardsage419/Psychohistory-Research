'use strict';
// Static, limited RR2018 notebook and strategy temporal-index audit.
// Inputs are locally obtained fixed author files. No real human rows are accessed.
function audit(strategyText,notebookText){
 const matches=[...strategyText.matchAll(/^def (s\d{2}_[a-zA-Z0-9_]+)\(actions, periods\):/gm)];
 const nb=JSON.parse(notebookText);
 let strategy=[];
 for(let i=0;i<matches.length;i++){
  const start=matches[i].index,end=i+1<matches.length?matches[i+1].index:strategyText.indexOf('\nif __name__',start);
  const body=strategyText.slice(start,end<0?undefined:end);
  const reads=[...body.matchAll(/actions\s*\[([^\]]+)\]/g)].map(x=>x[1].trim());
  const allowed=reads.filter(x=>/^t\s*-\s*[123]$/.test(x));
  const unsupported=reads.filter(x=>!/^t\s*-\s*[123]$/.test(x));
  strategy.push({name:matches[i][1],lagged_action_reads:allowed.length,unsupported_action_reads:unsupported,
    current_opponent_missingness_mask:body.includes('np.isnan(actions)')});
 }
 const code=nb.cells.map(c=>Array.isArray(c.source)?c.source.join(''):String(c.source||'')).join('\n');
 const flags={
  reads_action_data_csv:code.includes("pd.read_csv('input\\\\action_data_RR2018.csv')"),
  selected_supergames_31_to_50:code.includes('data.supergame>30')&&code.includes('data.supergame<51'),
  selected_periods_1_to_20:code.includes('data.period<21'),
  subject_matrix_grouping:code.includes("data.groupby('subject')"),
  opponent_action_array:code.includes('data.opponentAction'),
  strategy_fitted_using_all_selected_subjects:code.includes('C[k,n]')&&code.includes('E[k,n]'),
 };
 if(strategy.length!==20||strategy.some(x=>x.unsupported_action_reads.length)||Object.values(flags).some(x=>!x))throw Error('static audit failed');
 return {research_id:'A_RR2018_STRATEGY_TEMPORAL_STATIC_AUDIT',scope:'SOURCE_CODE_STATIC_ONLY',
   strategy_count:strategy.length,lagged_action_reads:strategy.reduce((a,x)=>a+x.lagged_action_reads,0),
   unsupported_action_reads:0,current_opponent_missingness_masks:strategy.filter(x=>x.current_opponent_missingness_mask).length,
   notebook_flags:flags,strategies:strategy,full_csv_rows_checked:0,independent_sessions_verified:0,
   R073_external_frozen_scoring_eligible:false,new_E2:0,new_E3:0};
}
if(typeof module!=='undefined'&&require.main===module){
 const fs=require('fs');
 process.stdout.write(JSON.stringify(audit(fs.readFileSync(process.argv[2],'utf8'),fs.readFileSync(process.argv[3],'utf8')),null,2)+'\n');
}
