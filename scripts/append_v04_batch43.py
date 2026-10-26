"""Batch 43: rent 054--077, landed property as commodity and division."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(358,41,42),(359,2,42),(360,2,42),(361,2,12)],
            join_page_hyphens=True)
ZH = stream('zh_collected', [(285,6,26),(286,2,26),(287,2,20)], {
    285: [('之W','之间'),('阶级:','阶级：'),('炮产','地产'),('(1)','（1）'),
          ('他3私','他。私'),('的;土地','的；土地')],
    286: [('封号;','封号；'),('俗语说:','俗语说：'),('同样.','同样，'),
          ('地位,','地位，'),('统治;','统治；'),('的~切','的一切')],
    287: [('财富;','财富；'),('所代替:，','所代替。'),('(2)','（2）'),('74,','74，'),
          ('来:','来：'),('竞争•样','竞争一样')],
})
DE_STARTS = [
    'Aus diesem Verhältniß','|XVn| Diese Concurrenz','Die lezte Folge','Diese Verschacherung',
    '1) Die sentimentalen Thränen','Erstens ist das feudale','Schon im Feudalgrundbesitz',
    'Ebenso gehört der Majoratsherr','Aber im feudalen Grundbesitz','Das Grundstück',
    'Ebenso erscheint die Herrschaft','|XVIII¡ Ebenso giebt','Ebenso haben die Bearbeiter',
    'Sitten, Charakter','Endlich sucht er','Es ist nöthig','Es ist nothwendig, daß, was',
    'Es ist nothwendig, daß das ruhende','Es ist endlich nothwendig','Damit tritt',
    '|XTX| 2) Was den Streit','Die Theilung des Grundbesitzes verneint','Die Folge davon',
    'Ausser den nationalökonomischen',
]
ZH_STARTS = [
    '从地租对货币利息','[XVII]这种竞争','因此，最终的结果','地产买卖，',
    '（1）浪漫主义者','首先，封建地产','封建的土地占有已经','同样，长子继承权',
    '但是，在封建的土地占有制下','地块随它','同样，地产的统治','[XVIII]正像',
    '同样，那些在领地','风尚、性格','最后，封建领主','这种外观必将消失',
    '地产的根源','稳定的垄断','最后，在这种竞争中','从而，中世纪的俗语',
    '[XIX]（2）关于','地产的分割否定','结果，地产的分割','除了工具分开',
]
LABELS = [
    '地租下降与地产集中','资本家兼任土地所有者','两阶级与所有者差别消失','地产商品化与贵族没落',
    '浪漫主义的感伤','封建地产与异化的土地','土地作为异己力量','长子继承与私有财产根基',
    '封建领主与密切关系外观','地块个性化与无机身体','地产统治与狭隘民族性','领地称号与家族史',
    '领地劳动者与政治依附','风尚性格与钱袋','贵族关系的浪漫灵光','地产卷入资本运动',
    '土地自利的无耻形式','稳定垄断转向竞争','资本对工人与所有者的统治','金钱与物质的统治',
    '地产分割争论引入','分割普遍化垄断','分割受私有制规律支配','工具分散与重复劳动',
]
ROWS = rows('rent',54,LABELS,DE,ZH,DE_STARTS,ZH_STARTS,de_end='Wo also die Theilung')
PRINTED = {('de_megai2',p):str(p) for p in range(358,362)}
PRINTED.update({('zh_collected',285):'260',('zh_collected',286):'261',('zh_collected',287):'262'})
SUSPECTS = ['|XVn|','Capitaüst','VoUendung','seme','Schern','individualisüt','seinpoütisches',
            'Seme','Nationaütät','|XVIII¡','Famüiengeschichte','f örmlich','Pf lichtverhältniß','|XTX|']
DOUBTS = {f'{s}_de_{n:03}':[w for w in SUSPECTS if w in de] for s,n,_,de,*_ in ROWS}
OVERRIDES = {uid:{w:dict(kind='glyph_doubt',status='open',
    reported_reading='可见页内标记或异常字形待复核',
    note='按扫描可见形式照录；保留原页定位，待研究者复核，不根据译文静默改写。')
    for w in ws} for uid,ws in DOUBTS.items()}
OVERRIDES['rent_de_065']['f örmlich']['evidence_pages'] = ['de_megai2:360']

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS,printed=PRINTED,batch=43,release='0.4.0-alpha39',reviewed_date='2026-10-21',
         doubts=DOUBTS,issue_overrides=OVERRIDES)
