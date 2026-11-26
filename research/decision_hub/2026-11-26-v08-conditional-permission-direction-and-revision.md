# v0.8 自主语义：条件逻辑方向、主体事实绑定、跨轮修订与政策冲突
2026-11-26。RESEARCH_CANDIDATE / FIXED_NATIVE_FUNCTION_SLICES_EXECUTED / SYNTHETIC_DEVELOPMENT / PYTHON_JS_LOGIC_PARITY / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。手动科研增量，非生产修复、真实白话能力验收、科学准入或版本发布。
## 基线与去重
起始main c50d6b79b661e2505b2b8e644426de3d47db3122；核对12近期提交、15开放PR、v3.2及同步规程前12行、唯一产品交接前12行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。固定Draft #63 head 734686980b19da9291bdd08b67d4e2519c011acf，open/draft/unmerged；base 82803894d9adf4a2a8bd7b8ff4ceaf4ba58da430。读取其PUBLIC_DEVELOPMENT.md blob 8557baeceba18a1630b769ac027889f14de16a45、独立交接 b0a70c4634693a916febc82ecddd39031b33bd33、语言源码 decision_language.py c01217b6d6f4c2465ffc0959f3c0219e9638e052 全文（分段审查条件、作用域、修订及归属）、decision_semantics.py 8c6ea6914b5b6e4f01d70331ed5c75c0dc32221b、decision_parser_registry.py ba28b0cd86a873d294f05d7cf3b3b8c80c5ad3b8。开发方公开集条件0/5、账本修订0/10、主体1/4、数值单位7/23仍未通过；4个逐字条件有候选守卫、4个他人主体有归属候选、7/10修订有操作锚。锚点命中不能当语义理解或可信计算。未重跑其公开ASGI集。
搜索grammar/chart parser/compositional/revision/discourse/guard/coreference。核对R61 e22acd18167c17df765996feea082ecc83703aaf、R64 378a75c40a2d3ecbf9ceaeeaf0de76b95dbc9a51、R65 683860d851312d75ae892af14fc2ec0999375b76、R114 7be37e102e3e636c148ff45e3aa05c6e0885be81、R131 condition-polarity-attachment-candidate-audit blob 81df7d2fc56f29084ecc623b98cdf0991d3260d4前25行、联合守卫68e05550a14779855649dc287364e99fc199430e报告前段。已有布尔表达式多树、条件适用性G=>B、共享解释、指代及字段修订、锚候选、歧义相关性不重复计为新成果。此轮新增必要/充分条件的方向和许可与禁止的关系代数，固定v0.8锚函数及C028片段实测、该语义类型的修订和多政策冲突连接。全库去重有限。
## 1 固定源码复用及原生边界
本地直接访问raw.githubusercontent.com DNS失败，改用GitHub连接器读取固定源。转录并实际运行source_anchor（331字符,FNV1a32 893bea0a）、_parts（1199,be66e774）、守卫常量块（321,47ce69e3）、_condition_relations（2594,30aaa2ff），四块字符数及FNV与连接器实际读取一致。FNV仅转录诊断，不是完整Git blob或密码学完整性证明；少量全局常量转录。复用前轮固定decision_feasibility_fixed.py并重算完整Git blob SHA1 6181d6c578c7ef251e9708d0ffcf65e95d35f88f，与本轮固定#63 decision_feasibility.py相同；实际通过AST调用check_constraint，输入为人工结构对象，不执行Pydantic状态、完整interpret、会话、Web/API/CLI。所有现有条件关系均authority NONE，不宣称现行产品已把条件方向错误用于计算。
## 2 条件方向及许可关系
有限语法明确区分守卫G（有主体、指标、单位、周期、比较符、阈值）及政策许可P（同一发言/政策所有者、同一候选行动）。P是该政策下允许选择的布尔变量，不是实际行动、概率、偏好分数、完整可行性或最终推荐。人工研究范围明确为约束许可语境，非所有日常语言“只要”“只有”“除非”必然同义。限定5类全句结构，不用不完整关键词匹配：只有G，我才允许选择A：P=>G；只要G，我就允许选择A：G=>P；如果G，我就不允许选择A：G=>非P；除非G，否则我不允许选择A：非G=>非P；如果G，我就允许选择A，否则我不允许选择A：P与G等价。除非的许可解释仅在显式否则否定本分支下成立，不一般化到歧义例外。初版除非模板语序不自然，已改为“否则我不允许”并全量重跑。只支持显式字面我/朋友、三个指标、四比较符、规范ASCII非负整数和匹配单位，混合守卫/自由中文/引用/外部规则/隐式语用或多重政策优先级留在外部。当前固定语法用一个有限整句匹配器作为诊断，不以扩大正则代替自主开放语义。
C028求合格区间内G可真或假集合。对每个G取与上述命题相容的全部P值，求并集；仅全真为PERMITTED_BY_POLICY，全假为FORBIDDEN_BY_POLICY，混合为UNRESOLVED_PERMISSION。许可未决不当成允许，许可通过也不能越过其他底线。缺主体、证据、适用性或权限资格为UNKNOWN_QUALIFICATION。只有/除非等需要正反方向及未确定分支，不允许补造双条件。人工限定公式仅用于显式政策。原生条件锚可复用为候选，但不能把when_true标志自动升级为充分蕴涵。
5结构×2事实主体×2政策发言者×3指标×4比较符×3阈值×2行动=1440条合成语句；每句10闭整数区间×2资格状态=28800判断，其中7200为已合格本人政策，21600未资格（包含他人政策，即使存在该人事实也不自动作为本人约束）。全部1440句在自定义语法下解析且原生片段目标锚存在，288条必要条件原生关系带when_true，但本身不声称蕴涵方向。原生C028及独立逐整数/许可赋值参照7200/7200相符。故意错误方向基线将必要误成充分、明确除非误成双向，1032错误确定许可，516漏掉应禁止（变未决）；无错误确定禁止或丢失确定许可。不是实际平台错误率。例“只有我的每周工时不超过0小时，我才允许选择方案A”，G真仅说明必要条件满足，许可仍未决；G假则该政策禁止。12不支持/矛盾句式拒绝。全部合成样例为ChatGPT辅助原创开发夹具，同一研究者定义语法及参照，不是真人、独立留出、训练或语言准确率。整数区间的单调谓词端点精确，非连续复杂决策测试。
## 3 主体与参数资格绑定
另设人工Fact合同，主体、指标、单位、周期必须精确匹配，仅一个记录、证据非空、当前代次、verified及宿主适用性为真才允许调用C028；同时提供错主体的同量诱饵。2主体×3指标×3阈值×6区间×128字段变异=13824组。108合格与逐点参照一致，13716错误资格拒绝；4额外重复、矛盾、无证据及未适用控制通过。此为人工给定来源/资格，不能由语言锚自行确认真事实或外部授权；实际个人事实版本、权属、用途及时效服务尚未接入。
## 4 跨轮阈值修订
复用既有稳定对象、字段继承思想，限定明确“把方案A的条件阈值改为N单位”的编辑，唯一目标、当前根和版本、明确匹配的人工确认票据、单位一致才生成新版本；多个同方案条件保守待澄清，禁止取最近记录。原文保留、条件方向/发言者/主体/指标/周期/另一个对象不变，阈值的新来源和跨度独立绑定，原对象在历史不可变。修订后的Policy派生threshold不表示该值仍在旧原文跨度；生产必须沿字段来源显示。人工票据仅元组匹配，不是签发、授权或真实防篡改；实验root由可信夹具给定，不从原文摘要认定同一长期身份。只支持阈值修改，暂不解决任意指代、作用域变更、删除及多次复合修订。4320组双政策修订配置，540提交、3780拒绝；5400修订后C028及逻辑复算一致；540旧票据重复提交拒绝。没有写入真实个人账本或生产会话。
## 5 联合政策冲突
两条已明确同时适用、同一行动、无优先级或例外覆盖的政策具有同一许可变量P；在每个共同世界w内分别求A(w),B(w)许可集合，必须求A(w)交B(w)。空集是政策冲突见证，不能从世界域删除；任一世界冲突则报告CONFLICT_POSSIBLE或CONFLICT_ALL，不以其他世界允许抵消。仅所有世界无冲突时再汇总P集合。这与已有G=>B联合事实判定不同，新增许可赋值相容性及方向冲突；不把语言矛盾视为物理状态不可能或真实风险概率。两条权限规则是否同时适用、是否有显式优先级等仍须用户确认。
5×5政策类型×4×4比较符×3×3阈值×15个非空联合域=54000组，底层4世界为两个指标值0/1的共同支持子集，真实调用C028点值及两政策许可集合，独立直接真值公式核对每个世界及域。全部一致，部分冲突6320、全部冲突5648、无冲突且该政策组合禁止21024、许可7712、未决13296。先按边际汇总许可再求交的错误基线产生6656结果差异，其中6336掩盖冲突。反例：只有工时<=0才允许，且只要房租<=0就允许，联合域包含(0,0),(1,0)；第二世界同时要求许可为真和假，不能被第一世界的许可消除。严格保留两种来源和冲突见证，触发有限必要澄清。以上为有限合成域计数，非真实决策错误率。
## 6 可复算资产
Python 3.13.5标准库，两份实验结果连续两次逐字节相同。完整会话ZIP psychohistory_conditional_research_2026-11-26.zip，8文件，7个校验文件全部通过，ZIP SHA256 7214583341e14d0c349c6214895b972f2431e910e75fd991818559138e69522b。native_slice.py 045432548cb20c7ff7c43e941c3eab99b9cd3f706d3954b4ad2e51d9e33f6f92；probe.py fb2b097727932bb3ea15e2dc7271f88883e71af3bc92cabbc3ad79d395e3be30；joint_probe.py f36ec501050669a18e7867e6aa3a62b816b4c0b0e82eb0cb1f4c76fe0864d3ce。运行python probe.py及python joint_probe.py。ZIP及完整本地源码未上传仓库，报告内附在连接器环境实际执行的独立逻辑枚举核心，复算标量及联合域计数；不执行Python原生片段、解析或资格、修订接口，不能替代完整包。
```js
function replay(){
 const kinds=["necessary","sufficient","forbid_if","unless","dual"],ops=["<=","<",">=",">"],cmp=(x,t,o)=>o==="<="?x<=t:o==="<"?x<t:o===">="?x>=t:x>t;
 const accept=(k,g,a)=>k==="necessary"||k==="unless"?(!a||g):k==="sufficient"?(!g||a):k==="forbid_if"?(!g||!a):a===g;
 const set=(k,g)=>[false,true].filter(a=>accept(k,g,a)),classify=a=>a.length===0?"CONFLICT_ALL":a.length===2?"UNRESOLVED_PERMISSION":a[0]?"PERMITTED_BY_POLICY":"FORBIDDEN_BY_POLICY";
 const union=rows=>[false,true].filter(a=>rows.some(row=>row.includes(a))),inter=(a,b)=>a.filter(x=>b.includes(x));
 const scalar=(k,o,t,l,h)=>classify(union(Array.from({length:h-l+1},(_,i)=>set(k,cmp(l+i,t,o)))));
 let s={qualified_cases:0,baseline_wrong_permit:0,baseline_wrong_forbid:0,baseline_lost_forbid:0,baseline_lost_permit:0};
 for(let k of kinds)for(let o of ops)for(let t=0;t<3;t++)for(let l=0;l<4;l++)for(let h=l;h<4;h++){
  let a=scalar(k,o,t,l,h),b=scalar(k==="necessary"?"sufficient":k==="unless"?"dual":k,o,t,l,h);
  // 2 guard actors × 3 metrics × 2 actions, self policy speaker and qualified only.
  s.qualified_cases+=12;if(a!==b){if(b==="PERMITTED_BY_POLICY")s.baseline_wrong_permit+=12;if(b==="FORBIDDEN_BY_POLICY")s.baseline_wrong_forbid+=12;if(a==="FORBIDDEN_BY_POLICY")s.baseline_lost_forbid+=12;if(a==="PERMITTED_BY_POLICY")s.baseline_lost_permit+=12}
 }
 let j={domains:0,CONFLICT_ALL:0,CONFLICT_POSSIBLE:0,FORBIDDEN_BY_POLICY:0,PERMITTED_BY_POLICY:0,UNRESOLVED_PERMISSION:0,marginal_mismatch:0,marginal_missed_conflict:0};
 let worlds=[[0,0],[0,1],[1,0],[1,1]];
 for(let k of kinds)for(let m of kinds)for(let o of ops)for(let p of ops)for(let t=0;t<3;t++)for(let u=0;u<3;u++){
  let x=worlds.map(([a,b])=>set(k,cmp(a,t,o))),y=worlds.map(([a,b])=>set(m,cmp(b,u,p)));
  for(let mask=1;mask<16;mask++){
   let ids=[0,1,2,3].filter(i=>mask>>i&1),rows=ids.map(i=>inter(x[i],y[i])),empty=rows.filter(a=>a.length===0).length;
   let got=empty?(empty===rows.length?"CONFLICT_ALL":"CONFLICT_POSSIBLE"):classify(union(rows)),old=classify(inter(union(ids.map(i=>x[i])),union(ids.map(i=>y[i]))));
   j.domains++;j[got]++;if(got!==old){j.marginal_mismatch++;if(got.startsWith("CONFLICT")&&!old.startsWith("CONFLICT"))j.marginal_missed_conflict++}
  }
 }
 return {scalar:s,joint:j}
}
console.log(JSON.stringify(replay(),null,2));
```
实测：
```json
{
  "scalar": {
    "qualified_cases": 7200,
    "baseline_wrong_permit": 1032,
    "baseline_wrong_forbid": 0,
    "baseline_lost_forbid": 516,
    "baseline_lost_permit": 0
  },
  "joint": {
    "domains": 54000,
    "CONFLICT_ALL": 5648,
    "CONFLICT_POSSIBLE": 6320,
    "FORBIDDEN_BY_POLICY": 21024,
    "PERMITTED_BY_POLICY": 7712,
    "UNRESOLVED_PERMISSION": 13296,
    "marginal_mismatch": 6656,
    "marginal_missed_conflict": 6336
  }
}
```
## 7 接入建议及下一责任方
沿用v0.8 RawTurn、原文锚及候选关系，建议增加版本化逻辑方向/谓词模态/许可变量身份、显式未知分支和资格合同；当前ParserRegistry的最小kind/source/span仅用于候选展示，不能直接携带受信义务或写入，扩展先走独立研究接口。以原文共享守卫、主体、动作、时间、单位、修订根和字段依赖生成条件化数学端口，C028只核验已资格数值谓词，联合政策保持世界及冲突身份，结果authority NONE。后续优先研究自主中文分词和组合关系对真实公开开发情节的候选覆盖、与v0.8原生解释/确认/投影的实际连接；本轮尚未改善公开开发集指标。模型轨科学合同、产品轨唯一交接、独立轨未见案例和原生真机；不开新零碎Codex任务。R073、PESEN及冻结不变。无训练、第三方AI运行时、真实个人数据、生产代码修改、合并、部署、主动CI或额外费用。
