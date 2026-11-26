"""Bounded Chinese-language extraction for user-reviewable decision proposals."""

import re
import unicodedata
from collections.abc import Iterable
from decimal import Decimal
from hashlib import sha256

from .decision_semantics import (
    BOUND_FIELDS, CLARIFICATIONS, CNY, MONTH, NIGHT, NON_CNY, NON_MONTHLY, PARKING,
    RENT, REPORTED, REPORTING_CUES, SEMANTIC_VERSION, blocking_obligations, comparison,
    external_attribution, is_joint, monetary_scope, occurrence, scope_reference, source_anchor,
)


_DOMAIN_CUES = {
    "career": r"工作|岗位|职业|跳槽|转行|辞职|留任|升职|入职|面试|工资|薪资|薪水|月薪|到岗|offer",
    "housing": r"租房|续租|租约|退租|房租|住房|买房|房子|房源|房东|合租|月租",
    "learning": r"学习|课程|培训|学业|自学|升学|学费|考研|报名|学校",
    "moving": r"搬家|搬去|搬迁|搬到|迁居|迁往|异地|跨城",
    "budget": r"财务|花钱|开支|支出|预算|存款|储蓄|现金流|贷款|攒钱|还债",
    "life": r"生活|家庭|关系|作息|习惯|日常|健康|休息|陪伴|和伴侣",
    "risk": r"风险|不确定|赌一把|保险|投资|理财|亏损|暴露|损失",
}
_SPECIFIC_DOMAINS = {"career", "housing", "learning", "moving"}
_OPTION_HINT = r"比较|纠结|犹豫|权衡|打算|考虑|该不该|该选|我该|要不要|选哪个|哪个好|可选|备选|选项|两个方案"
_OPTION_ACTION = (
    r"留下|继续|换|离开|留在|去|搬|租|买|报名|自学|学|读|接受|拒绝|找|选择|保持|"
    r"等待|跳槽|续约|辞职|留任|续租|在职|全职|兼职|读研|现状|远程|在家|转行"
)
_CHOICE_START = re.compile(
    r"^(?:请问|一开始|我现在|现在我|最近我|我在想|我在|我想|我该不该|我应该|我该|我想要不要|"
    r"要不要|究竟|到底|是选|该选|应该|纠结要不要|纠结|犹豫|正在考虑|考虑|比较一下|比较|权衡|想知道|有点|"
    r"备选(?:是|有)?|可选(?:是|有)?|选项(?:是|有)?|要不|到底是|是)(?:\s*)"
)
_SENTENCE_ENDS = "。！？!?；;\n"
_QUOTES = dict(zip("“‘「『", "”’」』", strict=True))
_SELF_RESET = re.compile(r"^(?:(?:但(?:是)?|而|不过)\s*)?(?:我(?:本人|自己|的|不|只|必须|预算|从不)|本人)")
_REPORT_RESET = re.compile(r"^(?:(?:但(?:是)?|而|不过)\s*(?:我|本人)|我(?:本人|自己)|本人)")
_ASCII_LABEL = r"[A-Za-zＡ-Ｚａ-ｚ][0-9０-９]{0,3}(?![A-Za-zＡ-Ｚａ-ｚ0-9０-９])"
_HAN_LABEL = r"[甲乙丙丁戊己庚辛]"
_LABEL_ROLE = r"方案|选项|岗位|工作|课程|培训|项目|房源|房子|公寓|计划|[Oo]ffer"
_LABEL = rf"(?:(?:{_LABEL_ROLE})\s*(?:{_ASCII_LABEL}|{_HAN_LABEL}|[一二三四五六七八九十0-9０-９]{{1,3}})|{_ASCII_LABEL}|{_HAN_LABEL})"
_LABELED_CLAUSE = re.compile(r"^\s*(?P<label>[^：:\s，,]{1,30})\s*[:：]\s*")
_NON_OPTION_LABEL = re.compile(r"预算|目标|偏好|限制|底线|约束|截止|时间|费用|成本|学费|租金|收入|工资|薪资|希望|备注|问题|^(?:我|我的|本次)$")
_OPTION_DECLARATION = re.compile(rf"^(?P<label>{_LABEL})(?:\s*)(?:是|为|[:：])(?=\S)")

_DIGIT_CHARS = "零〇一二两俩三四五六七八九壹贰叁肆伍陆柒捌玖"
_DECIMAL_DIGITS = "0-9０-９"
_NUMERAL = rf"[{_DECIMAL_DIGITS}{_DIGIT_CHARS}]"
_COUNT = (
    rf"(?:(?:[{_DECIMAL_DIGITS}]{{1,3}}(?:[,，][{_DECIMAL_DIGITS}]{{3}})+(?:[.．][{_DECIMAL_DIGITS}]+)?"
    rf"|[{_DECIMAL_DIGITS}{_DIGIT_CHARS}十百千万亿拾佰仟萬億]+(?:[.．点]{_NUMERAL}+)?)"
    r"(?:[kKｋＫwWｗＷ万萬亿億])?|(?:一|1|１)?个半|半)"
)
_RANGE = re.compile(rf"{_COUNT}\s*(?:到|至|[-~～—－])\s*(?:{_COUNT})")
_UPPER_STRICT = r"(?<!不)(?:少于|低于|小于|不足|不到)|(?<![=<])<(?![=])|＜"
_LOWER_STRICT = r"(?<!不)(?:高于|大于|多于|超过)|(?<![=>])>(?![=])|＞"
_UPPER = (
    r"最多|至多|顶多|不超过|不能超过|不可超过|不得超过|不多于|不高于|不大于|"
    r"只能|上限|封顶|控制在|<=|≤"
)
_LOWER = r"至少|最少|最低|不低于|不能低于|不得低于|不小于|起码|下限|底线|>=|≥"
_HEDGE = r"可能|大概|大约|估计|大致|大抵|左右|上下|也许|听说|好像|不知道|不确定|未核实|尚未确认|未必|未定|暂不清楚|我猜|看起来|是否"
_PREVIOUS = r"原来|之前|过去|原先|以前|此前|曾经|本来"
_REVISION = r"改为|改成|换成|改到|提高到|提升到|上调到|降到|下调到|调整为|调整到|放宽到|收紧到|更正为|修正为|更新为"
_CONDITION = r"(?:^|[，,]|若是|只要|先看)(?:\s*我?\s*)?(?:如果|如果说|假如|假设|除非|若|只要|一旦|万一|要是|只有|前提是)"
_CONDITION_PREFIX = r"^(?:如果说|如果|假如|假设|除非|若是|若|只要|一旦|万一|要是|只有|前提是|否则|那么|但是|但)"
_CORRECTION = r"^(?:我)?(?:不是说|不是|并非)(?=.{0,60}(?:预算|上限|最多|至少|下限|每周|底线))"
_REPLACEMENT = r"^(?:而是|实际是|应当是|应该是|准确来说是|是)"
_WEEK = r"每\s*(?:个\s*)?(?:周|星期|礼拜)|一\s*(?:周|星期|礼拜)|周\s*(?:内|均)|[/／]\s*(?:周|星期|礼拜)"
_ONSITE = r"到岗|到办公室|去办公室|来办公室|坐班|驻场|到公司|去公司|到现场|去现场|线下办公|到单位|去单位|现场上班|线下上班|到店|去门店"
_MOVE = r"搬家|搬迁|异地搬迁|跨城搬迁|搬到|搬去|迁居|迁往|搬(?=\s*$)"
_MOVING_OBJECT = r"桌子|办公桌|椅子|冰箱|家具|箱子|器材|设备|货物|物品|工位"
_COST = (
    r"总预算|预算|总价|总费用|费用|花费|花销|花掉|支出|开支|花\s*(?=[零〇\d一二两三四五六七八九十百千万亿])|"
    r"成本|学费|报名费|租金|房租|月租|价格|价钱|支付|动用|收费|报价|维修费"
)
_INCOME = (
    r"每月(?:的)?(?:税后)?(?:收入|工资|薪资|到手)|月薪|月收入|月工资|每个月(?:收入|工资|到手)|月到手|月税后|一月到手|"
    r"(?:收入|工资|薪资)(?:是|为|按|大概|大约|税后|到手|估计|\s)*(?:每月|每个月|一月|每个自然月)"
)
_MONEY_MARK = r"元|块钱?|人民币|RMB|CNY|[¥￥]|[kKＫｋwWｗＷ千万萬亿億]"
_CNY_PERIOD = r"月租|月房租|每月|每个月|按月|[/／]\s*月"
_DAY = r"(?:个\s*)?天|日"
_HOUR = r"(?:个\s*)?(?:小时|钟头)|时(?!间|候)"

