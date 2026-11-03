# TH219 Arrow 1950 与 Sen 1970：集体选择、无关选项与个人自由的两种不可能性

track: theory
subflow: primary
run_date: 2026-11-03 (Asia/Singapore)
observed_head_before_write: e19f633d5b6669e1e197ff60f62c49ca441e9e2b
target_key: (theory,Arrow1950+Sen1970,published-originals,ordinal-social-choice-IIA-vs-minimal-liberty-Pareto-conflict)
status: THEORY_NOTE_BOUNDED; TWO_PRIMARY_ORIGINALS; EXACT_EXAMPLE_AUDIT; NO_R_UPGRADE

## 一手来源及实际阅读范围

[A] Kenneth J. Arrow (1950), “A Difficulty in the Concept of Social Welfare”, *Journal of Political Economy* 58(4):328–346, DOI 10.1086/256963. 芝加哥大学统计系托管的原刊影印 https://www.stat.uchicago.edu/~lekheng/meetings/mathofranking/ref/arrow.pdf 。直接审读pp328–342关于偏好、社会福利函数、Condition 1至5、定理与证明，pp343–344关于解释与限定；对pp337、338、342扫描页面目视核对。pp345–346全文尚未逐段核对，不将其算入完整阅读。

[B] Amartya K. Sen (1970), “The Impossibility of a Paretian Liberal”, *Journal of Political Economy* 78(1):152–157, DOI 10.1086/259614. 北卡州立大学托管原刊影印 https://www.csc2.ncsu.edu/faculty/mpsingh/local/Social/f24/wrap/readings/Amartya-Sen-Paretian-liberal-1970.pdf ，直接审读pp152–157全文，目视核验pp154–155原刊证明与例子。哈佛大学作者论文存档书目及可开放副本 https://dash.harvard.edu/entities/publication/73120378-8203-6bd4-e053-0100007fdf3b ，仅作为合法可获取来源交叉核对。两份原刊受原出版版权保护，仓库仅保留原创笔记及代码，不复制全文或扫描。

[C] Duncan Black (1948), “On the Rationale of Group Decision-making”, *Journal of Political Economy* 56(1):23–34, DOI 10.1086/256633。只核对正式出版者书目 https://www.journals.uchicago.edu/doi/10.1086/256633 ，原文未读。单峰偏好与中位选民结论仅作为待查竞争线索，不能称已完成Black原著核验。

## 核心命题与原文重要区别

1. Arrow 1950 pp331–332的Axiom I为任意两项可比，Axiom II为弱偏好关系传递；社会排序必须同时满足。pp335–339的原始五条件依次为适当定义域、正向关联（Condition 2）、无关选项独立性（Condition 3）、非强加（Condition 4）、非独裁（Condition 5）。**1950年原始表述把非强加与正向关联作为推导严格一致偏好（Consequence 1）的前提**，不能将原文条件编号机械替换成后世简化教材的独立“帕累托公理”。pp340–342原作者先在两人三选项下证明矛盾，再陈述可推广至更大社会的可能性定理。该定理依赖广泛允许的偏好定义域及全社会完整传递排序，不能解释为一切集体制度皆不可能。

2. Arrow 1950 pp337–338原刊亲自给出位置计分法违反Condition 3的例子。两名投票者排列x>y>z>w，第三名z>w>x>y；四候选位置权重4,3,2,1得到(x,y,z,w)=(10,7,8,5)，唯一胜者x。删除全体都排在x之后的y，剩三候选权重3,2,1得到(x,z,w)=(7,7,4)，x与z并列。该示例展示相同存活选项的两两相对偏好下，排序计分会随删除选项改变选择集合。它是原作者数学构造，未涉及真实选举。

3. Arrow 1950 p339的Condition 4明确为“不强加”而非直接逐字的Pareto条件；p340 Consequence 1从Condition 2、3、4导出双方一致严格偏好时社会也严格偏好。pp343–344原作者说明：若事先限制允许的偏好结构，可能避开广泛定义域下的定理；不能从此直接推出某种具体历史社会必然存在或不存在一致偏好。

4. Sen 1970 pp153–154的Condition U为所有逻辑可能的个人偏好组均允许，Condition P为全体严格偏好时社会严格偏好，Condition L*仅要求**至少两人各对至少一对社会状态有决定权**。Theorem II指出，要求每个可行集合至少存在一个最佳选项的社会决策函数仍不能同时满足U、P、L*。原文pp156–157明确：该结论**无需社会偏好传递性，也无需Arrow的无关选项独立性**。它检验个人选择权与一致偏好之间的冲突，不能等同于Arrow原定理的简单改写。

5. Sen 1970 p155原刊书籍例子：x=个人1读书，y=个人2读书，z=无人读书；个人1偏好z>x>y，个人2偏好x>y>z。个人1对(x,z)的自由要求社会z>x；个人2对(y,z)的自由要求社会y>z；两人均x>y则Condition P要求社会x>y。得到x>y>z>x，三选项均有更优于它的选项，无法产生最佳选项。这是构造性规范冲突；“个人自由”在此为特定两两决定权的公理，其他权利理论可能不接受这一表述。

## 竞争解释、适用层级、证据界限

Arrow的冲突来自序数偏好汇总规则、独立性与社会排序要求；Sen的冲突来自个人权利决定权、严格Pareto与不受限制的偏好集合。二者适用条件不同，不做统一“社会选择不可能”断言。放松独立性可改变Arrow问题，但不能自动解决Sen问题；限制偏好定义域、明确权利边界、允许不同类型的选择规则是候选研究路径，必须逐一核对各自公理与适用条件。Black1948单峰限制的原文尚未审读，不能以其作为已核实的解决方案。

个体层：偏好排序、社会状态与行动机会。群体层：选票与规则映射。制度层：决策权、权利冲突、允许的偏好域。历史层：选举制度与权利演变须另用具体时间、群体、议题和档案验证。原著定理属于形式逻辑和规范分析，未测量任何真实群体的偏好、政治行为或历史轨迹。个人价值权重由未来使用者自主决定，本轨不设定人生目标。

## 本轮有限复核、完成与开放事项

可运行标准库脚本：`theory/th219_social_choice_primary_audit.py`。普通Python与`python -O`各执行10项实质检查PASS，脚本使用显式check以避免优化模式删除assert；一次将Arrow得分10篡改为11的负对照被正确拒绝。它只复算Arrow1950 pp337–338和Sen1970 p155的有限人工示例；Arrow完整不可能性证明、Sen全部证明分支的机器形式化、真人实验、历史因果和独立预测均NOT_RUN。Arrow pp345–346、Black1948原著全文仍未读。

覆盖改善：政治哲学、福利经济学、社会选择与制度权利冲突；原始两篇独立不可能性定理的适用范围分离。与既有TH205有限理性、TH218空间隔离及C011回顾测量仅作局部关联，不做项目级分类或模型熔炼。

C011: COMPLETE, 2026-11-03，只读核验，未重复创建。D003: COMPLETE, 2026-W45, 2026-11-02，只读核验，未重复创建。R073/PESEN v0.1冻结，R E1/E2/E3及MARKET证据等级不变。12个开放Codex PR均未计入main成果。GitHub Actions NOT_RUN，新增收费操作0，账户实际计费与免费额度NOT_VERIFIED。

next: 若后续可合法取得Black1948原刊全文，直接核对单峰限制下的多数规则；也可转向尚未覆盖的政治思想史或制度比较，不在社会选择专题反复制造TH编号。
