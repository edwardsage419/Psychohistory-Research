# R077 精确 Brier 评分候选：从补充核到可调用修复

track: Codex B; subflow: B1 exact paired Brier candidate
run_date: 2026-11-10 UTC
observed_head: 3221a84fba91731071b8931447837e07578210be
status: COMPLETE_SYNTHETIC_CANDIDATE / PARTIAL_OVERALL_B1
output_paths: 本目录；commit_sha/PR见HANDOFF与最终交付。
ci_status: NOT_RUN; billing_checked: 无付费API/安装/购买/dispatch；免费额度NOT_VERIFIED。
source_links: 项目workflow v2与sync规程；R077 Rev001/Rev002；原R073/R077；
既有PR16/18；14份固定版本见pins.json。仅本目录新增，不修改A/R轨。

## 问题、已有信息与本轮增量

最新main的原R077 blob仍70889bd15c6fd943bdb07ab3ae1f60c943ebc538，未采用
PR18补充核。已合并的PR18准确证明相同7事件/35种排列有11个错误改善；其
报告明确生产未修复。PR21–27均未覆盖R077的可调用修复：A24审查旧B21–23，
A26处理R127；B25/27为其它数学问题。开放范围快照见evidence/open-pr-scope.json。

此前exact_pair只接收外部提供的两个Fraction概率，既不生成七模型概率，也不替换
原评分输出。本轮提供特定的 `score_exact_brier(fit,sessions)`，输出 `{scores,
exact_Brier}`：scores保持原公共结构，Brier数值/方向改用精确值；exact_Brier
保留无个人标识的分数证书。没有另造第二个通用框架或七模型验证oracle。
这是可调用数值修复候选的完成，**原生产函数仍有已知FAIL，未声称已在正式调用修复**。

## 数学选择与冻结边界

原概率 `(c+20*p0)/(n+20)`、固定TFT/WSLS理论noise=1/20、原Brier定义、
七模型、六对照、先场次平均再等权全部保留。**精确实现数学计数公式不等于
逐位复现冻结代码的每一步float舍入**；Rev002还冻结原R073具体blob。因此本
候选不自行获得真人采用授权，不回写源程序/协议，也不发布修订真人结论。

来源p0从完整M4整数计数的C/N恢复；M1/M2/M3必须是M4相应投影的精确边际，
四表不一致、遗漏表、空表、错误计数类型/范围、训练总数和p0不匹配均拒绝。
原float p0须等于C/N的float表示；它仅用于一致性核对，不用其十进制字符串
冒充精确来源比例。未观测状态仍用同一冻结p0平滑。此契约要求完整相容的
来源计数，旧测试的空表假fit不是合格输入。**计数相容不证明真实来源身份或
完整性**，上游原资格/时间/场次门和源码认证仍须由A接入保留。

逐事件概率来自来源计数与给定四个历史bit，当前y只进入损失。复用PR18的
session_risks/summarize/as_float_pair；先Fraction平方损失/场次平均，再等权，
六组配对方向由精确差符号决定，无epsilon。最后的float只是公共JSON显示，
分数字符串证书保留真实非零量。没有新参数拟合、选择模型或切换评价指标。

原R077评分器在相同输入上执行一次，保留所有log loss和公共元数据；再覆盖
7模型总体/两个处理Brier及6配对字段。未修复或宣称log loss的float累加次序
不变性；它不参与本缺陷的配对票数。上游原代码仍可信且未被篡改是调用前提。
本目录pins和replay提供选定版本的重放证据，非通用安全沙箱或生产认证入口。

## 独立证明与可证伪反例

沿用PR18的相容32条完全合成来源，p0=16/32，M1=1/2，M3=5/14。7个目标
含3正4负。独立整数路线：M1平方分子和3*7²+4*7²=343，M3为3*9²+4*5²=343；
共同分母7*14²=1372，均为1/4。全部35排列复核，新证书一致；原结果24平局、
11错误改善。最初原样转发候选的1方法/35子例实跑11断言失败；修复后1方法通过。
原FAIL单独保存在每个模式日志，不用新PASS冲销。

近零非零保护：合成来源N=2^65，每格n=N/4，p0=1/2；在两个同own1的联合格
中把正例计数分别+1/−1，保持全部边际相容。目标history=(1,1,0,0),y=0，M1=1/2，
M3=1/2+1/(N/4+20)，精确风险差为1/(N/4+20)+1/(N/4+20)^2>0。
两概率float均为1/2，原程序报2平局；候选正确报2恶化。N仅是合成充分统计量，
没有生成或声称拥有2^65条真人记录。

