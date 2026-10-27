#!/usr/bin/env python3
"""Standard library only. Synthetic SQLite replay of fixed upstream memory SQL predicates."""
import sqlite3
N = 0
def ok(v, label):
    global N
    assert v, label
    N += 1
def dbnew():
    d = sqlite3.connect(":memory:")
    d.execute("PRAGMA foreign_keys=ON")
    d.executescript("""
    CREATE TABLE decisions(id TEXT PRIMARY KEY, updated_at INTEGER NOT NULL);
    CREATE TABLE memory_items(id TEXT PRIMARY KEY, state TEXT NOT NULL, user_authored INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE memory_sources(id TEXT PRIMARY KEY, item_id TEXT NOT NULL REFERENCES memory_items(id) ON DELETE CASCADE,
      decision_id TEXT REFERENCES decisions(id) ON DELETE CASCADE, revision INTEGER NOT NULL);
    INSERT INTO decisions VALUES ('A',1),('B',1);
    INSERT INTO memory_items VALUES ('M','approved',0);
    INSERT INTO memory_sources VALUES ('A','M','A',1),('B','M','B',1);
    """)
    return d
def state(d):
    r = d.execute("SELECT state FROM memory_items WHERE id='M'").fetchone()
    return r[0] if r else None
def valid(d):
    return d.execute("""SELECT COUNT(*) FROM memory_sources s JOIN decisions d ON d.id=s.decision_id
      WHERE s.item_id='M' AND s.revision=d.updated_at""").fetchone()[0]
def edit(d, did):
    d.execute("UPDATE decisions SET updated_at=2 WHERE id=?", (did,))
    rows = d.execute("""SELECT DISTINCT i.id FROM memory_items i JOIN memory_sources s ON s.item_id=i.id
      WHERE s.decision_id=? AND s.revision<2 AND i.user_authored=0""", (did,)).fetchall()
    for (iid,) in rows:
        other = d.execute("""SELECT 1 FROM memory_sources WHERE item_id=?
          AND NOT (decision_id=? AND revision<2) LIMIT 1""", (iid,did)).fetchone()
        if not other: d.execute("UPDATE memory_items SET state='stale' WHERE id=?", (iid,))
    return len(rows)
def delete(d, did):
    d.execute("DELETE FROM decisions WHERE id=?", (did,))
    d.execute("""DELETE FROM memory_items WHERE user_authored=0
      AND id NOT IN (SELECT item_id FROM memory_sources)""")
def main():
    for first,second in (("A","B"),("B","A")):
        d=dbnew()
        ok(state(d)=="approved", "initial approved")
        ok(valid(d)==2, "two current sources")
        ok(edit(d,first)==1, "edit invalidation checked")
        ok(state(d)=="approved", "other source retained")
        ok(valid(d)==1, "one current source")
        delete(d,second)
        ok(d.execute("SELECT COUNT(*) FROM memory_sources").fetchone()[0]==1, "cascade")
        ok(valid(d)==0, "all support expired")
        ok(state(d)=="approved", "stale approved remains")
        ok(d.execute("SELECT COUNT(*) FROM memory_items WHERE state='approved'").fetchone()[0]==1, "chat candidate")
        delete(d,first)
        ok(state(d) is None, "fully pruned")
        d.close()
    d=dbnew();delete(d,"A")
    ok(state(d)=="approved", "control live approval")
    ok(valid(d)==1, "control live source")
    d.close()
    d=dbnew();delete(d,"B")
    ok(edit(d,"A")==1, "single edit checked")
    ok(state(d)=="stale", "single source stale")
    ok(valid(d)==0, "single source no current")
    d.close()
    print(f"MKT087 checks={N} PASS={N} FAIL=0")
if __name__=="__main__": main()