_MOVE_ALLOWED = re.compile(
    rf"(?P<flag>不能接受|不能|不可以|没法|无法|不允许|不会考虑|不能考虑|不接受|不可|能接受|"
    rf"可以考虑|可以|能够|能|愿意|接受)\s*(?:再\s*)?(?:因为工作\s*)?(?:要\s*)?(?:离开本地\s*)?(?:异地\s*)?(?:{_MOVE})"
)
_MOVE_REQUIRED = re.compile(
    rf"(?P<flag>不需要|不用|不必|无需|不要求|免于|必须|有必要|要|需要|要求|得|需)\s*(?:我\s*)?(?:{_MOVE})"
)
_NO_HARD_MOVE = re.compile(r"不是(?:说|真的|完全|绝对|也|我|我们)?\s*(?:不|没|无)|不一定(?:非)?要|未必|并非(?:要|必须|需要|不能|不可以)|不用说")
_RELUCTANT_MOVE = re.compile(
    rf"(?:不愿意|不想|不太(?:能|能够|可以|愿意)|不怎么(?:能|愿意)|难以接受|很难接受|不方便)\s*(?:{_MOVE})"
)
_NO_ASSERTION = re.compile(r"^(?:不知道|不清楚|尚不清楚|未确认|无法确定|还没想好|先不定|没定|不确定|暂时不清楚)[。！!\s]*$")
_GOAL = re.compile(r"(?:我(?:的)?)?(?:目标(?:是|为)?|想达到|想实现|希望实现|希望能够|我希望|想要(?:实现|达到))\s*[:：]?\s*(?P<value>.+)")
_PREF = re.compile(
    r"(?:我)?(?:最看重|比较看重|更看重|看重|更重视|更在意|比较在意|更关心|更倾向于|倾向于|偏好|"
    r"优先考虑|最重要的是|更希望|更喜欢|不喜欢|不想|优先是|排在前面的是)\s*[:：]?\s*(?P<value>.+)"
)
_DATE = (
    rf"(?:[{_DECIMAL_DIGITS}]{{2,4}}年\s*)?{_COUNT}月\s*{_COUNT}[日号]"
    rf"|(?:这个|下个|上个|本|这|下|上)?(?:星期|礼拜|周)[一二三四五六日天末{_DECIMAL_DIGITS}]"
    rf"|今天|明天|后天|本月底|这个月底|下月底|月底|月末|年底|年末|月初|下周|本周|这周|本月|下月"
    rf"|{_COUNT}(?:天|周|个月|月|小时)(?=\s*内)"
)
_DEADLINE = re.compile(
    rf"(?P<date>{_DATE})(?P<edge>\s*(?:之前|以前|前|为止|截止|当天|到期|内|之前完成))?"
)
_DEADLINE_CONTEXT = r"决定|决策|答复|回复|签约|确认|截止|到期|报名|提交|选定|作出选择|给答复"
_OPEN_DEADLINE = re.compile(r"没有固定(?:的)?(?:期限|截止日?|截止时间)|无固定(?:期限|截止日?|截止时间)|没有明确(?:的)?截止(?:日期|日|时间)?")

_UNITS = {
    "onsite_max": "days/week", "onsite": "days/week",
    "hours_max": "hours/week", "hours": "hours/week",
    "cost_max": "yuan", "cost": "yuan",
    "income_min": "yuan/month", "income": "yuan/month",
    "onsite_min": "days/week", "hours_min": "hours/week",
    "cost_min": "yuan", "income_max": "yuan/month",
}
_BOUND_DIRECTION = {
    "onsite": ("onsite_min", "onsite_max"),
    "hours": ("hours_min", "hours_max"),
    "cost": ("cost_min", "cost_max"),
    "income": ("income_min", "income_max"),
}
_BOUNDED_BASE = {field: base for base, fields in _BOUND_DIRECTION.items() for field in fields}
_BOOLEAN_FIELDS = {"move_allowed", "move_required"}
_NARRATIVE_FIELDS = {"goal", "preference", "deadline"}
_MEASUREMENT_FIELDS = {"onsite", "hours", "cost", "income", "move_required"}
_CHINESE_DIGITS = str.maketrans("零〇一二两俩三四五六七八九壹贰叁肆伍陆柒捌玖", "0012223456789123456789")
_FINANCIAL_UNITS = str.maketrans("拾佰仟萬億", "十百千万亿")


def _numeric_integer(token: str) -> int:
    if token.isascii() and token.isdecimal():
        return int(token)
    for symbol, scale in (("亿", 100_000_000), ("万", 10_000)):
        if symbol not in token:
            continue
        head, tail = token.split(symbol, 1)
        if symbol in tail:
            raise ValueError("repeated decimal unit")
        remainder = _numeric_integer(tail) if tail else 0
        if len(tail) == 1 and tail.isdecimal() and tail != "0":
            remainder *= scale // 10
        return (_numeric_integer(head) if head else 1) * scale + remainder
    total, previous_scale = 0, None
    buffer = ""
    for digit in token:
        if digit.isascii() and digit.isdecimal():
            buffer += digit
            continue
        scale = {"千": 1000, "百": 100, "十": 10}.get(digit)
        if not scale or (previous_scale is not None and scale >= previous_scale):
            raise ValueError("invalid decimal unit")
        total += (int(buffer) if buffer else 1) * scale
        previous_scale, buffer = scale, ""
    if buffer:
        tail = int(buffer)
        if len(buffer) == 1 and previous_scale and previous_scale > 10:
            tail *= previous_scale // 10
        total += tail
    return total


def _number(token: str) -> str | None:
    normalized = unicodedata.normalize("NFKC", token).lower()
    if normalized in {"半", "个半"}:
        return "0.5"
    if normalized in {"一个半", "1个半"}:
        return "1.5"
    normalized = normalized.translate(_CHINESE_DIGITS).translate(_FINANCIAL_UNITS)
    normalized = normalized.replace(",", "").replace("点", ".")
    if not normalized or len(normalized) > 28:
        return None
    if normalized[-1] in "kw":
        normalized = normalized[:-1] + {"k": "千", "w": "万"}[normalized[-1]]
    try:
        match = re.fullmatch(r"(\d+(?:\.\d+)?)([十百千万亿]?)", normalized)
        if match:
            value = Decimal(match[1]) * {"": 1, "十": 10, "百": 100, "千": 1000, "万": 10_000, "亿": 100_000_000}[match[2]]
        else:
            value = Decimal(_numeric_integer(normalized))
    except (ArithmeticError, ValueError):
        return None
    if value > 10**12:
        return None
    result = format(value, "f")
    return result.rstrip("0").rstrip(".") if "." in result else result


