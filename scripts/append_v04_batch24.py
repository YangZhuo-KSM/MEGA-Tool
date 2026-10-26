"""Batch 24: 24 groups completing the surviving Mill government/tax excerpt."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream


DE = stream('de_megaiv2', [(460,39,42),(461,2,42),(462,2,35)], {
    460:[('116|','|16|')],
    461:[('117|','|17|')],
    462:[('jl8|','|18|')],
})
ZH = stream('zh_single', [(197,11,27),(198,1,26),(199,1,13)], {
    197:[(',', '，'),('第262一263页','第262—263页'),('收人','收入')],
    198:[(',', '，'),('贯族','贵族'),('第264」一265页','第[264]—265页'),
         ('做头卖','做买卖'),('希望哥托','希望寄托'),('不计人','不计入'),
         ('开在','并在'),('一培','一倍'),('第268一269页','第268—269页')],
    199:[(',', '，'),('第269一270页','第269—270页'),('第270一271页','第270—271页'),
         ('便地租','使地租'),('收人','收入')],
})

DE_STARTS = [
    '|16| 4) Alle Consumtion', 'Das, was das Gouvernement',
    'Wären aber nicht andre Sachen', 'Die Staatsrevenu muß',
    'In welcher Proportion', '5) Bestreitet man',
    'Die Landkultur hängt', 'Ihm ist es gleichgültig',
    'Früher bestritt der souverain', 'Zu dieser Zeit wurde',
    'Die Bestreitung der Staatskosten', 'Die Besitzer von Capitalien',
    '|17| Es versteht sich', 'Das sei partheiisch',
    'Aber — und dieß', 'Ja, das einzige Bedenken',
    'Die Grundrente, wie sie', 'Unterstellen wir nun',
    'Eine solche Maßregel', '|18| »Die Legislatur',
    'Im Maaß des Wachsthums', 'Cette augmentation continuelle',
    'Und der Grundrentner', '6) Eine direkte Taxe',
]
ZH_STARTS = [
    '(4)“所有的消费', '政府消费的东西',
    '不过，如果其他东西', '“国家收入是',
    '(第262页)“国家收入按什么比例', '(5)如果国家的支出',
    '土地的耕种取决于资本家', '对于资本家来说',
    '以前，君主', '“可见，在那时',
    '因此，国家的支出', '“资本占有者',
    '显然，穆勒像', '因为这对一个',
    '但是——', '国民经济学提出的',
    '“人们买和卖', '“现在我们假定',
    '这样的措施', '“立法机关实际上',
    '“随着人口的增长', '由社会而不是',
    '保持原有收入的', '(6)“资本利润的直接税',
]
LABELS = [
    '个人与政府的消费', '政府消费不形成产品', '其他消费与生产条件',
    '国家收入的三种来源', '抽取比例与直接间接方式', '从地租支付国家支出',
    '土地耕种与通常利润', '地租和赋税对资本家的等同', '君主领地与军费',
    '早期政府支出的地租来源', '地租支付国家支出的好处',
    '利润工资与资本用途', '反对以地租为唯一税源', '特殊阶级的不公负担',
    '地租税的无害与公正', '地租可能超过政府需要', '现存地租与交易预期',
    '立法使土地纯产品倍增的假定', '保持旧地租与公共利益',
    '立法增加人口和生活资料需求', '人口增长下地租与利润',
    '地租增长的社会条件', '新收入来源用于国家', '资本利润的直接税',
]

ROWS = rows('mill',38,['穆勒摘录：'+label for label in LABELS],
            DE,ZH,DE_STARTS,ZH_STARTS)
PRINTED = {('de_megaiv2',460):'468',('de_megaiv2',461):'469',
           ('de_megaiv2',462):'470',('zh_single',197):'187',
           ('zh_single',198):'188',('zh_single',199):'189'}
NOTES = {f'mill_{n:03}':
    '此组位于《穆勒摘要》政府消费与税收摘录，主要转录穆勒论述；马克思插语在正文中保留，不能将所摘观点整体直接视作马克思主张。'
    for n in range(38,62)}
DOUBTS = {
    'mill_de_038':['|16|'], 'mill_de_050':['|17|'], 'mill_de_057':['|18|'],
}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid,{})[word] = dict(
            kind='glyph_doubt', status='retained_as_source',
            reported_reading='页内手稿位置标记按扫描可见形式转写',
            note='本地扫描可见竖线包围的页内位置数字；正文保留为定位符号。')


if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=24, release='0.4.0-alpha20',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES, row_notes=NOTES,
         coverage_notes={'mill':'精选评注13组，后接穆勒供求、政府消费与税收摘录48组，共61组；覆盖德印刷463—470/中文181—189页内，已到该中文单行本摘录节尾。前部及全篇分母仍待处理。'})
