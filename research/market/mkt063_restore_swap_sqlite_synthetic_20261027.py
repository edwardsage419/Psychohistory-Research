"""Synthetic SQLite experiment corresponding to upstream restore(swap=True) DDL.
No upstream package imported; all inputs artificial and in memory.
"""
import sqlite3
import json

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT, qty INTEGER)')
conn.execute('CREATE TABLE _history_json_items(id INTEGER PRIMARY KEY, operation TEXT, pk_id INTEGER, updated_values TEXT)')

# Triggers model the upstream change capture, keeping the SQL DDL swap path identical.
triggers = {
    'insert': "CREATE TRIGGER _history_json_items_insert AFTER INSERT ON items BEGIN INSERT INTO _history_json_items(operation,pk_id,updated_values) VALUES ('insert',NEW.id,json_object('name',NEW.name,'qty',NEW.qty)); END",
    'update': "CREATE TRIGGER _history_json_items_update AFTER UPDATE ON items BEGIN INSERT INTO _history_json_items(operation,pk_id,updated_values) VALUES ('update',NEW.id,json_patch(CASE WHEN OLD.name IS NOT NEW.name THEN json_object('name',NEW.name) ELSE '{}' END,CASE WHEN OLD.qty IS NOT NEW.qty THEN json_object('qty',NEW.qty) ELSE '{}' END)); END",
    'delete': "CREATE TRIGGER _history_json_items_delete AFTER DELETE ON items BEGIN INSERT INTO _history_json_items(operation,pk_id,updated_values) VALUES ('delete',OLD.id,NULL); END"
}
for ddl in triggers.values():conn.execute(ddl)
checks=[]
def check(label, condition):
    checks.append((label,bool(condition)))
def active_triggers():
    return conn.execute("SELECT name,tbl_name FROM sqlite_master WHERE type='trigger' AND name LIKE '_history_json_items_%' ORDER BY name").fetchall()
def audit():
    return conn.execute('SELECT id,operation,pk_id,updated_values FROM _history_json_items ORDER BY id').fetchall()
def rows():
    return conn.execute('SELECT id,name,qty FROM items ORDER BY id').fetchall()
def replay():
    state={}
    for _id,op,pk,js in audit():
        if op=='delete':state.pop(pk,None)
        elif op=='insert':state[pk]=json.loads(js)
        elif op=='update':state[pk].update(json.loads(js))
    return sorted((k,v['name'],v['qty']) for k,v in state.items())

check('initial three triggers',len(active_triggers())==3)
conn.execute("INSERT INTO items VALUES (1,'A',1)")
conn.execute("UPDATE items SET name='B' WHERE id=1")
check('pre-swap two events',len(audit())==2)
check('pre-swap replay matches live',replay()==rows())

# Directly reproduce upstream core.py lines 568-573 after replay into temp table.
conn.execute('CREATE TABLE [_tmp_restore_items](id INTEGER PRIMARY KEY,name TEXT,qty INTEGER)')
conn.execute("INSERT INTO [_tmp_restore_items] VALUES (1,'A',1)")
conn.execute('DROP TABLE IF EXISTS [_tmp_old_items]')
conn.execute('ALTER TABLE [items] RENAME TO [_tmp_old_items]')
check('rename binds triggers to old table',all(t[1]=='_tmp_old_items' for t in active_triggers()))
conn.execute('ALTER TABLE [_tmp_restore_items] RENAME TO [items]')
check('new table contains restored value',rows()==[(1,'A',1)])
conn.execute('DROP TABLE [_tmp_old_items]')
check('post-swap no audit triggers',len(active_triggers())==0)
check('audit rows remain',len(audit())==2)
conn.execute("UPDATE items SET name='C' WHERE id=1")
check('post-swap update succeeds',rows()==[(1,'C',1)])
check('post-swap update unlogged',len(audit())==2)
check('replay differs after swap',replay()!=rows())

# Re-enable tracking without fresh baseline, as upstream enable_tracking does when history nonempty.
for ddl in triggers.values():conn.execute(ddl)
check('re-enable restores three triggers',len(active_triggers())==3)
conn.execute('UPDATE items SET qty=9 WHERE id=1')
check('later update recorded',len(audit())==3)
check('current state after later update',rows()==[(1,'C',9)])
check('replay after later update still stale',replay()==[(1,'B',9)] and replay()!=rows())
check('no provenance marker for restore',not any(e[1]=='restore' for e in audit()))

# Control: a separate non-swap restore table leaves source triggers intact.
c2=sqlite3.connect(':memory:')
c2.execute('CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT, qty INTEGER)')
c2.execute('CREATE TABLE _history_json_items(id INTEGER PRIMARY KEY, operation TEXT, pk_id INTEGER, updated_values TEXT)')
for ddl in triggers.values(): c2.execute(ddl)
c2.execute("INSERT INTO items VALUES (1,'A',1)")
c2.execute('CREATE TABLE items_restored(id INTEGER PRIMARY KEY,name TEXT,qty INTEGER)')
c2.execute("INSERT INTO items_restored VALUES (1,'A',1)")
check('non-swap control keeps source triggers',c2.execute("SELECT count(*) FROM sqlite_master WHERE type='trigger' AND tbl_name='items'").fetchone()[0]==3)
check('non-swap control creates separate table',c2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items_restored'").fetchone() is not None)
c2.execute("UPDATE items SET name='B' WHERE id=1")
check('non-swap control captures later update',c2.execute('SELECT count(*) FROM _history_json_items').fetchone()[0]==2)
check('non-swap control retains original live table',c2.execute('SELECT name FROM items WHERE id=1').fetchone()[0]=='B')
result={'sqlite_version':sqlite3.sqlite_version,'total_checks':len(checks),'passed':sum(v for _,v in checks),'failed':[k for k,v in checks if not v],'live':rows(),'replayed':replay(),'triggers':active_triggers()}
print(json.dumps(result,ensure_ascii=False,indent=2))
assert not result['failed'], result['failed']