来源比例保护：C=1,N=3且目标未观测历史，M0..M4风险精确1/9。错误修复
`Fraction(str(float_p0))`不能给出1/3；错误修复把条件概率先转float也丢失上述
真实方向。两种一次性候选源代码变异各被指定手算回归以assertion failure检出，
不把导入错误/SyntaxError当拒绝。完整补丁与SHA在summary，临时副本不改原文件。

其余检查包括既有PR16的独立历史直方图Fraction/Decimal oracle（本轮p0=1/2
对照，未冒称它能复原所有非终止来源比例）、16历史×2标签、log loss原样保留、
不等大小场次、目标标签翻转不改fit、严格二元与来源类型、元数据和匿名JSON。
新源概率方法为Codex B对冻结数学公式的实现，不冒称原作者算法或外部团队复现。

## 实际命令与结果

仓库根执行；输出路径必须不存在。当前Linux，无新增依赖：

```bash
python3 -B research/codex_b/2026-11-10-r077-exact-score-candidate/replay.py --output research/codex_b/2026-11-10-r077-exact-score-candidate/evidence/py312
python3 -O -B research/codex_b/2026-11-10-r077-exact-score-candidate/replay.py --output research/codex_b/2026-11-10-r077-exact-score-candidate/evidence/py312-O
/usr/bin/python3.13 -B research/codex_b/2026-11-10-r077-exact-score-candidate/replay.py --output research/codex_b/2026-11-10-r077-exact-score-candidate/evidence/py313
/usr/bin/python3.13 -O -B research/codex_b/2026-11-10-r077-exact-score-candidate/replay.py --output research/codex_b/2026-11-10-r077-exact-score-candidate/evidence/py313-O
```

Python3.12.14/3.13.5普通/-O四组exit0；每组原R073 23+原R077 24+既有PR18核12+
新增候选12=71方法，通过共284次，其中新增候选48次。35排列不是额外35测试方法。
原回归每组1方法/35子例有11失败（合计44子例失败），状态FAIL_RETAINED；两个
坏修复每组各1方法预期断言失败。四组18份选定代码/协议/结果指纹前后相同。

实际 `python3 -B -m unittest discover -v` 为0测试/exit5/NO TESTS RAN，replay也
逐模式记录这一现象，**不计通过，不声称全仓库测试成功**；未找到全仓统一test
配置。跨运行时仅同一Linux现有两个CPython，不是其它OS/硬件环境或外部团队。
commands.json记录真实argv/cwd/退出码及每条stdout/stderr字节/SHA256，非空流
原样保存；summary含版本、变异、风险证书与边界。重复运行请换全新临时输出目录。

## 原始版本、历史影响与下一步

R073原blob c8a0b47fd27bf05e7be5b87419a0824355fc911a；R077原blob
70889bd15c6fd943bdb07ab3ae1f60c943ebc538；历史真人JSON blob
13946754afc06e529f2d3a2072a7bae297453fa9。各SHA256/长度在summary来源表，
Rev001/Rev002、验收状态与既有补充核版本在pins。历史验收仍CLOSED_BOUNDED，
本轮不代替ChatGPT修订证据等级；154队列P0=27/P1=82/P2=45正式净关闭0。

历史真人票数影响 **UNKNOWN**。匿名公开汇总没有每场精确统计，既不能推出
14/0/1受影响，也不能从宏差远大于机器误差证明每场方向安全。没有取回或评分
真人原始文件；不能把合成反例当作原始研究发生了11次错误。

原冻结协议授权历史规定来源/原代码的既定评价，不明确授权以新精确实现发布修订
结果。需owner/ChatGPT审查：数学解释与float中间值区别、允许的只读来源范围、
原15场/1040共同风险集不变、源12场/18424计数、原资格与SHA检查全部保留；
在私有临时空间双跑旧/候选，按匿名六对照记录票数变化与精确余量而不发布逐人/
逐场标识，不调参。仅在批准后由A作独立可回退入口接入，原档案永久保留。
这是一份具体采用/重算方案，**本轮未执行、未批准或发布修订真人结果**。

本轮关闭“只有给定概率配对核、没有生成来源概率并修正完整输出的可调用候选”
缺口。生产采用/源码替换/真人历史影响/原研究重新验收、其它平台和全仓测试
NOT_RUN；无新真人/E2/E3/独立数据预测/外部团队复现。R073/PESEN冻结。
下一优先：A与ChatGPT审查B1采用方案；B刷新最新队列，选择尚无成熟实现的
实证或样本外评价计算障碍，不重复PR21–27已有补充工具或A的R127工作。
