# R100 Phase A2：原 Zenodo 双人阈值 XLSX 的严格重定向及可追溯来源收据修订

日期：2026-10-17；状态 PRESCORE_SOURCE_AMENDMENT_FROZEN；适用于本修订之后的官方原字节复验。前置 Phase A 原冻结维持，不回写、不撤回先前任何成功或失败记录。

## A2 修订动机与安全边界

Phase A 原程序曾使用 urllib 默认跳转，只有收到跳转完成的响应后才核验最终 URL。攻击或意外重定向时，可能先向非授权 host 发出 GET 再拒绝结果。现在严格改为自定义 `HTTPRedirectHandler.redirect_request`：只要 3xx 新 URL 不是冻结的精确 `https://zenodo.org/records/16918146/files/ThresholdPGG_ExperimentalData.xlsx` 且 query 仅空或 `download=1`，在任何后续 GET 请求发出前安全拒绝。包括同一 Zenodo 域的其它路径也 fail closed。不假定 Zenodo 一定能满足该策略。如果出版方实际交付需要另一官方重定向，先保存失败证据，另行出处验证并再次冻结具体白名单，不绕过。

增加两个纯 synthetic 负例，源程序从原18项增加为20项，无人类真实数据。不改变官方 MD5、文件大小、工作簿 ZIP/XML 白名单、10 张 sheet 只读目录、人物/行为零读取。

## 机读审计与 Git 归档

GitHub Actions 首先运行全部20项 synthetic，成功后才触发唯一第一手 Zenodo 文件认证。脚本输出最小匿名收据：E1官方原MD5 SHA及文件长度工作簿表数量，或者E0/E1失败编码及零真人结果，绝不保存 XLSX 二进制、工作表内容、个人/伙伴行为及姓名。CI在成功或阻断时尝试将收据写入 `research/R100/R100_PHASE_A_LIVE_CI_SOURCE_RECEIPT.json`，提交回 main，防止只存在30天工件而难以审计。这个 receipt 只表示程序运行报告，科研E1仍须核对GitHub实际提交及其内容。未能写入或未见提交不声称E1成功。

两次20轮 session 是一批重用的人；不存在可验证的独立招募实验室 session 字段之前不得叫独立 session-LOSO。R073模型不修改、PESEN v0.1 FROZEN。真人实验得分此阶段始终零。