def _parts(text: str, delimiters: str):
    """Split source spans while keeping quoted text and thousands separators intact."""
    start = 0
    quote_ends = []
    for pos, char in enumerate(text):
        closed = False
        if quote_ends and char == quote_ends[-1]:
            quote_ends.pop()
            closed = True
        elif char in _QUOTES or char == '"':
            quote_ends.append(_QUOTES.get(char, char))
        if quote_ends:
            continue
        if closed and delimiters == _SENTENCE_ENDS and pos and text[pos - 1] in delimiters and (
            _SELF_RESET.match(text[pos + 1:].lstrip())
        ):
            end = pos + 1
        elif char not in delimiters or char in ",，" and pos and text[pos - 1].isdigit() and re.match(
            r"[0-9０-９]{3}(?![0-9０-９])", text[pos + 1:pos + 5],
        ):
            continue
        else:
            end = pos
        fragment = text[start:end]
        if fragment.strip():
            yield fragment.strip(), start + len(fragment) - len(fragment.lstrip())
        start = pos + 1
    fragment = text[start:]
    if fragment.strip():
        yield fragment.strip(), start + len(fragment) - len(fragment.lstrip())


def _clauses(sentence: str) -> list[str]:
    return [clause for clause, _ in _parts(sentence, ",，")]


def _looks_labeled(label: str) -> bool:
    return bool(re.fullmatch(_LABEL, label)) or not bool(_NON_OPTION_LABEL.search(label))


def _unquote(fragment: str) -> str:
    return fragment.strip(" \t\r：:《》«»「」『』【】（）()“”‘’\"'")


def _left_option(fragment: str) -> str:
    # Decisions often start with several stacked conversational cues.
    left = _unquote(fragment)
    while match := _CHOICE_START.match(left):
        left = left[match.end():]
    return _unquote(left)


def _plausible_choice(left: str, right: str, sentence: str) -> bool:
    if not all(0 < len(option) <= 100 for option in (left, right)) or left == right:
        return False
    if re.match(r"^(?:不知道|不确定|因此|因为|由于|不能|不太|没想好|不是|很|挺|比较)", right):
        return False
    if re.search(_HEDGE, left) and not re.search(_OPTION_ACTION, left):
        return False
    return bool(
        re.search(_OPTION_HINT, sentence)
        or re.fullmatch(_LABEL, left)
        or re.fullmatch(_LABEL, right)
        or (re.search(_OPTION_ACTION, left) and re.search(_OPTION_ACTION, right))
    )


def _options(sentences: list[str], focus: str) -> list[str]:
    options = []
    for sentence in sentences:
        labeled = _LABELED_CLAUSE.match(sentence)
        if labeled and _looks_labeled(labeled["label"]) and not scope_reference(labeled["label"]) and (
            re.fullmatch(_LABEL, labeled["label"])
            or re.search(f"{_MOVE}|{_ONSITE}|{_COST}|{_INCOME}|{_HOUR}", sentence[labeled.end():])
        ):
            options.append(labeled["label"])
        if re.search(r"不是.{0,45}而是|并非.{0,45}而是", sentence):
            continue
        compare_marker = re.search(r"比较|权衡|二选一", sentence)
        pair = re.split(r"还是|或者|或是|\s+vs\.?\s+|[,，]\s*要不", sentence, maxsplit=1, flags=re.IGNORECASE)
        if len(pair) == 1 and compare_marker:
            pair = re.split(r"和|与", sentence[compare_marker.end():], maxsplit=1)
        if len(pair) == 2 and _clauses(pair[0]) and _clauses(pair[1]):
            left = _left_option(_clauses(pair[0])[-1])
            right = _unquote(_clauses(pair[1])[0])
            right = re.sub(r"(?:哪个(?:更|比较)?(?:好|合适|划算)|哪一个(?:更好|合适))$", "", right).strip()
            if _plausible_choice(left, right, sentence):
                options.extend((left, right))
        if focus == "options" or re.search(r"(?:备选|可选|我的选项)(?:有|是)\s*[:：]?", sentence):
            listed = re.sub(r"^(?:备选|可选|我的选项)(?:有|是)\s*[:：]?\s*", "", sentence)
            if re.search(r"[、/]|\s+或\s+|\s+和\s+", listed):
                entries = [_left_option(part) for part in re.split(r"[、/]|\s+或\s+|\s+和\s+", listed)]
                options.extend(part for part in entries if 0 < len(part) <= 100)
    declarations = [
        marker["label"] for sentence in sentences for clause in _clauses(sentence)
        if (marker := _OPTION_DECLARATION.match(clause))
    ]
    if len(set(declarations)) >= 2:
        options.extend(declarations)
    return list(dict.fromkeys(options))[:16]


def _domain(text: str) -> str:
    counts = {
        domain: len(re.findall(pattern, text, flags=re.IGNORECASE))
        for domain, pattern in _DOMAIN_CUES.items()
    }
    primary = [domain for domain in counts if domain in _SPECIFIC_DOMAINS and counts[domain]]
    candidates = primary or [domain for domain in counts if counts[domain]]
    return max(candidates, key=counts.__getitem__) if candidates else "general"


def _option_aliases(options: Iterable[str]) -> dict[str, str]:
    labels = set(options)
    by_alias = {}
    for option in labels:
        core = re.sub(r"^(?:留在|继续|转去|搬去|去|选|读|接受|换到|报名|参加)", "", option)
        candidates = {option, core}
        if match := re.fullmatch(rf"(?:{_LABEL_ROLE})\s*(?P<tag>{_ASCII_LABEL}|{_HAN_LABEL})", core):
            candidates.add(match["tag"])
        for suffix in ("教程", "课程", "夜课", "培训", "岗位", "公司", "房源", "公寓", "方案", "项目"):
            if core.endswith(suffix):
                candidates.add(suffix)
        for alias in candidates:
            if alias:
                by_alias.setdefault(alias, set()).add(option)
    aliases = {alias: next(iter(matches)) for alias, matches in by_alias.items() if len(matches) == 1}
    aliases.update((label, label) for label in labels)
    return aliases


def _subject(clause: str, aliases: dict[str, str]) -> tuple[str, str]:
    clause = re.sub(_CONDITION_PREFIX, "", clause, count=1).lstrip()
    labeled = _LABELED_CLAUSE.match(clause)
    if labeled and _looks_labeled(labeled["label"]) and not scope_reference(labeled["label"]):
        name = labeled["label"]
        return aliases.get(name, name), clause[labeled.end():]
    for name in sorted(aliases, key=lambda item: (-len(item), item)):
        if clause.startswith(name) and len(clause) > len(name):
            if re.fullmatch(_ASCII_LABEL, name) and re.match(r"[A-Za-z0-9]", clause[len(name):]):
                continue
            return aliases[name], clause[len(name):].lstrip()
    match = re.match(rf"(?P<label>{_LABEL})(?=\s*(?:的)?(?:{_ONSITE}|{_MOVE}|{_COST}|{_INCOME}|"
                     rf"{_WEEK}|{_HOUR}|{_CNY_PERIOD}|{PARKING}|{NIGHT}|当前实际排班|实际排班|"
                     rf"不|没|无|是|需要|要求|只|必须|可能|得|要|需))", clause)
    return (aliases.get(match["label"], match["label"]), clause[match.end():].lstrip()) if match else ("", clause)


def _claim(kind: str, field: str, subject: str, value: str, unit: str, source: str) -> dict[str, str]:
    return {"kind": kind, "field": field, "subject": subject, "value": value, "unit": unit, "source": source}


def _qualify(clause: str, base_kind: str, context: str, strict: bool = False) -> str:
    if context:
        return context
    if re.search(_HEDGE, clause):
        return "estimate"
    return "strict_constraint" if strict and base_kind == "constraint" else base_kind


def _historical(clause: str) -> bool:
    for match in re.finditer(_PREVIOUS, clause):
        if match[0] not in {"之前", "以前"} or not re.search(rf"(?:{_DATE})\s*$", clause[:match.start()]):
            return True
    return False


