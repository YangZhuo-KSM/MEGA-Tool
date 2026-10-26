"""Batch 48: Mill excerpts on wage/profit examples, exchange and money quantity.

Page ranges, corrections and boundaries were compared with the local scans.
Unusual German letter/fraction forms remain literal candidates with issues.
"""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream

DE = stream('de_megaiv2', [
    (433, 34, 42), (434, 2, 42), (435, 2, 42), (436, 2, 42),
    (437, 2, 42), (439, 2, 29),
], {
    # The shared line-number filter drops this body numeral at the line end.
    435: [('in den Fall No. gehören.', 'in den Fall No. 1 gehören.')],
}, join_page_hyphens=True)

# Chinese stacked fractions are restored from the scan, not from the German.
# The entire damaged extraction span is retained below for reproducibility.
ZH_FRACTION_RAW = (
    '1XXIV」“如果不是每块铸币在一年之内用于十次交换,而是货币总'
    '量增到十倍,并且每块铸币只用于一次交换,那么很清楚,货币总量的每'
    '次增加都会引起这些铸币中的每一单个铸币的价值相应降低。因为我们'
    '服定,所有货币能换取的商品量保持不变,所以,货币总量的价值在其总'
    '量增加之后不会变得比以前大。如果我们假定货币量增加0月那么它的'
    '每个部分(比如说1盎司)的价值就得减少如果货市总量为一百万盎1O'
    '司并且增加o,那么不管整体的价值怎样减少,这种减少必然相应地反映'
    '在整体的每个部分上;一百万的-1O'
    '司之比一样。”(第130一131页)“如果货币总量只有假定数的而它的每1O'
    '个部分在一年之内用于十次购买,那么这就同货币总量与商品总量的1O'
    '进行了十次交换一样。可是如果假定数的即货币总量,以某种比例增1O'
    '加,那么这就同整体或者假定数以这个比例增加一样。因此,不管货币总'
)
ZH_FRACTION_SCAN = (
    '[XXIV]“如果不是每块铸币在一年之内用于十次交换，而是货币总'
    '量增到十倍，并且每块铸币只用于一次交换，那么很清楚，货币总量的每'
    '次增加都会引起这些铸币中的每一单个铸币的价值相应降低。因为我们'
    '假定，所有货币能换取的商品量保持不变，所以，货币总量的价值在其总'
    '量增加之后不会变得比以前大。如果我们假定货币量增加1/10，那么它的'
    '每个部分（比如说1盎司）的价值就得减少1/10。如果货币总量为一百万盎'
    '司并且增加1/10，那么不管整体的价值怎样减少，这种减少必然相应地反映'
    '在整体的每个部分上；一百万的1/10与一百万之比如同1盎司的1/10与1盎'
    '司之比一样。”(第130—131页)“如果货币总量只有假定数的1/10，而它的每'
    '个部分在一年之内用于十次购买，那么这就同货币总量与商品总量的1/10'
    '进行了十次交换一样。可是如果假定数的1/10，即货币总量，以某种比例增'
    '加，那么这就同整体或者假定数以这个比例增加一样。因此，不管货币总'
)

ZH = stream('zh_single', [
    (168, 19, 28), (169, 1, 28), (170, 1, 28), (171, 1, 27),
    (172, 1, 26), (173, 1, 16),
], {
    168: [('我们把上述', '“我们把上述'), ('M1', 'No1'), ('M2', 'No2'),
          ('M3', 'No3'), ('N1', 'No1'), ('1100锈', '1100镑')],
    169: [('N2', 'No2'), ('M3', 'No3'), ('锈', '镑'), ('[XX1]', '[XXII]'),
          ('1O7贝', '107页'), ('[107」一1O8', '[107]—108')],
    170: [('M1', 'No1'), ('N2', 'No2'), ('M2', 'No2'), ('只便', '只使'),
          ('108一109', '108—109'), ('1XXⅢ」', '[XXIII]')],
    171: [('11O—111', '110—111'), ('112一113', '112—113'),
          ('5.“人们', '§5.“人们'), ('87.', '§7.'),
          ('金、银、货币§7', '金、银、货币。§7')],
    172: [('128一129', '128—129'), ('129一130', '129—130'), ('纷紧', '纷繁'),
          (ZH_FRACTION_RAW, ZH_FRACTION_SCAN)],
    173: [('购头', '购买'), ('131一132', '131—132'), ('132一133', '132—133')],
}, join_page_hyphens=True)
ZH = (ZH[0].replace(',', '，').replace(';', '；').replace(':', '：').replace('?', '？'),
      ZH[1], ZH[2])

