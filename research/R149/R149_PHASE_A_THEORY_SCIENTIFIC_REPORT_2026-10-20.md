# R149 结构化理论：结构—行动反馈和有限机制的 E1 初步验收
日期2026-10-20；既定目录 P2/06-007 Structuration Accounts。
原始概念核实：Anthony Giddens (1984), The Constitution of Society, University of California Press https://www.ucpress.edu/book/9780520057289/the-constitution-of-society （只核实出版社目录）；William H. Sewell Jr. (1992), A Theory of Structure: Duality, Agency, and Transformation, American Journal of Sociology 98(1):1–29 DOI https://doi.org/10.1086/229967 （核实原期刊摘要及可用文本转录）；**不声称完整Giddens著作或Sewell原刊逐页视觉核读**。文献未提供本项目以下方程，所有数值属于自行定义E1人工模拟。R144是固定事件顺序的历史状态机；本期测试结构和行动的**每一期双向闭环反馈**。

计算前冻结协议在main提前入库：commit `3ddf839aaac22445a03a14739b5e11eba155a56f`，路径 `protocols/R149_GIDDENS1984_SEWELL1992_STRUCTURATION_DUALITY_FINITE_FEEDBACK_PRESCORE_FREEZE_2026-10-20.md`。

两名条件独立行动者行动A/B。结构s∈{0,1,2,3,4}，初态2，行动A概率p_s=(s+1)/6；同一期两人共同选择A人数k=0/1/2时下一期s'=max(0,s−1)/s/min(4,s+1)。对照模型 fixed将p=1/2恒定但结构仍可更新；frozen冻结s不变、行动仍条件于s。精确Fraction测试期长1、2、4、8、16，两套相互独立转移实现逐状态相同，额外由行动四分支逐时点递归枚举对≤8期的合成历史精确复算；特别是8期有4^8=65536条**概念性的**有序行动历史，优化实现用按状态与剩余时间缓存的等价组合递归，**没有真的逐条生成65536条完整路径记录**，其等价性由独立前向算法检验。因此不可把缓存程序说成是全路径逐项留痕。

8期终态结构端点0或4的概率：feedback=16624456774/19591041024 ≈0.84858；fixed=24786/65536≈0.37820；frozen=0。三个机制任意期E[s]=2，期望A行动者数每期均为1；均值相同不表示结构分布相同。首期do(k=2) vs do(k=0)，保留后续自然反馈至t8，平均结构差：feedback `2500240439/816293376`、fixed `2375/2048`、frozen `0`。所有三模型都有不同制度传递规则，不能由数值直接证明现实结构化理论正确。

本地原生Python标准库主程序、41项真实unittest、确定性机器JSON已产生并验证：ZIP SHA256 `2db8c52eb2bb064d3df21e1f43c6bae78fab58d09037919ebdad36e61872de1e`，主程序 `250d720876d5a1b13c49da147fbc1af4647eb37bbb67ca12c055e343f6d055a9`，测试 `58c9f2ec7eb4cef4f6158aa7e097374ae643730364fec8ce8a8f91df3d13940a`，原JSON `c822e76a3424303dbb362cffeab29cc728d400475d01909181678a7c182960f9`。

**验收状态仅 LOCAL_VALIDATED_NOT_REMOTE_CI**：尚未将完整源码ZIP上传GitHub，也没有真实GitHub Actions双环境检查及remote验收收据；因此严禁写CLOSED_BOUNDED，暂时只保存先行协议和本地阶段报告。本地完整文件随对话交付，可用于下阶段上传远端持续复验。新真人E2=0，历史E3=0，R073及PESEN v0.1冻结。
