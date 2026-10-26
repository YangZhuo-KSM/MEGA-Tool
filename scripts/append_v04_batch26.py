"""Batch 26: 24 groups closing the Mill front-fill immediately before mill_001."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


DE = stream('de_megaiv2', [(453, 27, 42), (454, 2, 42), (455, 2, 10)])
ZH = stream('zh_single', [(189, 15, 28), (190, 1, 26), (191, 1, 6)], {
    189: [('‘需求”', '‘需求’'), ('意味看', '意味着'), ('购头愿望', '购买愿望'),
          ('供目己', '供自己'), ('他的求', '他的需求'),
          ('第252一253页', '第252—253页'),
          (',', '，'), (':', '：')],
    190: [('功利的目的而且', '功利的目的，而且'),
          ('变换归结', '交换归结'), ('消贾关系', '消费关系'),
          ('LXXXII」', '[XXXII]'), (',', '，'), (';', '；')],
    191: [(',', '，')],
})

DE_STARTS = [
    '»Zwei Sachen sind nöthig', 'Eine demande bezeichnet',
    'Der Besitz eines aequivalenten Gegenstandes', 'Das äquivalente Objekt',
    'Die Nachfrage und der aequivalente Gegenstand', 'Man hat schon gesehn',
    'Eben so evident ist es', 'Mill analysirt hier',
    'Der Mensch — dieß ist die Grundvoraussetzung',
    'Und nicht nur hat die Production', 'Der Mensch, für sich',
    'Der Mensch producirt daher in diesem Zustand',
    'Die Grenze seines Bedürfnisses', 'In diesem Fall findet kein Austausch',
    'Sobald der Austausch stattfindet', 'Diese Mehrproduktion ist aber keine Erhebung',
    'Die Production ist zur Erwerbsquelle', 'Während also in dem ersten Verhältniß',
    'Ich habe für mich producirt', 'Das Resultat meiner Production',
    'D. h. unsere Productionen', 'Als Mensch hat also keiner von uns',
    'Unser Austausch kann daher auch nicht', 'Der Austausch kann nur in Bewegung setzen',
]
ZH_STARTS = [
    '“构成需求必须有两个条件', '‘需求’这一用语意味着',
    '拥有等价物品是任何一种需求', '一个人所提供的等价物品',
    '需求和等价物品是两个可以相互代替', '我们已经看到',
    '同样明显的是', '穆勒在这里以其惯于嘲讽',
    '人——这是私有制的基本前提', '生产不仅有这样一种功利的目的',
    '因此，人本身——在未开化的野蛮状态下',
    '因此，人在这种状态下生产的东西', '他需要的界限',
    '在这种情况下就没有交换', '一旦有了交换',
    '但是这种剩余产品并没有超出', '生产成为收入的来源',
    '可见，在第一种情况下', '我是为自己而不是为你生产',
    '我的生产的结果本身', '换句话说，我们的生产',
    '也就是说，我们中间没有一个人', '因此，我们的交换也就不可能',
    '交换只能导致运动',
]
LABELS = [
    '穆勒摘录：构成需求的两个条件',
    '穆勒摘录：需求是愿望和购买手段',
    '穆勒摘录：等价物是需求基础',
    '穆勒摘录：等价物是需求工具',
    '穆勒摘录：需求与等价物可互换',
    '穆勒摘录：生产总量衡量需求',
    '穆勒摘录：购买愿望与手段相等',
    '马克思评注：私有制交换的分析',
    '马克思评注：生产的目的是拥有',
    '马克思评注：生产的利己目的',
    '马克思评注：直接需要衡量生产',
    '马克思评注：生产不超过直接需要',
    '马克思评注：需要与供给相抵',
    '马克思评注：交换的潜在形式',
    '马克思评注：交换产生剩余产品',
    '马克思评注：剩余产品仍服务利己需要',
    '马克思评注：生产成为谋生劳动',
    '马克思评注：需要和占有的两种尺度',
    '马克思评注：各自为自己生产',
    '马克思评注：生产结果彼此无关',
    '马克思评注：生产缺少社会性',
    '马克思评注：彼此产品没有享受关系',
    '马克思评注：交换不以人的本质为纽带',
    '马克思评注：交换确认对象化私利',
]

ROWS = rows('mill', 86, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {
    ('de_megaiv2', 453): '461', ('de_megaiv2', 454): '462',
    ('de_megaiv2', 455): '463', ('zh_single', 189): '179',
    ('zh_single', 190): '180', ('zh_single', 191): '181',
}
SEQUENCES = {f'mill_{number:03}': -19976 + offset for offset, number in enumerate(range(86, 110))}
NOTES = {
    f'mill_{number:03}': (
        '此组转录穆勒供需论摘录；所摘观点不能整体直接视作马克思主张。'
        if number <= 92 else
        '此组为马克思对私有制交换、生产和人的关系的评注。'
    )
    for number in range(86, 110)
}
DOUBTS = {
    'mill_de_090': ['e/i2er dem andern'],
    'mill_de_103': ['2tcn'],
    'mill_de_108': ['||XXXII.|'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid, {})[word] = dict(
            kind='glyph_doubt', status='open',
            reported_reading='页内位置、缩写或插入字形待辨',
            note='按本地扫描可见候选照录；不依据译文或语义静默改写。')


if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=26, release='0.4.0-alpha22',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES, row_notes=NOTES, sequence_overrides=SEQUENCES,
         coverage_notes={'mill':
             '现有稳定ID保留；后补前部用mill_062—109及负sequence排在mill_001之前。'
             '已覆盖德印刷456及459—470/中文175—189页内；德印刷457—458及更前范围待审计。'})
