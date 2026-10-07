# alpha6 本地接续（2026-10-03，香港）

新专题“私有财产和共产主义”收录communism_001—006，来自MEGA I/2第二种呈现印刷386—387及中文全集第3卷印刷294—295。第004组中文跨页，保留注号93—95及①、德文编辑补字和||标记。第006组止于分号，后文“endlich spricht sich diese Bewegung…”从下一批接续，不补造句末。

当前60对应、134文本单元、36逐页映射、5专题。旧54组记录与审核指纹保持，24条有效用户确认；第10批6组仍待审。抽样清单16/36，旧14条建议原样保留；本批建议communism_003、004。

新专题动态组织成2个阅读页（每页3组），覆盖表5/14项开始收录，120/120主读文本AI扫描校订；全文单元分母仍待建立。德中检索、固定引用、原页和阅读位置联动已接入。

验证：92项完整pytest通过（10.08秒），四原PDF哈希/总页数及数据校验通过。新增2项测试覆盖新专题登记、抽样延续、跨页来源/引用、两原页路由与高亮跳转。浏览器在1440×1000复核覆盖表及双栏阅读，截图docs/screenshots/communism-alpha6.png；临时尺寸已恢复。AppTest重复渲染已打开原页属于界面重跑，测试校验实际地址集合。

实现：scripts/append_v04_batch6.py新增new_sections与coverage_updates参数，先验证每专题只归入一项目录并拒绝覆盖已有分配；备份新增coverage_plan/sampling_plan。scripts/append_v04_batch10.py只追加本批；语料schema仍1，无重复正文模型。新文本自动使用既有阅读/检索模块。测试新增tests/test_communism.py，更新数据规模断言；软件版本0.4.0-alpha6。

下一正文：MEGA I/2印刷387/PDF387，第23行“endlich spricht sich diese Bewegung…”；中文全集印刷295/PDF320，“最后，用普遍的私有财产来反对私有财产这个运动…”；必要时接德文388/中文321。下一批从communism_007开始。

本轮本地交付，GitHub更新仍暂停。第10批核对材料docs/reviews/batch-10.md；原PDF与用户reviews.json保留本地。
