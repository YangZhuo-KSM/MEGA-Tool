"""Batch 25: 24 source-ordered groups from the missing front of the Mill section."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


DE = stream('de_megaiv2', [(450, 2, 42), (451, 2, 42), (452, 2, 42), (453, 2, 27)], {
    451: [('1001. St.', '100l. St.'), ('Oer Werth', 'Der Werth')],
    452: [('Lils achète', '»ils achète')],
})
ZH = stream('zh_single', [(185, 15, 26), (186, 1, 25), (187, 1, 25),
                          (188, 1, 28), (189, 1, 15)], {
    185: [(',', '，'), (';', '；'),
          ('多样化人', '多样化，人'), ('相异化同人的', '相异化。同人的'),
          ('工便人成为', '工使人成为'), ('不冉', '不再')],
    186: [(',', '，'), (';', '；'), (':', '：'),
          ('活动和精神', '活动和享受'), ('包含看', '包含着'), ('目身', '自身'),
          ('便得目我异化', '使得自我异化'),
          ('14生产和消费', '¹⁰⁴生产和消费')],
    187: [('9.“', '§9.“'), ('810.', '§10.'), ('811.', '§11.'),
          ('812.', '§12.'), ('813.', '§13.'), ('100锈', '100镑'),
          ('价康', '价廉'), ('价贯', '价贵'), ('贯金属', '贵金属'),
          ('贱头贵卖', '贱买贵卖'),
          ('第137一138页', '第137—138页'), (',', '，'), (':', '：')],
    188: [('81.消费', '§1.消费'), ('不是于段', '不是手段'),
          ('第238一239页', '第238—239页'),
          ('第1241」一242页)“', '第[241]—242页)。“'),
          ('第[242]一243页', '第[242]—243页'),
          (',', '，'), (';', '；'), (':', '：')],
    189: [('LXXX1」', '[XXXI]'), ('把它们脱手', '把它脱手'),
          ('撒开不谈', '撇开不谈'), ('第251一252页', '第251—252页'),
          (',', '，'), (';', '；'), (':', '：')],
})

DE_STARTS = [
    'Je grösser, je ausgebildeter', 'Wie der wechselseitige Austausch',
    'Grade die Einheit der menschlichen Arbeit',
    'Innerhalb der Voraussetzung der Theilung der Arbeit',
    'Im Geld, der vollständigen Gleichgültigkeit', '|XXX. I Es versteht sich',
    'Die Trennung der Arbeit von sich selbst', 'Man unterstelle nun den Fall',
    '§ 9. Wenn 2 Individuen', '§ 10. Ersparung',
    '§ 11. Die Unbequemlichkeiten', '§ 12. Edle Metalle',
    '§ 13. Der Werth', '§ 14. Das Verhältniß', '4) De la consommation.',
    '§ 1. Die Consumtion ist: 1) produktiv.', '2) improduktive Consumtion.',
    '»Was man produktiv', 'Der produktiven und improduktiven Consumtion',
    '§ 2. Alles, was im Lauf eines Jahres', '§ 3. Die Consumtion dehnt sich aus',
    'Bei der Theilung der Arbeit beschränkt', 'Producirt ein Mensch für sich selbst',
    'Sprechen wir hier von offre und demande',
]
ZH_STARTS = [
    '因此，在私有权关系的范围内', '同人的活动的产品的相互交换',
    '现在正是人的劳动的统一', '在分工的前提下',
    '在不论对材料的性质', '[XXX]不言而喻', '劳动同它自身的分离',
    '现在假定有这样一个情况', '§9.“如果两个人', '§10.通过纸币',
    '§11.“使用纸币的弊端', '§12.贵金属是商品',
    '§13.“贵金属的价值', '§14.国家之间的关系', '四论消费',
    '§1.消费分为：(1)生产性消费', '(2)非生产性消费',
    '“生产地消费的东西总是资本', '与生产性消费和非生产性消费相应',
    '§2.“在一年内生产的一切', '§3.“消费随着生产的扩大而扩大',
    '在分工的情况下', '“如果一个人只为自己生产',
    '我们在这里谈论供给和需求',
]
LABELS = [
    '马克思评注：私有权中的社会力量与异化',
    '马克思评注：产品交换与分工',
    '马克思评注：劳动统一表现为分离',
    '马克思评注：等价物与交换中介',
    '马克思评注：货币中物对人的统治',
    '马克思评注：国民经济学把发展视为事实',
    '马克思评注：劳动资本地产的分离',
    '穆勒摘录：政府固定货币量',
    '穆勒摘录：债券与汇票',
    '穆勒摘录：纸币节省非生产性消费',
    '穆勒摘录：纸币的弊端',
    '穆勒摘录：贵金属的进出口',
    '穆勒摘录：贵金属的价值',
    '穆勒摘录：国家间的商人关系',
    '穆勒摘录：生产交换是消费的手段',
    '穆勒摘录：生产性消费',
    '穆勒摘录：非生产性消费',
    '穆勒摘录：生产消费与年度纯产品',
    '穆勒摘录：生产性和非生产性劳动',
    '穆勒摘录：年度产品的消费',
    '穆勒摘录：消费随生产扩大',
    '穆勒摘录：分工扩大可得产品',
    '穆勒摘录：自给生产与供需',
    '穆勒摘录：总供需与个别商品',
]

ROWS = rows('mill', 62, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='»Zwei Sachen sind nöthig', zh_end='“构成需求必须有两个条件')
heading = ROWS[14]
ROWS[14] = (*heading[:3],
            heading[3].replace('4) De la consommation. Production',
                               '4) De la consommation.\nProduction'),
            heading[4].replace('四论消费“', '四 论 消 费\n“'), *heading[5:])
PRINTED = {
    ('de_megaiv2', 450): '456', ('de_megaiv2', 451): '459',
    ('de_megaiv2', 452): '460', ('de_megaiv2', 453): '461',
    ('zh_single', 185): '175', ('zh_single', 186): '176',
    ('zh_single', 187): '177', ('zh_single', 188): '178',
    ('zh_single', 189): '179',
}
SEQUENCES = {f'mill_{number:03}': -20000 + offset for offset, number in enumerate(range(62, 86))}
NOTES = {
    f'mill_{number:03}': (
        '此组为马克思对私有财产、分工和异化的评注。'
        if number <= 68 else
        '此组转录穆勒货币或消费论摘录；所摘观点不能整体直接视作马克思主张。'
    )
    for number in range(62, 86)
}
DOUBTS = {
    'mill_de_067': ['|XXX. I'],
    'mill_de_068': ['l||(|'],
    'mill_de_072': ['L altération du cours1'],
    'mill_de_077': ['2l'],
    'mill_de_084': ['||XXXI.|'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid, {})[word] = dict(
            kind='glyph_doubt', status='open',
            reported_reading='页内位置、字母或上标字形待辨',
            note='按本地扫描可见候选照录；不依据译文或语义静默改写。')


if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=25, release='0.4.0-alpha21',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES, row_notes=NOTES, sequence_overrides=SEQUENCES,
         coverage_notes={'mill':
             '现有稳定ID保留；后补前部按source sequence排在mill_001之前。'
             '已覆盖德印刷456及459—470/中文175—189页内；德印刷457—458及更前范围待审计。'})
