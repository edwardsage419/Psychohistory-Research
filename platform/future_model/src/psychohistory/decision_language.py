"""Bounded Chinese-language extraction for user-reviewable decision proposals."""

import re
import unicodedata
from collections.abc import Iterable
from decimal import Decimal


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
_SENTENCES = re.compile(r"[^。！？!?；;\n]+")
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
_CONDITION = r"(?:^|[，,]|若是|只要|先看)(?:\s*我?\s*)?(?:如果|如果说|假如|假设|除非|若|只要|一旦|万一|要是)"
_CONDITION_PREFIX = r"^(?:如果说|如果|假如|假设|除非|若是|若|只要|一旦|万一|要是|否则|那么|但是|但)"
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
_NON_CNY = r"美元|美金|港元|港币|港幣|台币|台幣|新台币|新台幣|日元|日圆|欧元|歐元|英镑|英鎊|澳元|新币|新幣|加元|\b(?:USD|AUD|HKD|SGD|CAD|EUR|GBP|JPY|TWD)\b|[$€£]"
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
}
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


def _clauses(sentence: str) -> list[str]:
    """Keep grouping commas inside Arabic numerals and preserve original spans."""
    parts = []
    start = 0
    for match in re.finditer(r"[,，]", sentence):
        pos = match.start()
        if pos and sentence[pos - 1].isdigit() and re.match(r"[0-9０-９]{3}(?![0-9０-９])", sentence[pos + 1:]):
            continue
        parts.append(sentence[start:pos].strip())
        start = match.end()
    parts.append(sentence[start:].strip())
    return [part for part in parts if part]


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
        if labeled and _looks_labeled(labeled["label"]) and (
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
    if labeled and _looks_labeled(labeled["label"]):
        name = labeled["label"]
        return aliases.get(name, name), clause[labeled.end():]
    for name in sorted(aliases, key=lambda item: (-len(item), item)):
        if clause.startswith(name) and len(clause) > len(name):
            return aliases[name], clause[len(name):].lstrip()
    match = re.match(rf"(?P<label>{_LABEL})(?=\s*(?:的)?(?:{_ONSITE}|{_MOVE}|{_COST}|{_INCOME}|"
                     rf"{_WEEK}|{_HOUR}|{_CNY_PERIOD}|不|没|无|是|需要|要求|只|必须|可能|得|要|需))", clause)
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
            unit_matches.append(("onsite", "onsite_max", "days/week", _DAY, True, _ONSITE))
    if re.search(_HOUR, clause) and (weekly or focus in {"hours", "hours_max"}):
        unit_matches.append(("hours", "hours_max", "hours/week", _HOUR, True, _HOUR))
    currency_allowed = not re.search(_NON_CNY, clause, flags=re.IGNORECASE)
    if currency_allowed and re.search(_INCOME, clause):
        unit_matches.append(("income", "income_min", "yuan/month", r"(?:元|块钱?)?", False, _INCOME))
    if currency_allowed and re.search(_COST, clause):
        unit = "yuan/month" if re.search(_CNY_PERIOD, clause) else "yuan"
        if unit == "yuan/month" or not re.search(rf"{_WEEK}|每年|每季|按年|[/／]\s*年", clause):
            unit_matches.append(("cost", "cost_max", unit, r"(?:元|块钱?)?", True, _COST))
    elif currency_allowed and re.match(r"^(?:房源|房子|公寓)", subject) and re.search(_CNY_PERIOD, clause):
        unit_matches.append(("cost", "cost_max", "yuan/month", r"(?:元|块钱?)", True, _CNY_PERIOD))
    elif currency_allowed and subject and re.fullmatch(rf"(?:只)?(?:要|收)\s*{_COUNT}\s*(?:元|块钱?)", clause):
        unit_matches.append(("cost", "cost_max", "yuan", r"(?:元|块钱?)", True, ""))

    if context == "revision" and not unit_matches and focus in _UNITS and currency_allowed:
        base = {"onsite_max": "onsite", "hours_max": "hours", "cost_max": "cost", "income_min": "income"}.get(focus, focus)
        suffix = {"onsite": _DAY, "hours": _HOUR}.get(base, r"(?:元|块钱?)?")
        unit_matches.append((base, focus, _UNITS[focus], suffix, base != "income", ""))

    result = []
    for base, hard, unit, suffix, upward, metric in unit_matches:
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
        upper = re.search(_UPPER, clause)
        lower = re.search(_LOWER, clause)
        upper_strict = not lower and bool(re.search(_UPPER_STRICT, clause))
        lower_strict = not upper and bool(re.search(_LOWER_STRICT, clause))
        if (upward and (lower or lower_strict)) or (not upward and (upper or upper_strict)):
            continue
        strict = upper_strict if upward else lower_strict
        hard_phrase = upper if upward else lower
        budget = base == "cost" and bool(re.search(r"预算", clause))
        condition_limit = conditional_onsite and bool(re.search(r"只(?:需要|需|要|用)", clause))
        revision_limit = context == "revision" and focus == hard and focus not in _MEASUREMENT_FIELDS
        known_limit = bool(hard_phrase or strict or budget or condition_limit or revision_limit)
        field = hard if known_limit and not subject else base
        if known_limit and subject:
            # The observed cap on a particular option is not a point measurement.
            if context != "conditional":
                kind = "estimate"
            else:
                kind = context
        else:
            kind = _qualify(clause, "constraint" if field == hard else "measurement", context, strict and not hard_phrase)
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


def _narrative(clause: str, source: str, context: str) -> list[dict[str, str]]:
    result = []
    for field, pattern in (("goal", _GOAL), ("preference", _PREF)):
        if match := pattern.search(clause):
            value = match["value"].strip()
            if field == "preference" and match[0].startswith(("不喜欢", "不想", "我不喜欢", "我不想")):
                value = match[0].strip()
            if not (field == "preference" and re.match(r"(?:权重|百分之)", value)):
                result.append(_claim(context or field, field, "", value, "", source))
    if match := _OPEN_DEADLINE.search(clause):
        result.append(_claim(context or "deadline", "deadline", "", "无固定期限", "", source))
    elif re.search(_DEADLINE_CONTEXT, clause) and (match := _DEADLINE.search(clause)):
        strict_date = re.search(r"最晚|必须|要求|截止|到期|要在", clause)
        hoped_for = re.search(r"希望|想要|最好|理想(?:是|为)|争取", clause)
        if strict_date or (match["edge"] and not hoped_for):
            result.append(_claim(_qualify(clause, "deadline", context), "deadline", "", match[0].strip(), "", source))
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


def interpret(text: str, focus: str | None = None, *, known_options: Iterable[str] = ()) -> dict:
    """Extract exact-source candidates. The conversation layer confirms or rejects them."""
    text = text.strip()
    field, _, focus_subject = (focus or "").partition(":")
    focus_subject = focus_subject.strip()
    sentences = [match[0].strip() for match in _SENTENCES.finditer(text) if match[0].strip()]
    options = _options(sentences, field)
    aliases = _option_aliases((*known_options, *options))
    claims = []
    previous_seen = False
    for sentence in sentences:
        sentence_claims = []
        clauses = _clauses(sentence)
        conditional_start = _conditional_start(clauses)
        subject = ""
        inferred_focus = field
        correction_pending = False
        for index, clause in enumerate(clauses):
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
            numeric = _numeric_claims(content, actual_subject, source, scoped, inferred_focus)
            sentence_claims.extend(numeric)
            if numeric:
                inferred_focus = numeric[-1]["field"]
            if move := _move_claim(content, actual_subject, source, scoped):
                sentence_claims.append(move)
            sentence_claims.extend(_narrative(content, source, scoped))
            if scoped == "previous":
                previous_seen = True
        if conditional_start < len(clauses):
            scope_text = sentence[sentence.index(clauses[conditional_start]):]
            branch = [item for item in sentence_claims if item["kind"] == "conditional"]
            onsite = {item["value"] for item in branch if item["field"] == "onsite_max"}
            can_move = any(item["field"] == "move_allowed" and item["value"] == "yes" for item in branch)
            sufficient = re.search(r"只要|那么|则|就", scope_text) and not re.search(
                r"除非|才(?:能|可以)|同时|而且|并且|还要|还需|以及|且", scope_text,
            )
            inclusive = re.search(_UPPER, scope_text) and not re.search(rf"{_UPPER_STRICT}|{_HEDGE}", scope_text)
            if len(onsite) == 1 and can_move and sufficient and inclusive:
                sentence_claims.append(_claim(
                    "conditional", "move_if_onsite_max", "", next(iter(onsite)), "days/week", scope_text,
                ))
        claims.extend(sentence_claims)
    for option in options:
        if not re.fullmatch(_LABEL, option):
            claims.extend(_numeric_claims(option, option, option, "", ""))
    if len(sentences) == 1 and not any(item["field"] == field for item in claims):
        focused = _focus_answer(text, field, focus_subject)
        if focused:
            claims.append(focused)
    deduplicated = list({tuple(item.values()): item for item in claims}.values())[:48]
    intent = "比较" + "与".join(f"「{option}」" for option in options) if len(options) >= 2 else text
    return {"domain": _domain(text), "intent": intent[:400], "options": options, "claims": deduplicated}
