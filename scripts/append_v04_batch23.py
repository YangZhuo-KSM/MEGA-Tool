"""Batch 23: 24 groups from Mill's supply/demand excerpts, with source provenance."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream

DE = stream('de_megaiv2', [(458,20,38),(459,2,42),(460,2,38)])
ZH = stream('zh_single', [(195,6,27),(196,1,28),(197,1,10)], {
    195:[('息量','总量'),('第253一255页','第253—255页'),(',', '，'),(';','；')],
    196:[('第256、257一258页','第256、257—258页'),('—一','——'),(',', '，'),(';','；')],
    197:[('一一','——'),(',', '，'),(':','：')],
})
DE_STARTS = [
 '1131 Mill.','Unter welcher Form','Wenn er einen Theil','Weil also die Nachfrage',
 'Offre und demande haben','Jede dargebotne','Wenn zwei Menschen',
 'Sind aber offre','Die Totalität des jährlichen','11-4 j Man wirft',
 'Obgleich die Nachfrage','Dennoch streng genommen','Da Nachfrage und Zufuhr',
 'In diesem Fall Ueberfluß','Gesezt nun diese','Findet sich aber',
 'Die praktischen Folgen','Der überflüssig zugeführte','Das Fallen des ersten',
 'Das Steigen des selten','Das Stärkste,','In diesem Fall würde',
 'Da der Theil jedes','Die Production kann also nie',
]
ZH_STARTS = [
 '(3)“显然','无论年产品','如果他自己消费','“可见，因为每个人',
 '供给和需求处于','每一种被供给','当两个人进行交换',
 '但是如果每一个人','有多少人分配','人们对此提出异议',
 '“虽然每一个','尽管如此，严格地说','“既然每个人的需求',
 '“在这种情况下，无论','现在假定','但是，如果某一商品',
 '“需求和供给之间','供给过剩的商品','前一种商品跌价',
 '短缺商品涨价','“可以用来证明','“在这种情况下，每个人',
 '既然每个人在年产品','可见，同需求相比',
]
LABELS = ['个人产品与总供给','年产品脱手的供给','消费余额与供给','个人供需相等论',
 '供需的特殊关系','商品兼为供给与需求对象','交换双方的供给和需求','个人与全国供需',
 '年产品各部分与总需求','商品过剩的异议','找不到适当买者','严格意义的供需相等',
 '个别商品供需与总量','没有总量过剩的主张','呢绒增产与资本转移','短缺与过剩的相互关系',
 '供需不一致的实际结果','过剩跌价与短缺涨价','跌价与资本流出','涨价与利润平均化',
 '只消费必需品的假设','节余投入生产','原料日用品与总供需','生产创造需求的结论']
ROWS = rows('mill',14,['穆勒摘录：'+label for label in LABELS],DE,ZH,DE_STARTS,ZH_STARTS)
PRINTED = {('de_megaiv2',458):'466',('de_megaiv2',459):'467',
           ('de_megaiv2',460):'468',('zh_single',195):'185',
           ('zh_single',196):'186',('zh_single',197):'187'}
NOTES = {f'mill_{n:03}':'此组位于《穆勒摘要》后续摘录段，主要转录穆勒供求论述，不能将所摘观点直接视作马克思主张。' for n in range(14,38)}
NOTES['mill_014'] += '德文此处编号4)，中文为(3)，按各自底本保留；德文页内13形标记暂照文字层候选1131。'
DOUBTS = {'mill_de_014':['1131','\\'], 'mill_de_022':['|'],
          'mill_de_023':['11-4 j'], 'mill_de_031':['||15|'],
          'mill_de_034':['L','1'], 'mill_de_037':['|']}
OVERRIDES = {}
for uid, words in DOUBTS.items():
    for word in words:
        OVERRIDES.setdefault(uid,{})[word] = dict(kind='glyph_doubt',status='open',
          reported_reading='页内数字界符或引文界符待核',
          note='保留本地扫描可见定位符号的候选转写；不依据另一版本的编号改写。')

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=23, release='0.4.0-alpha19',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         source_by_section=ROUTES, row_notes=NOTES,
         coverage_notes={'mill':'精选评注13组，后接供求摘录24组，共37组；覆盖德印刷463—468/中文181—187页内，未收全篇。前部及后续摘录、全篇分母仍待处理。'})
