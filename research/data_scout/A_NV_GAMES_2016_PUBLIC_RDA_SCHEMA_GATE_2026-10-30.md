# A轨 NV_games 公开真人重复博弈聚合数据来源核验

日期2026-10-30 UTC。目标键(A,NayVorobeychik2016,JohnNay-datafsm-c2e55eab,trial-schema-identity-license-gate)。状态 SCHEMA_AND_PUBLIC_FILE_CONFIRMED / RAW_ROWS_NOT_PARSED / R073_DIRECT_TRANSFER_NOT_READY。

原论文 Nay & Vorobeychik (2016), Predicting Human Cooperation, PLOS ONE 11(5) e0155656，DOI https://doi.org/10.1371/journal.pone.0155656 。作者公开软件仓库 https://github.com/JohnNay/datafsm ，固定commit c2e55eab12f1a24d3a5b09a9b42aeefff8bc5be4。实际读取该仓库man/NV_games.Rd、DESCRIPTION、LICENSE.md和data目录GitHub元数据。公开二进制data/NV_games.rda Git blob 36a961908385a7fe33ba688479b5dfc7b0a6b609，761556字节。文档声称168386条真人重复囚徒困境回合、30个游戏变体、51字段；本轮未解析RDA，不能称独立核验行数。

字段含period（局内轮次）、my.decision（当轮自身行动）、my.decision1..9和other.decision1..9（双方历史行动）、my.payoff1..9和other.payoff1..9（历史收益）、data（来源研究）、group（游戏变体）、delta、risk、error和收益参数r/t/s/p。所列51字段没有明确的稳定participant_id、dyad_id、session_id或supergame_id；不能仅靠period/group/data建立独立局次或跨期身份。对手当期行动、缺失和最长连续对局长度仍需解析后核验。

软件包datafsm 0.2.4的DESCRIPTION为MIT + file LICENSE；软件许可条款未明确授权对所有原真人数据的再分发，数据许可 UNKNOWN。公开可访问性CONFIRMED；实际逐行行为与身份验证NOT_RUN；复现准备PARTIAL；R073冻结100连续轮真人双人独立数据适用性NOT_VERIFIED。下一步在免费本地R中解析RDA并核验字段类型、分组、最大period、历史变量跨局重置及独立场次；如缺身份键需追溯八个原始实验来源。没有再发布第三方原始真人记录，没有新增E2预测或E3证据，没有付费操作。
