# alpha11：黑格尔批判专题42组

2026-10-12，Asia/Hong_Kong。第15批新增hegel_019—060，共42组，覆盖德文印刷402—408页、中文《马克思恩格斯全集》第3卷第316—324页。累计192对应/398单元/86逐页映射/6专题；主读384单元。黑格尔专题现60组，Reading Page由现有对应组动态生成；新关系均为uncertain。

本批从《现象学》目录接续至“现实的、肉体的人”的对象性活动。跨页单元完整保留：hegel_021中文316—317页，hegel_027德文402—403页，hegel_036德文403—404页，hegel_042德文404—405页，hegel_055德文406—407页，hegel_059—060德文407—408页。页码均为逐页显式映射。

扫描页清晰可见的wtklichen、wüd、gegenständüches、natürÜches、f ixüt、wirküchen等照录并显示语义疑点；词中和跨页双竖线另作开放字形标记。中文按扫描正文校正文字层误识；PDF中既有彩色高亮未转作正文强调。纯文本路线延续，不恢复字重或斜体。

增量抽样为61/168，原48条建议及理由冻结，第15批新增13条。reviews.json字节保持，24条既有人工确认有效；新增组未自动确认。追加脚本scripts/append_v04_batch15.py已执行，禁止重跑；两个最初漏记的页界标记由scripts/fix_batch15_markers.py补入，正文和reviews未改。

完整测试112项通过（19.15秒），包含旧记录/审核/抽样保护、跨页定位、照录异常和AppTest。四PDF哈希及508/825/574/236页数、398/192/86数据校验通过。实际浏览器搜索wtklichen→MEGA² I/2 S.406→原页→阅读页18高亮通过；疑点警告去重后仅显示两个实际字形。证据tmp/alpha11-tests.log、tmp/alpha11-validation.log及screenshots/hegel-alpha11.png。

Windows文件夹式exe位于dist/MEGA_Tool_Windows/MEGA_Tool_Windows.exe；便携交付为dist/MEGA_Tool-Windows-alpha11.zip，SHA256 `e74f563174921110334177da82b8977b8b61722546fe006a28180beb9307b169`。独立中文目录从无服务状态启动、8501占用回退、重复启动、无PDF提示、检索及阅读页跳转均通过，退出后8513关闭且原8501服务健康。exe依赖同目录的`_internal`、app.py、data和.streamlit，因此复制或交付时使用完整文件夹或ZIP。

下一批建议从hegel_061接续德文408页后半、中文324页后半，目标48组；继续按完整论证和扫描页边界决定实际数量。
