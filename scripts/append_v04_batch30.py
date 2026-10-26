"""Batch 30: 24 groups continuing the first manuscript's alienated-labor section."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


DE = stream('de_megai2', [(369, 6, 42), (370, 2, 42), (371, 2, 38)], {
    369: [('leztere', 'letztere'), ('ein Bewußtes Wesen', 'ein bewußtes Wesen'),
          ('Bearbeitungaex', 'Bearbeitung d[er]'),
          ('Bedürf nisses', 'Bedürfnisses')],
    370: [('Wirldichkeit', 'Wirklichkeit'),
          ('gegenständhchkeit', 'gegenständlichkeit'),
          ('seift unorganischer', 'sein unorganischer'),
          ('Selbsttätigkeit', 'Selbstthätigkeit'),
          ('seingeistige[s]', 'sein geistige[s]'), ('Mííei', 'Mittel'),
          ('das gut von dem Verhältniß', 'das gilt von dem Verhältniß')],
    371: [('entf remdete[n]', 'entfremdete[n]'), ('Wü', 'Wir'),
          ('Wirküchkeit', 'Wirklichkeit'), ('Die Götterl', 'Die Götter!'),
          ('ζ. B.', 'z. B.'), ('eme fremde', 'eine fremde'),
          ('mögüch', 'möglich'), ('seme Thätigkeit', 'seine Thätigkeit')],
}, join_page_hyphens=True)
ZH = stream('zh_collected', [(297, 23, 24), (298, 2, 26),
                              (299, 2, 26), (300, 2, 26), (301, 2, 9)], {
    297: [('（1)', '（1）'), ('（2)', '（2）'), (';', '；'), (',', '，')],
    298: [('第~，', '第一，'), ('目的。83', '目的。⁸³'),
          ('对象3仅仅', '对象。仅仅'), (';', '；')],
    299: [('他听创造', '他所创造'), ('自然界.使', '自然界，使'),
          ('(3)', '（3）'), ('(4)', '（4）'), ('适甩于', '适用于'),
          (',', '，')],
    300: [('概念:异化', '概念：异化'), ('矛盾:', '矛盾：')],
    301: [('如杲', '如果'), ('~种', '一种')],
})

DE_STARTS = [
    'Indem die entfremdete Arbeit dem Menschen',
    'Denn erstens erscheint d[em] Menschen',
    'Das Thier ist unmittelbar eins',
    'Das praktische Erzeugen einer gegenständlichen Welt',
    'Eben in der Bearbeitung der gegenständlichen Welt',
    'Indem daher die entfremdete Arbeit',
    'Ebenso indem die entfremdete Arbeit',
    'I Das Bewußtsein, welches der Mensch',
    'Die entfremdete Arbeit macht also',
    '3) das Gattungswesen des Menschen',
    '4) Eine unmittelbare Consequenz davon',
    'Ueberhaupt der Satz, daß dem Menschen',
    'Die Entfremdung d[es] Menschen',
    'Also betrachtet in dem Verhältniß',
    '|XXV| Wir gingen aus von einem nationalökonomischen factum',
    'Sehn wir nun weiter',
    'Wenn das Produkt der Arbeit mir fremd ist',
    'Wenn meine eigne Thätigkeit nicht mir gehört',
    'Einem andern Wesen als mir',
    'Wer ist dieß Wesen',
    'Die Götter!',
    'Allerdings erscheint in den ersten Zeiten',
    'Das fremde Wesen, dem die Arbeit',
    'Wenn das Product der Arbeit nicht dem Arbeiter gehört',
]
ZH_STARTS = [
    '异化劳动，由于（1）使自然界',
    '因为，首先，劳动这种生命活动',
    '动物和自己的生命活动是直接同一的',
    '通过实践创造对象世界',
    '因此，正是在改造对象世界中',
    '因此，异化劳动从人那里夺去了他的生产的对象',
    '同样，异化劳动把自主活动',
    '因此，人具有的关于自己的类的意识',
    '这样一来，异化劳动导致',
    '（3）人的类本质',
    '（4）人同自己的劳动产品',
    '总之，人的类本质同人相异化',
    '人的异化，一般地说',
    '因此，在异化劳动的条件下',
    '[XXV]我们的出发点是经济事实',
    '现在让我们看一看',
    '如果劳动产品对我来说是异己的',
    '如果我自己的活动不属于我',
    '属于另一个有别于我的存在物',
    '这个存在物是谁呢',
    '是神吗',
    '确实，起初主要的生产活动',
    '劳动和劳动产品所归属的那个异己的存在物',
    '如果劳动产品不属于工人',
]
LABELS = [
    '异化劳动使类生活成为手段', '生产生活与类生活',
    '有意识的生命活动', '人和动物生产的差别',
    '对象世界证明类存在', '异化劳动夺走类生活',
    '自由活动降为生存手段', '类意识变为手段意识',
    '异化劳动的结论', '类本质变为异己手段',
    '人同人相异化', '类本质异化的普遍命题',
    '人的异化通过他人关系实现', '异化劳动中的他人尺度',
    '从经济事实到异化劳动概念', '在现实中说明异化劳动',
    '劳动产品属于谁', '异己活动属于谁',
    '属于另一个存在物', '追问异己存在物',
    '神的候选答案', '神和自然都不是劳动主人',
    '异己存在物只能是人', '他人享有工人活动的成果',
]

ROWS = rows('alienation', 37, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='Man bedenke noch', zh_end='还必须注意上面提到的这个命题')
PRINTED = {('de_megai2', p): str(p) for p in range(369, 372)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(297, 302)})
DOUBTS = {
    'alienation_de_038': ['||'],
    'alienation_de_043': ['|'],
    'alienation_de_044': ['I'],
    'alienation_de_050': ['|'],
    'alienation_de_051': ['|XXV|'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid, {})[word] = dict(
            kind='glyph_doubt', status='open',
            reported_reading='页内界符、位置标记或罗马数字的转写待复核',
            note='按本地扫描可见形式照录；不依据译文或语义静默删除或改写。')


if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=30, release='0.4.0-alpha26',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES,
         coverage_notes={'alienation':
             '本节现有开头连续60组，覆盖德印刷364—371/中文267—276；'
             '当前到异己力量只能属于工人之外的他人段末，后文及全节范围待继续。'})
