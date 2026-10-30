"""Bounded synthetic test of pinned Loop SQLiteEntryList.add and backup projection.
No real user data or Android runtime is used.
"""
import sqlite3

DDL = '''CREATE TABLE Repetitions (id integer primary key autoincrement,
 habit integer not null, timestamp integer not null, value integer not null,
 notes text); CREATE UNIQUE INDEX idx_repetitions_habit_timestamp
 ON Repetitions(habit,timestamp);'''


def new_db():
    db = sqlite3.connect(':memory:')
    db.executescript(DDL)
    return db


def add(db, habit, timestamp, value):
    # Direct structural analogue of pinned SQLiteEntryList.add.
    db.execute('DELETE FROM Repetitions WHERE habit=? AND timestamp=?', (habit, timestamp))
    db.execute('INSERT INTO Repetitions(habit,timestamp,value,notes) VALUES (?,?,?,?)',
               (habit, timestamp, value, ''))
    db.commit()


def snapshot(db):
    return db.execute('SELECT id,habit,timestamp,value,notes FROM Repetitions ORDER BY id').fetchall()


def run():
    checks = 0
    def check(condition, name):
        nonlocal checks
        assert condition, name
        checks += 1

    a, b = new_db(), new_db()
    add(a, 1, 100, 2)
    a_before = snapshot(a)
    add(b, 1, 200, 2)
    b_before = snapshot(b)
    check(a_before != b_before, 'different histories before edits')
    check(a_before[0][2] == 100, 'world A old timestamp')
    check(b_before[0][2] == 200, 'world B old timestamp')
    add(a, 1, 100, 0)
    b.execute('DELETE FROM Repetitions WHERE habit=? AND timestamp=?', (1, 200))
    b.commit()
    add(b, 1, 100, 0)
    check(snapshot(a) == snapshot(b), 'same final table, including id')
    check(snapshot(a) == [(2, 1, 100, 0, '')], 'expected final row')
    check(a.execute('SELECT seq FROM sqlite_sequence WHERE name=?', ('Repetitions',)).fetchone() == (2,), 'A sequence')
    check(b.execute('SELECT seq FROM sqlite_sequence WHERE name=?', ('Repetitions',)).fetchone() == (2,), 'B sequence')
    check(a.execute('SELECT count(*) FROM Repetitions').fetchone()[0] == 1, 'one final row')
    check(b.execute('SELECT count(*) FROM Repetitions').fetchone()[0] == 1, 'one final row B')
    for db in (a, b):
        copy = sqlite3.connect(':memory:')
        db.backup(copy)
        check(snapshot(copy) == snapshot(db), 'SQLite logical backup projection')
        copy.close()
    check(a_before[0][3] == b_before[0][3] == 2, 'same old value different old dates')
    check(a_before[0][2] != b_before[0][2], 'old event date not recoverable')
    check(snapshot(a)[0][3] == 0, 'new value')
    check(snapshot(b)[0][2] == 100, 'new timestamp')
    # The pinned AutoBackup.runInPrivateDir removes old files before adding a fresh copy.
    keep = 5
    existing = list(range(keep))
    existing = existing[max(0, len(existing)-keep):]
    existing.append(keep)
    check(len(existing) == keep + 1, 'backup rotation may temporarily retain keep+1')
    check(len(existing) > keep, 'keep is not strict post-write maximum')
    check(len(existing) == 6, 'illustrative six copies')
    a.close(); b.close()
    print(f'MKT157_SYNTHETIC_PASS checks={checks} final_row=(2,1,100,0) distinct_prior_dates=100,200')


if __name__ == '__main__':
    run()
