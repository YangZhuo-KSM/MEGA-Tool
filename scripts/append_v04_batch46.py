"""Batch 46: two alienated-labour opening groups and 22 groups from Mill's opening."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


ALIEN_DE = stream('de_megai2', [(363, 17, 39), (364, 2, 9)], {
    363: [('Wüklichkeit', 'Wirklichkeit'), ('Wü', 'Wir'),
          ('untersteüten', 'unterstellten'),
          ('fürchterüchere', 'fürchterlichere'), ('Capitaüst', 'Capitalist'),
          ('Theüung', 'Theilung'),
          ('Privateigehthums', 'Privateigenthums')],
})
ALIEN_ZH = stream('zh_collected', [(291, 2, 22), (292, 2, 2)], {
    291: [('国民经济学42', '国民经济学⁷⁴'), ('消失T', '消失了'),
          ('者盼级', '者阶级'), ('事实7So', '事实⁷⁵。'),
          ('最终原因•', '最终原因；'), (',', '，'), (';', '；')],
    292: [('®', '①')],
})
ALIEN_LABELS = ['异化劳动：国民经济学前提及其社会结果', '异化劳动：私有财产事实未获说明']
ALIEN_ROWS = rows(
    'alienation', 85, ALIEN_LABELS, ALIEN_DE, ALIEN_ZH,
    ['[Entfremdete Arbeit und Privateigentum]', 'Die Nationalökonomie geht vom Factum'],
    ['[异化劳动和私有财产]', '国民经济学从私有财产的事实出发'],
)


MILL_DE = stream(
    'de_megaiv2',
    [(424, 2, 29), (425, 2, 42), (426, 3, 43), (427, 2, 42),
     (428, 2, 42), (429, 2, 13)],
    {
        424: [('Élémens', 'Éléments'), ('Vexistence', "l'existence"),
              ('IL De la distribution', 'II. De la distribution'), ('I.e.', 'l.c.')],
        427: [('um 2k, der Capitalien um Vs', 'um 2/8, der Capitalien um 1/8'),
              ('Bevölkerung um !/8', 'Bevölkerung um 1/8')],
        428: [("20—40' Jahr", '20—40sten Jahr')],
    },
    join_page_hyphens=True,
)
MILL_ZH = stream(
    'zh_single',
    [(159, 1, 17), (160, 1, 28), (161, 1, 26),
     (162, 1, 27), (163, 1, 28), (164, 1, 9)],
    {
        159: [('XVⅢ」', '[XVIII]'), ('(第11页“', '(第11页)“'),
              (',', '，')],
        160: [('投人', '投入'), ('第16一17页', '第16—17页'),
              ('第[17]一18页', '第[17]—18页'), ('第18一19页', '第18—19页'),
              ('第19一20页', '第19—20页'), ('土地M1', '土地No.1'),
              ('第20一21页', '第20—21页'), (',', '，'), (':', '：')],
        161: [('投人', '投入'), ('土地M2', '土地No.2'), ('土地M1', '土地No.1'),
              ('第L21—22页', '第[21]—22页'), ('报酮', '报酬'),
              ('第[22]一23页', '第[22]—23页'),
              ('第30一3页', '第30—31页'), ('[XTX」', '[XIX]'),
              (',', '，'), (';', '；'), (':', '：')],
        162: [('雁主', '雇主'),
              ('另一种量的增加额等于双方实际增长额之2,那么结果就是这样:资本量没有增变,工资水平也就保持不变',
               '另一种量的增加额等于双方实际增长额之差。”例如，人口增加2/8，资本量增加1/8，那么结果就是这样：资本量没有增加，而人口增加1/8。(第36—37页)因此，“如果资本量同人口的比例不变，工资水平也就保持不变'),
              ('第34一35页', '第34—35页'), ('第35一36页', '第35—36页'),
              ('第37一38页', '第37—38页'), (',', '，'), (';', '；'), (':', '：')],
        163: [('[38]—4O页', '[38]—40页'), ('82.', '§2.'),
              ('第140、421、43页', '第[40、42]、43页'), ('3.资本', '§3.资本'),
              ('收人', '收入'), ('第46一47页', '第46—47页'),
              (',', '，'), (';', '；'), (':', '：')],
        164: [('第[48」一49页', '第[48]—49页'), ('孚受', '享受'),
              ('为丁', '为了'), ('酒牲', '牺牲'), ('第50一51贝', '第50—51页'),
              (',', '，'), (';', '；')],
    },
    join_page_hyphens=True,
)

MILL_DE_STARTS = [
    '|XVIII.| Éléments d\'Économie Politique.',
    '» LComme en général',
    '» LPour diviser le travail',
    'II. De la distribution',
    '»Bis die Totalität der besseren Erdart',
    '»Sobald der Theil des Capitals',
    '»So lang die Erde nichts producirt',
    'Kömmt die Zeit',
    '»Also wenn man ein Capital',
    'Dem praktischen Widerspruch',
    '|XIX.| 2) Des salaires.',
    '»Statt zu warten',
    '§ 1. Nach welchem Verhältniß',
    'Man unterstelle eine bestimmte Zahl',
    'Man unterstelle das Gegentheil',
    'Vermehren sich beide',
    'Nach diesem Gesetz',
    'Hätten die Capitalien eine natürliche Tendenz',
    '§2. Die natürliche Tendenz',
    'Zweitens: man stellt dagegen',
    '§3. Die Capitalien haben',
    'Das jährliche Produkt ist auf 2erlei Weise',
]
MILL_ZH_STARTS = [
    '*詹姆斯·穆勒《政治经济学原理》一书摘要',
    '“鉴于人们不能',
    '“为了最有利地',
    '二论分配',
    '“当还没有在全部',
    '“当农业需要一部分',
    '“当土地什么也不生产',
    '“但是，必须耕种二等土地',
    '“因此，无论是把资本',
    '有这样的情况',
    '[XIX](2)关于工资',
    '“人们发现，对工人说来',
    '§1.“产品按什么比例',
    '“假定有一定数目的资本家',
    '“假定情况与此相反',
    '“如果这两种量以不同的比例增加',
    '“根据这个规律',
    '“如果资本增长的自然趋势比人口增长快',
    '§2.“可以从以下几点推论出人口增长的自然趋势”',
    '第二，可以把官方的人口统计表',
    '§3.资本的增长趋势较小',
    '年产品必然按两种方式分配',
]
MILL_LABELS = [
    '穆勒摘录：生产所需生活资料',
    '穆勒摘录：限制个人操作项目',
    '穆勒摘录：大规模生产与大制造业',
    '穆勒摘录：土地肥力与边际投入',
    '穆勒摘录：追加资本的产品递减',
    '穆勒摘录：较低产品资本的两种用途',
    '穆勒摘录：未耕土地与地租缺位',
    '穆勒摘录：较劣土地与地租产生',
    '穆勒摘录：地租是资本产品差额',
    '穆勒摘录：萨伊异议与租地资本',
    '穆勒摘录：生产中的劳动和资本',
    '穆勒摘录：工资预付与产品归属',
    '穆勒摘录：工资率与自由交易',
    '穆勒摘录：工人增加使工资下降',
    '穆勒摘录：资本增加使工资提高',
    '穆勒摘录：人口资本比例与工资',
    '穆勒摘录：人民处境的比例条件',
    '穆勒摘录：人口资本趋势与贫困',
    '穆勒摘录：人口增长的生理条件',
    '穆勒摘录：人口统计表的限度',
    '穆勒摘录：资本增长来自储蓄',
    '穆勒摘录：年产品的两种分配',
]
MILL_ROWS = rows(
    'mill', 110, MILL_LABELS, MILL_DE, MILL_ZH, MILL_DE_STARTS, MILL_ZH_STARTS,
    de_end='Siehe p. sqq.', zh_end='看一看以下各页',
)

ROWS = ALIEN_ROWS + MILL_ROWS
PRINTED = {
    ('de_megai2', 363): '363', ('de_megai2', 364): '364',
    ('zh_collected', 291): '266', ('zh_collected', 292): '267',
    ('de_megaiv2', 424): '428', ('de_megaiv2', 425): '431',
    ('de_megaiv2', 426): '432', ('de_megaiv2', 427): '433',
    ('de_megaiv2', 428): '434', ('de_megaiv2', 429): '435',
    ('zh_single', 159): '149', ('zh_single', 160): '150',
    ('zh_single', 161): '151', ('zh_single', 162): '152',
    ('zh_single', 163): '153', ('zh_single', 164): '154',
}
SEQUENCES = {'alienation_085': -2, 'alienation_086': -1}
SEQUENCES.update({f'mill_{number:03}': -30000 + offset
                  for offset, number in enumerate(range(110, 132))})
NOTES = {
    'alienation_086': '中文PDF292页首①指向原手稿删句说明；正文保留注号，删句留在注释层。',
}
NOTES.update({f'mill_{number:03}':
              '此组转录穆勒《政治经济学原理》摘录；所摘观点不能整体直接视作马克思主张。'
              for number in range(110, 132)})
DOUBTS = {
    'alienation_de_085': ['|XXIl|'],
    'mill_de_110': ['|XVIII.|'],
    'mill_de_111': ['LComme'],
    'mill_de_112': ['LPour'],
    'mill_de_120': ['|XIX.|'],
}
OVERRIDES = {uid: {word: dict(
    kind='glyph_doubt', status='open', reported_reading='页内界符或L形标记待辨',
    note='按本地扫描可见候选照录；不依据译文或语义静默删除。')
    for word in words} for uid, words in DOUBTS.items()}


if __name__ == '__main__':
    assert len(ALIEN_ROWS) == 2 and len(MILL_ROWS) == 22 and len(ROWS) == 24
    main(
        rows=ROWS, printed=PRINTED, batch=46, release='0.4.0-alpha42',
        reviewed_date='2026-10-21', doubts=DOUBTS, issue_overrides=OVERRIDES,
        source_by_section=ROUTES, row_notes=NOTES, sequence_overrides=SEQUENCES,
        coverage_notes={
            'alienation': '正文从节首连续至节尾；新稳定ID以source sequence前置，注释/删文保持独立。',
            'mill': '现有稳定ID保留；后补前部按source sequence排列。已从德印刷428/中文149起连续收录至德印刷435/中文154页内，后续前部范围待补。',
        },
    )