def _numeric_claims(
    clause: str, subject: str, source: str, context: str, focus: str,
) -> list[dict[str, str]]:
    if _RANGE.search(clause) or re.search(rf"[-−﹣－负]\s*{_COUNT}|{_COUNT}\s*[%％]|百分之", clause):
        return []

    unit_matches = []
    weekly = re.search(_WEEK, clause)
    conditional_onsite = context == "conditional" and bool(re.search(r"上班|去(?:一|两|\d)天", clause))
    if re.search(_ONSITE, clause) or conditional_onsite:
        if weekly or focus in {"onsite", "onsite_max"}:
            unit_matches.append(("onsite", "onsite_max", "days/week", _DAY, _ONSITE))
    if re.search(_HOUR, clause) and (weekly or focus in {"hours", "hours_max"}):
        unit_matches.append(("hours", "hours_max", "hours/week", _HOUR, _HOUR))
    currency_allowed = not re.search(NON_CNY, clause, flags=re.IGNORECASE) and not re.search(NON_MONTHLY, clause)
    if currency_allowed and re.search(_INCOME, clause):
        unit_matches.append(("income", "income_min", "yuan/month", r"(?:元|块钱?)?", _INCOME))
    if currency_allowed and re.search(_COST, clause):
        unit = "yuan/month" if re.search(_CNY_PERIOD, clause) else "yuan"
        if unit == "yuan/month" or not re.search(rf"{_WEEK}|每年|每季|按年|[/／]\s*年", clause):
            unit_matches.append(("cost", "cost_max", unit, r"(?:元|块钱?)?", _COST))
    elif currency_allowed and re.match(r"^(?:房源|房子|公寓)", subject) and re.search(_CNY_PERIOD, clause):
        unit_matches.append(("cost", "cost_max", "yuan/month", r"(?:元|块钱?)", _CNY_PERIOD))
    elif currency_allowed and subject and re.fullmatch(rf"(?:只)?(?:要|收)\s*{_COUNT}\s*(?:元|块钱?)", clause):
        unit_matches.append(("cost", "cost_max", "yuan", r"(?:元|块钱?)", ""))

    if context == "revision" and not unit_matches and focus in _UNITS and currency_allowed:
        base = _BOUNDED_BASE.get(focus, focus)
        suffix = {"onsite": _DAY, "hours": _HOUR}.get(base, r"(?:元|块钱?)?")
        unit_matches.append((base, focus, _UNITS[focus], suffix, ""))

    result = []
    for base, hard, unit, suffix, metric in unit_matches:
        segment = clause
        marker = list(re.finditer(_REVISION, clause))
        if marker:
            segment = clause[marker[-1].end():]
        if base in {"cost", "income"} and not marker:
            metric_start = re.search(metric, segment)
            if metric_start:
                head = segment[:metric_start.start()]
                # An amount before the metric is acceptable if directly tied to a currency.
                if not re.search(rf"{_COUNT}\s*(?:元|块钱?|人民币)\s*(?:的)?\s*$", head):
                    segment = segment[metric_start.end():]
        matches = list(re.finditer(rf"(?P<count>{_COUNT})\s*(?:{suffix})", segment))
        if len(matches) != 1:
            continue
        value = _number(matches[0]["count"])
        if value is None:
            continue
        if base == "onsite" and Decimal(value) > 7:
            continue
        operator = comparison(clause)
        if operator == "UNKNOWN":
            continue
        strict = operator in {"<", ">"}
        if operator:
            hard = _BOUND_DIRECTION[base][int(operator.startswith("<"))]
        if context == "revision" and not operator and _BOUNDED_BASE.get(focus) == base:
            hard = focus
        budget = base == "cost" and bool(re.search(r"预算", clause))
        condition_limit = conditional_onsite and bool(re.search(r"只(?:需要|需|要|用)", clause))
        revision_limit = context == "revision" and focus == hard and focus not in _MEASUREMENT_FIELDS
        known_limit = bool(operator or budget or condition_limit or revision_limit)
        field = hard if known_limit and not subject else base
        if known_limit and subject:
            # The observed cap on a particular option is not a point measurement.
            if context != "conditional":
                kind = "estimate"
            else:
                kind = context
        else:
            kind = _qualify(clause, "constraint" if field == hard else "measurement", context, strict)
            if not context and re.search(r"承诺|据说|据称|转述|预计|打算|声称", clause):
                kind = "estimate"
        if base in {"income", "cost"} and not (
            re.search(_MONEY_MARK, clause, flags=re.IGNORECASE) or metric or focus in _UNITS
        ):
            continue
        if field == base and not subject and focus != base:
            continue
        result.append(_claim(kind, field, subject if field == base else "", value, unit, source))
    return result


def _move_claim(
    clause: str, subject: str, source: str, context: str,
) -> dict[str, str] | None:
    if _NO_HARD_MOVE.search(clause) or re.search(_MOVING_OBJECT, clause):
        return None
    if not subject and (reluctant := _RELUCTANT_MOVE.search(clause)):
        return _claim(context or "preference", "preference", "", reluctant[0], "", source)
    match = (_MOVE_REQUIRED if subject else _MOVE_ALLOWED).search(clause)
    if not match:
        return None
    flag = match["flag"]
    negative = flag.startswith(("不", "没", "无", "免"))
    if not subject and flag in {"可以考虑", "愿意"}:
        return _claim(context or "preference", "preference", "", match[0], "", source)
    kind = "estimate" if re.search(_HEDGE, clause) else _qualify(
        clause, "measurement" if subject else "constraint", context,
    )
    return _claim(
        kind,
        "move_required" if subject else "move_allowed",
        subject,
        "no" if negative else "yes",
        "",
        source,
    )


def _narrative(clause: str, source: str, context: str, subject: str) -> list[dict[str, str]]:
    result = []
    for field, pattern in (("goal", _GOAL), ("preference", _PREF)):
        if match := pattern.search(clause):
            value = match["value"].strip()
            if field == "preference" and match[0].startswith(("不喜欢", "不想", "我不喜欢", "我不想")):
                value = match[0].strip()
            if not (field == "preference" and re.match(r"(?:权重|百分之)", value)):
                result.append(_claim(context or field, field, subject, value, "", source))
    if match := _OPEN_DEADLINE.search(clause):
        result.append(_claim(context or "deadline", "deadline", subject, "无固定期限", "", source))
    elif re.search(_DEADLINE_CONTEXT, clause) and (match := _DEADLINE.search(clause)):
        strict_date = re.search(r"最晚|必须|要求|截止|到期|要在", clause)
        hoped_for = re.search(r"希望|想要|最好|理想(?:是|为)|争取", clause)
        if strict_date or (match["edge"] and not hoped_for):
            result.append(_claim(_qualify(clause, "deadline", context), "deadline", subject, match[0].strip(), "", source))
    return result


def _focus_answer(source: str, focus: str, subject: str) -> dict[str, str] | None:
    if len(source) > 160 or _NO_ASSERTION.fullmatch(source):
        return None
    clause = source.strip("。！？!?；; \t\n")
    if focus in _BOOLEAN_FIELDS:
        good, bad = ("可以|能|接受|同意|行|可|能搬|可以搬", "不能|不可以|不行|不接受|不搬|无法|不行的")
        if focus == "move_required":
            good, bad = ("是|需要|必须|要|要搬|需要搬|必须搬", "不用|不需要|无需|不必|否|不需要搬|不用搬")
        if re.fullmatch(good, clause):
            value = "yes"
        elif re.fullmatch(bad, clause):
            value = "no"
        else:
            return None
        return _claim("constraint" if focus == "move_allowed" else "measurement", focus, subject, value, "", source)
    if focus in _UNITS:
        suffix = r"(?:元|块钱?|人民币)?(?:[/／]\s*月)?"
        if focus.startswith("onsite"):
            suffix = rf"(?:{_DAY})?(?:\s*[/／]\s*周)?"
        if focus.startswith("hours"):
            suffix = rf"(?:{_HOUR})?(?:\s*[/／]\s*周)?"
        cue = rf"(?P<cue>{_UPPER}|{_LOWER}|{_UPPER_STRICT}|{_LOWER_STRICT})"
        match = re.fullmatch(
            rf"(?:{_WEEK})?\s*(?:{cue}\s*)?[¥￥]?(?P<count>{_COUNT})\s*{suffix}\s*(?P<hedge>左右|上下)?",
            clause,
        )
        if not match or (value := _number(match["count"])) is None:
            return None
        if focus.startswith("onsite") and Decimal(value) > 7:
            return None
        if match["cue"] and (
            (focus.endswith("_max") and re.fullmatch(rf"{_LOWER}|{_LOWER_STRICT}", match["cue"]))
            or (focus.endswith("_min") and re.fullmatch(rf"{_UPPER}|{_UPPER_STRICT}", match["cue"]))
        ):
            return None
        kind = "measurement" if focus in _MEASUREMENT_FIELDS else "constraint"
        if match["cue"] and kind == "measurement" or match["hedge"]:
            kind = "estimate"
        elif match["cue"] and re.fullmatch(rf"{_UPPER_STRICT}|{_LOWER_STRICT}", match["cue"]):
            kind = "strict_constraint"
        unit = "yuan/month" if _UNITS[focus] == "yuan" and re.search(r"[/／]\s*月", clause) else _UNITS[focus]
        return _claim(kind, focus, subject, value, unit, source)
    if focus == "deadline" and (re.fullmatch(_DEADLINE, clause) or _OPEN_DEADLINE.fullmatch(clause)):
        return _claim("deadline", "deadline", "", clause, "", source)
    if focus in {"goal", "preference"} and not re.search(rf"{_HEDGE}|如果|除非|权重|概率", clause):
        return _claim(focus, focus, "", clause, "", source)
    return None