DE_STARTS = [
    'Die erste und einzige Frage',
    'Die 3 oben angegebnen Fälle',
    'Man unterstelle ein Capital von 10001.',
    'Befinden sich alle Artikel in dem Fall No. 2',
    'Der Fall bliebe genau derselbe',
    '»Wären alle Artikel im Fall No. 3',
    '»Unterstellen wir, was sehr wahrscheinlich ist',
    '»Steigen die Salaire, fallen alle Gewinne',
    '»Die Capitalisten, welche Artikel im Fall No. 1',
    '»In Summa ist das Resultat also',
    '»Nach diesen Principien',
    '§ 4. Es ist im Interesse der Nationen',
    '§5. Der Vortheil',
    'Wenn ein Mensch eine gewisse Waare',
    "Eben so verhält's sich mit Nationen.",
    '§ 6. Der Vermittler',
    '§ 7. Werth des Geldes',
    'Dieß Verhältniß ist bestimmt',
    'Der Fall ist ganz derselbe im wirklichen',
    'Man fixire diese Taxe',
    '|XXIV.| Wenn anstatt',
    '»Erhebt sich die Totalmasse des Geldes',
    'Wenn eine Portion des jährlichen Products',
    '§ 8. Was regelt nun',
]
ZH_STARTS = [
    '因此，首要的和惟一的问题',
    '“我们把上述三种情况',
    '“假定所使用的资本是1000镑',
    '如果所有商品的生产都处在No2',
    '“如果没有用来支付工资的那1000镑',
    '“如果所有商品的生产处在No3',
    '“如果我们假定，实际上发生了同样多',
    '“如果随着工资上涨',
    '在No1的情况下生产商品的资本家',
    '“因此，总的结果是',
    '“根据这些原则',
    '§4.互相交换产品',
    '§5.“人们从一种商品',
    '“如果一个人拥有某种工业品',
    '各个国家的情况也是这样',
    '中介§6.',
    '§7.“货币的价值',
    '这个比例是由一个国家',
    '“实际上情况完全是这样的',
    '我们可以把这个平均数',
    '[XXIV]“如果不是每块铸币',
    '“如果货币总量只有假定数的1/10',
    '“如果年产品的一部分',
    '§8.用什么来调节货币量',
]
LABELS = [
    '穆勒摘录：工资上涨与利润下降的比例',
    '穆勒摘录：直接劳动生产的第一种情况',
    '穆勒摘录：第一种情况的千镑资本算例',
    '穆勒摘录：劳动与资本各半的第二种情况',
    '穆勒摘录：固定资本与流动资本混合算例',
    '穆勒摘录：无须支付工资的第三种情况',
    '穆勒摘录：极端情形补偿与利润平均下降',
    '穆勒摘录：工资变动与商品相对价值',
    '穆勒摘录：交换对追加成本的补偿',
    '穆勒摘录：生产者总体的利润损失',
    '穆勒摘录：以货币比较的产品价格变化',
    '穆勒摘录：分工和各国交换产品的利益',
    '穆勒摘录：贸易利益与进口商品',
    '穆勒摘录：个人交换中的价值偏好',
    '穆勒摘录：国家交换所获得的产品',
    '穆勒摘录：交换中介与金银货币',
    '穆勒摘录：货币价值与交换比例',
    '穆勒摘录：货币总量及集中交换假设',
    '穆勒摘录：实际交换次数与流通平均数',
    '穆勒摘录：十次购买的货币周转算例',
    '穆勒摘录：货币增加及各部分价值降低',
    '穆勒摘录：货币量和流通速度变化',
    '穆勒摘录：不进入货币交换的年产品',
    '穆勒摘录：调节货币数量的两种方式',
]
ROWS = rows('mill', 156, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='Im ersten Fall öffnet', zh_end='在第一种情况下')
PRINTED = {('de_megaiv2', 433): '439', ('de_megaiv2', 434): '440',
           ('de_megaiv2', 435): '441', ('de_megaiv2', 436): '442',
           ('de_megaiv2', 437): '443', ('de_megaiv2', 439): '444',
           ('zh_single', 168): '158', ('zh_single', 169): '159',
           ('zh_single', 170): '160', ('zh_single', 171): '161',
           ('zh_single', 172): '162', ('zh_single', 173): '163'}
