import re
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

_HEDGE = r"可能|大概|大约|估计|大致|大抵|左右|上下|也许|听说|好像|不知道|不确定|未核实|尚未确认|未必|未定|暂不清楚|我猜|看起来|是否"
_ONSITE = r"到岗|到办公室|去办公室|来办公室|坐班|驻场|到公司|去公司|到现场|去现场|线下办公|到单位|去单位|现场上班|线下上班|到店|去门店"
_MOVE = r"搬家|搬迁|异地搬迁|跨城搬迁|搬到|搬去|迁居|迁往|搬(?=\s*$)"
_COST = (
    r"总预算|预算|总价|总费用|费用|花费|花销|花掉|支出|开支|花\s*(?=[零〇\d一二两三四五六七八九十百千万亿])|"
    r"成本|学费|报名费|租金|房租|月租|价格|价钱|支付|动用|收费|报价|维修费"
)
_INCOME = (
    r"每月(?:的)?(?:税后)?(?:收入|工资|薪资|到手)|月薪|月收入|月工资|每个月(?:收入|工资|到手)|月到手|月税后|一月到手|"
    r"(?:收入|工资|薪资)(?:是|为|按|大概|大约|税后|到手|估计|\s)*(?:每月|每个月|一月|每个自然月)"
)
_HOUR = r"(?:个\s*)?(?:小时|钟头)|时(?!间|候)"


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


