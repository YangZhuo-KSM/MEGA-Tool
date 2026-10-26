"""Batch 21: 24 money groups, using explicit scan-reviewed extraction slices."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(434,21,38),(435,2,38),(436,2,41),(437,2,42),(438,2,39)])
ZH = stream('zh_collected', [(384,3,22),(385,2,27),(386,2,26),(387,2,21),
                              (388,2,26),(389,2,26),(390,2,3)], {
    384: [('待殊性','特殊性'),(';','；'),('（1)', '（1）'),('（2)', '（2）'),
          ('（3)', '（3）'),('（5)', '（5）'),('(4)', '（4）')],
    385: [('你的!','你的！'),('我的9','我的？'),('歌德〈浮士德〉(靡菲斯特斐勒司的话)®',
          '歌德《浮士德》（靡菲斯特斐勒司的话）①'),
          ('莎士比亚在<雅典的泰门》中说：','莎士比亚在《雅典的泰门》中说：'),
          ('拜金客。','拜金客。\n……'),('癩病','癞病'),(';','；')],
    386: [('oOOO0',''),('呼譽','冰炭'),('[xlii]^t不同的a的，','[XLII]为了不同的目的，'),
          ('法力.让他们互相枣f','法力，让他们互相砍杀'),('鲁类','兽类'),('°©°','②'),(',', '，')],
    387: [('的~切','的一切'),(';','；')],
    389: [('不完蕃性','不完善性'),('变成爱.','变成爱，'),(',', '，'),(':','：')],
})

DE_STARTS = [
 '|XL[I]|','2) da, wo','3) insofern','4) erst durch','5) der Sinn',
 'Das Geld, indem','Das Geld ist der Kuppler','Was mü aber','„Was Henker?',
 'I Shakespeare','Und weiter unten:', 'Shakespeare schildert',
 'Was durch das Geld','So groß die Kraft','Die Eigenschaften des Geldes',
 'Das was ich bin','Ich bin häßlich','Ich — meiner Individuaütät',
 'ich bin ein schlechter','Das Geld ist das höchste Gut', 'ich bin geistlos',
 'Zudem kann er','Ich, der durch','Verwandelt also',
 'Wenn das Geld das Band', 'Kann es nicht alle Bande','Ist es darum',
 'Es ist die wahre', 'Shakespeare hebt', '2) Es ist die',
 'Die Verkehrung und Verwechslung','Was ich qua Mensch',
 'Wenn ich mich nach','Als diese Vermittlung','Die demande existirt',
 'Der Unterschied der effectiven','Ich, wenn ich kern Geld zum Reisen',
 'Ich, wenn ich Beruf','Das Geld — als das äussere','Schon dieser Bestimmung',
 'Als diese verkehrende Macht','|Da das Geld','Wer die Tapferkeit',
 'Da das Geld nicht','Setze den Menschen','Jedes deiner Verhältnisse','Wenn du liebst',
]
ZH_STARTS = [
 '[XLI]','（2）','（3）','（4）','（5）',
 '货币，因为','货币是需要','但是，在我','“见鬼！',
 '莎士比亚在','并且下面又说：','莎士比亚把',
 '依靠货币','货币的力量多大','货币的特性就是',
 '因此，我是什么','我是丑的','我——就我的个人',
 '我是一个邪恶的','货币是最高的善','我是没有头脑的',
 '再说他可以','既然我有能力','这样，我的货币',
 '如果货币是','它难道不能够','因此，它难道不也是',
 '它既是地地道道','莎士比亚特别','(2)它是',
 '使一切人的和自然的性质','凡是我作为人',
 '当我渴望食物','作为这样的中介','当然，没有货币',
 '以货币为基础的','如果我没有供旅行','如果我有进行研究',
 '货币是一种外在','因此，仅仅按照这个规定','其次，对于个人',
 '因为货币作为现存','谁能买到勇气','因为货币所交换',
 '我们现在假定','你对人和对自然界','如果你在恋爱',
]
LABELS = [
 '感觉与激情的本体论肯定','感性肯定与对象扬弃','他人肯定与自己的享受','工业与人的激情',
 '私有财产意义与本质对象','货币的万能特性','需要与对象的牵线人','人与生活的中介',
 '歌德浮士德引诗','莎士比亚泰门第一段引诗','莎士比亚泰门第二段引诗','货币描绘与诗句解释',
 '货币购买力与占有者','货币力量与我的力量','货币特性成为人的力量','个性不再决定能力',
 '丑与美的购买','跛足与二十四只脚','货币尊敬与占有者','最高善与诚实推定',
 '货币作为实际的头脑','支配有头脑者','购买人的一切能力','无能力变成对立物',
 '一切纽带的纽带','联结与解开纽带','通用的分离剂','辅币与社会电化学势',
 '货币的第一特性','货币的第二特性','异化的类本质与神力','货币改变个人本质力量',
 '愿望转化为感性现实','中介的创造力','没有货币的需求','有效与无效需求的区别',
 '旅行需要的实现','研究本领与货币','现实与观念的转化','个性的普遍颠倒',
 '社会关系的颠倒','价值概念与普遍替换','购买勇气','全部对象世界的交换',
 '人的关系与相互交换','关系作为个人生命表现','爱与相应的爱',
]
ALL_ROWS = rows('money',1,LABELS,DE,ZH,DE_STARTS,ZH_STARTS)


def line_breaks(text, starts):
    for start in starts:
        at = text.find(start)
        if at <= 0:
            raise ValueError(f'Poem line boundary missing: {start}')
        text = text[:at].rstrip() + '\n' + text[at:]
    return text


POEM_LINES = {
 9: (['Und Kopf','Doch alles','Ist das drum','Wenn ich sechs','Sind ihre Kräfte',
      'Ich renne','Als hätt','Göthe.'],
     ['还有头','可是，我新','难道因此','我假如','它们的脚力','我骑着','真好像','歌德《']),
 10: (['„Gold?','Nicht eitel','So viel','Schlecht gut','Dieß lockt','Reißt Halbgenesnen',
       'Ja dieser','Geweihte Bande','Er macht','Und giebt','Im Rath','Der über',
       'Sie von','Mit Ekel','Zu Maienjugend','Gemeine Hure','Die Völker'],
      ['“金子','不，天神','我不是无聊','……','这东西，只','就可以','错的变成','老人变成',
       '这东西会','把壮汉','这黄色','它可以使受','使害着','它可以使窃贼','它可以使鸡皮',
       '即使她','有了这东西','该死的土块','你惯会']),
 11: (['„Du süsser','Des Sohns','Von Hymens','Du ewig','Deß rother','Auf Dianas',
       'Die du','Zum Kuß','|XLIl|','Denk,','Vernichte','Daß Thieren'],
      ['“啊，','帝王','亲生','你灿烂','淫污','你勇敢','你永远','你的羞颜','你有形',
       '你会使冰炭','[XLII]','你会说','你动人','你的奴隶','快快','留下']),
}
for n,(de_lines,zh_lines) in POEM_LINES.items():
    old = ALL_ROWS[n-1]
    ALL_ROWS[n-1] = (*old[:3],line_breaks(old[3],de_lines),line_breaks(old[4],zh_lines),*old[5:])

ROWS = ALL_ROWS[:24]
PRINTED = {('de_megai2', p):str(p) for p in (434,435,436,437,438)}
PRINTED.update({('zh_collected',384):'359',('zh_collected',385):'360',
 ('zh_collected',386):'361',('zh_collected',387):'362',('zh_collected',388):'363',
 ('zh_collected',389):'364',('zh_collected',390):'365'})


def issues_for(selected):
    # Literal anomalous words visible on these scans; retain them with annotations.
    vocabulary = ['Eigenthümüchkeit','menschUch','mü','freüich','Individuaütät','wtkliche',
      'Gegentheü','aügemeine','Quaütäten','Unmögüchkeiten','individueUen','wül',
      'VorsteUung','sümliches','wüküche','Sem','kern','kerne','Wükung','unwirküch',
      'basüten','inmü','wtkücher','wüküches','verwüküchendes','Studüen','wtksamen',
      'wüküch','kernen','Wülen','GeseUschaft','aUgemeine','eher','wirküchen','menschüchen',
      'gemessen']
    markers = ['|XL[I]|','I','|XLIl|','||','|¡XLIIl|','|']
    doubts, overrides = {}, {}
    for section,n,_,de,_,dp,_ in selected:
        uid = f'{section}_de_{n:03}'
        words = [w for w in vocabulary + markers if w in de]
        doubts[uid] = words
        for w in markers:
            if w in words:
                overrides.setdefault(uid,{})[w] = dict(kind='glyph_doubt',status='open',
                  reported_reading='页内界符或罗马数字转写待核',
                  note='扫描页可见标记按候选形式保留，界符与罗马数字字形待研究者核对。')
    return doubts, overrides


if __name__ == '__main__':
    assert len(ROWS) == 24
    doubts, overrides = issues_for(ROWS)
    main(rows=ROWS, printed=PRINTED, batch=21, release='0.4.0-alpha17',
         reviewed_date='2026-10-19', doubts=doubts, issue_overrides=overrides,
         new_sections=[dict(id='money',title='货币',work='1844年经济学哲学手稿',
           manuscript='第三手稿',aliases=['Geld'],coverage='开头连续片段')],
         coverage_updates={'money':['money']})
