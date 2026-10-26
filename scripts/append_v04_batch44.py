"""Batch 44: rent 078--102, division, association and end of the section (25 groups)."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2',[(361,12,42),(362,2,42),(363,3,16)],join_page_hyphens=True)
ZH = stream('zh_collected',[(287,21,24),(288,2,26),(289,2,23),(290,2,7)],{
    287:[('否定(扬弃)①','否定（扬弃）①')],
    288:[('垄断、联合','垄断。联合'),('优点是,','优点是，'),('自已','自己'),('压搾','压榨')],
    289:[('敌人、如果','敌人。如果'),('堆厚','雄厚'),('地产;','地产；')],
})
DE_STARTS = [
    'Wo also die Theilung','Das ist aber nicht die Rückkehr','Die erste Aufhebung',
    'Die Aufhebung des Monopols','Die Association,','Ein grosser Vortheü',
    'Was den grossen Grundbesitz','Ebenso haben sie den Verschacherungsgeist',
    'Wie das grosse Grundeigenthum','Ueberhaupt beruht','Uebrigens, wie die Theilung',
    'Denn das grosse Grundeigenthum','Es macht die Majorität','Hat die Industrie',
    'Unter der Herrschaft der Industrie','Einmal in die Concurrenz','||XXl| Die unmittelbare',
    'Endlich führt der grosse','Der grosse Grundbesitz hat','Die Landarbeiter sind',
    'Durch die Concurrenz mit dem Ausland','Ein grosser Theil der Grundeigenthümer',
    'Andrerseits werden sich','Endüch muß','Das Grundeigenthum mußte',
]
ZH_STARTS = [
    '因此，凡是进行地产分割','但是，这不是回到','对垄断的最初扬弃','扬弃了具有最广泛',
    '联合一旦应用于土地','地产分割的一大优点','至于说到大地产','同样，这些维护者',
    '大地产可以把地产分割','总之，私有财产','此外，正如地产分割','这是因为大地产',
    '大地产把国内的大多数','如果工业获得雄厚','因为，在工业的统治下','地产一旦卷入竞争',
    '[XXI]直接的结果','最后，那种就这样','正如我们在英国看到的','结果，农业工人',
    '由于同外国竞争','很大一部分土地所有者','另一方面，有许多租地农场主',
    '最后，为了经受住新的竞争','工业必然以垄断',
]
LABELS = [
    '地产分割的两种去向','扬弃土地私有制','垄断的最初扬弃','垄断的完全消灭',
    '土地联合平等与个人财产','分割与摆脱农奴制','大农业优势和所有权废除','大小地产的牟利行为',
    '分割与垄断的相互责难','私有财产以分割为基础','封建地产必然分割或转移','大地产制造资本的力量',
    '工业人口成为大地产敌人','工业迫使地产参加国际竞争','封建地产与外国垄断',
    '竞争中的地产波动','地产分散与工业资本','大地产更快引向危机','英国产业化地产和收入',
    '雇农最低工资与租地阶级','外国竞争与地租收入','土地所有者取代租地者','租地者占有地产与破产',
    '工资进一步降低与革命','地产两种形式的必然灭亡',
]
ROWS = rows('rent',78,LABELS,DE,ZH,DE_STARTS,ZH_STARTS)
PRINTED = {('de_megai2',361):'361',('de_megai2',362):'362',('de_megai2',363):'363',
           ('zh_collected',287):'262',('zh_collected',288):'263',
           ('zh_collected',289):'264',('zh_collected',290):'265'}
SUSPECTS = ['Veraügemeinerung','theüt','Vortheü','ursprüngüche','Theüung','persönüches','wüd',
            'seme','theüs','(|XX|','angegriff en','dies]','f ortgehn','f hegend','prädesünirten',
            '||XXl|','größtentheüs','Einkornmen','theüweise','exploitüen','ruinüt','Endüch',
            'reducüte','reducüt','ruüiüen']
DOUBTS = {f'{s}_de_{n:03}':[w for w in SUSPECTS if w in de] for s,n,_,de,*_ in ROWS}
OVERRIDES = {uid:{w:dict(kind='glyph_doubt',status='open',
    reported_reading='可见页内标记或异常字形待复核',
    note='照录扫描可见形式；跨页疑点指向实际来源页，不按译文或常见词形静默改写。')
    for w in ws} for uid,ws in DOUBTS.items()}
OVERRIDES['rent_de_100']['größtentheüs']['evidence_pages'] = ['de_megai2:363']

if __name__ == '__main__':
    assert len(ROWS) == 25  # complete the chapter without splitting its final argument
    main(rows=ROWS,printed=PRINTED,batch=44,release='0.4.0-alpha40',reviewed_date='2026-10-21',
         doubts=DOUBTS,issue_overrides=OVERRIDES,
         coverage_notes={'rent':'从节首连续102个句群至节尾；非原书自然段，首尾/衔接和注释范围待集中审计'})
