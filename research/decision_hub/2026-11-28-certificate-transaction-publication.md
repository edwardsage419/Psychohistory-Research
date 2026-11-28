# 数学证书与事务发布连接
2026-11-28。基线 f036ddfe08a5de555f86d928fac9146619e38e88。实际容器执行四个脚本，输出120 2160 360；publication, revocation, stale rejection: 120 120 120；120 2520；120 2160 120。
新增发布函数（依赖此前聊天附件 policy_replay.py、policy_certificate.py）：
```python
def publish(db,scope,rev,grant):
    db.execute('BEGIN IMMEDIATE')
    try:
        row=db.execute('SELECT rev,grant_id,raw,mac FROM s').fetchone()
        if row[:2]!=(rev,grant) or row[2] is None: return False
        v=json.loads(row[2]); rows=v['rows']
        if v['scope']!=scope or not verify(scope,rows,row[3]): return False
        pts={tuple(p) for _,p in rows if p is not None}
        f=sorted(p for p in pts if not any(q!=p and q[0]>=p[0] and q[1]>=p[1] for q in pts))
        db.execute('UPDATE s SET result=?',(enc(f),));db.commit();return True
    finally:
        if db.in_transaction:db.rollback()
```
120配置沿用既有网格，逐一发布合法记录，逐行翻转18条可行性记录并重新签名，2160次拒绝且结果NULL；撤回清空后120次拒绝。单连接顺序测试，未验证竞争、崩溃、恶意类型、可信宿主参数、签名绑定授权或多会话。当前签名仅绑定数学scope和rows，rev/grant由数据库检查，旧签名重新植入新授权仍需防护。单行表假设，非生产。完整新增脚本保留聊天附件。唯一交接及全库去重未核实。无训练、合并、部署或新增费用。