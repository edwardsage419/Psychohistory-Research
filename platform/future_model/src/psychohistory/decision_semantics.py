"""Bounded rule contracts for source obligations and typed measurements."""

import re
from hashlib import sha256
from unicodedata import normalize


SEMANTIC_VERSION = "0.8.0"
CONFIRMED = {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"}
BOUND_FIELDS = {
    "cost_max", "cost_min", "income_max", "income_min", "hours_max", "hours_min",
    "onsite_max", "onsite_min", "move_allowed", "move_if_onsite_max",
    "rent_parking_max", "night_shift_max",
}
CLAIM_KEYS = ("kind", "field", "subject", "value", "unit", "source")
CNY = r"人民币|(?<![A-Za-z])(?:CNY|RMB)(?![A-Za-z])|[¥￥]|(?<![美韩港澳日欧台泰加新])元|块钱?"
NON_CNY = (
    r"美金|美元|港[元币幣]|台[币幣]|新[台臺][币幣]|日[元圆圓币幣]|欧元|歐元|英[镑鎊]|"
    r"澳[元币幣]|[新加泰韩韓][元币幣]|卢布|泰铢|泰銖|越南盾|比索|卢比|林吉特|马币|瑞士法郎|"
    r"(?<![A-Za-z])(?:USD|AUD|HKD|SGD|CAD|EUR|GBP|JPY|TWD|KRW|CHF|THB|INR|RUB|"
    r"VND|MYR|NZD|PHP|SAR|AED|BRL|MXN|ZAR|IDR|NOK|DKK|SEK|BTC)(?![A-Za-z])|[$＄€£₩₽₹฿]"
)
NON_MONTHLY = (
    r"每\s*(?:个\s*)?(?:天|日|小时|钟头|周|星期|礼拜|年|季度?|次|晚|夜)|"
    r"按\s*(?:天|日|小时|钟头|周|星期|礼拜|年|季度?|次|晚|夜)|"
    r"[\/／]\s*(?:天|日|小时|钟头|周|星期|礼拜|年|季度?|次|晚|夜)|"
    r"\d\s*(?:天|小时|周|年|季)(?:结算|一付|收费)|周租|日租|年租|季租|年薪"
)
MONTH = r"每个自然月|每个月|每月|按月|[\/／]\s*月|月租"
RENT = r"月房租|月租金|月租|房租|租金"
PARKING = r"停车(?:费用|费|位租金|位)?|车位(?:费|租金)?"
JOINT = r"合计|共计|总共|一共|一起|加起来|加在一起|合在一起|合并|相加|共享|共用|联合|共同|两项"
NIGHT = r"夜班|夜间班次|夜间值班"
EXTERNAL_PARTY = (
    r"(?P<actor>同事|朋友|室友|伴侣|配偶|家人|亲戚|爸妈|父母|我妈|我爸|老板|主管|雇主|客户|同学|房东|"
    r"他们|她们|他|她|对方|公司|招聘方|经纪人|中介|负责人|人事|部门|HR)"
    r"(?P<cue>的|说|听说|称|表示|承诺|转述|希望|要求|规定|告诉我|转告|认为|打算|在考虑|正在考虑|自己|"
    r"[:：]|也|不|要|能|预算|上限|底线|最晚|是否|$)"
)
_EXTERNAL_PARTY = re.compile(EXTERNAL_PARTY, re.IGNORECASE)
REPORTING_CUES = frozenset({"说", "听说", "称", "表示", "承诺", "转述", "告诉我", "转告"})
REPORTED = r"听说|转述|据称|据说|口头(?:说|表示|承诺)|承诺|保证|宣称|计划|预计|如果|假如|假设|除非|尚未|未确认|不确定|不知道|能否|是否"
QUOTE_OR_REPORT = r"[“”‘’「」『』\"`]|据|传闻|有人说|别人说|对方称"
NEGATION = r"不能|不得|不可以|不允许|不可|没有|未|不"
COMPARATORS = re.compile(
    rf"(?P<ge>(?:{NEGATION})\s*(?:低于|小于|少于)|至少|最少|最低|起码|下限|>=|≥|＞＝)"
    rf"|(?P<le>(?:{NEGATION})\s*(?:高于|大于|多于|超过)|最多|至多|顶多|只能|上限|封顶|控制在|<=|≤|＜＝)"
    r"|(?P<gt>高于|大于|多于|超过|(?<![=>＞])>(?![=>])|＞)"
    r"|(?P<lt>低于|小于|少于|不到|不足|(?<![=<＜])<(?![=<])|＜)"
)
_OPERATOR = {"ge": ">=", "le": "<=", "gt": ">", "lt": "<"}
CLARIFICATIONS = {
    "VERIFY_JOINT": "这几项需要合并计算吗？请说明共同上限以及它涵盖的项目。",
    "VERIFY_CURRENCY": "这笔金额使用哪一种币种？请把金额、币种和对应项目写在一起。",
    "VERIFY_PERIOD": "这笔金额适用于哪个周期？请把金额和对应的周期写在一起。",
    "VERIFY_SUBJECT": "这是谁的条件，它是否适用于你的当前决定？",
    "VERIFY_CONDITION": "这个底线什么时候生效？请说明目前已满足的条件。",
    "VERIFY_EXPRESSION": "这里同时提到了多个比较条件，请分别说明适用范围和阈值。",
    "VERIFY_SCHEDULE": "这个岗位已经核对过的当前实际排班中是否有夜班？",
    "VERIFY_BOUND": "请用一句话说明这个底线的主体、数值、单位和适用范围。",
    "VERIFY_PARKING": "停车费是多少，采用什么币种和周期？",
    "MISSING_EVIDENCE": "这项信息还缺少什么依据，或者有哪些已经核对过的信息？",
    "VERIFY_REVISION": "你要撤回哪条底线？请指出原条件和它现在是否仍适用。",
    "AWAITING_CONFIRMATION": "请确认这个底线的含义和适用范围。",
    "VERIFY_NUMBER": "请把数额写完整，以确认口语省略的位数。",
    "LIMIT_EXCEEDED": "本轮条件较多，请先单独列出最重要的底线。",
}


def comparison(text: str) -> str | None:
    """Return one explicit comparison, or UNKNOWN for compound or negated syntax."""
    matches = list(COMPARATORS.finditer(text))
    if not matches:
        return None
    # Explicit connective bounds can repeat the same symbol and still refer to
    # different thresholds. Only one comparator has a qualified projection.
    if len(matches) != 1 or re.search(
        rf"(?:不是|并非|不一定|没|{NEGATION})\s*$", text[:matches[0].start()]
    ):
        return "UNKNOWN"
    return _OPERATOR[matches[0].lastgroup]


def monetary_scope(clause: str, *, monthly=False) -> str | None:
    if re.search(NON_CNY, clause, re.IGNORECASE) or not re.search(CNY, clause, re.IGNORECASE):
        return "VERIFY_CURRENCY"
    if re.search(NON_MONTHLY, clause) or (monthly and not re.search(MONTH, clause)):
        return "VERIFY_PERIOD"
    return None


def is_joint(clause: str) -> bool:
    return bool(
        re.search(JOINT, clause) and re.search(r"预算|上限|总额|总价|费用|花费|容量|少于|不超过|最多|至多", clause)
        or re.search(r"联合约束|共同上限", clause)
        or re.search(RENT, clause) and re.search(PARKING, clause)
    )


def scope_reference(text: str) -> str | None:
    match = external_attribution(text)
    if match:
        return match[0]
    match = re.search(QUOTE_OR_REPORT, text)
    return match[0] if match else None


def external_attribution(text: str) -> re.Match | None:
    return _EXTERNAL_PARTY.search(text)


def source_anchor(source, start, raw_sha256):
    """Bind a displayed span to exact UTF-8 source and Unicode scalar coordinates."""
    end = start + len(source)
    identifier = sha256(f"{raw_sha256}:{start}:{end}".encode()).hexdigest()[:24]
    return {"id": identifier, "source": source, "span": {"start": start, "end": end}}


def fingerprint(item):
    return {key: item[key] for key in CLAIM_KEYS}


def occurrence(source, start, *, field, subject, hard, operator=None, condition=None, reason=None,
               matches=(), reference=None, repair=None):
    end = start + len(source)
    identifier = sha256(f"{start}:{end}:{field}:{source}".encode()).hexdigest()[:24]
    return {
        "id": identifier, "kind": "obligation" if hard else "unresolved_field", "field": field,
        "source": source, "span": {"start": start, "end": end}, "subject": subject,
        "condition": condition, "operator": operator, "hard": hard, "reference": reference,
        "status": "UNKNOWN" if reason and reason != "AWAITING_CONFIRMATION" else "PROVISIONAL",
        "reason": reason or "AWAITING_CONFIRMATION",
        "matches": [fingerprint(item) for item in matches], "repair": repair,
    }


def _covered_fingerprints(claims):
    by_id = {item["id"]: item for item in claims if item.get("id")}
    superseded = set()
    covered = set()
    for item in claims:
        if item["status"] not in CONFIRMED:
            continue
        covered.add(tuple(item[key] for key in CLAIM_KEYS))
        prior = item.get("supersedes")
        while prior in by_id and prior not in superseded and by_id[prior]["status"] == "SUPERSEDED":
            superseded.add(prior)
            predecessor = by_id[prior]
            covered.add(tuple(predecessor[key] for key in CLAIM_KEYS))
            prior = predecessor.get("supersedes")
    return covered


def _repair_key(claim, operator, source):
    # A restatement can qualify the original expression. Sharing only a field
    # and amount would incorrectly equate distinct expenses and obligations.
    units = rf"(?:{CNY}|{MONTH})" if claim["field"] == "rent_parking_max" else CNY
    expression = re.sub(units, "", normalize("NFC", source), flags=re.IGNORECASE)
    expression = re.sub(r"\s+", "", expression)
    return (claim["field"], claim["subject"], claim["value"], operator, expression)


def blocking_obligations(semantic_turns, claims, options):
    """Keep raw obligations current through explicit confirmation and revision links."""
    covered = _covered_fingerprints(claims)
    confirmed_options = {option["label"] for option in options if option["status"] == "CONFIRMED"}
    groups = []
    subsequent = set()
    for semantic in reversed(semantic_turns):
        repaired_here = set()
        unresolved = []
        for obligation in semantic["obligations"]:
            if not obligation["hard"]:
                continue
            repair = obligation.get("repair")
            source = obligation["source"]
            if repair and _repair_key(repair, repair["operator"], source) in subsequent:
                continue
            if obligation["status"] != "UNKNOWN":
                matching = [item for item in obligation["matches"]
                            if tuple(item[key] for key in CLAIM_KEYS) in covered]
                if matching:
                    if obligation["operator"] and not obligation["condition"]:
                        repaired_here.update(_repair_key(item, obligation["operator"], source) for item in matching
                                             if not item["subject"] or item["subject"] in confirmed_options)
                    continue
            unresolved.append(obligation)
        subsequent.update(repaired_here)
        groups.append(unresolved)
    return [item for turn in reversed(groups) for item in turn]
