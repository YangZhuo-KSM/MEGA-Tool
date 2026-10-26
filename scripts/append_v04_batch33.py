"""Batch 33: wages 025-048, ending before the Schulz quotation."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(330, 41, 42), (331, 2, 42),
                           (332, 2, 42), (333, 2, 19)], join_page_hyphens=True)
ZH = stream('zh_collected', [(254, 20, 23), (255, 2, 26),
                             (256, 2, 25), (257, 2, 22)], {
    254: [('(3广', '（3）“')],
    255: [('道受', '遭受'), ('逭受', '遭受'), ('国民经济学42(', '国民经济学⁴²（'),
          ('私人利益的社会)', '私人利益的社会）'), ('提髙', '提高'),
          (',', '，'), (';', '；'), ('价格C', '价格。'), ('这么多:', '这么多：')],
    256: [(';', '；'), ('提髙', '提高'), ('活动•，', '活动；'), (',', '，'),
          ('（1)', '（1）'), ('（2)', '（2）'), ('増', '增')],
    257: [('最富裕状态.', '最富裕状态，'), ('市民社会2', '市民社会⁴³'),
          (',', '，'), ('(1)', '（1）'), ('(2)', '（2）'), ('提髙', '提高'), ('目标《', '目标⁶⁵')],
})
DE_STARTS = [
    '3) „In einem Land', 'Das Plus müßte', 'Also im abnehmenden', '|Vl| Da aber',
    'In Bezug auf das Verhältniß', 'Stellen wü uns', 'Er sagt uns',
    'Der Nationalökonom sagt uns', 'Während die Grundrente',
    '|VIl| Während nach', 'Während nach d[em] Nationalökonomen die Arbeit der einzig',
    'Während die Theilung', 'Während das Interesse', 'Nach d[em] Nationalökonomen steht',
    'Daß die Arbeit aber selbst', 'Nach dem Begriff', 'Im verfallenden Zustand',
    'Aber im fortschreitenden', 'Der reichste Zustand', 'Es versteht sich von selbst',
    'Erheben wir uns nun', '1) Welchen Sinn', '2) Welche Fehler', 'Die Arbeit kömmt nur',
]
ZH_STARTS = [
    '（3）“在财富', '超过这个人数', '因此，在社会的衰落', '[VI]但是',
    '关于工人和资本家', '现在让我们完全站在', '国民经济学家对我们说，劳动的全部产品',
    '国民经济学家对我们说，一切东西', '懒惰的土地占有者',
    '[VII]按照国民经济学家的意见', '按照国民经济学家的意见，劳动是惟一',
    '分工提高劳动的生产力', '按照国民经济学家的意见，工人的利益',
    '按照国民经济学家的意见，工人的利益', '劳动本身，不仅', '按照理论，地租',
    '在社会的衰落状态中，工人遭受', '而在社会的增长', '社会的最富裕状态',
    '不言而喻', '现在让我们超出', '（1）把人类', '（2）主张细小改革', '劳动在国民经济学中',
]
LABELS = [
    '财富顶点的工资与利息', '过剩人口的生存', '三种社会状态的贫困',
    '经济学目的与社会不幸', '工资和资本利息影响价格', '从经济学家的立场比较',
    '产品归属与工人所得', '积累劳动与出卖人性', '地租利润和工人所得',
    '劳动财产与特权者支配', '不变物价与工资波动', '分工财富与工人的贫困',
    '工人与社会利益的对立', '工人利益不冲突的经济学理由', '增长财富目的下的劳动',
    '工资扣除的理论与现实', '衰落状态与工人压迫', '增长状态中的劳动贫困',
    '富裕理想与持续贫困', '无产者作为工人与作为人', '超出国民经济学的两个问题',
    '抽象劳动的人类发展意义', '细小改革与工资平等', '谋生活动的经济学形式',
]
ROWS = rows('wages', 25, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(330, 334)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(254, 258)})
SUSPECTS = ['|Vl|', '|VIl|', '||', '|', 'GeseUschaft', 'Capitaüst', 'Capitaüsten',
            'compensüt', 'wüd', 'wüken', 'wü', 'Wüklichkeit', 'aUerunumgänglichste',
            'Theü', 'aUes', 'seme', 'FaU', 'er sezt', 'Krirninaljustiz', 'détaü', 'woüen']
DOUBTS = {f'{section}_de_{number:03}': [w for w in SUSPECTS if w in de]
          for section, number, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                           reported_reading='页内位置标记或界符待复核',
                           note='按扫描可见形式保留，待用户定向核查。')
                   for w in words if '|' in w} for uid, words in DOUBTS.items()}

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=33, release='0.4.0-alpha29',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         coverage_notes={'wages': '节首连续48句群，至德印刷333/中文232“劳动仅以谋生活动形式出现”句末；后续舒尔茨引文与其余正文待续。中文PDF250插图、251空白独立登记。'})
