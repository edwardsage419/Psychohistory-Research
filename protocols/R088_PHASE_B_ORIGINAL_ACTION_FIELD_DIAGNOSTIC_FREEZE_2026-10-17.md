# R088 Phase B：原作者完整六人群体行动标签异常的受限来源编码审计

2026-10-17。**Phase A首先冻结、再独立执行**：研究主协议 `protocols/R088_SIX_PERSON_MULTILEVEL_PUBLIC_GOODS_171_GROUP_ORIGINAL_SOURCE_E2_FREEZE_2026-10-17.md` commit `1f84bf430e4bb3c4aff8bf25eb90ba54e008df24`；首次纯合成35项成功，但原作者完整CSV真实代码run `39011042473` 报 `R088_HUMAN_ORIGINAL_ACTION_NULL_OR_UNEXPECTED`，真实组结果 **0**，整体作业scientific FAIL_CLOSED。这一负结果永久保留，不改首次代码的科学评分阈值、群体分母、阈值。

此Phase B在接下来第二次读原始2025/2026完整人类CSV字节**之前单独冻结**，仅审计为什么作者文本值没有落在主协议的原始 `global, local, other, self` 四类：每个原始字段值归入这几个来源类型：
* `EXACT` 四个冻结原分类（含原作者可记录的空格/大小写? 不含，必须严格相等），
* `CASE_OR_SPACE_ONLY`：非Exact，但剥两端空格转小写后严格属于四类；
* `DECLARED_COMMON_NON_EQUIVALENT`：诸如 kept, defect, keep, 0, 1, 2, 3，**不得擅自映射为四类**；仅分类为不能自动修复；
* `EMPTY_MISSING`：空字符串、None或源NA；
* `UNRECOGNIZED_OTHER`：任何别的文本，不在日志输出其原文或哈希（可能泄露受试者语句）。
审计器只发布以上安全模式的匿名计数、是否存在任一违约、每条件分布和原来源CSV Git SHA校验，无任何人/组/session字段值或原始决策明细。最多1026×20个来源字段验证，两个必要R作者源码Git blob同时验证。若 `CASE_OR_SPACE_ONLY` 是唯一非Exact模式，可随后再**另冻结**有限正规化映射后严格重算；若出现EMPTY或非等价其它标签，E2真实完整组资格暂时OPEN；不可擅自丢人、插补或修改原先群体构成。严禁对实际global率/阈值达标率或初末变化进行额外实算直到新码本确定。

Phase B仅做原始字段schema review，纯合成>=10项验收，再真实作者SHA核验及匿名计数，至少一次独立重放与第一次严格安全收据SHA相同才归档。原始作者有效完整组171、三处理各57、每组6人、20轮主约束不修改；本实验已经发表不是新E3。把source blockage与真正E2科学实证严格分开，PESEN v0.1 FROZEN。