def _conditional_start(clauses: list[str]) -> int:
    for index, clause in enumerate(clauses):
        if re.search(_CONDITION, clause):
            return index
    for index, clause in enumerate(clauses):
        if re.search(rf"(?:就|才)(?:可以|能|愿意)(?:考虑)?\s*(?:{_MOVE})", clause):
            for preceding in range(index, max(index - 2, -1), -1):
                if re.search(rf"{_WEEK}|{_ONSITE}", clauses[preceding]):
                    return preceding
    return len(clauses)


_JOINT_PAIR = rf"(?:(?:{RENT})\s*(?:和|与|及|加(?:上)?|[+＋、])\s*(?:{PARKING})|(?:{PARKING})\s*(?:和|与|及|加(?:上)?|[+＋、])\s*(?:{RENT}))"
_NIGHT_POLICY = re.compile(
    rf"(?:我(?:目前|绝对)?|本人)?(?:不能|不得|不接受|不允许|拒绝|接受不了|不能接受)(?:上|排|任何)?(?:{NIGHT})"
    rf"|(?:我的)?(?:{NIGHT})(?:零容忍|必须为零|(?:一个|一次|一晚)都不能(?:上|有|接受)?)"
    rf"|(?:我)?(?:{NIGHT})(?:一个|一次|一晚)都(?:不接受|不能接受|不能上|不行|不可以)"
    rf"|(?:我|本人)?(?:只考虑|只接受)(?:没有|不含|无)(?:{NIGHT})(?:的)?(?:岗位|工作|安排)"
)
_NIGHT_ACTUAL = re.compile(
    rf"(?:已经核对的|已核对的|核对过的|当前|目前|本期|现行)?实际(?:排班|班表)(?:显示|里|中|表明|[:：])?"
    rf"(?:(?P<no>无|没有|不含|未安排|没有安排)|(?P<yes>有|包含|安排了?))(?:任何|了)?(?:{NIGHT})"
)
_SIMPLE_RELOCATION_EXCEPTION = re.compile(
    rf"(?:如果|只要|若)?\s*(?:我\s*)?(?:{_WEEK})\s*(?:{_ONSITE})?\s*(?:{_UPPER})\s*{_COUNT}\s*"
    rf"(?:{_DAY})(?:\s*(?:{_ONSITE}))?\s*[,，]?\s*(?:我\s*)?(?:那么|则|就)\s*(?:可以|能)\s*(?:{_MOVE})"
)
_HARD_SIGNAL = re.compile(r"上限|下限|底线|不可以|不能|不得|务必|严禁|必须|零容忍|一律不要|不接受|硬约束|绝不|只(?:考虑|接受)")
_BOUND_SIGNAL = re.compile(rf"(?:{_UPPER}|{_LOWER}|{_UPPER_STRICT}|{_LOWER_STRICT})")
_OPTION_REFERENCE = re.compile(r"这(?:个|项|份|家)(?:方案|岗位|公司|项目|选项)?|那(?:个|项|份|家)|另外(?:的|一个)?|另一个|后者|前者|它(?:的|每|不)|其他方案|别的岗位")
_PHRASE_NEGATED = re.compile(r"不是(?:说)?|并非|不一定|未必|没说|从没说|从未说")
_NEGATION_SIGNAL = re.compile(r"未|没|无|不能|不得|不可以|不允许|不接受|拒绝|不[低小少高大多]于|不超过")
_RETRACTION = re.compile(
    r"(?:预算|上限|底线|约束|前面说的|之前说的|上一条)(?:.{0,12})(?:撤回|取消|作废|不再适用)"
    r"|(?:撤回|取消|作废)(?:.{0,12})(?:预算|上限|底线|约束|前面说的|之前说的|上一条)"
)
_MISSING_EVIDENCE = re.compile(
    r"还没(?:问|定|拿到|查|核实|决定|选定)|还没(?:有)?资料|没有资料|还没有(?:书面)?(?:报价|回复)|"
    r"还未(?:知|问|定|核对|决定|确认|核实)|尚未(?:知|定|核对|确认|核实)|(?:还|也)?不清楚|不知道|"
    r"未核实|未确认|未知|没谱|没法查|无法查|预测不了|有待核实|得问|要问|待确认|待核实|是真是假"
)
_CONDITIONAL_REFUSAL = re.compile(r"(?:我(?:就|也)?|(?:那|那么|则|就)我?)(?:不(?:去|选|签|做|干|买|租|上|报名|参加|接受|考虑|换)|拒绝)")
_UNSUPPORTED_LOGIC = re.compile(r"或者|要么|二者择一|至少一项|两者之一|但(?:我(?:只|还|又)|是)|除非|否则")
_DURATION_BOUNDARY = re.compile(rf"{_COUNT}\s*(?:天|周|个月|月|小时)\s*内")
_READING_COLLOQUIAL = re.compile(rf"^[{_DIGIT_CHARS}十百千万亿拾佰仟萬億]+[百千万亿佰仟萬億][{_DIGIT_CHARS[2:]}]$")
_LEXICAL_DATE = re.compile(
    rf"\d{{4}}[-‐‑−]\d{{1,2}}[-‐‑−]\d{{1,2}}(?:前|以后|之后)?|{_DEADLINE.pattern}"
)
_LEXICAL_NUMERAL = re.compile(rf"(?P<percent>百分之)?(?P<count>{_COUNT})\s*(?P<suffix>[%％]|成)?")
_LEXICAL_UNIT = re.compile(
    rf"(?P<currency>{NON_CNY}|{CNY})|(?P<hour>(?:个\s*)?(?:小时|钟头))|"
    r"(?P<minute>分钟)|(?P<second>秒)|(?P<workday>工作日)|(?P<day>天|日)|(?P<week>周)|(?P<month>个月|月)|"
    r"(?P<count>次|个|人|套)|(?P<distance>公里|千米|米)",
    re.IGNORECASE,
)
_PERIODS = re.compile(
    rf"(?P<month>{MONTH}|月薪)|(?P<week>{_WEEK})|(?P<year>每年|按年|[/／]\s*年|年薪)"
    r"|(?P<day>每天|每日|按日|[/／]\s*[天日])"
    r"|(?P<event>每次|单次|按次|[/／]\s*次)",
)
_GUARD_OPENERS = ("前提是", "如果说", "如果", "假如", "假设", "除非", "若是", "只要", "一旦", "万一", "要是", "只有", "若")
_GUARD_CONTINUATIONS = ("并且", "而且", "同时", "或者", "且", "或", "并")
_BRANCH_MARKER = re.compile(r"(?<![本刚曾已现早也])(?:那么|我(?:就|才|则)|就(?=不|只|得|可|必|要|能|取消)|则|才(?=会|能|可|肯))")
_SCOPE_ONLY = re.compile(r"仅(?:适用|用于)(?:于)?(?P<scope>.+)$")
_EDIT_MARKER = re.compile(
    rf"(?P<replace>{_REVISION}|更正|修正|刚核实|实际是)|"
    r"(?P<retract>撤回|撤掉|取消|作废|不再适用|不作为强制条件)"
)


