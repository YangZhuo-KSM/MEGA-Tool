# 从研究问题到Python代码

## 1. 数据如何读进来

`paris/corpus.py`用`json.loads`把文件转换成Python字典和列表。`index()`把一组对象变成`{ID: 对象}`，通过ID查询即可得到原文，避免依赖两个列表刚好排列一致。

`aligned_units()`先读一组关系中的`de_ids`和`zh_ids`，再分别取回文本。因此一段德文可以对多段中文，两段德文也可以对一段中文。UI把同组全部文本显示出来。

## 2. 搜索为何需要位置映射

`paris/search.py`生成检索副本。例：`Straße`折叠为`strasse`，检索文本变长，但两个`s`都映射回原文的`ß`位置。组合重音符也有同样问题。每个检索字符保存原文起止位置，查到命中后可高亮真实原文，正文不用修改。

搜索是字面匹配，线性遍历当前小型语料即可。完整词选项检查命中前后的字符边界。没有词形分析、语义相似或自动翻译。

## 3. 页码如何对应

`paris/pages.py`查询明确保存的页记录。印刷267对应PDF292是一条资料事实，不能推导另一本书或整卷其他区间。

本地预览先检查源文件哈希，再用`pypdfium2`渲染指定页。多个Streamlit会话可能同时请求图片，PDFium调用使用锁，避免同时操作这个非线程安全库。

## 4. diff和计数怎样计算

`paris/compare.py`把德文分成词、标点与空白，中文分成字符，再用标准库`difflib.SequenceMatcher`得到相同、插入、删除、替换片段。左右片段拼回去必须分别等于输入，测试覆盖这一性质。

`paris/stats.py`复用搜索结果，按章节相加。每条导出行包含ID、次数、正文和页码，所以可以手工复算。统计采用不重叠命中，不统计比较副本。

## 5. 核验为什么另存

`paris/reviews.py`保存的是某个人对某一版内容的确认。用哈希绑定正文和定位；正文修改后，旧确认不能继续代表新内容。审核记录保留历史，写入时先写临时文件再替换，降低中断造成半个JSON的风险。

## 6. 界面与测试

`app.py`只负责选择控件、调用核心模块、显示结果和导出。Streamlit每次交互会重新执行脚本；当前选中ID由`session_state`保存，专题或搜索变化后先检查选中ID是否仍有效。

pytest测试研究数据引用、Unicode边界和页码等逻辑；AppTest模拟页面选择。真实浏览器检查负责字体、长段落和原页图像等视觉事项。学术对应是否正确仍由研究者判断，测试不能替代这一步。

## 7. 阅读页与检索联动（0.2.1）

reading.py的visual_lines按字符显示宽度和换行估计行高；group_height取德中较高侧；reading_pages依次填充完整组。page_for_alignment把已有组定位到其阅读页。pages不存正文，搜索过滤页面也不重新分页。

locator.py复用search.py；德文使用可选完整词边界，中文继续字面匹配。snippets按命中位置截取并合并上下文，保持高亮位置。reading_targets优先直接对应，只有比较单元才借已有comparisons桥接，标记via_comparison。

citations.py的mapped_locations同时检查来源、印刷标签、PDF地址，保留重复印刷标签的不同原页；reference按source选择固定模板，format_pages合并连续阿拉伯页，保持实际非连续页。元数据核验状态不由formatter修改。

reader_ui.py承接两个新工作区。搜索跳转先写一个session_state意图，在下一次创建控件前consume_jump更新专题、阅读页与目标高亮，避免控件状态交叉或残留筛选。app.py保留原页渲染、比较、统计和用户审核入口。clipboard.py生成本地iframe的复制按钮，固定代码和JSON转义防止正文被解释为脚本；失败时提供手动复制文本。

本版测试新增tests/test_reading.py、tests/test_reader_workflow.py；更新test_app和test_pages_v02的界面入口，核心页码/审核/validation测试继续保留。

## 8. 研究覆盖与范围统计

