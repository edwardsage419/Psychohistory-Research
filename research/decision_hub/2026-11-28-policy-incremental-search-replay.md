# 增量策略求解与认证发布
基线 fcb58bc1c98fb369c947bd565e50f12cb1ba08e4，开放PR 63,62,61,60,59。本轮实际容器执行 policy_integrated.py 输出504 1008 5872 504，新增 policy_incremental.py 输出1512 9044 17616 9044。
沿用504配置及剪枝条件，每批预算1/3/7条记录。初始pending=[0,0]，rows=[]；每次重开SQLite并核对完整载荷MAC与宿主身份，拒绝未完成发布，再按(j,k)计算一条剪枝或叶记录，推进游标并提交。j=2时pending清空；复用完整证书验证及事务发布，与解析最低成本公式比较。1512次一致，9044次重开与未完成发布拒绝，17616条记录。无预生成证书。核心增量步骤：
```python
def step(s,j,k):
    c,a,b,g,r=s; balance=c-j*a+j*g
    if k==0 and (c<j*a or balance<max(a,b)):
        return (j,'cut',None),(j+1,0)
    x,y=divmod(k,3); costs=(a,b,a+b); end=balance-max(costs[x],costs[y])
    p=(j,end) if x!=1 and y!=0 and (r or x==y) and end>=0 else None
    return (j,k,p), (j+1,0) if k==8 else (j,k+1)
```
完整脚本及依赖为聊天附件。同进程正常关闭重开，未测试进程终止、并发游标更新、防回滚、恶意游标或资源实际耗时；共享frontier函数，非独立验收。参数由研究者选定，与既有网格重叠。唯一交接及全库去重未核实。无生产修改、训练、合并、部署或新增费用。