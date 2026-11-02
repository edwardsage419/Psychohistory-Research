# TH211 剑桥原始手稿影像可达性与文书证据链更正

track: theory
subflow: main
run_date: 2026-11-02 (Asia/Singapore)
observed_main_head_before_write: 81410bc5a943791432ad499fbc920ff84dd0c059
target_key: (theory,TH211+T-S-13J25.12+PGPID1070,Cambridge-IIIF-500px-2026-11-02,original-image-availability-and-address-provenance)
status: COMPLETE_BOUNDED_IMAGE_ACCESS; PARTIAL_PALEOGRAPHIC_VERIFICATION; HISTORICAL_CAUSAL_NOT_RUN
dedup: 延续TH211原始1055年书信的档案核查；前一补记只读Gil学术转录，明确原件影像NOT_READ。本轮首次直接打开两面原始手稿的剑桥托管低分辨率影像。无新TH编号，不重复声称原文转录独立完成。

## 原始材料、版本与实际阅读范围

原始历史作者：Abūn b. Ṣadaqa al-Maghribī，约1055年3月，致Ḥayyim b. ʿAmmār的信。剑桥大学图书馆 Taylor-Schechter Collection，馆藏号 T-S 13J25.12，PGPID 1070。原始手稿无DOI，馆藏号与PGPID为稳定识别键。

2026-11-02实际通过Princeton Geniza Project文书页 https://geniza.princeton.edu/en/documents/1070/ 中“Image: 1r”和“Image: 1v”链接，分别直接打开由 Cambridge University Library 托管的原件影像缩略图：

1. 正面 recto 1r，约500像素宽： https://images.lib.cam.ac.uk/iiif/MS-TS-00013-J-00025-00012-000-00001.jp2/full/500%2C/0/default.jpg
2. 背面 verso 1v，约500像素宽： https://images.lib.cam.ac.uk/iiif/MS-TS-00013-J-00025-00012-000-00002.jp2/full/500%2C/0/default.jpg

直接目视观察范围：正面完整页布局、密集书写行及边栏书写；背面上部两行地址文字和分散附记的布局。图像与PGP的正反面分配在结构上相符。**500像素宽的缩略图不足以独立逐字判读Judaeo-Arabic或Arabic，无法以本次目视核验确证verso的“الفسطاط”、recto 31至33行“מגלס אלרייס”的字形及任何法律术语。**原语逐行内容仍依据Moshe Gil 1983年学术转录，未进行独立古文字校勘。

来源分级：约1055年手稿本体的数字影像属于原始物质证据的现代复制；Gil 1983转录是编辑文本；PGP网页2026-11-02编目是现代元数据；Greif1993、Edwards/Ogilvie2012、Greif2012是相互竞争的历史解释。四层不能互相替代。

## 真正新增与更正

1. **纠正可达性判断。** 前一TH211补记记载剑桥CUDL查看器返回403，故原件影像未读。该403仍是查看器访问失败的真实记录，但PGP文书页的Cambridge IIIF直接图像链接可打开两面500像素缩略图。因此应将状态改为“原件低分辨率影像已直接目视，独立原语字形核验仍未完成”，而非“所有原件影像不可访问”。
2. **物质版面证据与文字释读分离。** 本轮可以独立观察两面手稿的存在、版面布局及背面地址区的书写。Fustat的确切拼写、收件人实际所在地、majlis的制度属性及赔偿事实均未因缩略图可达而被独立证实。PGP编目仍标收信人Fustat；Edwards/Ogilvie2012 p426称实际所在地Alexandria。两者冲突未闭合。
3. **地址与人所在地的不可识别性。** 构造历史A：信封写Fustat且收件人在Fustat；历史B：信封同样写Fustat但收件人在Alexandria、由第三方转递。两种情形产生相同的已观察地址，真实所在地不同。仅凭书面地址，即使高清影像完全确认字形，也不能排除历史B。此为构造性逻辑反例，不代表历史B确曾发生。
4. **法院与联合制裁仍为竞争解释。** recto 31至33行的Gil转录及后世论文不能因取得缩略图而升级为法院裁判原件；也不能据Palermitan称号证明Sicily有独立第三方制裁。仍需更高分辨率的合法图像、语言专家校勘、独立事件文书和可核的实际行为记录。

## 使用许可、测试、证据边界

PGP页脚“Image Permissions Statement”明确图片由Cambridge提供，zoom image © Cambridge University Library，all rights reserved；研究教学适用fair use/fair dealing，公开再发表需联系馆方。本次仅在线浏览，不下载、复制或上传原图到公开GitHub。PGP大学图书馆数据库另有限制自动抓取与分发的使用说明；没有批量抓取。

本轮仅做两面原件缩略图的直接视觉核查及原网页版权说明核对。高分辨率原件逐字校勘、Gil原刊与其他译本逐词对照、11世纪历史事件重编码、真实因果估计、预测验证、数学人工测试均NOT_RUN。该结果仅纠正来源可达性与证据链状态，没有新增R系列E1/E2/E3或MARKET证据。

C010已于2026-11-02 COMPLETE，D003已于2026-W45的2026-11-02 COMPLETE；本轮只读其main原文件，不新增C/D编号。R073及PESEN v0.1保持冻结；最新R177的原始239 08-001跨表正式采纳仍待处理，开放Codex PR未计入main。

下一步：在合法许可和可用条件下，人工打开更高分辨率的Cambridge IIIF图像，优先逐字校对verso地址及recto 31至33行；若无法取得或缺乏足够古文字能力，明确保持PARTIAL并转其他弱覆盖学科。没有触发GitHub Actions、收费API、云算力或付费全文；新增费用0，实际账单和免费CI配额NOT_VERIFIED。全部R研究完成后才统一分类，再有条件熔炼。
