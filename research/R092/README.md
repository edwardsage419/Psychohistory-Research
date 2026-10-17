# R092：Wang–Hilbe–Zhang 2025 四人非对称阈值公共品数据的真实来源认证（格式阻断）

**日期2026-10-17。R092=CLOSED_SOURCE_FORMAT_BLOCKED；E1作者固定来源字节、MD5和SHA256成功；E2真实人类行为预测未执行；绝不以不能解析的数据伪造模型结论。PESEN v0.1=FROZEN。**

第三次原作者之外、第四个实验团队候选：Wang, Hilbe & Zhang (2025)，[Zenodo v2固定数据 DOI 10.5281/zenodo.16918146](https://zenodo.org/records/16918146)，阈值公共品四人组数据 `ThresholdPGG_4P_ExperimentalData.mat`，官方MD5 `6036f73c2f758ab3aeed6dcf4f74585b`，实测17,159字节，完整原文件SHA256 `76b02d921d02ad652cb952a71173e84b206135e4deb7bfc6235b9387738a6b05`。作者说明276名原真人、2场次各20轮、第二场同受试者重配组，不能拿两场次当全新独立人类样本；当前项目**未从真实文件解码出参与者贡献或群组成员数据**。

所有实验读源前独立冻结：[Phase A基础MAT](../../protocols/R092_WANG_HILBE_ZHANG_2025_ASYMMETRIC_THRESHOLD_4P_ORIGINAL_ZENODO_MAT_SOURCE_FREEZE_2026-10-17.md)→19synthetic全PASS、真实`scipy.io.whosmat`源不兼容[CI39016888560](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39016888560)；[Phase A2 HDF5兼容来源方案](../../protocols/R092_PHASE_A2_ORIGINAL_PUBLISHER_MATLAB_V73_HDF5_METADATA_ONLY_FREEZE_2026-10-17.md)→34synthetic全PASS、官方MD5真实下载，但不是预设HDF5格式[CI39017000035](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017000035)；[Phase A3严格限定MAT/ZIP/HDF5文件头信号检查](../../protocols/R092_PHASE_A3_ORIGINAL_THRESHOLD_MAT_RESTRICTED_FILE_SIGNATURE_DIAGNOSTIC_FREEZE_2026-10-17.md)→[CI39017117283](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39017117283) **47synthetic与真实完整来源审计均SUCCESS**，固定真实文件确为`MATLAB 5.0 MAT-file`文件头、非MATLAB7.3/HDF5，SciPy读取真实文件报`TypeError`。仅保留异常类与安全文件格式标识，不输出真人个体贡献或原始字节。读取器异常并不能证明原件损坏，后续可冻结专用MATLAB5读取器独立再试。

[研究科学限制与全部失败记录](R092_ORIGINAL_THRESHOLD_4PERSON_PUBLISHED_SOURCE_FORMAT_ADMISSION_REPORT_2026-10-17.md) · [A01–A06实际有限状态（其中A03**BLOCKED**而非PASS）](R092_SOURCE_QUALIFICATION_FINAL_ACCEPTANCE_STATUS.json) · [19synthetic及旧MAT源程序](r092_original_2025_4player_threshold_mat_source_structure_only.py) · [HDF5变体结构审计程序](r092_phase_a2_original_mat_v73_HDF5_metadata_only.py) · [最终真实文件签名检测源码](r092_phase_a3_fixed_author_original_mat_signature_only.py)。源码与三份独立纯合成测试、三工作流均同步GitHub。

R092本轮不是新的正面或反面合作行为研究。项目R089正、R090负、R091正的**已完成E2原作者实验指标没有改变**。未来R093优先另找独立真正可解码、二元是否投资全球公共品的真人数据并冻模型检验；PESEN v0.1继续FROZEN。
