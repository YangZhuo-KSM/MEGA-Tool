# alpha12：黑格尔批判专题48组

2026-10-12，Asia/Hong_Kong。第16批新增hegel_061—108，共48组，覆盖德文印刷408—411页、中文《马克思恩格斯全集》第3卷第324—329页。累计240对应/494单元/94逐页映射/6专题；主读480单元。黑格尔专题现108组，Reading Page由现有对应组动态生成；新关系均为uncertain。

本批接续“现实的人的对象性活动”，覆盖自然主义与人道主义、人的自然存在、对象性和感性、物性扬弃，以及思辨幻想的前半段。跨页单元完整保留：hegel_066中文324—325页，hegel_072德文408—409页，hegel_080中文325—326页，hegel_090德文409—410页，hegel_092中文326—327页，hegel_100中文327—328页，hegel_108中文328—329页。页码均为逐页显式映射。

扫描图清晰时以图像为准：文字层中的`natürÜch`、`Wirküchkeit`、`Sinnüchkeit`、`weü`、`Schern`、`Reügion`等未写入正文，分别按图像录为`natürlich`、`Wirklichkeit`、`Sinnlichkeit`、`weil`、`Schein`、`Religion`。可见页界符`exis||tiren`、`||XXVII|`、`||XXVIII|`及两个段界标记原样保留并作为开放字形疑点。纯文本路线延续，不恢复字重或斜体。

增量抽样为76/216，原61条建议及理由冻结，第16批新增15条。reviews.json字节保持，24条既有人工确认有效；新增组未自动确认。追加脚本scripts/append_v04_batch16.py已执行，禁止重跑；追加前四JSON备份在local_backups/v04-before-batch16。

完整测试117项通过（20.77秒）。四PDF哈希及508/825/574/236页数、494/240/94数据校验通过。实际浏览器显示alpha12/240/24/6；搜索exis||tiren→MEGA² I/2 S.408固定引用→408原页→阅读页22高亮通过，页面内显示页界转录疑点。证据tmp/alpha12-tests.log、tmp/alpha12-validation.log。

源码包`dist/paris-manuscripts-0.4.0-alpha12.zip`已在无PDF环境通过240对应/6专题/6工作区冒烟；公开版同步README后重新打包，最终校验值见Release附带的`.sha256`文件。Windows便携包`dist/MEGA_Tool-Windows-alpha12.zip`已在独立中文目录从无服务状态启动，8501占用时自动转到8513，重复启动、内置检查、搜索、缺PDF提示、跳到阅读页22及正常退出均通过；退出后8513关闭，正式8501服务保持在线。便携包SHA256为`bb13119b443444011e1ef6f4eb3837e634ded430d2200a93b9b5c6abc7a70129`，包内不含PDF、个人`reviews.json`或本机来源配置；运行文件和四份研究JSON与发行目录逐字节一致。证据`tmp/alpha12-smoke.log`、`tmp/alpha12-exe-checks.json`。

下一批从hegel_109接续德文411页后半、中文329页，继续扩大到约54组；实际数量仍由完整论证和扫描页边界决定。
