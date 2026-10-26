"""Batch 40: finish profit 097--115 and open rent 001--005."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(348,42,42),(349,2,42),(350,2,42),(351,2,9)], join_page_hyphens=True)
ZH = stream('zh_collected', [(274,5,25),(275,2,31),(276,2,5)], {
    274: [('劳动吋间','劳动时间'),('法律•','法律……'),('82页)','82页）'),('拼种','耕种'),
          ('人数,','人数，'),('髙','高'),('。”(','。”（'),("'‘因为",'“因为'),('事•物','事物'),
          ('越多,','越多，'),('越细.','越细，'),('T具','工具'),('分工。"','分工。”'),('大人提高','大大提高')],
    275: [('提髙','提高'),('资本,','资本，'),('数董','数量'),('195页)','195页）'),('过剥','过剩'),
          ('"由于','“由于'),('数竜','数量'),(';','；'),('自已','自己'),('••••••','……'),('_个','一个'),
          ('OOO',''),('〈德意志季刊〉','《德意志季刊》'),('<伯明翰的矿区〉~文','〈伯明翰的矿区〉一文'),
          ('公司中.','公司中，'),('积蓄.','积蓄，'),('对立。"','对立。”'),('(舒尔茨','（舒尔茨'),('41页)','41页）')],
    276: [('7fl','70')],
})
ROWS = rows('profit',97,[
    '雇主与贫困的物的力量','英国地方产业缺少资本','增加年产品的两种方式','资本积累与劳动分工',
    '积累推动劳动生产力','由此出现生产过剩','生产力更广泛的联合','主要生产部门的结合',
    '工厂与地产商业的联合','英国厂主与小国家','伯明翰制铁过程的集中','股份公司的财力与知识',
    '资本多种用途与利益结合','有产与无产阶级的对立加深','房租与工业贫困','从无产者恶习获利',
    '资本地产联合与竞争减少','对人的漠不关心与彩票','萨伊的纯收入与总收入',
],DE,ZH,[
    '«le maître','„In England giebt','«Pour augmenter','„Weü es also','„Ebenso wie die Arbeit',
    'Also Ueberproduktion','„Umfassendere Combinationen','Auch schon hie','So werden grosse Fabrikanten',
    'In England, wo einzelne','So übernehmen','Endlich sehn wir','Hierdurch den Capitalisten',
    'Aber selbst diese','Ungeheurer Gewinn','Ebenso Procente','Die Accumulation der Capitaüen',
    'Gleichgültigkeit gegen','Revenu net et brut',
],[
    '“雇主用只够','“英国许多地方','“要增加土地','“因为按照事物','“劳动生产力的大大提高',
    '由此出现了生产过剩','“由于在更大规模','有些地方，主要','例如，大工厂主',
    '在英国，单个的工厂主','例如，伯明翰','最后，我们在目前','这样一来，资本家',
    '然而，这种用不同','房东从贫困','还从堕落','当资本和地产','对人的漠不关心','萨伊的纯收入',
])
DE_RENT = stream('de_megai2',[(351,10,39),(352,2,12)],join_page_hyphens=True)
ZH_RENT = stream('zh_collected',[(277,2,21),(278,2,7)],{
    277: [('136贸','136页'),('注)','注）'),('认为.','认为，'),('但是,','但是，'),('(1)','（1）'),
          ('地租,','地租，'),('(追加费)','（追加费）'),(';(2)','；（2）'),('金,','金，'),
          ('如此,','如此，'),('提商','提高'),('Ô己','自己'),('（3〉','（3）'),('301页)','301页）'),
          ('(Seekrapp，salicorne〉','（Seekrapp，salicorne）'),('盐,','盐，'),('各地,','各地，'),
          ('〈涨潮，marée>','〈涨潮，marée〉')],
    278: [('地阻','地租'),('东两','东西'),('比例。"','比例。”'),('"可以','“可以'),
          ('祖地','租地'),('。”(','。”（')],
})
ROWS += rows('rent',1,['土地权利的掠夺起源','未播种而收获的土地所有者','改良费用与原始地租',
                     '海草渔业和土地地租','地租作为自然力产物'],DE_RENT,ZH_RENT,
             ['|l| Grundrente.','Die Grundeigenthümer üeben','„Man könnte sich vorstellen',
              'Smith führt als Beispiel','„Man kann die Grundrente'],
             ['地租[I]土地所有者','土地所有者也像','“也许有人认为',
              '为说明后一种情况','“可以把地租'])
PRINTED = {('de_megai2',p):str(p) for p in range(348,353)}
PRINTED.update({('zh_collected',p):str(p-25) for p in range(274,279)})
NEW_SECTIONS = [dict(id='rent',title='地租',work='1844年经济学哲学手稿',manuscript='第一手稿',
                     aliases=['Grundrente'],coverage='节首连续5句群')]
SUSPECTS = ['Capitaüen','Woüe','theüs','weü','||XTV|','residüen','travaü','ü','„Weü',
            'Theüung','kerne','Unterabtheüungen','zerf äüt','avancüten','classificüen',
            'unterabzutheüen','Capitaüst','nämhch','|/XV/','w\'e/erTheilnehmendenmitden',
            'wissenschaf tüchen','landwirthschafüiche','||XVl|','|l|','üeben','äraten','gjebt','||ll|']
DOUBTS={f'{s}_de_{n:03}':[w for w in SUSPECTS if w in de] for s,n,_,de,*_ in ROWS}
OVERRIDES={uid:{w:dict(kind='glyph_doubt',status='open',reported_reading='可见标记或字形待复核',
                       note='按本地扫描可见形式照录，未据译文统一定位符或异常字形。')
                for w in ws if '|' in w} for uid,ws in DOUBTS.items()}
OVERRIDES['profit_de_101']['|/XV/']['evidence_pages']=['de_megai2:350']

if __name__=='__main__':
    assert len(ROWS)==24
    main(rows=ROWS,printed=PRINTED,batch=40,release='0.4.0-alpha36',reviewed_date='2026-10-21',
         doubts=DOUBTS,issue_overrides=OVERRIDES,new_sections=NEW_SECTIONS,
         coverage_updates={'rent':['rent']},
         coverage_notes={'profit':'节首连续至115节尾，章节首尾及注释范围集中审计待做。',
                         'rent':'节首连续5句群，德351—352/中文252—253，停在自然力产物定义末。'})
