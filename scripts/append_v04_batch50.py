"""Batch 50: credit, banking and the opening statement on social exchange.

Scan-reviewed German PDF443-445 and Chinese PDF177-180. Original extraction
is retained separately; no previously frozen unit is edited.
"""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream

DE = stream('de_megaiv2', [(443, 3, 42), (444, 2, 42), (445, 2, 19)],
            join_page_hyphens=True)
ZH = stream('zh_single', [(177, 22, 26), (178, 1, 23), (179, 1, 26), (180, 1, 24)], {
    178: [('[XXV1」', '[XXVI]'), ('不冉', '不再'),
          ('完全的异化信贷', '完全的异化。信贷'), ('归还债款的保证;', '归还债款的保证：')],
    179: [('早鄙', '卑鄙'), ('倾务人', '债务人'), ('货市', '货币'),
          ('给于', '给予'), ('并且便富人', '并且使富人'),
          ('尔质我诈', '尔虞我诈')],
    180: [('LXXVIⅡ」', '[XXVII]'), ('货巾', '货币'), ('成丁头卖', '成了买卖'),
          ('成丁相互', '成了相互'), ('国冢', '国家'), ('屈情假意', '虚情假意'),
          ('早鄙', '卑鄙'), ('产品的交换其意义', '产品的交换，其意义'),
          ('。|因为', '。因为')],
}, join_page_hyphens=True)
ZH = (ZH[0].replace(',', '，').replace(';', '；').replace(':', '：')
      .replace('?', '？').replace('!', '！'), ZH[1], ZH[2])

DE_STARTS = [
    'Im Creditwesen', 'Die St. Simonisten', 'Aber diese Aufhebung',
    'Was constituirt', 'Wir sehn also', 'Der Credit ist unter',
    'Allein selbst diese Ausnahme', 'Der Tod des Armen', 'Man bedenke',
    'Ist nun der', 'Der Credit ist das nationalökonomische', 'Das Medium',
    'Nicht das Geld', 'Die menschliche Individualität', 'Statt Geld',
    'So sehr sind alle', 'Innerhalb des Creditsystems',
    '2) indem die wechselseitige', '||XXVII.| 3)', 'Hier zeigt sich dann',
    'Im Staatscredit', '4) Das Creditsystem', '| ( | Indem', '||Der Austausch',
]
ZH_STARTS = [
    '在信用业', '被这种假象所迷惑的', '但是，这种扬弃',
    '信贷的本质', '就是说，我们不谈', '信贷在两种关系',
    '即使假定有这种例外', '因此，债权人', '请想一想',
    '如果债务人', '信贷是对一个人', '这样，交换',
    '在信贷关系中', '人的个性本身', '构成货币灵魂',
    '虚伪制度内', '在信用业的范围内', '(2)尔虞', '[XXVII](3)',
    '同时这里', '在国家信贷中', '(4)信用业', '因为在信用业中',
    '不论是生产本身',
]
LABELS = ['信用业恢复人际关系的假象', '圣西门主义与组织起来的银行业',
          '信任假象下的自我异化', '信贷本质与货币内容', '诚实与支付能力',
          '富人对穷人的浪漫信贷', '生命活动作为偿还保证', '穷人的死亡与资本死亡',
          '用货币估价人与法律保证', '富裕债务人与观念货币', '信贷的道德判断与人的中介',
          '交换媒介返回人的条件', '人与货币合为一体', '个性与道德成为买卖物品',
          '人的肉体作为货币灵魂的物质', '虚伪制度中的进步与倒退',
          '信用业与贫富对立加深', '无信用者的屈辱', '人把自己变成赝币',
          '信任的基础与信用窥探', '国家信贷与公债投机', '银行业与货币的完成',
          '道德承认与国家信任的秘密', '交换与社会活动和享受']
LABELS = ['马克思评注：' + label for label in LABELS]
ROWS = rows('mill', 204, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='Indem das menschliche', zh_end='因为人的本质')
PRINTED = {('de_megaiv2', 443): '450', ('de_megaiv2', 444): '451',
           ('de_megaiv2', 445): '452', ('zh_single', 177): '167',
           ('zh_single', 178): '168', ('zh_single', 179): '169', ('zh_single', 180): '170'}
SEQUENCES = {f'mill_{n:03}': -29906 + i for i, n in enumerate(range(204, 228))}
NOTES = {f'mill_{n:03}': '此组为马克思对穆勒摘录的评注。' for n in range(204, 228)}
NOTES['mill_208'] += '中文夏洛克后的①为注释锚点；PDF178底部编者注留在原页。'
NOTES['mill_220'] += '保留总述与第1项，随后两组接续第2、3项；德文分号与中文句号分别按底本。'
NOTES['mill_223'] += '德文Creditsuchen-跨PDF444/445接den，拼合为Creditsuchenden；原提取逐页保留。'
NOTES['mill_227'] += '完整收入社会交换首句；中文句后红色批注竖线不作正文，后句留待下一批。'
DOUBTS = {
    'mill_de_206': ['||XXVI.|', "Schein'"],
    'mill_de_207': ["Credits'!"],
    'mill_de_220': ['Uber'], 'mill_de_221': ['Uber'],
    'mill_de_222': ['||XXVII.|'],
    'mill_de_226': ['| ( |', 'Hegt', '||)'],
    'mill_de_227': ['||'],
}
ISSUE_PAGES = {206:443, 207:443, 220:444, 221:444, 222:444, 226:445, 227:445}
OVERRIDES = {uid: {word: dict(kind='glyph_doubt', status='open',
    reported_reading='按扫描保留字形候选，待研究者核查',
    note='原页异常字形、标点或页内界符按扫描保留，未按译文或语义替换。',
    evidence_pages=[f'de_megaiv2:{ISSUE_PAGES[int(uid.rsplit("_",1)[1])]}'])
    for word in words} for uid, words in DOUBTS.items()}
NEXT_START = dict(id='mill_228', sequence=-29882, de_pdf=445, de_line=19,
                  de_printed='452', de_anchor='Indem das menschliche',
                  zh_pdf=180, zh_line=24, zh_printed='170', zh_anchor='因为人的本质')
SCAN_PAGES = dict(de_megaiv2=[443,444,445], zh_single=[177,178,179,180])

def extra_assertions(data, evidence):
    from paris.corpus import index
    units = index(data['units'])
    assert units['mill_de_203']['text'].endswith('Entwicklung des Geldwesens.')
    assert units['mill_de_204']['text'].startswith('Im Creditwesen')
    assert units['mill_de_209']['text'].count('2 ') == 3
    assert 'Creditsuchenden;' in units['mill_de_223']['text']
    assert units['mill_de_227']['text'].endswith('gesellschaftliche Genuß ist.')
    assert units['mill_zh_227']['text'].endswith('社会的活动和社会的享受。')
    assert '因为人的本质' not in units['mill_zh_227']['text']

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=50, release='0.4.0-alpha46',
         reviewed_date='2026-10-23', source_by_section=ROUTES,
         sequence_overrides=SEQUENCES, doubts=DOUBTS, issue_overrides=OVERRIDES, row_notes=NOTES,
         coverage_notes={'mill':'前补从德印刷428/中文149连续至德印刷452/中文170社会交换首句；后续缺口待补，旧ID与sequence保留。'})
