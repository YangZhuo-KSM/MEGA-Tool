"""Batch 49: free coinage, value laws and Marx's money-mediator commentary.

Literal slices checked against German PDF439-443 and Chinese PDF173-177.
The original extraction is preserved; only explicit scan corrections apply.
"""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream

DE = stream('de_megaiv2', [
    (439, 29, 42), (440, 2, 42), (441, 2, 42), (442, 2, 42), (443, 2, 3),
], join_page_hyphens=True)
ZH = stream('zh_single', [
    (173, 16, 28), (174, 1, 26), (175, 1, 26), (176, 1, 24), (177, 1, 22),
], {
    173: [('134一136', '134—136'), ('1XXV」', '[XXV]')],
    174: [('第137页)', '(第137页)'), ('货巾', '货币'),
          ('经济学家5歪曲', '经济学家45歪曲'), ('国民经济学+归结', '国民经济学4归结')],
    175: [('既然人便', '既然人使'), ('不冉', '不再'), ('中介,—', '中介，——'),
          ('奴录', '奴隶'), ('外化的私有财产是', '外化的私有财产，是'),
          ('(3)人面前的人同样', '(3)人面前的人。同样'),
          ('为了社会的私有财产但是', '为了社会的私有财产。但是')],
    176: [('systememonetairel01', 'système monétaire101'), ('百目信仰', '盲目信仰'),
          ('贯金属', '贵金属'), ('质币', '货币'), ('而这种抽象的关系是价值货币', '而这种抽象的关系是价值。货币')],
    177: [('货巾', '货币'), ('货市', '货币'), ('晋通性', '普遍性'), ('贯金属', '贵金属'),
          ('百目信', '盲目信'), ('卯的感性形式', '仰的感性形式'),
          ('在本质上有看', '在本质上有着'), ('国民经济学的诂', '国民经济学的话'),
          ('目在地', '自在地'), ('目身存在', '自身存在'), ('造合于', '适合于')],
}, join_page_hyphens=True)
ZH = (ZH[0].replace(',', '，').replace(';', '；').replace(':', '：').replace('?', '？'), ZH[1], ZH[2])

DE_STARTS = [
    'Im ersten Fall öffnet', 'Die Quantität des Geldes kann', '|XXV.| So oft also',
    'Wenn aber der Geldwerth', '|(Bei jener Compensation', 'Wenn es ein beständiges Gesetz',
    'Ja, Nachfrage und Zufuhr', 'Diese wirkliche Bewegung', 'Das wahre Gesetz der Nationalökonomie',
    'Sehr gut und das Wesen', 'Indem der Mensch diese vermittelnde', 'Durch diesen fremden Mittler',
    'Daß dieser Mittler nun', 'Die Gegenstände, getrennt', 'Dieser Mittler ist daher',
    'Alle Eigenschaften, welche', 'Christus repräsentirt ursprünglich', 'So repräsentirt das Geld',
    'Aber Christus ist', 'Warum muß das Privateigenthum', 'Der Gegensatz der modernen Nationalökonomen',
    'Das metallne Dasein', 'Der Gegensatz der modernen Nationalökonomen', 'Das persönliche Dasein',
]
ZH_STARTS = [
    '在第一种情况下', '“如果流通中的货币量太大', '[XXV]“因此', '“可是，如果货币量',
    '在谈到货币和金属价值', '如果说，例如生产费用', '的确，由于需求和供给的波动',
    '这种现实的运动', '国民经济学的真正规律', '穆勒把货币称为交换的中介',
    '既然人使这种中介活动', '由于这种异己的中介', '因为中介是支配',
    '同这个中介脱离的物', '因此，这个中介是私有财产', '因此，凡是人的这种类生产活动',
    '基督最初代表', '同样，货币按照自己的概念', '但是，基督是外化',
    '为什么私有财产必然发展', '现代国民经济学同货币主义', '——货币的金属存在',
    '现代国民经济学同货币主义', '货币越是抽象',
]
LABELS = [
    '自由铸币与私人恢复货币平衡', '铸币过量与熔回金银条块', '金属价值调节货币数量',
    '金银价值和生产费用', '抽象规律与规律的不断扬弃', '生产费用与价格的暂时相适应',
    '供求波动与暂时均衡', '现实运动与经济规律的对立面', '偶然性与固定规律',
    '货币中介与人的社会行动异化', '中介活动的外化与非人化', '异己中介与人的奴隶地位',
    '货币中介的权力和崇拜', '物的价值与原始关系的颠倒', '货币作为外化的私有财产',
    '属性转移与人的贫穷', '基督的三重代表关系', '货币的三重代表关系',
    '基督与货币的外化类比', '私有财产到交换价值和货币', '货币主义与现代国民经济学',
    '货币金属存在与货币灵魂', '精致与粗陋的盲目信仰', '纸币与货币抽象存在的发展',
]
LABELS = [('穆勒摘录：' if i < 4 else '马克思评注：') + s for i, s in enumerate(LABELS)]
ROWS = rows('mill', 180, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='Im Creditwesen', zh_end='在信用业')
PRINTED = {('de_megaiv2', 439): '444', ('de_megaiv2', 440): '447',
           ('de_megaiv2', 441): '448', ('de_megaiv2', 442): '449', ('de_megaiv2', 443): '450',
           ('zh_single', 173): '163', ('zh_single', 174): '164', ('zh_single', 175): '165',
           ('zh_single', 176): '166', ('zh_single', 177): '167'}
