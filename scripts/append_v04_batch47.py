"""Batch 47: Mill's population, capital profits and opening exchange excerpts."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream

DE = stream('de_megaiv2', [(429,13,42),(430,2,42),(431,2,42),(432,2,42),(433,2,34)], {
    432: [('I.e.', 'l.c.')],
    433: [('de s andern', 'des andern'), ('[98-199.', '[98-]99.')],
}, join_page_hyphens=True)
ZH = stream('zh_single', [(164,9,27),(165,1,28),(166,1,26),(167,1,25),(168,1,19)], {
    164: [('感多','越多'),('附难','困难'),('第55一[561页','第55—[56]页'),
          ('XX」因此,”','[XX]因此，“'),('第56一57页。','第56—57页)。'),
          ('紧衍','繁衍'),('58一59','58—59'),('目己','自己'),('第59贝','第59页'),
          ('期立法拥有反著侈派','则立法拥有反奢侈浪')],
    165: [('便用','使用'),('投人','投入'),('收人','收入'),('便土地','使土地'),
          ('整延','蔓延'),('第L63」一64页','第[63]—64页'),('61一62','61—62'),('62一63','62—63')],
    166: [('不依颗','不依赖'),('种种乐要','种种乐趣'),('投人','投入'),('收人','收入'),
          ('额(第67页)','额”(第67页)'),('LXXL」','[XXL]'),('第76一7页','第76—77页'),('随看','随着')],
    167: [('投人','投入'),('随看','随着'),('犹豫不决的这样','犹豫不决的。这样'),
          ('81一[82]','81—[82]'),('[83、84」','[83、84]'),('第85页)','第85页)。')],
    168: [('82.','§2.'),('83.','§3.'),('贤本','资本'),('便用','使用'),
          ('[91]一92','[91]—92'),('第100一101','第100—101'),
          ('第[91]—92页)这个','第[91]—92页)。这个')],
}, join_page_hyphens=True)
# Punctuation follows the visible Chinese print, retaining its parentheses style.
ZH = (ZH[0].replace(',', '，').replace(';', '；').replace(':', '：'), ZH[1], ZH[2])
DE_STARTS = [
    'Siehe p. sqq.', 'Die Tendenz der Bevölkerung', '|XX.| »So langsam',
    '§ 4. Die Hauptmittel', 'In den ihrer direkten Action', 'Was die Beschleunigung',
    'In Folge dieser Operation', 'Im Verhältniß, wonach die Capitalien',
    'Man unterstelle, daß die Taxe', 'In diesem Zustand wäre',
    '»Die menschliche perfectibilité', 'Die glücklichsten Menschen',
    '3) Von den Gewinnen', '»Da aber die Proportion', 'Die Profite —',
    '»Die Verminderung der Profite', 'Durch welche Stufen',
    'Durch die Vermehrung des Getreidewerths', 'So alle Capitalisten',
    '3) Des échanges.', '§ 2. Wenn die Quantität', '§3. Ltravail',
    '3 Fälle werden', '»Wenn 2 Arbeitsarten',
]
ZH_STARTS = [
    '看一看以下各页', '“人口增长的趋势', '[XX]因此', '§4.“惩罚和奖励',
    '“立法在不直接起作用', '至于加速资本的增长', '这样做的结果是',
    '“如果资本带来的产品', '“假定工资水平保持不变', '“在这种情况下，出售土地',
    '“人类追求完善化的能力', '“最幸福的人', '(3)关于资本的利润',
    '“可是，因为资本家和工人', '“因此，利润', '“随着投入农业的资本',
    '“要经过哪些阶段', '由于谷物价值的增大', '这样，所有的资本家',
    '三论交换', '§2.“如果一种产品', '§3.直接劳动', '“劳动和资本参加生产',
    '“如果在生产中两种劳动',
]
LABELS = [
    '穆勒评注：对后续人口论述的评论', '穆勒摘录：人口与资本增长趋势',
    '穆勒摘录：资本增长较慢与工资下降', '穆勒摘录：立法奖惩与人口增长',
    '穆勒摘录：间接立法和公众制裁', '穆勒摘录：所得税及资本借贷方案',
    '穆勒摘录：人口增长与土地投入', '穆勒摘录：资本收入递减',
    '穆勒摘录：工资不变与土地所有者财富', '穆勒摘录：土地分割与灾害储备',
    '穆勒摘录：富裕阶级与知识发展', '穆勒摘录：中等财产和余暇',
    '穆勒摘录：利润工资分配与地租', '穆勒摘录：人口工资作为调节者',
    '穆勒摘录：利润的份额及总价值', '穆勒摘录：农业利润与其他产业',
    '穆勒摘录：谷物需求及利润趋同', '穆勒摘录：生活资料价格与劳动报酬',
    '穆勒摘录：工资提高与资本利润下降', '穆勒摘录：交换及其代理人',
    '穆勒摘录：交换比例与生产费用', '穆勒摘录：直接劳动与积累劳动',
    '穆勒摘录：劳动资本参与的三种情况', '穆勒摘录：劳动价格与交换价值比例',
]
ROWS = rows('mill',132,LABELS,DE,ZH,DE_STARTS,ZH_STARTS,
            de_end='Die erste und einzige Frage', zh_end='因此，首要的和惟一的问题')
PRINTED = {('de_megaiv2',429):'435',('de_megaiv2',430):'436',
           ('de_megaiv2',431):'437',('de_megaiv2',432):'438',('de_megaiv2',433):'439',
           ('zh_single',164):'154',('zh_single',165):'155',('zh_single',166):'156',
           ('zh_single',167):'157',('zh_single',168):'158'}
SEQUENCES = {f'mill_{n:03}': -29978+i for i,n in enumerate(range(132,156))}
NOTES = {f'mill_{n:03}':'此组为穆勒著作摘录，保留摘录与评注的区别。' for n in range(133,156)}
NOTES['mill_132'] = '此句为马克思对后续摘录的评语；与随后穆勒观点分开编组。'
NOTES['mill_145'] += '中文PDF166的页内标记按可见字形保留[XXL]，与德文||XXI.|分别照录，转写待核。'
DOUBTS = {'mill_de_133':['I'], 'mill_de_134':['|XX.|'], 'mill_de_145':['||XXI.|'],
          'mill_de_153':['Ltravail', 'Jravail']}
OVERRIDES = {uid:{word:dict(kind='glyph_doubt',status='open',reported_reading='页内界符或起讫标记待辨',
    note='按扫描可见候选保留；不按译文静默替换。',
    evidence_pages=[f'de_megaiv2:{429 if uid in ("mill_de_133","mill_de_134") else 431 if uid=="mill_de_145" else 433}'])
    for word in words} for uid,words in DOUBTS.items()}

if __name__ == '__main__':
    assert len(ROWS)==24
    main(rows=ROWS,printed=PRINTED,batch=47,release='0.4.0-alpha43',
         reviewed_date='2026-10-22',source_by_section=ROUTES,sequence_overrides=SEQUENCES,
         doubts=DOUBTS,issue_overrides=OVERRIDES,row_notes=NOTES,
         coverage_notes={'mill':'后补前部已从德印刷428/中文149连续至德印刷439/中文158页内；后续待补，旧ID和sequence保留。'})
