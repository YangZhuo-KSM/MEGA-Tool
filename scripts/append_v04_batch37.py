"""Batch 37: profit 025--048, commercial secrets through capital accumulation."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(340, 33, 42), (341, 2, 43), (342, 2, 38)], {
    341: [('Manuf actur', 'Manufactur')],
}, join_page_hyphens=True)
ZH = stream('zh_collected', [(265, 24, 29), (266, 2, 25), (267, 2, 25)], {
    265: [(';', '；'), ('髙', '高'), (':', '：'), ('(以', '（以'), ('交易。)', '交易。）')],
    266: [('待定', '特定'), ('葡萄酒)', '葡萄酒）'), ('最髙', '最高'), ('124页)', '124页）'),
          ('冨国', '富国'), ('提髙', '提高'), ('每--后', '每一后'), ('増加', '增加'),
          (';', '；'), ('死资木', '死资本'), ('丄资扣比', '工资相比'), ('同—水平', '同一水平'), ('228页)', '228页）')],
    267: [('手段(', '手段（'), ('使用,', '使用，'), ('髙', '高'), ('阶级,', '阶级，'),
          ('163-165', '163—165'), ('増加', '增加')],
})
DE_STARTS = [
    'Einmal: durch Handelsgeheimniß', 'Dann: durch Fabrikgeheimniß', 'Ferner: wo die Production',
    'Endlich: durch Monopole', 'Andre zufällige Ursachen', 'Erwerbung von neuen Territorien',
    'Je mehr eine Waare', 'In dem Fortschritt', 'Das Capital, welches die Leinweber',
    'Der Fortschritt, den also', 'Ueber den Gewinn', 'Er gewinnt doppelt',
    'In einer und derselben Gesellschaft', 'Bei den verschiedenen Anwendungen', 'Es versteht sich von selbst',
    '3) Die Herrschaft', 'Die nützlichste Anwendung', 'Die wichtigsten Operationen',
    'Also: Die Taxe', 'Das Interesse dieser Klasse', 'Das besondre Interesse',
    'Das Interesse des Kaufmanns', 'Es ist dieß eine Klasse', '4) Die Accumulation',
]
ZH_STARTS = [
    '首先，如果那些', '其次，利用制造业秘密', '再次，把生产', '最后，利用个人',
    '可能提高资本利润', '新领土的获得', '商品加工越多', '随着对商品加工', '雇用织工的资本',
    '由此可见，在对自然产品', '关于资本家从分工', '资本家是双重获利', '在同一社会',
    '各种不同用途', '不言而喻', '三、资本对劳动', '对资本家来说', '最重要的劳动操作',
    '就是说：利润率', '因此，这一阶级', '经营某一特殊', '商人的利益', '这是这样一些人的阶级',
    '四、资本的积累',
]
LABELS = [
    '商业秘密与价格保密', '制造业秘密与利润', '生产地点与有效需求', '个人和公司垄断',
    '提高利润的偶然原因', '新领土和新行业', '加工与价格构成', '手工劳动与后续利润',
    '织工和纺工的资本', '加工劳动与资本增长', '分工获利的后续讨论', '资本家的双重获利',
    '平均利润率与工资差异', '资本回收风险与利润率', '流通手段与利润', '资本对劳动的统治与投资动机',
    '资本家与社会的有利用途', '劳动操作的计划与利润目的', '利润率与社会盛衰',
    '资本阶级与社会利益', '特殊行业与公众利益', '扩大市场和限制竞争',
    '商人阶级的利益', '资本积累竞争与利润减少',
]
ROWS = rows('profit', 25, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(340, 343)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(265, 268)})
SUSPECTS = ['ζ.', 'LI', 'Compaginen', 'Capitaüen', 'weü', 'Theü', 'gehehne', 'wüd',
            '||IV|', 'Salaüe', 'theüs', 'Capitaüst', 'Theüung', 'menschüche', 'Antheü',
            'gewöhnüche', 'voüständiger', 'Kostspieügkeit', 'Cüculationsmittel', '||V|', 'Π']
DOUBTS = {f'{s}_de_{n:03}': [w for w in SUSPECTS if w in de] for s, n, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                          reported_reading='底本标记或字形待复核',
                          note='按扫描可见形式照录，保留底本定位符号；未据译文统一。')
                  for w in words if '|' in w or w in ('ζ.', 'LI', 'Π')}
             for uid, words in DOUBTS.items()}

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=37, release='0.4.0-alpha33',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES)