SEQUENCES = {f'mill_{n:03}': -29954 + i for i, n in enumerate(range(156, 180))}
NOTES = {f'mill_{n:03}': '此组为穆勒著作摘录，保留摘录与马克思评注的区别。'
         for n in range(156, 180)}
NOTES['mill_167'] += '德文β项的字形照录为ß；不按中文希腊字母静默替换。'
NOTES['mill_171'] += '中文的“中介”标题保留，德文无独立标题；不新增独立正文对应。'
NOTES['mill_176'] += '中文PDF172的八处叠排分数（跨两组）按扫描转写为1/10，保留两语字形差异。'
NOTES['mill_177'] += ('德文PDF437→439跨过手稿XXV影印页438；'
                     '439印刷页码为444，按原页独立登记，不作统一偏移。')
NOTES['mill_178'] += '法文引号边界的数字/竖线形符号按当前候选保留，另列字形疑点。'
EXTRA_PAGE_MAPS = [dict(
    source_id='de_megaiv2', pdf_page=438, printed_page=None,
    page_kind='illustration', status='scan_checked_ai', checked_by='Codex',
    checked_at='2026-10-23',
    note='原页为穆勒摘录手稿XXV影印；未见本版印刷页码，不转录为正文。正文PDF437印刷443续至PDF439印刷444。')]

DOUBTS = {
    'mill_de_158': ['||XXII.|'],
    'mill_de_159': ['2V2p/c'],
    'mill_de_160': ['büden', '2V2p/c'],
    'mill_de_164': ['21l2plc', '2ll2pU', '2V2p/c', "2'/2p/c"],
    'mill_de_165': ['2V2 PU', '|| XXIII. |', "2'/c p/c"],
    'mill_de_167': ['ß)'],
    'mill_de_171': ['Vermittler\\'],
    'mill_de_175': ['lOmal', 'J'],
    'mill_de_176': ['|XXIV.|', 'Vio'],
    'mill_de_177': ['Vi0', 'lOmal'],
    'mill_de_178': ['Lparce', 'pas.1'],
}
ISSUE_PAGES = {158: 434, 159: 434, 160: 434, 164: 435, 165: 435,
               167: 436, 171: 436, 175: 437, 176: 437, 177: 437, 178: 439}
OVERRIDES = {uid: {word: dict(
    kind='glyph_doubt' if word != 'büden' else 'semantic_doubt',
    status='open' if word != 'büden' else 'retained_as_source',
    reported_reading='按底本保留的字形候选，待研究者核查',
    note=('已对照原页及放大图；保留当前PDF可见异常字形、界符或分数字形候选，'
          '不按算术、译文或通常拼写替换。'),
    evidence_pages=[f'de_megaiv2:{ISSUE_PAGES[int(uid.rsplit("_", 1)[1])]}'])
    for word in words} for uid, words in DOUBTS.items()}

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=48, release='0.4.0-alpha44',
         reviewed_date='2026-10-23', source_by_section=ROUTES,
         sequence_overrides=SEQUENCES, doubts=DOUBTS,
         issue_overrides=OVERRIDES, row_notes=NOTES, extra_page_maps=EXTRA_PAGE_MAPS,
         coverage_notes={'mill': '后补前部从德印刷428/中文149连续至德印刷444/中文163的§8货币数量调节两种方式；后续待补，旧ID和sequence保留。'})
