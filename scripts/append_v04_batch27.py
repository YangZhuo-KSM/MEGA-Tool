"""Batch 27: 24 groups continuing the second manuscript's private-property relation."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


DE = stream('de_megai2', [(376, 26, 29), (377, 2, 42),
                           (378, 2, 42), (379, 3, 10)], {
    377: [('11 so weit', 'II so weit'), ('ausst[kbt]', 'ausst[irbt]'),
          ('nöthigenXosfen', 'nöthigen Kosten'), ('Capitaüsten', 'Capitalisten'),
          ('Theü', 'Theil'), ('producüt', 'producirt'),
          ('geistigwie', 'geistig wie'), ('Immoraütät', 'Immoralität'),
          ('Mül etc', 'Mill etc'), ('engüschen', 'englischen'),
          ('völüger', 'völliger'), ('jährÜchen', 'jährlichen'),
          ('Uebervortheüung', 'Uebervortheilung'),
          ('gesellschaftüches', 'gesellschaftliches'), ('wüküches', 'wirkliches'),
          ('Amendment bül', 'Amendment bill'), ('||XLl|', '||XLI|'),
          ('Capitaüst', 'Capitalist')],
    378: [('Dlusionen', 'Illusionen'), ('Meresse', 'Interesse'),
          ('wtklichen', 'wirklichen')],
    379: [('constituüte', 'constituirte'), ('wüküchen', 'wirklichen'),
          ('eme Verwandlung', 'eine Verwandlung'), ('Mittelgüed', 'Mittelglied')],
}, join_page_hyphens=True)
ZH = stream('zh_collected', [(307, 3, 26), (308, 2, 24), (309, 2, 21)], {
    307: [(',', '，')],
    308: [('关系(，一方面', '关系。一方面'), ('人的活动的生产,', '人的活动的生产，'),
          ('充实的Æ', '充实的无'), ('待质', '特质'),
          ('想像^一一', '想像——'), ('从向使', '从而使'),
          ('亚当•斯密', '亚当·斯密'), (',', '，'), (':', '：'), (';', '；')],
    309: [('地产(贵族生活(封建生活〉①)相对立', '地产（贵族生活（封建生活）①）相对立'),
          ('内容漢不关心', '内容漠不关心'), ('代表,', '代表，'),
          (';', '；')],
})

DE_STARTS = [
    'Die Nationalökonomie kennt daher', 'Der Spitzbube',
    'Die Bedürfnisse des Arbeiters', 'Der Arbeitslohn hat daher ganz denselben Sinn',
    'Der Arbeitslohn gehört daher zu den nöthigen Kosten', 'Es war daher ganz consequent',
    'Die Production producirt den Menschen nicht nur', 'Ihr Product ist die selbstbewußte',
    'Grosser Fortschritt von Ricardo', 'Nicht, wie viel Arbeiter',
    'Es war ebenfalls ein grosser', 'Nicht die Uebervortheilung',
    'Das Verhältniß des Privateigenthums enthält',
    'Die Production der menschlichen Thätigkeit',
    'wie andrerseits die Production', 'dieser Gegensatz auf die Spitze',
    'Es ist daher wieder eine grosse That', 'und die Bewegung der Wirklichkeit',
    'Der Unterschied von Capital und Erde', 'In der Industrie etc',
    'Als eine besondre Art der Arbeit', 'innerhalb welcher Bestimmungen',
    'Aber die nothwendige Entwicklung', 'Mit der Verwandlung des Sklaven',
]
ZH_STARTS = [
    '因此，国民经济学42不知道有失业的', '小偷、骗子、乞丐',
    '因此，在国民经济学看来，工人的需要', '因此，工资就与其他任何生产工具',
    '可见，工资是资本和资本家的必要费用', '因此，英国工厂主在实行1834年的济贫',
    '生产不仅把人当作商品', '这种生产的产品是自我意识的',
    '李嘉图、穆勒等人比斯密', '在他们看来，生产的真正目的',
    '同样，现代[XLI]英国国民经济学88', '不是对消费者诈取',
    '私有财产的关系潜在地包含', '一方面是作为劳动',
    '另一方面是作为资本', '劳动和资本的这种对立',
    '因此，现代英国国民经济学的又一重大成就', '它预料到并且准备了这样一个现实的运动',
    '资本和土地的差别', '同不动的地产相反',
    '这种差别只要在下述情况下', '而在这些形式的规定内',
    '[XLII]但是，获得自由的', '随着奴隶转化为自由工人',
]
LABELS = [
    '国民经济学排除失业工人', '国民经济学领域外的幽灵',
    '工人需要限于维持劳动力', '工资等同生产工具保养',
    '工资是资本的必要费用', '济贫金被扣作工资组成',
    '生产把人变成商品人', '自我意识的商品',
    '人的存在被视为无关紧要', '利息和积攒成为生产目的',
    '工资和资本利息的反比例', '资本家与工人的彼此诈取',
    '私有财产包含劳动和资本', '作为异己劳动的人的活动',
    '作为资本的活动对象', '劳动资本对立的极端',
    '地租差额与土地所有者幻象', '土地所有者转化为资本家',
    '资本土地差别的历史性', '工业与农业对立的产生',
    '工业差别的封建形态', '劳动尚未成为自由资本',
    '自由工业与工业化农业', '奴隶和地主的资本主义转化',
]

ROWS = rows('private_relation', 7, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='Aber der Pächter ist', zh_end='但是，租地农场主是')
PRINTED = {('de_megai2', p): str(p) for p in range(376, 380)}
PRINTED.update({('zh_collected', 307): '282', ('zh_collected', 308): '283',
                ('zh_collected', 309): '284'})
DOUBTS = {
    'private_relation_de_009': ['II'],
    'private_relation_de_017': ['||XLI|'],
    'private_relation_de_023': ['II'],
    'private_relation_de_025': ['der* Sache'],
    'private_relation_de_028': ['||XLII|'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid, {})[word] = dict(
            kind='glyph_doubt', status='open',
            reported_reading='页内标记或校勘符号的转写待复核',
            note='按本地扫描可见形式照录；不依据译文或语义静默改写。')


if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=27, release='0.4.0-alpha23',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES,
         coverage_notes={'private_relation':
             '本节现有开头连续30组，已覆盖德印刷376—379/中文281—284页内；'
             '当前到租地农场主作为地主转化中介句末，后文及全节范围待继续。'})