def _condition_relations(sentence, start, clauses, raw_sha256):
    """Attach guard and branch anchors without assuming either branch is true."""
    relations = []
    guard = None
    polarity = "when_true"
    primary_polarity = polarity
    branch_seen = False
    for index, (clause, pos) in enumerate(clauses):
        target = clause
        target_pos = pos
        prefix_length = next((i for i, char in enumerate(clause) if char.isalnum()), len(clause))
        search = clause[prefix_length:]
        opening = next(
            (candidate for candidate in _GUARD_OPENERS if search.startswith(candidate)), None,
        )
        if not opening:
            prefix = re.match(r"^(?:但(?:是)?|不过|而)\s*", search)
            if prefix:
                search = search[prefix.end():]
                opening = next((candidate for candidate in _GUARD_OPENERS if search.startswith(candidate)), None)
        if opening:
            guard_start = pos + len(clause) - len(search)
            boundary = _BRANCH_MARKER.search(search, len(opening))
            primary_polarity = "when_false" if opening == "除非" else "when_true"
            polarity = primary_polarity
            branch_seen = False
            if boundary:
                target_pos = guard_start + boundary.start()
                target = search[boundary.start():]
                guard_end = target_pos
            else:
                guard_end = pos + len(clause)
                target = ""
            source = sentence[guard_start:guard_end].rstrip()
            guard = source_anchor(source, start + guard_start, raw_sha256)
        elif guard and not branch_seen and clause.startswith(_GUARD_CONTINUATIONS):
            guard_start = guard["span"]["start"] - start
            source = sentence[guard_start:pos + len(clause)]
            guard = source_anchor(source, start + guard_start, raw_sha256)
            continue
        elif guard and clause.startswith("否则"):
            polarity = "when_false" if primary_polarity == "when_true" or not branch_seen else "when_true"
        elif scoped := _SCOPE_ONLY.search(clause):
            guard = source_anchor(scoped["scope"], start + pos + scoped.start("scope"), raw_sha256)
            primary_polarity = polarity = "when_true"
        if guard and target:
            relations.append((index, {
                "kind": "condition", "guard": guard,
                "target": source_anchor(target, start + target_pos, raw_sha256),
                "polarity": polarity, "authority": "NONE",
            }))
            branch_seen = True
    return relations


def _personal_choice_scope(sentence):
    label = _LABELED_CLAUSE.match(sentence)
    if label and re.fullmatch(_LABEL, label["label"]):
        return True
    attribution = external_attribution(sentence)
    if not attribution:
        return True
    choice_cue = re.search(_OPTION_HINT, sentence)
    return bool(choice_cue and choice_cue.start() < attribution.start())


def _verified_amount(clause):
    """Return a lexical amount only when the clause has a single explicit CNY amount."""
    matches = list(re.finditer(_COUNT, clause))
    if len(matches) != 1 or not re.search(
        rf"(?:{CNY})\s*{_COUNT}|{_COUNT}\s*(?:{CNY})", clause, re.IGNORECASE
    ):
        return None
    return _number(matches[0][0])


def _joint_claim(clause, subject, source, context):
    if subject or monetary_scope(clause, monthly=True) or not re.search(_JOINT_PAIR, clause):
        return None
    match = re.fullmatch(
        rf"(?:(?:{_REVISION})\s*)?(?:我(?:的|想要)?)?\s*(?:{MONTH}\s*)?{_JOINT_PAIR}\s*"
        rf"(?:都|这两项|两项)?\s*(?:(?:合计|共计|总共|一共|一起|合并|相加|共享|共用|联合|共同)\s*)?"
        rf"(?:(?:{MONTH}|总预算|预算|总额|的|是|为|只能是|{_UPPER}|{_UPPER_STRICT})\s*)*"
        rf"(?:{CNY}\s*)?{_COUNT}\s*(?:{CNY})?\s*(?:{MONTH})?\s*(?:的?预算)?",
        clause,
        re.IGNORECASE,
    )
    operator = comparison(clause)
    if match and (operator in {"<=", "<"} or operator is None and "预算" in clause):
        if (value := _verified_amount(clause)) is not None:
            return _claim(_qualify(clause, "constraint", context, operator == "<"),
                          "rent_parking_max", "", value, "yuan/month", source)
    return None


def _components(clause, subject, source, context):
    if not subject or monetary_scope(clause, monthly=True) or re.search(REPORTED, clause):
        return []
    for field, metric in (("parking_monthly", PARKING), ("rent_monthly", RENT)):
        if re.fullmatch(
            rf"的?\s*(?:{MONTH}\s*)?(?:{metric})\s*(?:(?:{MONTH}|{_REVISION}|为|是|实际|：|:)\s*)*"
            rf"(?:{CNY}\s*)?{_COUNT}\s*(?:{CNY})?\s*(?:{MONTH})?",
            clause, re.IGNORECASE,
        ):
            if (value := _verified_amount(clause)) is not None:
                return [_claim(_qualify(clause, "measurement", context), field, subject,
                               value, "yuan/month", source)]
    return []


def _night_claim(clause, subject, source, context):
    if not subject and _NIGHT_POLICY.fullmatch(clause):
        return _claim(_qualify(clause, "constraint", context), "night_shift_max", "",
                      "0", "presence", source)
    if subject and not context and (match := _NIGHT_ACTUAL.fullmatch(clause.lstrip("的"))):
        return _claim("measurement", "night_shift_required", subject,
                      "no" if match["no"] else "yes", "presence", source)
    return None


def _span(source, start):
    return {"start": start, "end": start + len(source)}


def _claim_candidate(item, start, guard=None):
    source = item["source"]
    return {**item, "kind": "claim", "span": _span(source, start), "role": item["kind"],
            "condition": guard if item["kind"] == "conditional" else None,
            "operator": comparison(source), "negation": bool(_NEGATION_SIGNAL.search(source)),
            "revision": "replace" if item["kind"] == "revision" else None,
            "source_identity": "current_user", "authority": "NONE", "status": "PROVISIONAL"}


