#!/usr/bin/env python3
"""MKT092 offline structural reproduction. Python standard library only.
The SQLite DDL is a bounded transcription of DecisionOS migration FK rules,
not a live Next.js/PostgreSQL execution.
Upstream commit af288e9f1e6c6c097e3eccd30f3b97a85ac22a69.
"""
import sqlite3
checks=0
def check(v,label):
    global checks
    checks+=1
    if not v: raise AssertionError(label)
c=sqlite3.connect(':memory:')
c.execute('PRAGMA foreign_keys=ON')
c.executescript("""
CREATE TABLE user(id TEXT PRIMARY KEY,email TEXT NOT NULL);
CREATE TABLE workspace(id TEXT PRIMARY KEY);
CREATE TABLE membership(user_id TEXT NOT NULL,workspace_id TEXT NOT NULL,role TEXT NOT NULL,
 FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
 FOREIGN KEY(workspace_id) REFERENCES workspace(id) ON DELETE CASCADE);
CREATE TABLE decision(id TEXT PRIMARY KEY,workspace_id TEXT NOT NULL,creator_id TEXT NOT NULL,
 FOREIGN KEY(workspace_id) REFERENCES workspace(id) ON DELETE CASCADE,
 FOREIGN KEY(creator_id) REFERENCES user(id) ON DELETE RESTRICT);
CREATE TABLE note(id TEXT PRIMARY KEY,author_id TEXT NOT NULL,
 FOREIGN KEY(author_id) REFERENCES user(id) ON DELETE RESTRICT);
CREATE TABLE audit_log(id TEXT PRIMARY KEY,actor_user_id TEXT,actor_email TEXT);
""")
for uid in ('author','coadmin','commenter'):
    c.execute('INSERT INTO user VALUES (?,?)',(uid,uid+'@example.invalid'))
c.execute("INSERT INTO workspace VALUES ('w')")
for uid in ('author','coadmin','commenter'):
    c.execute("INSERT INTO membership VALUES (?,'w',?)",(uid,'admin' if uid!='commenter' else 'member'))
check(c.execute('PRAGMA foreign_keys').fetchone()[0]==1,'FK enabled')
check(c.execute("SELECT COUNT(*) FROM membership WHERE role='admin'").fetchone()[0]==2,'two admins')
c.execute("INSERT INTO decision VALUES ('d','w','author')")
try:
    c.execute("DELETE FROM user WHERE id='author'")
    raise AssertionError('authored decision should restrict deletion')
except sqlite3.IntegrityError:
    check(True,'authored decision restrict')
check(c.execute("SELECT COUNT(*) FROM user WHERE id='author'").fetchone()[0]==1,'author remains')
check(c.execute("SELECT COUNT(*) FROM decision WHERE id='d'").fetchone()[0]==1,'decision remains')
check(c.execute("SELECT COUNT(*) FROM membership WHERE user_id='author'").fetchone()[0]==1,'membership remains')
c.execute("DELETE FROM user WHERE id='coadmin'")
check(c.execute("SELECT COUNT(*) FROM user WHERE id='coadmin'").fetchone()[0]==0,'coadmin deleted')
check(c.execute("SELECT COUNT(*) FROM membership WHERE user_id='coadmin'").fetchone()[0]==0,'membership cascade')
c.execute("INSERT INTO note VALUES ('n','commenter')")
try:
    c.execute("DELETE FROM user WHERE id='commenter'")
    raise AssertionError('authored note should restrict deletion')
except sqlite3.IntegrityError:
    check(True,'note restrict')
check(c.execute("SELECT COUNT(*) FROM user WHERE id='commenter'").fetchone()[0]==1,'commenter remains')
c.execute("DELETE FROM note WHERE id='n'")
c.execute("DELETE FROM user WHERE id='commenter'")
check(c.execute("SELECT COUNT(*) FROM user WHERE id='commenter'").fetchone()[0]==0,'after note removal deletion succeeds')
c.execute("INSERT INTO audit_log VALUES ('a','author','author@example.invalid')")
c.execute("DELETE FROM decision WHERE id='d'")
c.execute("DELETE FROM user WHERE id='author'")
check(c.execute("SELECT COUNT(*) FROM user WHERE id='author'").fetchone()[0]==0,'after decision removal deletion succeeds')
check(c.execute("SELECT actor_email FROM audit_log WHERE id='a'").fetchone()[0]=='author@example.invalid','audit survives')
check(c.execute("SELECT COUNT(*) FROM membership").fetchone()[0]==0,'memberships cascaded')
print(f'MKT092 structural SQLite checks={checks} failed=0; real deployment UNKNOWN')
