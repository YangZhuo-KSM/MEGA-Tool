"""Batch 31: finish the alienated-labor body; retain scan-visible anomalies."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(371, 38, 42), (372, 2, 42),
                           (373, 2, 42), (374, 2, 42), (375, 2, 19)],
            join_page_hyphens=True)
ZH = stream('zh_collected', [(301, 9, 24), (302, 2, 26),
                             (303, 2, 24), (304, 2, 26), (305, 2, 12)], {
    301: [('命题:', '命题：'), ('因此.如果', '因此，如果')],
    302: [(',', '，'), ('(外化的生命)', '（外化的生命）'),
          ('关系、', '关系。'), ('(1)', '（1）')],
    303: [('M然而', '⁸⁴然而'), ('私有財产', '私有财产'), ('同~的', '同一的'),
          (',', '，'), ('结论，', '结论。⁸⁵'), ('(且', '（且'),
          ('提髙', '提高'), ('资本家。86.', '资本家。⁸⁶'), ('(2)', '（2）')],
    304: [(',', '，'), ('<1)', '（1）'), ('<2)', '（2）'),
          ('私有財产', '私有财产'), ('补入(1)', '补入（1）'),
          ('慨括', '概括'), ('两种关系:', '两种关系：')],
    305: [('(作为', '（作为'), ('状态)', '状态）'), (',', '，')],
})
DE_STARTS = [
    'Man bedenke noch', 'Jede Selbstentfremdung', 'Wir haben bis jezt',
    'Also durch die entfremdete', 'Das Privateigenthum ist also',
    'Das Privateigenthum ergiebt sich also', 'Wir haben allerdings',
    'Erst auf dem lezten', 'Diese Entwicklung', '1) Die Nationalökonomie',
    'Wir sehn daher auch ein', 'Eine gewaltsame Erhöhung',
    'Ja selbst die Gleichheit', 'Arbeitslohn ist eine unmittelbare',
    '2) Aus dem Verhältniß', 'Wie wir aus dem Begriff',
    'Bevor wir jedoch', '1) Das allgemeine', '2) Wir haben die Entfremdung',
    'ad.l Allgemeines', 'Wir haben die eine Seite', 'Wenn wir nun gesehn',
    'Zunächst ist zu bemerken', 'Zweitens, daß',
]
ZH_STARTS = [
    '还必须注意上面提到的这个命题', '人同自身和自然界的任何自我异化',
    '到目前为止', '总之，通过异化的、外化的劳动', '因此，私有财产是',
    '因此，我们通过分析', '诚然，我们从国民经济学',
    '私有财产只有发展到最后', '这些论述使', '（1）国民经济学',
    '因此，我们也看到', '强制提高工资', '甚至蒲鲁东所要求',
    '工资是异化劳动', '（2）从异化劳动', '正如我们通过分析',
    '但是，在考察这些范畴', '（1）从私有财产', '（2）我们已经承认',
    '补入（1）', '我们已经考察了一个方面', '我们已经看到，对于',
    '首先必须指出', '其次，工人在生产中',
]
LABELS = [
    '自身关系通过他人关系实现', '自我异化与他人的支配', '工人与非工人的两面',
    '劳动关系产生资本家关系', '私有财产是外化劳动的结果', '从外化劳动分析私有财产',
    '因果关系转为相互作用', '私有财产的双重秘密', '由此阐明经济矛盾',
    '国民经济学的内在矛盾', '工资与私有财产', '提高工资与人的尊严',
    '工资平等与抽象资本家', '工资和私有财产的共同根源', '工人解放与普遍人的解放',
    '从两个因素展开经济范畴', '尚待解决的两个任务', '规定私有财产的普遍本质',
    '劳动异化与人类发展', '占有与外化的两个组成部分', '私有财产包含的两种关系',
    '转向非工人与劳动的关系', '异化活动与异化状态', '实践态度与理论态度及节尾',
]
ROWS = rows('alienation', 61, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(371, 376)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(301, 306)})
DOUBTS = {
    'alienation_de_061': ['||', 'vergegenständÜchten'],
    'alienation_de_062': ['feindüchen', 'Entwirkhchung'],
    'alienation_de_065': ['||'],
    'alienation_de_071': ['Conse||[XX]Vl|[que]nzen'],
    'alienation_de_073': ['Salate'],
    'alienation_de_075': ['weü', 'menschüche', 'Knechtsschaftsverhältnisse',
                          'Modificai|tionen', '(Konsequenzen'],
    'alienation_de_078': ['Wiesen'],
    'alienation_de_080': ['ad.l', '\\', '/in'],
    'alienation_de_084': ['wkkliche', '|', '|XXVIl|'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        if any(mark in word for mark in ('|', '\\', '/in')) or word == 'ad.l':
            OVERRIDES.setdefault(uid, {})[word] = dict(
                kind='glyph_doubt', status='open',
                reported_reading='页内界符或位置标记的转写待复核',
                note='按来源扫描可见形式照录；完整标记与邻字一起保留，待定向复核。')
ROW_NOTES = {'alienation_062': '中文在“力量”处有编者注号①，德文正文为Menschen；保留两底本差异，脚注全文回查中文PDF301。'}

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=31, release='0.4.0-alpha27',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         row_notes=ROW_NOTES, coverage_notes={'alienation':
             '现收录84个句群，已接续至德印刷375/中文280节尾；首部、衔接和注释范围仍待集中审计，全文分母未确定。'})
