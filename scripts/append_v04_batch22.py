"""Batch 22: 23 money groups and the closing Mill-commentary group."""
from append_v04_batch6 import main
from append_v04_batch21 import ALL_ROWS, PRINTED, issues_for
from source_slices import rows, stream

MILL_DE = stream('de_megaiv2', [(458,15,19)])
MILL_ZH = stream('zh_single', [(195,2,5)], {195:[(',', '，')]})
MILL_ROWS = rows('mill',13,['马克思评注：劳动与自我丧失'],MILL_DE,MILL_ZH,
                 ['Nur als das'], ['我的劳动是什么'])
ROWS = ALL_ROWS[24:] + MILL_ROWS
PRINTED = dict(PRINTED, **{})
PRINTED.update({('de_megaiv2',458):'466',('zh_single',195):'185'})
ROUTES = {'mill':('de_megaiv2','zh_single')}
COVERAGE = {
 'money':'本节正文已从印刷434/359页开头收录至438/365页节尾，共47个项目句群；注释全文及完整范围审计待做。',
 'mill':'精选评注片段13组，德文印刷463—466/中文181—185页内；覆盖起点及全摘录分母待审计，未声称从全篇开头连续收录。',
}

if __name__ == '__main__':
    assert len(ROWS) == 24
    doubts, overrides = issues_for(ROWS)
    main(rows=ROWS, printed=PRINTED, batch=22, release='0.4.0-alpha18',
         reviewed_date='2026-10-19', doubts=doubts, issue_overrides=overrides,
         source_by_section=ROUTES, coverage_notes=COVERAGE,
         row_notes={'mill_013':'此组为马克思评注的收尾，后页块转入穆勒著作摘录。'})
