"""Batch 51: human community, private-property exchange and exchange value.

Nine source pages visually checked; coloured reader annotations are excluded
from Chinese body text, while original extraction evidence remains intact.
"""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream

DE = stream('de_megaiv2', [(445,19,42),(446,2,42),(447,2,42),(448,2,8)],
            {447: [('NaturProdukts','Natur-Produkts')]}, join_page_hyphens=True)
ZH = stream('zh_single', [(180,24,26),(181,1,28),(182,1,26),(183,1,26),(184,1,12)], {
    180: [('。|因为','。因为')],
    181: [('个人—一都是','个人——都是'), ('2nd;人同自盘相异化',''),
          ('1st:物象异化(der_Sache)',''), ('面名高却是他现为','现为'),
          ('3rd:类不质异化',''), ('积极实现看的','积极实现着的')],
    182: [('便命','使命'), ('[XXVIⅢI」','[XXVIII]'), ('目己','自己'),
          ('并便自己','并使自己'), ('财严','财产'), ('我便它','我使它'),
          ('换句诂说','换句话说'), ('除外—我','除外——我'),
          ('本质所必需的','本质所必需的。')],
    183: [('除丁','除了'), ('他开不是他目','他并不是他自'), ('不冉','不再'),
          ('双方来有','双方来看')],
    184: [('目身','自身'), ('LXXIX」','[XXIX]'),
          ('成为价格应当','成为价格，应当'), ('Erwerbsarbeit','')],
}, join_page_hyphens=True)
ZH = (ZH[0].replace(',', '，').replace(';', '；').replace(':', '：')
      .replace('?', '？').replace('!', '！'), ZH[1], ZH[2])

DE_STARTS = ['Indem das menschliche', 'Nicht durch Reflection', 'Es hängt',
    'Die Menschen, nicht', 'Es ist daher ein identischer',
    'Die Nationalökonomie nun', 'Die Gesellschaft, sagt Destutt', 'Man sieht,',
    'IXXVIII. I', 'Wenn der Mensch als', 'Wenn ich mein Privateigenthum',
    'In Bezug auf mich', 'Entäussertes Privateigenthum wird',
    'Den Fall der Gewalt', 'Der andre Mensch', 'Das Band,', 'Die Sehnsucht',
    'Beide Eigenthümer', 'Die gesellschaftliche Beziehung', 'Der Tausch oder',
    'Durch die wechselseitige', 'Zweitens ist', 'Auf beiden Seiten', 'Wie nun dieser']
ZH_STARTS = ['因为人的本质', '因此，上面', '有没有这种', '人——不是抽象',
    '因此，以下论点', '国民经济学以交换', '德斯杜特·德·特拉西说', '我们看到',
    '[XXVIII]', '如果假定一个人', '如果我把我的', '因此，对于我来说',
    '物只有当', '如果把强制', '另一个人也是', '使两个私有者', '对这两种物的渴望',
    '这样，两个', '因此，两个私有者', '因此，交换或', '私有财产本身由于',
    '其次，它同', '因而，私有财产', '如何更详细地']
LABELS = ['人的本质与真正的社会联系', '社会联系的产生', '异化形式下的社会联系',
    '现实个人与社会本质', '异化社会与类生活的颠倒', '国民经济学对社会联系的理解',
    '特拉西与斯密论商业社会', '把异化交往固定为人的使命', '私有者之间的关系',
    '私有财产与人格及外化', '出让私有财产', '单方面外化与自然力',
    '他人的私有财产与外化', '需要推动财产转让', '另一私有者及其产品',
    '物的特殊性质与所有者联系', '需要与总体的存在物', '在私有权关系中放弃财产',
    '相互外化的社会关系', '物物交换作为外化的类行为', '财产失去原占有者的私人意义',
    '不同私有财产相互替代', '等价物与交换价值', '价值与价格的进一步规定']
LABELS = ['马克思评注：' + label for label in LABELS]
ROWS = rows('mill',228,LABELS,DE,ZH,DE_STARTS,ZH_STARTS,
            de_end='Das Verhältniß des Tausches', zh_end='交换关系的前提')
