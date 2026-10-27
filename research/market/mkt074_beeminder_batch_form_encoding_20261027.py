#!/usr/bin/env python3
"""Offline Beeminder batch form serialization check. No network or credentials.
Requires open-source requests, tested with requests 2.32.5.
"""
import json
from urllib.parse import parse_qs
import requests

checks = 0
def check(condition, description):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(description)

points = [{"value": 1}, {"value": 2, "comment": "two"}]
url = "https://example.invalid/api/v1/users/demo/goals/demo/datapoints/create_all.json"
# The pinned client's _post() uses requests.post(..., data=data).
# Its create_multiple_datapoints() passes a raw list of dicts as data["datapoints"].
bad = requests.Request("POST", url, data={"datapoints": points, "auth_token": "FAKE"}).prepare()
check(bad.method == "POST", "method")
check(bad.headers["Content-Type"] == "application/x-www-form-urlencoded", "form type")
check(isinstance(bad.body, str), "form body type")
bad_parsed = parse_qs(bad.body)
check(bad_parsed["auth_token"] == ["FAKE"], "fake token")
check(bad_parsed["datapoints"] == ["value", "value", "comment"], "dict keys leaked")
check(bad.body.count("datapoints=") == 3, "three repeated form keys")
check("%7B" not in bad.body, "no JSON object serialization")
check("1" not in bad_parsed["datapoints"], "numeric values lost")
check("two" not in bad_parsed["datapoints"], "comment value lost")
check(bad_parsed["datapoints"] != [json.dumps(points)], "not JSON")
good = requests.Request("POST", url, data={"datapoints": json.dumps(points), "auth_token": "FAKE"}).prepare()
good_parsed = parse_qs(good.body)
check(good.method == "POST", "good method")
check(good.headers["Content-Type"] == "application/x-www-form-urlencoded", "good form type")
check(len(good_parsed["datapoints"]) == 1, "single JSON field")
check(json.loads(good_parsed["datapoints"][0]) == points, "JSON roundtrip")
check(good_parsed["auth_token"] == ["FAKE"], "good token")
check(good.body != bad.body, "different wire representations")
check("%7B" in good.body, "encoded JSON braces")
check("%22value%22" in good.body, "encoded JSON key")
check("two" in good.body, "comment preserved")
check(good_parsed["datapoints"][0].startswith("["), "JSON array starts")
single = requests.Request("POST", url, data={"value": 1, "comment": "two"}).prepare()
single_parsed = parse_qs(single.body)
check(single_parsed["value"] == ["1"], "single numeric value")
check(single_parsed["comment"] == ["two"], "single comment")
check("datapoints" not in single_parsed, "single has no batch field")
check(len(single_parsed) == 2, "single two fields")
print(json.dumps({"assertions": checks, "failures": 0, "requests_version": requests.__version__,
                  "actual_batch_form_body": bad.body, "json_string_batch_form_body": good.body}))
