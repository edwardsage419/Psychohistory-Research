#!/usr/bin/env python3
"""Offline CSV export regression for SifisoScS decision-journal fixed app.py."""
import csv
import hashlib
import io
import json
import re
import sqlite3
import sys
EXPECTED_BLOB="ffb9141344344f15ef044ca3b57b4ffa9fdee1c5"
DECISIONS_CSV_QUERY="""SELECT d.id, d.title, d.timestamp, d.confidence, GROUP_CONCAT(t.name) as tags
FROM decisions d LEFT JOIN decision_tags dt ON d.id = dt.decision_id
LEFT JOIN tags t ON dt.tag_id = t.tag_id GROUP BY d.id"""
FULL_JSON_QUERY="""SELECT d.*, GROUP_CONCAT(t.name) as tags
FROM decisions d LEFT JOIN decision_tags dt ON d.id = dt.decision_id
LEFT JOIN tags t ON dt.tag_id = t.tag_id GROUP BY d.id"""
def main():
    checks=0
    def check(ok,reason):
        nonlocal checks
        checks+=1
        if not ok: raise AssertionError(reason)
    if len(sys.argv)>1:
        source=open(sys.argv[1],encoding="utf-8").read()
        raw=source.encode("utf-8")
        blob=hashlib.sha1(("blob %d\0"%len(raw)).encode()+raw).hexdigest()
        check(blob==EXPECTED_BLOB,"Git blob mismatch")
        patterns=[r"SELECT d\.id, d\.title, d\.timestamp, d\.confidence, GROUP_CONCAT\(t\.name\) as tags",
                  r"SELECT d\.\*, GROUP_CONCAT\(t\.name\) as tags",
                  r"SELECT \* FROM reflections",r"Download Decisions CSV",
                  r"Download Full Journal \(JSON\)"]
        for pattern in patterns: check(re.search(pattern,source) is not None,"Missing source pattern "+pattern)
        check(re.search(r"\bUPDATE\s+decisions\b",source,re.I) is None,"Unexpected decision update")
    db=sqlite3.connect(":memory:")
    db.executescript("""
CREATE TABLE decisions(id INTEGER PRIMARY KEY,title TEXT,context TEXT,timestamp TEXT,confidence INTEGER);
CREATE TABLE tags(tag_id INTEGER PRIMARY KEY,name TEXT);
CREATE TABLE decision_tags(decision_id INTEGER,tag_id INTEGER);
CREATE TABLE reflections(id INTEGER PRIMARY KEY,decision_id INTEGER,thought_now TEXT,difference TEXT,timestamp TEXT);
INSERT INTO decisions VALUES(1,'Career change','Private original reasoning: option A rejected','2026-10-28',7);
INSERT INTO tags VALUES(1,'Career');
INSERT INTO decision_tags VALUES(1,1);
INSERT INTO reflections VALUES(1,1,'Reconsidered assumptions','More data needed','2026-11-28');
""")
    def rows(query):
        cur=db.execute(query)
        return [dict(zip([x[0] for x in cur.description],row)) for row in cur.fetchall()]
    csv_records=rows(DECISIONS_CSV_QUERY)
    json_records=rows(FULL_JSON_QUERY)
    reflection_records=rows("SELECT * FROM reflections")
    check(len(csv_records)==1,"CSV count")
    check(len(json_records)==1,"JSON count")
    check(len(reflection_records)==1,"reflection count")
    check("context" not in csv_records[0],"CSV context unexpectedly present")
    check("context" in json_records[0],"JSON context missing")
    check("Private original reasoning" in json_records[0]["context"],"JSON reasoning")
    check("context" not in reflection_records[0],"Reflection context")
    check(csv_records[0]["confidence"]==7,"Confidence")
    check(csv_records[0]["tags"]=="Career","Tag")
    buf=io.StringIO()
    writer=csv.DictWriter(buf,fieldnames=csv_records[0].keys())
    writer.writeheader()
    writer.writerows(csv_records)
    check("Private original reasoning" not in buf.getvalue(),"CSV original reasoning")
    check("Private original reasoning" in json.dumps({"decisions":json_records,"reflections":reflection_records}),"JSON reasoning lost")
    print(json.dumps({"status":"PASS","checks":checks,"failures":0,"csv_columns":list(csv_records[0]),"csv_has_context":False,"json_has_context":True}))
if __name__=="__main__": main()
