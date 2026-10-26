"""Batch 28: 24 groups completing the surviving private_relation section."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


DE = stream('de_megai2', [(379, 10, 43), (380, 2, 42),
                           (381, 2, 41), (382, 2, 8)], {
    379: [('Grundeigenthümer s ;', 'Grundeigenthümers;'),
          ('durch um ist', 'durch ihn ist'), ('wesentüch', 'wesentlich'),
          ('Capitaüst', 'Capitalist'), ('Wüklichkeit', 'Wirklichkeit'),
          ('Gründls herr', 'Grundherr'),
          ('beeüiträchtigt', 'beeinträchtigt'), ('seme', 'seine'),
          ('anschauüches', 'anschauliches'), ('souvenus', 'souvenirs'),
          ('Rerniniscenzen', 'Reminiscenzen'), ('schüdert', 'schildert'),
          ('feübietenden', 'feilbietenden'),
          ('aüer', 'aller'), ('aües', 'alles')],
    380: [('Weinbürgerlichen', 'kleinbürgerlichen'),
          ('Habsüchtige', 'habsüchtige'), ('/|XLIIl|', '/|XLIII|'),
          ('genante', 'genannte')],
    381: [('Habsuchtüber', 'Habsucht über')],
}, join_page_hyphens=True)
ZH = stream('zh_collected', [(309, 21, 24), (310, 2, 23),
                              (311, 2, 26), (312, 2, 25), (313, 2, 19)], {
    309: [('代表,', '代表，')],
    310: [('发生:', '发生：'), ('----', '——'), ('胁;', '胁；'), ('业;', '业；'),
          ('(自私自利的)①', '（自私自利的）①'), ('©', '②')],
    311: [('•', '·'), ('贪財', '贪财'),
          ('〈法国', '《法国'), ('著作;89', '著作；89'),
          ('<爱国主义', '《爱国主义'),
          ('》这些幻想', '》90，这些幻想'),
          ('奇迹,', '奇迹，'), ('本质(', '本质（'), ('对的)，', '对的），'),
          ('蠢人;', '蠢人；'),
          ('据说,', '据说，'), ('桎桔', '桎梏'), ('手段;', '手段；'),
          (',', '，'), (';', '；')],
    312: [('可能性;', '可能性；'), ('衰退,', '衰退，'),
          ('耕作者(资本家和雇农)', '耕作者（资本家和雇农）'),
          ('敌人;', '敌人；'), ('物质;', '物质；'), ('尔•路易•库利埃', '尔·路易·库利埃'),
          ('德斯杜特•德•特拉西', '德斯杜特·德·特拉西'),
          ('进程中(这里插一句）', '进程中（这里插一句）'), ('荦鄙行为', '卑鄙行为'),
          ('•', '·')],
    313: [('资本,是', '资本，是'), ('私有財产', '私有财产'),
          ('第一:', '第一：'), ('排斥;', '排斥；'),
          ('资本=积累的劳动二劳动', '资本=积累的劳动=劳动'),
          ('工人一■但', '工人——但'), ('因而,', '因而，'), (';', '；')],
})

DE_STARTS = [
    'Aber der Pächter ist', 'Und dieß muß sich auch',
    'Als ihrer gegensätzlichen Entstehung', 'der Capitalist weiß den Grundeigenthümer',
    'Man braucht nur die Angriffe', 'Der Grundeigenthümer macht den Geburtsadel',
    'Er schildert zugleich seinen Gegner', 'Das bewegliche Eigenthum seiner Seits',
    'es bedauert seinen Gegner', 'es schildert ihn als einen Don Quixotte',
    'es erklärt ihn für einen durchtriebnen Monopolisten', '/|XLIII| Es habe der Welt',
    'es habe dem Volk statt seiner rohen', 'Endlich solle er nur auf seinen Pächter sehn',
    'Alles, was er wirklich zu seinen Gunsten', 'Ohne Capital sei das Grundeigenthum',
    'Aus dem wirklichen Lauf der Entwicklung', 'I Die Staaten, welche etwas',
    'Das Grundeigenthum, in seinem Unterschied', 'Das Verhältniß des Privateigenthums ist',
    'Erstens: unmittelbare oder vermittelte Einheit beider', 'Gegensatz beider',
    'Gegensatz jedes gegen sich selbst', 'Arbeit zerfallen in sich',
]
ZH_STARTS = [
    '但是，租地农场主是土地所有者的代表', '而这种情况也必然在现实中发生',
    '但是，当土地所有者和资本家回想起', '而资本家则知道土地所有者',
    '只要看一看不动产对动产的攻击', '土地所有者炫耀他的财产的贵族渊源',
    '同时，他把自己的对手描绘为', '动产也显示工业和运动的奇迹',
    '它很遗憾自己的对手', '它把他描绘成一个用率直坦诚',
    '它宣布自己的对手是诡计多端的垄断者', '[XLIII]据说，动产已经使人人获得了政治的自由',
    '它给人民以文明的需要', '最后，让土地所有者看一看自己的租地农场主',
    '土地所有者实际上提出的有利于自己的一切', '据说，没有资本，地产是死的',
    '从现实的发展进程中（这里插一句）', '那些多少预感到完成的自由工业',
    '与资本不同，地产是还带有地域的', '私有财产的关系是劳动、资本以及二者的关系',
    '第一：二者直接的或间接的统一', '[第二：]二者的对立',
    '[第三：]二者各自同自身对立', '劳动分解为自身和工资',
]
LABELS = [
    '租地农场主揭示土地所有者', '租地农场主与地主相互转化',
    '土地所有者眼中的资本家', '资本家眼中的土地所有者',
    '动产与不动产互相揭短', '土地所有者的贵族自我辩护',
    '土地所有者对资本家的指控', '动产宣称工业的奇迹',
    '动产指责封建暴力', '动产的堂吉诃德画像',
    '浪漫城堡与封建罪行', '动产宣称现代文明成就',
    '动产指责地租阻碍积累', '土地所有者实际属于自由工业',
    '土地所有者的论证反对自身', '资本以劳动取代死的物',
    '发达私有财产战胜地产', '国家阻止地产资本化',
    '地产是未完成的资本', '私有财产关系的三个成分',
    '劳动与资本的直接或间接统一', '劳动与资本互相排斥',
    '资本同自身对立', '劳动同自身及敌对性对立',
]

ROWS = rows('private_relation', 31, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(379, 383)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(309, 314)})
DOUBTS = {
    'private_relation_de_036': ['\\Reminiscenzen, /|'],
    'private_relation_de_037': ['//den', '|/ [„haus]backenen"'],
    'private_relation_de_041': ['/|XLIII|'],
    'private_relation_de_048': ['I'],
    'private_relation_de_054': ['\\'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid, {})[word] = dict(
            kind='glyph_doubt', status='open',
            reported_reading='页内插入、界符或位置标记的转写待复核',
            note='按本地扫描可见候选照录；不依据译文或语义静默删除或改写。')


if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=28, release='0.4.0-alpha24',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES,
         coverage_notes={'private_relation':
             '本节现有连续54组，覆盖德印刷376—382/中文281—288；'
             '已到传世第二手稿《私有财产的关系》节尾，首部缺失范围按底本省略号保留。'})