SEQUENCES = {f'mill_{n:03}': -29930 + i for i, n in enumerate(range(180, 204))}
NOTES = {f'mill_{n:03}': ('此组为穆勒著作摘录。' if n < 184 else '此组为马克思对穆勒摘录的评注。') for n in range(180, 204)}
NOTES['mill_181'] += '德文PDF439印刷444直接续至PDF440印刷447；按原页登记，不推定缺失正文。'
NOTES['mill_187'] += '中文上标45及4分别保留为纯文本注号；不纳入相邻正文词语。'
NOTES['mill_199'] += '中文PDF176脚注①说明马克思重复页码XXV；保留正文注号，脚注全文留在原页。'
NOTES['mill_203'] += '中文语序与德文不同，保留整个完整句及纸币结句；跨页句群不拆为局部错配。'
DOUBTS = {
    'mill_de_181': ['|'], 'mill_de_182': ['|XXV.|'],
    'mill_de_184': ['|('], 'mill_de_185': ['ζ.', 'periodisch \\', 'Preiß \\'],
    'mill_de_193': ['ers/erepräsentirte'], 'mill_de_199': ['||XXV [a].|', 'wirkliehe'],
    'mill_de_200': ['NachfrageX', 'Natiohalökonomen', 'exclüsiven'],
    'mill_de_203': ['Standesyerhältnifli..der', 'Naturwüchsiger'],
}
ISSUE_PAGES = {181:440,182:440,184:440,185:440,193:441,199:441,200:442,203:442}
OVERRIDES = {uid: {word: dict(kind='glyph_doubt', status='open',
    reported_reading='按扫描保留字形候选，待研究者核查',
    note='已对照原页；保留异常字形、历史拼写或页内界符，不按译文或语义静默替换。',
    evidence_pages=[f'de_megaiv2:{ISSUE_PAGES[int(uid.rsplit("_",1)[1])]}'])
    for word in words} for uid, words in DOUBTS.items()}
NEXT_START = dict(id='mill_204', sequence=-29906, de_pdf=443, de_line=3,
                  de_printed='450', de_anchor='Im Creditwesen',
                  zh_pdf=177, zh_line=22, zh_printed='167', zh_anchor='在信用业')
SCAN_PAGES = dict(de_megaiv2=list(range(439,444)), zh_single=list(range(173,178)))

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=49, release='0.4.0-alpha45',
         reviewed_date='2026-10-23', source_by_section=ROUTES,
         sequence_overrides=SEQUENCES, doubts=DOUBTS, issue_overrides=OVERRIDES, row_notes=NOTES,
         coverage_notes={'mill':'前补从德印刷428/中文149连续至德印刷450/中文167信用业评注前；后续缺口待补，旧ID与sequence保留。'})
