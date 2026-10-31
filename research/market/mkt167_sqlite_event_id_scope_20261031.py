#!/usr/bin/env python3
"""SQLite event ID scope experiment. No ActivityWatch runtime or personal data."""
import sqlite3


def db():
    c = sqlite3.connect(':memory:')
    c.execute('CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, bucketrow INTEGER, starttime INTEGER, endtime INTEGER, data TEXT)')
    return c


def put(c, bucket, event_id, data):
    c.execute('INSERT OR REPLACE INTO events(bucketrow,id,starttime,endtime,data) VALUES (?,?,?,?,?)', (bucket, event_id, 100, 130, data))
    return c.execute('SELECT last_insert_rowid()').fetchone()[0]


def run():
    a, b = db(), db()
    checks = 0
    def ok(condition):
        nonlocal checks
        assert condition
        checks += 1
    ok(put(a, 1, None, 'A') == 1)
    ok(put(b, 1, None, 'B') == 1)
    ok(a.execute('SELECT data FROM events WHERE id=1').fetchone()[0] == 'A')
    ok(b.execute('SELECT data FROM events WHERE id=1').fetchone()[0] == 'B')
    ok(put(a, 2, None, 'C') == 2)
    ok(a.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 2)
    ok(put(a, 1, 1, 'A-revised') == 1)
    ok(a.execute('SELECT data FROM events WHERE id=1').fetchone()[0] == 'A-revised')
    ok(a.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 2)
    ok(b.execute('SELECT data FROM events WHERE id=1').fetchone()[0] == 'B')
    ok(a.execute('SELECT bucketrow FROM events WHERE id=1').fetchone()[0] == 1)
    ok(put(a, 2, 1, 'C-crossbucket') == 1)
    ok(a.execute('SELECT bucketrow FROM events WHERE id=1').fetchone()[0] == 2)
    ok(a.execute('SELECT COUNT(*) FROM events WHERE bucketrow=1').fetchone()[0] == 0)
    ok(a.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 2)
    a.close(); b.close()
    print(f'PASS {checks} SQLite assertions; ID allocation local to DB; explicit ID replacement')


if __name__ == '__main__':
    run()