PRINTED = {('de_megaiv2',445):'452',('de_megaiv2',446):'453',
    ('de_megaiv2',447):'454',('de_megaiv2',448):'455',
    ('zh_single',180):'170',('zh_single',181):'171',('zh_single',182):'172',
    ('zh_single',183):'173',('zh_single',184):'174'}
SEQUENCES = {f'mill_{n:03}': -29882+i for i,n in enumerate(range(228,252))}
NOTES = {f'mill_{n:03}':'此组为马克思对穆勒摘录的评注。' for n in range(228,252)}
NOTES['mill_228'] += '接续第50批社会交换首句；中文红色批注线排除。'
NOTES['mill_230'] += '德文der后的上标状1按扫描保留为der1并标疑点。'
NOTES['mill_232'] += '中文PDF181红色异化分类批注及其误识文字排除；原提取仍完整保存。德文完整长句跨PDF445—446。'
NOTES['mill_234'] += '中文引文后102、103为原书注号，保留锚点；两条引文与德文同组对应。'
NOTES['mill_244'] += '双方均跨页，完整保留需要与内在所有权关系的句群。'
NOTES['mill_250'] += '德文eigenthüm-跨PDF447/448拼合为eigenthümliches；异常字形及页内标记照录待核。'
NOTES['mill_251'] += '中文PDF184红色Erwerbsarbeit批注排除；止于价值与价格另行讨论的完整句。'
DOUBTS = {'mill_de_230':['der1'], 'mill_de_233':['Menscnenwesen'],
          'mill_de_235':['\\'], 'mill_de_236':['IXXVIII. I'],
          'mill_de_250':['e/ifäusserfe','Bestimmung)','|XXIX. I']}
ISSUE_PAGES = {230:445,233:446,235:446,236:446,250:448}
OVERRIDES = {uid:{word:dict(kind='glyph_doubt',status='open',
    reported_reading='按扫描保留字形候选，待研究者核查',
    note='原页异常字形、标点或页内界符按扫描保留，未按译文或语义替换。',
    evidence_pages=[f'de_megaiv2:{ISSUE_PAGES[int(uid.rsplit("_",1)[1])]}'])
    for word in words} for uid,words in DOUBTS.items()}
NEXT_START = dict(id='mill_252',sequence=-29858,de_pdf=448,de_line=8,
    de_printed='455',de_anchor='Das Verhältniß des Tausches',
    zh_pdf=184,zh_line=12,zh_printed='174',zh_anchor='交换关系的前提')
SCAN_PAGES = dict(de_megaiv2=[445,446,447,448],zh_single=[180,181,182,183,184])

def extra_assertions(data,evidence):
    from paris.corpus import index
    u=index(data['units'])
    assert u['mill_de_227']['text'].endswith('gesellschaftliche Genuß ist.')
    assert u['mill_de_228']['text'].startswith('Indem das menschliche')
    assert u['mill_zh_228']['text'].startswith('因为人的本质')
    assert u['mill_de_232']['text'].endswith('der Knecht dieser Schöpfung erscheint.')
    assert '本质的联系表现为非本质的联系' in u['mill_zh_232']['text']
    assert all(x not in u['mill_zh_232']['text'] for x in ['2nd','1st','3rd','4th','der_Sache','面名高'])
    assert '102亚当' in u['mill_zh_234']['text'] and u['mill_zh_234']['text'].endswith('103')
    assert 'eigenthümliches.' in u['mill_de_250']['text']
    assert 'Natur-Produkts' in u['mill_de_250']['text']
    assert u['mill_de_251']['text'].endswith('wie er zum Preiß wird.')
    assert u['mill_zh_251']['text'].endswith('应当在其他地方加以探讨。')
    assert 'Erwerbsarbeit' not in u['mill_zh_251']['text']

if __name__ == '__main__':
    assert len(ROWS)==24
    main(rows=ROWS,printed=PRINTED,batch=51,release='0.4.0-alpha47',
         reviewed_date='2026-10-24',source_by_section=ROUTES,
         sequence_overrides=SEQUENCES,doubts=DOUBTS,issue_overrides=OVERRIDES,row_notes=NOTES,
         coverage_notes={'mill':'前补从德印刷428/中文149连续至德印刷455/中文174价值与价格讨论句；后续缺口待补，旧ID与sequence保留。'})
