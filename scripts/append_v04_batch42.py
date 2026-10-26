"""Batch 42: rent 030--053, social benefits, conflicting interests and competition."""
from append_v04_batch6 import main
from source_slices import rows,stream

DE=stream('de_megai2',[(355,11,42),(356,2,42),(357,2,42),(358,2,42)],join_page_hyphens=True)
ZH=stream('zh_collected',[(281,4,27),(282,2,24),(283,2,26),(284,2,27),(285,2,5)],{
    281:[('⑴','（1）'),('增加。’71(','增加。”71（'),('(2)','（2）'),('(3)','（3）'),('(4)','（4）'),
         ('増加','增加'),('提萵','提高'),('髙','高'),('高,','高，'),('剰下','剩下'),('159页)','159页）'),
         ('价格,','价格，')],
    282:[('奢侈品。"','奢侈品。”'),('结论说(','结论说（'),('161页)','161页）'),('挥翟','挥霍'),
         ('农业短工)','农业短工）'),('(1)','（1）'),('(2)','（2）'),('(3)','（3）'),('系•，','系；'),('髙','高')],
    283:[('(4)','（4）'),('(5)','（5）'),('(1)','（1）'),('(2)','（2）'),('(3)','（3）'),
         ('看来,','看来，'),('但是,','但是，'),('可能性,','可能性，'),('分工,','分工，'),
         ('(a)','（α）'),('331页)','331页）'),('髙','高')],
    284:[('地租,井能','地租，并能'),(';','；'),('(ß)','（β）'),('同样,','同样，'),('(Y)','（γ）'),
         ('用〜定量','用一定量'),('矿物量。"(','矿物量。”（'),('。”(','。”（'),('结果,','结果，'),
         ('秘魯','秘鲁'),('以后,','以后，'),('353页〉','353页）'),('(S)"','（δ）“'),('••••••','……')],
    285:[('价洛','价格')],
})
DE_STARTS=[
    '1) „Die Grundrente vermehrt','2) Wir haben schon von Say','3) „Jede Verbesserung',
    '|IX| Die grössere Nachfrage','Ausser diesem Vortheil','4) „Die Arten von Verbesserungen',
    'Wenn aber nun Smith','Wir erwähnen nur','1) Der Grundeigenthümer ist','2) Nach d[em] Nationalökonomen',
    '|Xl| 3) Da der Grundeigenthümer','4) Da die reale','5) Wenn also das Interesse',
    'Allgemein schon verhalten','|XIl| 1) nimmt','2) Der grosse Grundbesitz','3) Während jede',
    '4) Es sind noch 2','Nahrungsmittel, wie Vieh','Der kleine selbstarbeitende',
    'ß) Wir haben übrigens','7) „Man kann von einer Mine','Ganz dasselbe, was Smith','δ) „Es ist zu bemerken',
]
ZH_STARTS=[
    '（1）“地租随着','（2）我们已经从萨伊','（3）“社会状况','[IX]对原产品',
    '除了土地所有者','（4）“提高劳动生产力','但是，斯密从土地','我们现在只是顺便',
    '（1）按照国民经济学','（2）根据国民经济学家','[XI]（3）因为租地农场主',
    '（4）因为工业品','（5）由此看来','大地产和小地产','[XII]（1）工人和劳动工具',
    '（2）大地产把','（3）每一项社会改良','（4）还要考察','归根结底','在这种情况下，自耕',
    '（β）此外','（γ）“一般说来','斯密在这里关于矿山','（δ）“应该指出',
]
LABELS=[
    '人口增长与地租','交通工具改善与地租','社会改善与所有者财富','原产品需求和新的工业用途',
    '还有另一种利益','工业品降价提高实际地租','所有者与社会利益的反比','垄断欲及略去的制度问题',
    '财富增长与贫困奴役','所有者与租地农场主利益敌对','所有者与雇农利益敌对',
    '所有者与工业贫困的利害关系','所有者之间利益也不一致','大地产小地产与资本大小',
    '土地规模与工具分工的优势','土地改良资本利息的归属','社会改良与小地产的现金负担',
    '食物耕地调节其他地租','大地产调节地租并压低','自耕小土地所有者的处境',
    '资本大小和肥力优势','富矿价格调节与废弃矿山','矿山规律适用于地产','土地市价与货币利息',
]
ROWS=rows('rent',30,LABELS,DE,ZH,DE_STARTS,ZH_STARTS,de_end='Aus diesem Verhältniß')
PRINTED={('de_megai2',p):str(p) for p in range(355,359)}
PRINTED.update({('zh_collected',p):str(p-25) for p in range(281,286)})
SUSPECTS=['|IX|','Manuf actur','Theü','||X|','1611. H','|Xl|','Grundeigenthümer s',
          '|XIl|','accumulüt','Für um','cc)','cultivüt','producüen','bef indet','//XVI/','ß)','7)']
DOUBTS={f'{s}_de_{n:03}':[w for w in SUSPECTS if w in de] for s,n,_,de,*_ in ROWS}
OVERRIDES={uid:{w:dict(kind='glyph_doubt',status='open',reported_reading='扫描可见标记或字形待复核',
                       note='照录可见定位符及条目标记；不按中文希腊字母或罗马数字静默改写。')
                for w in ws if '|' in w or w in ('//XVI/','1611. H','ß)','7)','cc)')}
           for uid,ws in DOUBTS.items()}
OVERRIDES['rent_de_049']['//XVI/']['evidence_pages']=['de_megai2:358']

if __name__=='__main__':
    assert len(ROWS)==24
    main(rows=ROWS,printed=PRINTED,batch=42,release='0.4.0-alpha38',reviewed_date='2026-10-21',
         doubts=DOUBTS,issue_overrides=OVERRIDES)