def _lexical_candidates(text, raw_sha256):
    calendars = list(_LEXICAL_DATE.finditer(text))
    durations = [match for match in calendars if _DURATION_BOUNDARY.fullmatch(match[0])]
    dates = [match for match in calendars if match not in durations]
    segments = [(clause, start + offset) for sentence, start in _parts(text, _SENTENCE_ENDS)
                for clause, offset in _parts(sentence, ",，")]
    candidates = [
        {"kind": "date", "source": match[0], "span": _span(match[0], match.start()),
         "reading": "UNANCHORED_DATE", "value": None, "unit": None,
         "period": None, "authority": "NONE"}
        for match in dates
    ]
    for match in _LEXICAL_NUMERAL.finditer(text):
        if any(match.start() < date.end() and match.end() > date.start() for date in dates):
            continue
        source = match[0].rstrip()
        end = match.start() + len(source)
        unit_start = end
        while unit_start < len(text) and text[unit_start] in " \t\u3000":
            unit_start += 1
        unit_match = _LEXICAL_UNIT.match(text, unit_start)
        if not unit_match and not match["suffix"] and not match["percent"]:
            if re.search(rf"(?:{_LABEL_ROLE})\s*$", text[:match.start()]) or (
                len(match["count"]) == 1 and match["count"] in _DIGIT_CHARS
            ):
                continue
        value = _number(match["count"])
        if value is None:
            continue
        unit = unit_match.lastgroup if unit_match else None
        unit_source = unit_match[0] if unit_match else None
        if unit == "currency":
            unit = unit_match[0] if re.search(NON_CNY, unit_match[0], re.IGNORECASE) else "CNY"
        if any(duration.start() <= match.start() < duration.end() for duration in durations):
            reading = "DURATION"
        elif _READING_COLLOQUIAL.fullmatch(match["count"]):
            reading = "COLLOQUIAL_ELLIPSIS"
        else:
            reading = "LITERAL"
        if match["suffix"] or match["percent"]:
            unit = "tenth" if match["suffix"] == "成" else "percent"
            token = "suffix" if match["suffix"] else "percent"
            unit_source = match[token]
            unit_start = match.start(token)
        location, start = next(((part, pos) for part, pos in segments if pos <= match.start() < pos + len(part)),
                               ("", 0))
        periods = list(_PERIODS.finditer(location))
        labels = {token.lastgroup for token in periods}
        period = periods[0] if len(labels) == 1 else None
        candidate = {"kind": "quantity", "source": source, "span": _span(source, match.start()),
                     "reading": reading, "value": value, "unit": unit,
                     "unit_source": unit_source,
                     "unit_anchor": source_anchor(unit_source, unit_start, raw_sha256) if unit_source else None,
                     "period": period.lastgroup if period else None,
                     "period_anchor": source_anchor(period[0], start + period.start(), raw_sha256) if period else None,
                     "authority": "NONE"}
        if unit in {"tenth", "percent"}:
            ratio = Decimal(value).scaleb(-1 if unit == "tenth" else -2)
            candidate["ratio"] = format(ratio.normalize(), "f")
        candidates.append(candidate)
    return sorted(candidates, key=lambda item: item["span"]["start"])[:192]


def _clause_obligations(clause, content, start, subject, scope, reference, candidates, exception, guard):
    """Audit obligation signals in raw text before depending on candidate availability."""
    if _RETRACTION.search(content):
        item = occurrence(clause, start, field="constraint", subject=subject, hard=True,
                          condition=guard, reason="VERIFY_REVISION", reference=reference)
        return [{**item, "revision": "retract"}]
    if scope == "previous":
        return []
    candidate_bounds = [item for item in candidates if item["field"] in BOUND_FIELDS | {"deadline"}
                        and not item["subject"] and item["kind"] != "estimate"]
    operator = comparison(content)
    joint = is_joint(content)
    money = bool(re.search(rf"{_COST}|{_INCOME}|{PARKING}|{RENT}", content))
    night = bool(re.search(NIGHT, content))
    externally_scoped_deadline = reference and re.search(r"最晚|截止|到期", content) and re.search(
        _DEADLINE_CONTEXT, content)
    monetary_bound = money and bool(re.search(r"预算|上限|下限", content) or operator)
    hard = bool(candidate_bounds or joint and not subject or monetary_bound and not subject
                or _HARD_SIGNAL.search(content) and (not subject or reference and not night)
                or subject and content.startswith(("我", "本人")) and _HARD_SIGNAL.search(content)
                or scope == "conditional" and _CONDITIONAL_REFUSAL.search(content)
                or externally_scoped_deadline
                or not subject and operator and re.search(rf"{_ONSITE}|{_HOUR}|{_BOUND_SIGNAL.pattern}", content))
    if re.search(_PHRASE_NEGATED, content) and not candidate_bounds and not monetary_bound and not joint:
        hard = False
    field = next((item["field"] for item in candidate_bounds), None)
    if not field and joint:
        field = "rent_parking_max" if re.search(_JOINT_PAIR, content) else "joint_constraint"
    if not field and night:
        field = "night_shift_required" if subject else "night_shift_max"
    if not field and externally_scoped_deadline:
        field = "deadline"
    if not field and monetary_bound:
        base = "income" if re.search(_INCOME, content) else "cost"
        field = _BOUND_DIRECTION[base][int(not operator or operator.startswith("<"))]
    if not field and money and re.search(PARKING, content):
        field = "parking_monthly"
    if not field and money and re.search(RENT, content):
        field = "rent_monthly"
    if not field and money:
        field = "income" if re.search(_INCOME, content) else "cost"
    explicit_unknown = _MISSING_EVIDENCE.search(content)
    if not field:
        field = "constraint" if hard else "unresolved" if explicit_unknown else None
    if field is None:
        if reference and (_GOAL.search(content) or _PREF.search(content) or re.search(_DEADLINE_CONTEXT, content)):
            return [occurrence(clause, start, field="attribution", subject=subject, hard=False,
                               reason="VERIFY_SUBJECT", reference=reference)]
        return []

    reason = None
    matches = candidate_bounds
    condition = guard if scope == "conditional" else None
    if explicit_unknown and field == "parking_monthly":
        reason = "VERIFY_PARKING"
    elif reference or _OPTION_REFERENCE.search(content) and not subject or (
        subject and hard and content.startswith(("我", "本人"))
    ):
        reason = "VERIFY_SCHEDULE" if night and subject else "VERIFY_SUBJECT"
    elif explicit_unknown:
        reason = "MISSING_EVIDENCE"
    elif operator == "UNKNOWN" or hard and _UNSUPPORTED_LOGIC.search(content) and not condition:
        reason = "VERIFY_EXPRESSION"
    elif scope == "conditional" and hard:
        if exception and candidate_bounds and {c["field"] for c in candidate_bounds} <= {"onsite_max", "move_allowed"}:
            matches = [exception]
        else:
            reason = "VERIFY_CONDITION"
    elif joint and not re.search(_JOINT_PAIR, content):
        reason = "VERIFY_JOINT"
    elif money and re.search(_COUNT, content):
        reason = monetary_scope(content, monthly=joint or field in {"rent_monthly", "parking_monthly"})
    if not reason and hard and not matches:
        reason = "VERIFY_JOINT" if joint else "VERIFY_BOUND"
    if not reason and night and not any(c["field"] == field for c in candidates):
        reason = "VERIFY_SCHEDULE"
    if not hard and not reason:
        return []
    repair = None
    if hard and not subject and not condition and operator in {"<", ">", "<=", ">="} and (
        reason == "VERIFY_CURRENCY" and not re.search(NON_CNY, content, re.IGNORECASE)
        or reason == "VERIFY_PERIOD" and field == "rent_parking_max" and not re.search(NON_MONTHLY, content)
    ):
        amounts = list(re.finditer(_COUNT, content))
        if len(amounts) == 1 and (value := _number(amounts[0][0])) is not None:
            repair = {"field": field, "subject": "", "value": value, "operator": operator}
    return [occurrence(clause, start, field=field, subject=subject, hard=hard, operator=operator,
                       condition=condition, reason=reason, matches=matches, reference=reference,
                       repair=repair)]


