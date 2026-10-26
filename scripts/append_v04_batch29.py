"""Batch 29: 24 groups continuing the first manuscript's alienated-labor section."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


DE = stream('de_megai2', [(366, 11, 42), (367, 2, 42),
                           (368, 2, 42), (369, 2, 6)], {
    366: [('er sezt', 'ersezt'), ('wirf t', 'wirft'),
          ('Creünismus', 'Cretinismus'), ('wesentüche', 'wesentliche')],
    367: [('ausserihr', 'ausser ihr'), ('wüd', 'wird'),
          ('äusserüche', 'äusserliche'), ('Aüsserlichkeit', 'Äusserlichkeit'),
          ('Reügion', 'Religion'), ('Hüns', 'Hirns'),
          ('göttüche', 'göttliche'), ('wükt', 'wirkt'),
          ('menschüchen', 'menschlichen')],
    368: [('lezten', 'letzten'), ('|XXTV|', '|XXIV|'),
          ('Tbiere', 'Thiere')],
}, join_page_hyphens=True)
ZH = stream('zh_collected', [(294, 14, 26), (295, 2, 26),
                              (296, 2, 26), (297, 2, 23)], {
    294: [('主体冰[能]', '主体才[能]'),
          ('不考察；冬(劳动〉同产品的草哮关系', '不考察工人（劳动）同产品的直接关系'),
          ('宫殷', '宫殿'), ('(', '（'), (':', '：'), (';', '；'), (',', '，')],
    295: [('生产丁愚钝', '生产了愚钝'), ('舒杨', '舒畅'),
          ('因比', '因此'), (',', '，')],
    296: [('第―，', '第一，'), ('------种', '——一种'),
          ('人(工人）', '人（工人）'), ('脫离', '脱离'),
          ('。81他的活动', '。⁸¹他的活动'),
          (':', '：'), (';', '；')],
    297: [('对待。82', '对待。⁸²'), ('对象(材料）', '对象（材料）'),
          ('（1)', '（1）'), ('（2)', '（2）'),
          ('人(和动物一样)', '人（和动物一样）'),
          (';', '；'), (',', '，')],
})

DE_STARTS = [
    'Nach dieser doppelten Seite hin',
    '(Die Entfremdung des Arbeiters',
    '\\Die Nationalökonomie verbirgt',
    'Die Arbeit producirt Wunderwerke',
    'Das unmittelbare Verhältniß der Arbeit',
    'Das Verhältniß d[es] Vermögenden',
    'Wir haben bisher die Entfremdung',
    'Worin besteht nun die Entäusserung',
    'Erstens, daß die Arbeit dem Arbeiter',
    'Der Arbeiter fühlt sich daher',
    'Seine Arbeit ist daher nicht freiwillig',
    'Ihre Fremdheit tritt darin rein hervor',
    'Die äusserliche Arbeit',
    'Endlich erscheint die Äusserlichkeit',
    'Es kömmt daher zu dem Resultat',
    'Essen, Trinken und Zeugen etc. sind zwar',
    'Wir haben den Akt der Entfremdung',
    '2) Das Verhältniß der Arbeit',
    '|XXIV| Wir haben nun noch eine dritte',
    'Der Mensch ist ein Gattungswesen',
    'Das Gattungsleben, sowohl beim Menschen',
    'Wie Pflanzen, Thiere, Steine',
    'Physisch lebt der Mensch nur',
    'Die Universalität des Menschen erscheint',
]
ZH_STARTS = [
    '因此，工人在这两方面成为自己的对象的奴隶',
    '（按照国民经济学的规律',
    '国民经济学由于不考察工人（劳动）同产品的直接关系',
    '劳动为富人生产了奇迹般的东西',
    '劳动对它的产品的直接关系',
    '有产者对生产对象和生产本身的关系',
    '以上我们只是从一个方面',
    '那么，劳动的外化表现在什么地方呢',
    '首先，劳动对工人来说是外在的东西',
    '因此，工人只有在劳动之外才感到自在',
    '因此，他的劳动不是自愿的劳动',
    '劳动的异己性完全表现在',
    '外在的劳动，人在其中使自己外化的劳动',
    '最后，对工人来说，劳动的外在性表现在',
    '因此，结果是，人（工人）只有在运用自己的动物机能',
    '吃、喝、生殖等等',
    '我们从两个方面考察了实践的人的活动即劳动的异化行为',
    '第二，在劳动过程中劳动对生产行为的关系',
    '[XXIV]我们现在还要根据',
    '人是类存在物',
    '无论是在人那里还是在动物那里',
    '从理论领域来说',
    '人在肉体上只有靠这些自然产品',
    '在实践上，人的普遍性正是表现为这样的普遍性',
]
LABELS = [
    '对象奴役的双重条件', '异化的国民经济学表现',
    '国民经济学遮蔽劳动异化', '劳动为富人与工人的相反生产',
    '劳动与产品的直接关系', '有产者关系是前一关系的后果',
    '从产品异化转向生产活动', '劳动外化的问题',
    '劳动的外在性', '劳动内外的自我感受',
    '强制劳动及其手段性质', '劳动异己性的显现',
    '外在劳动是自我牺牲', '劳动属于他人',
    '人的机能与动物机能颠倒', '抽象后的动物机能',
    '异化劳动的对象关系', '异化劳动的活动关系',
    '异化劳动的第三个规定', '人作为类存在物',
    '人和动物的无机自然范围', '自然作为精神与实践对象',
    '自然产品维持肉体生活', '自然界是人的无机身体',
]

ROWS = rows('alienation', 13, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='Indem die entfremdete Arbeit', zh_end='异化劳动，由于')
PRINTED = {('de_megai2', p): str(p) for p in range(366, 370)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(294, 298)})
DOUBTS = {
    'alienation_de_014': ['|'],
    'alienation_de_015': ['\\'],
    'alienation_de_023': ['||'],
    'alienation_de_030': ['|'],
    'alienation_de_031': ['|XXIV|'],
    'alienation_de_036': ['\\ Materie'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid, {})[word] = dict(
            kind='glyph_doubt', status='open',
            reported_reading='页内界符、位置标记或校勘符号的转写待复核',
            note='按本地扫描可见形式照录；不依据译文或语义静默删除或改写。')


if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=29, release='0.4.0-alpha25',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES,
         coverage_notes={'alienation':
             '本节现有开头连续36组，覆盖德印刷364—369/中文267—272；'
             '当前到自然界作为人的无机身体段末，后文及全节范围待继续。'})
