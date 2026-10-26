"""Batch 39: profit 073--096, fixed capital and excerpts on competition."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(345, 23, 42), (346, 2, 42), (347, 2, 42), (348, 2, 41)], {
    345: [(',Jede Ersparung', '„Jede Ersparung')],
}, join_page_hyphens=True)
ZH = stream('zh_collected', [(270, 20, 28), (271, 2, 28), (272, 2, 30), (273, 2, 26), (274, 2, 4)], {
    270: [('原状.', '原状，'), ('增长3', '增长。'), ('其中-部分', '其中一部分')],
    271: [('咸少', '减少'), ('。”(', '。”（'), ('髙', '高'), ('喩', '喻'), ('地方,', '地方，'),
          ('那样,', '那样，'), ('须域', '领域'), ('进~步', '进一步'), ('负偾', '负债'), (';', '；'),
          ('（生产运动〉', '《生产运动》'), ('改变,', '改变，')],
    272: [('降低菩', '降低11/12'), ('马歌尔', '马歇尔'), ('18M年', '1814年'), ('消费.', '消费，'),
          ('咸少', '减少'), ('1820—1833', '1820—1833'), ('1■便士', '1 1/3便士'), ('结桌', '结果'),
          ('个别--些', '个别一些'), ('过剰', '过剩'), (';', '；'), ('。”(', '。”（'), ('63页)', '63页）'),
          ('<社会', '《社会'), ('理论〉', '理论》'), ('官有', '富有'), ('自已', '自己'),
          ('{同上', '（同上'), ('412页])', '412页]）'), ('肀均', '平均'), ('—个成年人', '一个成年人'),
          ('间接池', '间接地'), ('因而,', '因而，'), ('(路易-菲力浦', '（路易-菲力浦'),
          ('劳动。〉', '劳动。）'), ('同上.', '同上，'), ('賦千', '赋予'), ('支配,', '支配，'),
          ('物品。•’', '物品。”'), ('第W3页', '第413页')],
    273: [("'•竞争", '“竞争'), (':', '：'), ('过我', '过贱'), ('財富', '财富'), (';', '；'),
          ('浪费。"', '浪费。”'), ('414一416', '414—416'), ('书①(', '书①（')],
    274: [('①"德•西', '①“德·西'), ('先生说(', '先生说（'), ('〈Kurbel〉', '〈Kurbel〉')],
})
DE_STARTS = [
    '„Capital circulant', 'Capital fixe besteht', '„Jede Ersparung', 'Das Gesammtcapital',
    'Bei der Gleichheit', 'Das capital cüculant', 'Also jede Ersparniß', 'Man sieht von vorn herein',
    'Ein sehr grosser Banquier', 'Die Instrumente eines grossen', 'Ebenso ist der Credit',
    'Es versteht sich endlich', 'Ueberhaupt findet', '„Ebenso ist im Bereiche', '„Die Beschaffenheit',
    '„Im Durchschnitt', '«Louer son travaü', "«l'élément matière", '«En supposant',
    '«les propriétaües', '«überté entière', '«La concurrence', 'Ricardo in seinem Buch', '«H serait',
]
ZH_STARTS = [
    '“流动资本是', '固定资本是', '“固定资本维持费', '任何企业家的总资本', '只要资本总额',
    '流动资本供他', '因此，固定资本的任何节约', '从一开头', '最大的银行家', '大土地占有者',
    '同样，大资本家', '最后，不言而喻', '与较小的资本家相比', '“同样，在工业领域',
    '“同一种商品', '“四十五年来', '“出租自己的劳动', '“材料要素', '“假定一个工人',
    '“人们制定的法律', '“对生产的性质', '“竞争不过是', '李嘉图在他的书', '“对于一个拥有',
]
LABELS = [
    '流动资本的循环', '固定资本的用途', '固定资本节约与纯利润', '总资本的两种构成',
    '固定和流动资本的此消彼长', '流动资本购买原料和劳动', '固定资本节约与工业基金',
    '资本比例有利于大资本', '银行家的固定资本', '大土地所有者的工具', '信用节约准备货币',
    '工厂劳动与小资本门槛', '固定资本积聚和工具组织', '舒尔茨论大地产和工业',
    '机器改变商品性质', '棉纺织降价利润与生产过剩', '贝魁尔论出租劳动和材料',
    '材料所有权的财富魔力', '租金收入与他人劳动', '所有者使用滥用的法律权利',
    '生产和交换的自由', '任意交换竞争及其后果', '李嘉图的生产世界', '人口与纯收入及西斯蒙第评语',
]
ROWS = rows('profit', 73, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(345, 349)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(270, 275)})
SUSPECTS = ['wüd', 'Cüculation', 'theüt', 'cüculant', 'Theü', 'üefert', 'Salaüe', '/|Xl|',
            'f ortgesezte', 'Guiñeen', 'um1V12', '181416', 'Mande', 'IV2', '|¡XIl|', 'IV3',
            'travaü', 'hberté', 'contraüe', "s'üs", 'propriétaüe', 'üidüectement', 'travaüler',
            'Mülionen', 'Phüippe', 'propriétaües', "qu'Us", 'üs', 'f ournü', 'salaüe',
            'überté', 'quaüté', 'übre', 'ü', '|[XIIl|', 'Π', 'rinstabilité', 'Le.', 'H']
DOUBTS = {f'{s}_de_{n:03}': [w for w in SUSPECTS if w in de] for s, n, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                          reported_reading='可见定位符或数字/字形候选待复核',
                          note='扫描可见形式照录；数字连排、分数及页内标记未按译文改写，保留待审。')
                  for w in words if '|' in w or w in ('um1V12', '181416', 'IV2', 'IV3', 'Π', 'H')}
             for uid, words in DOUBTS.items()}
for word in ('Mande', 'IV2', '|¡XIl|', 'IV3'):
    OVERRIDES['profit_de_088'].setdefault(word, {})['evidence_pages'] = ['de_megai2:347']

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=39, release='0.4.0-alpha35',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES)
