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
