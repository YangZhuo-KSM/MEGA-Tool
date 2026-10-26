"""Batch 41: rent 006--029, monopoly price, tenant conflict and food rents."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE=stream('de_megai2',[(352,13,42),(353,2,42),(354,2,42),(355,2,10)],{
    354:[('sie reicht nicht 1 o hin','sie reicht nicht hin')],
},join_page_hyphens=True)
ZH=stream('zh_collected',[(278,8,25),(279,2,30),(280,2,30),(281,2,3)],{
    278:[('一来.','一来，'),('。”(','。”（'),('161页)','161页）'),('"如果','“如果'),
         ('篚场','渔场'),('拼作','耕作')],
    279:[('"当','“当'),('份额,','份额，'),('余額','余额'),('地租,','地租，'),('萨伊说/','萨伊说：“'),
         (';','；'),('以外,','以外，'),('独車','独享'),('提髙','提高'),('诚然,','诚然，'),
         ('一满,','一满，'),('最髙','最高'),('价格。"','价格。”'),('。”(','。”（')],
    280:[('。”(','。”（'),('378页〉','378页）'),('髙','高'),('303、304页)','303、304页）'),
         ('亊情','事情'),('劳动量,','劳动量，'),('狗买','购买'),('数a','数量'),
         ('305,306','305、306'),('"不仅','“不仅'),('345页〉','345页）'),
         ('入的食物','人的食物'),('地租的。"','地租的。”'),('337页)','337页）'),('湖口','糊口'),
         ('342页)','342页）'),('339]页〉','339]页）')],
    281:[('搾取','榨取')],
})
DE_STARTS=[
    '„Die Grundrente als Preiß','„Von den 3 produktiven','Wir haben schon gehört','Ein andres Moment',
    '„Die Rente wechselt','„Sind Ländereien','Diese Sätze von Smith','Betrachten wir aber',
    'Die Grundrente wird festgesezt','Sehn wir nun, wie Grundeigenthümer','„Der Grundeigenthümer sucht',
    '„Die Grundeigenthümer", sagt Say','„Die Grundrente, betrachtet','„Die Grundrente der Oberfläche',
    'Nicht bei allen Waaren','„Gewöhnlich kann man','„Die Grundrente geht','Zu den Produkten',
    '„Da die Menschen','„Die Grundrente zieht','„Die Nahrung d[es]','„Die Länder bevölkern',
    '„Die 2 größten','jvmj Sehn wir',
]
ZH_STARTS=[
    '“这样一来','“在这三大阶级','我们已经听说','决定地租数量','“不管土地','“如果土地',
    '斯密的这些论点','现在让我们来考察','地租是通过','现在我们来看','“当决定租约',
    '萨伊说：“土地所有者','“因此被看成','“因此，土地地面','不可能为一切商品',
    '“通常人们只能','“地租以与工资','食物是始终','“因为像一切动物',
    '“不仅食物','“可见，人的食物','“一国有多少','“除了食物','[VIII]现在',
]
LABELS=[
    '地租是一种垄断价格','无需劳心劳力的收入','土地肥力与地租数量','土地位置与地租数量',
    '肥力和位置的变动','资本使用与土地富饶程度','把肥力变成土地所有者特性','现实关系中的地租',
    '租地农场主与所有者的斗争','双方相互关系的问题','租约与自然地租','萨伊论所有者的垄断优势',
    '租地农场主能支付的最高价格','总产品份额与固定地租','有些商品不支付地租','市场运输成本与地租',
    '地租作为价格结果','食物始终提供地租','食物剩余与地租支付','其他产品地租与食物生产力',
    '食物足以支付地租','人口与能供养的人数','衣服住宅取暖与地租','所有者榨取社会利益的问题',
]
ROWS=rows('rent',6,LABELS,DE,ZH,DE_STARTS,ZH_STARTS)
PRINTED={('de_megai2',p):str(p) for p in range(352,356)}
PRINTED.update({('zh_collected',p):str(p-25) for p in range(278,282)})
SUSPECTS=['Fruchtbarkeitder','| |lll|','Ueberau','||IV|','mögüch','Vortheü','semer','SteUung',
          'aUein','zuprofitiren','verhältmßmässig','Π','wüd','natürÜcher','3l','Theü','zufäüigen',
          '||V|','74','Ζ.','weiches','Salate','Wtkung','||VI|','LI','jvmj']
DOUBTS={f'{s}_de_{n:03}':[w for w in SUSPECTS if w in de] for s,n,_,de,*_ in ROWS}
OVERRIDES={uid:{w:dict(kind='glyph_doubt',status='open',reported_reading='定位符或分数/字形待复核',
                       note='扫描可见形式照录，保留数字字形和页内定位符候选；未据译文统一。')
                for w in ws if '|' in w or w in ('3l','74','Ζ.','Π','LI','jvmj')}
           for uid,ws in DOUBTS.items()}
OVERRIDES['rent_de_019']['74']['evidence_pages']=['de_megai2:354']

if __name__=='__main__':
    assert len(ROWS)==24
    main(rows=ROWS,printed=PRINTED,batch=41,release='0.4.0-alpha37',reviewed_date='2026-10-21',
         doubts=DOUBTS,issue_overrides=OVERRIDES)
