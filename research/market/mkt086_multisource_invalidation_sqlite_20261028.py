#!/usr/bin/env python3
"""SQLite reproduction of fixed Decision Journal store.ts source predicates.
Synthetic data only. Standard library only. No network or paid API.
"""
import sqlite3

AFFECTED = """SELECT DISTINCT i.id AS id FROM memory_items i
JOIN memory_sources s ON s.item_id = i.id
WHERE s.decision_id = ? AND s.revision < ? AND i.user_authored = 0"""
OTHER = """SELECT 1 FROM memory_sources
WHERE item_id = ? AND NOT (decision_id = ? AND revision < ?) LIMIT 1"""
DEDUP = "SELECT 1 FROM memory_sources WHERE item_id = ? AND decision_id = ? LIMIT 1"
checks = 0

def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)

def setup(sources, user_authored=0):
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE memory_items(id TEXT PRIMARY KEY, state TEXT, user_authored INTEGER)")
    db.execute("CREATE TABLE memory_sources(item_id TEXT, decision_id TEXT, revision INTEGER)")
    db.execute("INSERT INTO memory_items VALUES ('M','approved',?)", (user_authored,))
    db.executemany("INSERT INTO memory_sources VALUES ('M',?,?)", sources)
    return db

def invalidate(db, decision, new_revision):
    ids = [row[0] for row in db.execute(AFFECTED, (decision, new_revision))]
    for item_id in ids:
        if db.execute(OTHER, (item_id, decision, new_revision)).fetchone():
            continue
        db.execute("UPDATE memory_items SET state='stale' WHERE id=?", (item_id,))
    return len(ids)

def state(db):
    return db.execute("SELECT state FROM memory_items WHERE id='M'").fetchone()[0]

def current_count(db, revisions):
    return sum(1 for decision, revision in db.execute(
        "SELECT decision_id,revision FROM memory_sources"
    ) if revisions.get(decision) == revision)

db = setup([("A",1)])
check(invalidate(db,"A",2)==1,"single source affected")
check(state(db)=="stale","single source invalidated")
check(current_count(db,{"A":2})==0,"single source no current support")
db.close()

db = setup([("A",1),("B",1)])
check(invalidate(db,"A",2)==1,"A edited")
check(state(db)=="approved","B remains valid")
check(current_count(db,{"A":2,"B":1})==1,"one current support")
check(invalidate(db,"B",2)==1,"B edited")
check(current_count(db,{"A":2,"B":2})==0,"all support obsolete")
check(state(db)=="approved","approved remains with no current support")
check(db.execute(DEDUP,("M","A")).fetchone() is not None,"A old source blocks reinsertion")
check(db.execute(DEDUP,("M","B")).fetchone() is not None,"B old source blocks reinsertion")
db.close()

db = setup([("A",1),("B",1)])
check(invalidate(db,"B",2)==1,"B edited first")
check(invalidate(db,"A",2)==1,"A edited second")
check(state(db)=="approved","reverse order also retains approved")
check(current_count(db,{"A":2,"B":2})==0,"reverse order no support")
db.close()

db = setup([("A",1)],user_authored=1)
check(invalidate(db,"A",2)==0,"user authored excluded")
check(state(db)=="approved","user authored remains approved")
db.close()

print("MKT086_SQLITE_SOURCE_PREDICATE_CHECKS=%d; FAILURES=0" % checks)
print("CONDITIONAL_COUNTEREXAMPLE=two old source revisions; approved remains")
