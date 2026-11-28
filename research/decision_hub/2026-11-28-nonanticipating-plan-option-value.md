# 非预知条件规划与信息时点
2026-11-28。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / authority NONE。
基线 b9df44d2c26642f42c19a466af6443868f37a709。前轮核对近期提交、开放PR #63/#62/#61、既有 joint-goal-deadline-extension-frontier (6587769d44804abed17808e7986368178455fbdf)、exact-joint-resource-elimination (4fd11be9cce05eba5f5a7e402a3c712ad3)、V08_INDEPENDENT_HANDOFF (b0a70c4634693a916febc82ecddd39031b33bd33)。本轮重新核对HEAD，沿用前轮规程阅读；未重新确认唯一产品交接或全库查重。新增信息披露时点和非预知约束，不声称原创动态规划。
固定行动序列可行集合包含于非预知策略可行集合，后者包含于逐世界完全预知可行集合（以实例可行性计）。两世界在披露前必须共享行动前缀；披露后可分别执行。无概率或默认效用。所有情景须通过硬约束。真实信息覆盖、披露时点、行动资格和现金到账须确认。
实验一：四期，每期一个行动（等待、支付投入、前置投入完成后领取收益、支付目标）。三个非等待行动各一次；收入冲击在指定期发生，行动前观察；现金初始及每期行动后不低于储备。参数 cash 0/1/2/3，reserve 0/1，cost 1/2/3，reward 1/2/4，target 1/3/5，shock 0/1/3，reveal 1/2/3（零起始）。递归按共同信息状态选择动作，披露时分支；参照枚举每世界4^4序列并比较披露前前缀。1944配置全部一致，固定、条件、预知各405。非负收入增量和共同目标造成低收入世界方案对高收入世界仍可行。未检验到账前日内储备。
实验二：三期，每期等待或选择一次互斥资格路径A/B/通用。世界0要求A或通用，世界1要求B或通用。路径费用a/b/a+b，支付后现金须非负，随后释放reward；无后续支出，reward因此不影响可行性，重复参数非独立样本。必须在零起始deadline之前选择；reveal时观察世界。枚举每世界64序列，比较共同前缀；解析参照 cash>=a+b 或 reveal<deadline且cash>=max(a,b)。实际执行代码如下：
```js
let o={cases:0,static:0,adaptive:0,clairvoyant:0,adaptiveGain:0,foresightGap:0,checks:0};
for(let cash=0;cash<=5;cash++)for(let a=1;a<=4;a++)for(let b=1;b<=4;b++)for(let reward=0;reward<=4;reward++)for(let deadline=1;deadline<=3;deadline++)for(let reveal=0;reveal<=3;reveal++){
let valid=[[],[]];for(let w=0;w<2;w++)for(let n=0;n<64;n++){let q=n,c=cash,credential=0,seq=[],ok=true;for(let t=0;t<3;t++){let x=q%4;q>>=2;seq.push(x);if(x){if(credential||t>=deadline){ok=false;break}c-=x===1?a:x===2?b:a+b;credential=x;if(c<0){ok=false;break}c+=reward}}if(ok&&(credential===w+1||credential===3))valid[w].push(seq)}
let clair=valid.every(v=>v.length>0),stat=valid[0].some(x=>valid[1].some(y=>x.join()===y.join())),adapt=valid[0].some(x=>valid[1].some(y=>x.slice(0,reveal).join()===y.slice(0,reveal).join()));let ref=cash>=a+b||reveal<deadline&&cash>=Math.max(a,b);if(adapt!==ref||stat&&!adapt||adapt&&!clair)throw Error("mismatch");o.cases++;o.checks++;o.static+=+stat;o.adaptive+=+adapt;o.clairvoyant+=+clair;o.adaptiveGain+=+(adapt&&!stat);o.foresightGap+=+(clair&&!adapt)}
console.log(o);
```
实测 cases/checks 5760，static 1200，adaptive 1980，clairvoyant 2760，adaptiveGain 780，foresightGap 780。
接口建议：将披露历史、可观察信息、行动前缀、资源状态、截止日、来源及版本绑定到共同情景；仅在同信息历史共享行动。缺失披露时点或覆盖则UNKNOWN。禁止以逐世界最优拼接成现实策略；条件可行不等于授权执行。例 cash=2,a=b=2，deadline=2，reveal=1 可等待后选择，reveal=2 则不可保证完成，完全预知仍可行。通用方案成本4。下一步加入真实收益时序、互补任务、多阶段信息树和有界搜索，独立轨验证未见案例。研究者选定夹具、范围和基线；无真实用户数据、概率、实际性能、原生运行或独立验收。实验一仅保存算法描述与计数，未保存完整执行脚本，复算完整性不足。实验二保存完整脚本。未修改产品、冻结、交接、训练、合并PR、部署或新增费用。