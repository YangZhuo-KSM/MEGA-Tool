# 数据结构与编辑约定

`schema_version=1`。JSON是权威研究数据，Python模块读取后检查引用；界面不通过数组下标猜测翻译对应。

## 实体

| 表 | 关键字段 | 含义 |
| --- | --- | --- |
| sources | id, file_name, sha256, pdf_page_count | 一个具体PDF文件 |
| editions | id, source_id, title, editor, translator, publisher, year, edition, presentation | 出版版本及呈现方式；两个呈现可共用source |
| sections | id, work, manuscript, title, aliases, coverage | 研究结构，正式标题与别名分开 |
| units | id, edition_id, language, section_id, sequence, text, locations | 一个文本单元及全部页位置 |
| alignments | id, de_ids[], zh_ids[], status, review_batch | 一组德中关联，不要求同样段落数 |
| page_map | source_id, printed_page, pdf_page, status | 逐页核对的文件映射 |
| comparisons | left_ids[], right_ids[], kind, status | 同语种比较，kind为edition或presentation |
| corrections | unit_id, extracted_reading, corrected_text, evidence_pages, note | 校订内容与可回查依据 |

印刷页是字符串（如`XI*`），PDF页序是从1开始的整数。跨页使用多个location，位置绑定文件来源。未定位内容允许locations为空，UI明确提示；已知位置必须存在于page_map。

主读文本 `role` 省略或为 `primary`；比较用副本为 `comparison`。统计只取首选德文主读文本，因此同一段落不会因多个版本或多个对齐重复计数。新增手稿时需增加章节、文本、关系与coverage，不能只改统计说明。

## 核验状态

文字：`scan_checked_ai`。目前62个单元经过AI图像核对，研究者仍须复核。

对应：`uncertain`（待审）、`automatically_aligned`（算法候选）、`manually_verified`（研究者已确认）。初始24组全部为uncertain；不存在自动批准或根据测试通过升级学术状态的规则。

实际用户审核保存在reviews.json。每条记录绑定关联ID列表、正文、页码和版本元数据的SHA256指纹；变化后显示`stale`，保留旧记录供追溯。保存采用临时文件后原子替换。本地单用户使用；没有账号系统或多用户并发写入协议。

当前14组同语种比较尚没有独立的在线审核表单，其状态保持待审；不能把德中确认自动传播到同语种比较。

## 编辑工作流

1. 定向提取扫描页，将文字层保留在extraction.json。
2. 对照图像校订正文，保留历史拼写、注号和可读手稿定位符号。编辑性补字不凭猜测。
3. 为新单元分配未使用的稳定ID；只修订正文时保留ID。
4. 在alignments中列出两侧ID，1:N/N:1均可；无中文时zh_ids为空。
5. 为每个来源位置建立精确映射，校验后导出审核批次。
6. 研究者确认后保存审核。变更后重新运行`validate_data.py`及相关测试。

首批数据的 `extracted_reading`：德文为去除排版成分后的OCR候选；中文为null，表示从扫描页逐段转录，原文字层在evidence_pages指向的extraction.json中。null不表示原书没有文字。

当前未恢复斜体、粗体或编者注全文。上标注号是注释锚点；需要注释内容时应回到对应原书。简化排版后的diff只能说明这两份转录的字面差异。
# 照录疑点标注（2026-10-01增补）

v0.2页码扩展：`page_map`允许`printed_page=null`，限`page_kind=unnumbered/blank/illustration`且必须有说明；PDF页序依然为1起算的有效整数。同一印刷标签允许多个PDF页，查询全部返回。独立`missing_pages`要求来源、印刷标签、`status=confirmed_missing`、证据和说明，PDF页序为null，不能与存在映射冲突；无记录表示未收录，不自动断言缺页。

`editorial_issues`中的`kind=semantic_doubt`、`status=retained_as_source`表示按底本照录且持续展示的语义疑点。`text_anchor`保存Python字符索引start/end（左闭右开）及quote；正文变动导致锚点不匹配时数据校验报错，禁止把标记贴到其他字。`note`记录保留理由，`evidence_pages`指向来源页。标注独立于用户对应确认，不自动改变其状态。


## 展示层阅读页与引用（0.2.1）

语料结构不变。Reading Page由reading.py在内存按既有对应组生成，包含id、number、section_id、alignment_ids、estimated_lines，不写回JSON。内部阅读页号按专题区分，不能当作书本印刷页。

citations.py的BIBLIOGRAPHY为来源级用户引用样式配置，独立于editions元数据及metadata_status。template、short_title、volume、place、publisher、year、language集中存储；印刷页样式由language决定。source通过edition.source_id绑定，引用只能使用文本的已存在逐页映射，复制内容不包含PDF页序。存在年份冲突或版权页未核验时保留并提示两层信息，不能改写原件书目信息。

locate返回原文本单元、命中字符范围、候选上下文、reference及阅读页目标；比较版本只通过已有comparisons提供明确标注的桥接。跨页索引精度目前为整个unit，不包含逐字页边界，不能给某个词猜测单页页码。详见READER_RELEASE.md。

## v0.4目录与动态覆盖

coverage_plan.json独立存目录项、所属手稿、关联section_ids、目录起始印刷页及证据。total_groups=null表示尚未建立全文分母；checked_ratio以已收录文本为分母，confirmed_ratio以已收录对应组为分母且复核有效指纹。corpus.coverage旧摘要保留历史数据，不再作为新界面的当前覆盖事实。新增第5批12单元/6组/4映射仅追加，既有记录未改；proofread_at新记录为香港日期字符串，不虚构时分秒。
