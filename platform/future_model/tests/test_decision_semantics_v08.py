from psychohistory.decision_language import interpret


def anchored(text, anchor):
    start, end = anchor["span"]["start"], anchor["span"]["end"]
    assert text[start:end] == anchor["source"]


def test_condition_chain_and_its_complement_share_the_original_guard():
    text = "🧭 如果培训到账，而且每周工时少于40小时，那么我必须接受。"
    semantic = interpret(text)["semantic"]
    [relation] = semantic["relations"]
    assert relation["kind"] == "condition"
    assert relation["guard"]["source"] == "如果培训到账，而且每周工时少于40小时"
    assert relation["target"]["source"] == "那么我必须接受"
    assert relation["authority"] == "NONE"
    anchored(text, relation["guard"])
    anchored(text, relation["target"])

    text = "如果报名延期，我就不签，否则我必须答复。"
    branches = interpret(text)["semantic"]["relations"]
    assert [branch["polarity"] for branch in branches] == ["when_true", "when_false"]
    assert branches[0]["guard"]["id"] == branches[1]["guard"]["id"]
    assert {row["condition"] for row in interpret(text)["semantic"]["obligations"]} == {"如果报名延期"}


def test_report_carries_a_distinct_actor_across_commas_until_self_assertion():
    text = "🧭 同事说：下周再确认，预算最多5000元，但我自己的预算最多3000元。"
    result = interpret(text)
    assert [item["value"] for item in result["claims"] if item["field"] == "cost_max"] == ["3000"]
    semantic = result["semantic"]
    report = next(item for item in semantic["obligations"] if item["source"] == "预算最多5000元")
    assert report["subject"] == "同事"
    assert report["reason"] == "VERIFY_SUBJECT"
    [link] = [item for item in semantic["relations"] if item["target"]["source"] == report["source"]]
    assert link["actor"]["source"] == "同事"
    anchored(text, link["actor"])


def test_punctuation_inside_report_quote_cannot_release_report_scope():
    text = "同事说：“可以等一等。预算最多5000元。” 我自己的预算最多3000元。"
    result = interpret(text)
    assert [item["value"] for item in result["claims"] if item["field"] == "cost_max"] == ["3000"]


def test_unicode_raw_source_and_revision_candidates_are_presentation_only():
    text = "🧭 e\u0301 先撤回上一条底线。"
    result = interpret(text)
    semantic = result["semantic"]
    assert semantic["outside"] is True
    assert semantic["raw_sha256"] != interpret("🧭 é 先撤回上一条底线。")["semantic"]["raw_sha256"]
    [edit] = semantic["edits"]
    assert edit["operation"] == "retract"
    assert edit["marker"]["source"] == "撤回"
    assert edit["authority"] == "NONE"
    anchored(text, edit["marker"])
    assert not result["claims"]


def test_lexical_cadence_and_currency_use_separate_anchored_tokens():
    text = "每年收1000美元，另外每次花50元。"
    items = interpret(text)["semantic"]["candidates"]
    assert [(item["value"], item["unit"], item["period"]) for item in items] == [
        ("1000", "美元", "year"), ("50", "CNY", "event"),
    ]
    for item in items:
        anchored(text, item["unit_anchor"])
        anchored(text, item["period_anchor"])


def test_cross_turn_reference_does_not_infer_a_personal_bound():
    options = ("项目甲", "项目乙")
    text = "后者的预算最多五百元。"
    result = interpret(text, known_options=options)
    [reference] = result["semantic"]["references"]
    assert reference["anchor"]["source"] == "后者"
    assert reference["possible_targets"] == ["项目乙"]
    assert reference["authority"] == "NONE"
    assert not result["claims"]
    assert result["semantic"]["obligations"][0]["reason"] == "VERIFY_SUBJECT"


def test_other_persons_reported_choices_do_not_populate_personal_option_list():
    other = "同事说她在犹豫是换工作还是继续留任。"
    assert not interpret(other)["options"]
    personal = "我在犹豫是换工作还是继续留任。"
    assert interpret(personal)["options"] == ["换工作", "继续留任"]


def test_report_does_not_supply_personal_goal_via_focus_fallback():
    assert not interpret("主管表示想提高薪资", focus="goal")["claims"]


def test_consequent_coordination_preserves_guard_anchors():
    text = "如果到账，我就报名，并且我必须回信。"
    relations = interpret(text)["semantic"]["relations"]
    assert [row["target"]["source"] for row in relations] == ["我就报名", "并且我必须回信"]
    assert {row["guard"]["source"] for row in relations} == {"如果到账"}


def test_first_person_inside_report_has_no_personal_authority():
    text = "房东说，我的预算最多2000元。"
    assert not interpret(text)["claims"]


def test_ratio_unit_anchor_matches_prefix_or_suffix():
    text = "费用高出百分之二十，另一个估计是30%。"
    candidates = [item for item in interpret(text)["semantic"]["candidates"] if "ratio" in item]
    assert [(item["ratio"], item["unit_anchor"]["source"]) for item in candidates] == [
        ("0.2", "百分之"), ("0.3", "%"),
    ]
    for item in candidates:
        anchored(text, item["unit_anchor"])