def interpret(text: str, focus: str | None = None, *, known_options: Iterable[str] = ()) -> dict:
    """Extract exact-source candidates. The conversation layer confirms or rejects them."""
    raw_sha256 = sha256(text.encode("utf-8")).hexdigest()
    field, _, focus_subject = (focus or "").partition(":")
    focus_subject = focus_subject.strip()
    sentence_spans = list(_parts(text, _SENTENCE_ENDS))
    sentences = [sentence for sentence, _ in sentence_spans]
    options = _options([sentence for sentence in sentences if _personal_choice_scope(sentence)], field)
    option_order = tuple(dict.fromkeys((*known_options, *options)))
    aliases = _option_aliases(option_order)
    claims = []
    claim_candidates = []
    obligations = []
    relations = []
    edits = []
    references = []
    previous_seen = False
    for sentence, start in sentence_spans:
        sentence_claims = []
        raw_clauses = []
        clause_spans = list(_parts(sentence, ",，"))
        clauses = [clause for clause, _ in clause_spans]
        condition_links = dict(_condition_relations(sentence, start, clause_spans, raw_sha256))
        conditional_start = _conditional_start(clauses)
        if condition_links:
            first_guard_start = next(iter(condition_links.values()))["guard"]["span"]["start"] - start
            conditional_start = min(
                conditional_start,
                next(i for i, (clause, pos) in enumerate(clause_spans) if pos <= first_guard_start < pos + len(clause)),
            )
        relations.extend(condition_links.values())
        subject = ""
        carried_actor = None
        inferred_focus = field
        correction_pending = False
        for index, (clause, pos) in enumerate(clause_spans):
            conditional = index >= conditional_start
            if index == conditional_start:
                subject = ""
            explicit, content = _subject(clause, aliases)
            if explicit:
                subject = explicit
            elif clause.startswith(("我", "自己", "我们", "个人", "现阶段", "不过我", "但我", "预算总额", "预算上限")):
                subject = ""
            scoped = "conditional" if conditional else ""
            correction = not conditional and bool(re.search(_CORRECTION, clause))
            replacement = correction_pending and re.search(_REPLACEMENT, clause)
            if not scoped:
                if correction or (_historical(clause) and not re.search(_REVISION, clause)):
                    scoped = "previous"
                elif replacement or re.search(_REVISION, clause) or (
                    previous_seen and re.search(r"现在|目前|而今", clause)
                ):
                    scoped = "revision"
            correction_pending = correction or bool(re.search(r"^(?:更正一下|修正一下|之前说错了)$", clause))
            source = sentence if conditional or replacement or (subject and not explicit) else clause
            actual_subject = subject
            if not actual_subject and focus_subject and field in _MEASUREMENT_FIELDS and not re.search(
                r"另一|别的|新方案|其它|其他|至于", clause
            ):
                actual_subject = focus_subject
            if _REPORT_RESET.match(clause):
                carried_actor = None
            attribution = external_attribution(content)
            actor = carried_actor
            if attribution:
                actor_start = start + pos + len(clause) - len(content) + attribution.start("actor")
                actor = source_anchor(attribution["actor"], actor_start, raw_sha256)
                if attribution["cue"] in REPORTING_CUES:
                    carried_actor = actor
            reference = scope_reference(content) or (actor["source"] if actor else None)
            clause_anchor = source_anchor(clause, start + pos, raw_sha256)
            if actor:
                relations.append({"kind": "attribution", "actor": actor, "target": clause_anchor,
                                  "authority": "NONE", "applicability": "UNKNOWN"})
            if marker := _EDIT_MARKER.search(content):
                marker_pos = start + pos + len(clause) - len(content) + marker.start()
                edits.append({"operation": marker.lastgroup,
                              "marker": source_anchor(marker[0], marker_pos, raw_sha256),
                              "target": clause_anchor, "authority": "NONE",
                              "status": "UNRESOLVED_TARGET"})
            unresolved_reference = _OPTION_REFERENCE.match(content)
            if unresolved_reference and not explicit:
                actual_subject = ""
                word = unresolved_reference[0]
                candidates = list(option_order)
                if word in {"前者", "后者"} and len(option_order) == 2:
                    candidates = [option_order[0 if word == "前者" else 1]]
                ref_start = start + pos + len(clause) - len(content)
                references.append({"anchor": source_anchor(word, ref_start, raw_sha256),
                                   "possible_targets": candidates, "authority": "NONE", "outside": True})
            local = []
            if not reference and not unresolved_reference:
                if is_joint(content):
                    if joint := _joint_claim(content, actual_subject, source, scoped):
                        local.append(joint)
                    numeric = []
                else:
                    numeric = [] if re.search(PARKING, content) else _numeric_claims(
                        content, actual_subject, source, scoped, inferred_focus)
                    local.extend(numeric)
                    local.extend(_components(content, actual_subject, source, scoped))
                if numeric:
                    inferred_focus = numeric[-1]["field"]
                if move := _move_claim(content, actual_subject, source, scoped):
                    local.append(move)
                if night := _night_claim(content, actual_subject, source, scoped):
                    local.append(night)
                local.extend(_narrative(content, source, scoped, actual_subject))
            sentence_claims.extend(local)
            raw_clauses.append((clause, content, start + pos, actual_subject, scoped, reference, local, actor))
            if scoped == "previous":
                previous_seen = True
        exception = None
        guard = None
        if conditional_start < len(clauses):
            scope_text = sentence[raw_clauses[conditional_start][2] - start:]
            guard = re.split(r"[,，]|(?=我?(?:就|则|才|那么|否则))", scope_text, maxsplit=1)[0] or scope_text
            branch = [item for item in sentence_claims if item["kind"] == "conditional"]
            onsite = {item["value"] for item in branch if item["field"] == "onsite_max"}
            can_move = any(item["field"] == "move_allowed" and item["value"] == "yes" for item in branch)
            if len(onsite) == 1 and can_move and _SIMPLE_RELOCATION_EXCEPTION.fullmatch(scope_text):
                exception = _claim(
                    "conditional", "move_if_onsite_max", "", next(iter(onsite)), "days/week", scope_text,
                )
                sentence_claims.append(exception)
        for index, raw_clause in enumerate(raw_clauses):
            actor = raw_clause[-1]
            effective_guard = condition_links[index]["guard"]["source"] if index in condition_links else guard
            extracted = _clause_obligations(*raw_clause[:-1], exception, effective_guard)
            for obligation in extracted:
                if actor:
                    obligation["attribution"] = actor
                    obligation["subject"] = obligation["subject"] or actor["source"]
            obligations.extend(extracted)
            for item in raw_clause[-2]:
                claim_candidates.append(_claim_candidate(item, start if item["source"] == sentence
                                                         else raw_clause[2], effective_guard))
        if exception:
            claim_candidates.append(_claim_candidate(exception, start + sentence.index(exception["source"]), guard))
        claims.extend(sentence_claims)
    for option in options:
        if not re.fullmatch(_LABEL, option) and not scope_reference(option) and not is_joint(option):
            local = _numeric_claims(option, option, option, "", "")
            claims.extend(local)
            if local and (start := text.find(option)) >= 0:
                claim_candidates.extend(_claim_candidate(item, start) for item in local)
    if len(sentences) == 1 and not relations and not references and not scope_reference(text) and not any(
        item["field"] == field for item in claims
    ):
        focused = _focus_answer(text.strip(), field, focus_subject)
        if focused:
            claims.append(focused)
            claim_candidates.append(_claim_candidate(focused, text.index(focused["source"])))
            if focused["field"] in BOUND_FIELDS and focused["kind"] != "estimate":
                source = focused["source"]
                reason = monetary_scope(source) if field in {"cost_min", "cost_max", "income_min", "income_max"} else None
                obligations.append(occurrence(
                    source, text.index(source), field=field, subject=focus_subject,
                    hard=True, operator=comparison(source), reason=reason, matches=[focused],
                ))
    deduplicated = list({tuple(item.values()): item for item in claims}.values())[:48]
    unknowns = [item for item in obligations if item["status"] == "UNKNOWN"]
    first_critical = next((item for item in unknowns if item["hard"]), None)
    first = first_critical or next(iter(unknowns), None)
    semantic = {"version": SEMANTIC_VERSION, "coverage": "BOUNDED_RULES", "outside": True,
                "span_encoding": "unicode_code_points", "raw_sha256": raw_sha256,
                "candidates": _lexical_candidates(text, raw_sha256),
                "claim_candidates": claim_candidates[:96],
                "relations": relations[:96], "edits": edits[:96], "references": references[:96],
                "obligations": [item for item in obligations if item["hard"]], "unknowns": unknowns,
                "clarification": CLARIFICATIONS[first["reason"]] if first else None}
    intent = "比较" + "与".join(f"「{option}」" for option in options) if len(options) >= 2 else text.strip()
    return {"domain": _domain(text), "intent": intent[:400], "options": options,
            "claims": deduplicated, "semantic": semantic}