coverage.py把独立目录计划关联实时corpus/reviews，分别计算目录是否开始、已收录文字校订及对应确认；未知全文分母返回None。stats.research_distribution先筛选语言/版本/专题/主读/确认，再对去重查询逐条检索，返回scope、summary、hits供CSV/JSON和界面共同使用。research_ui.py负责第六个覆盖工作区和扩展术语界面；reading_targets继续提供统计命中回读入口。追加脚本append_v04_batch.py备份后只追加新记录，逐条检查旧指纹及reviews不变，并拒绝重复覆盖。

## 新专题追加（alpha6）
append_v04_batch6.main可接收new_sections与coverage_updates；在写入前检查新ID、既有目录分配不得覆盖、每专题只属于一项覆盖计划。批次脚本只提供转录、逐页位置和专题配置；旧记录/指纹逐项保护，四JSON备份至local_backups。正文模型、阅读聚合及搜索接口不变。

alpha7的issue_overrides只允许指定kind/status/note/reported_reading/evidence_pages，保留由照录文字生成的锚点。跨页单元的疑点可指向实际后一页，不默认使用第一来源页。

alpha8的extra_page_maps用于追加正文之外已核对的插图、未编号或空白页；拒绝覆盖既有映射，缓存页级提取，交由原validator校验。批次组数由rows长度决定，界面审核与导出不固定为6。sampling.py将正文来源位置跨过PDF插页的组定向选出；实际跨页引用仍由citations.py按明确印刷标签生成，不虚构连续范围。

alpha19固定三批各24组。append_v04_batch6的source_by_section可显式将mill路由到de_megaiv2/zh_single，默认对仍为de_megai2/zh_collected。coverage_notes避免将精选穆勒片段描述为全篇开头连续收录；row_notes区分评注和摘录。source_slices.py按extraction.json的原页行范围、局部扫描修正和句群锚点重建正文；未保存的页才读tmp缓存。词间空白不归入下一来源页，诗行按已核对行首还原。配方脚本可导入检查，已执行批次拒绝重复追加。

alpha20补入穆勒前部时，旧mill_001起的稳定ID与sequence均不得改写。append_v04_batch6的sequence_overrides允许新ID使用独立整数顺序值；阅读页仍按unit.sequence排列。覆盖只接受当前批次的alignment ID且必须是非bool整数，避免拼错ID或隐式类型改变顺序。前补批次从mill_062起分配ID，并使用递增负序列恢复来源顺序。

自动扩充第31批起使用scripts/audit_incremental_batch.py读取指定批次配方和local_backups/v04-before-batchN，逐项保护旧记录、指纹、extraction证据、目录分配、reviews字节及冻结抽样。读取顺序审计目前适用于正常正sequence章节，穆勒负sequence前补仍使用对应专项审计。当前研究数据版本由corpus.release决定；数据自动扩充不逐批重建发行包。

scripts/checkpoint_automation.py从实际corpus/sampling文件读取计数，以同一标记块刷新四份恢复文件并回读；phase和next明确未完成事项，quota只传最近工具实读值。它只写文档检查点，不修改语料/抽样/审核。收尾将阶段块整理为当前快照。

scripts/repair_sampling_evidence_page.py用于2026-10-21已授权的单项修复，默认只读：仅当profit_de_049_literal_298的evidence_pages是343，且内存恢复342后恰好匹配原冻结scope_digest，才迁移该digest。建议、范围和其他计划字段保持，corpus不写；--apply先备份并记录新旧digest/哈希，原子替换计划。它不改正常抽样保护规则、不重抽建议；tests/test_sampling_evidence_migration.py验证拒绝额外正文/位置/疑点变化。

## Windows启动器（2026-10-07）
desktop_launcher.py提供Tk启动窗口和同一exe的--serve子进程。paris/desktop.py负责研究目录选择、单实例文件锁、端口选择、就绪检测和Windows Job进程树清理。就绪后才打开浏览器，重复打开复用已有服务；不终止其他端口上的程序。corpus.ROOT允许启动器通过MEGA_TOOL_ROOT指定研究目录，普通源码运行路径不变；各研究模块仍共用同一个ROOT。启动器不写语料或审核。

scripts/build_windows.py生成PyInstaller文件夹发行版，捆绑运行时和依赖，拷贝app.py及样本JSON；排除原PDF、reviews.json和本机路径。内部构建优先原研究目录，独立副本使用自身data。requirements-build.txt记录构建工具版本。不能把exe单独从发行目录拿走。
