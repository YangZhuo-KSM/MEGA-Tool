"""Communism groups 007–012: local scans 387–388 and 295–296."""
from append_v04_batch6 import main

ROWS = [
('communism',7,'公妻制与粗陋共产主义',
'endlich spricht sich diese Bewegung, dem Privateigenthum das allgemeine Privateigenthum entgegenzustellen, in der thierischen Form aus, daß der Ehe (welche allerdings eine Form des exclusiven Privateigenthums ist) die Weibergemeinschaft, wo also das Weib zu einem gemeinschaftlichen und gemeinen Eigenthum wird, entgegengestellt wird. Man darf sagen, daß dieser Gedanke der Weibergemeinschaft das ausgesprochne Geheimniß dieses noch ganz rohen und gedankenlosen Communismus ist.',
'最后，用普遍的私有财产来反对私有财产这个运动是以一种动物的形式表现出来的：用公妻制——也就是把妇女变为公有的和共有的财产——来反对婚姻（它确实是一种排他性的私有财产的形式）。人们可以说，公妻制这种思想是这个仍然十分粗陋的和无思想的共产主义的昭然若揭的秘密。⁹⁶',[387],[320]),
('communism',8,'财富与共同体的关系',
'Wie das Weib aus der Ehe in die allgemeine Prostitution, so tritt die ganze Welt des Reichthums, d. h. des gegenständlichen Wesens d[es] Menschen, aus dem Verhältniß der exclusiven Ehe mit dem Privateigenthümer in das Verhältniß der universellen Prostitution mit der Gemeinschaft.',
'正像妇女从婚姻转向普遍卖淫一样，财富——人的对象性的本质——的整个世界，也从它同私有者的排他性的婚姻的关系转向它同共同体的普遍卖淫关系。',[387],[320]),
('communism',9,'个性的否定与私有财产',
'Dieser Communismus — indem er die Persönlichkeit d[es] Menschen überall negirt — ist eben nur der conséquente Ausdruck des Privateigenthums, welches diese Negation ist.',
'这种共产主义——由于到处否定人的个性——只不过是私有财产的彻底表现，私有财产就是这种否定。',[387],[320]),
('communism',10,'忌妒心与平均主义欲望',
'Der allgemeine und als Macht sich constituirende Neid ist die versteckte Form, in welcher die Habsucht sich herstellt und nur auf eine andre Weise sich befriedigt. Der Gedanke jedes Privateigenthums als eines solchen ist wenigstens gegen das reichere Privateigenthum als Neid und Nivellirungssucht gekehrt, so daß diese sogar das Wesen der Concurrenz ausmachen.',
'普遍的和作为权力而形成的忌妒心，是贪财欲所采取的并且只是用另一种方式使自己得到满足的隐蔽形式。任何私有财产，就它本身而言，至少对较富裕的私有财产怀有忌妒心和平均主义欲望，这种忌妒心和平均主义欲望甚至构成竞争的本质。',[387],[320]),
('communism',11,'粗陋共产主义与抽象否定',
'Der rohe Communist ist nur die Vollendung dieses Neides und dieser Nivellirung von dem vorgestellten Minimum aus. Er hat ein bestimmtes begrenztes Maaß. Wie wenig diese Aufhebung des Privateigenthums eine wirkliche Aneignung ist, beweist eben die abstrakte Negation der ganzen Welt der Bildung und der Civilisation; die Rückkehr zur unnatürlichen ||IV| Einfachheit des armen und bedürfnißlosen Menschen, der nicht über das Privateigenthum hinaus, sondern noch nicht einmal bei demselben angelangt ist.',
'粗陋的共产主义②不过是这种忌妒心和这种从想像的最低限度出发的平均主义的完成。它具有一个特定的、有限制的尺度。对整个文化和文明的世界的抽象否定，向贫穷的、需求不高的人——他不仅没有超越私有财产的水平，甚至从来没有达到私有财产的水平——的非自然的[IV]简单状态的倒退，恰恰证明私有财产的这种扬弃决不是真正的占有。⁹⁷',[387,388],[320,321]),
('communism',12,'劳动共同性与普遍资本家',
'Die Gemeinschaft ist nur eine Gemeinschaft der Arbeit und der Gleichheit des Salairs, den das gemeinschaftliche Capital, die Gemeinschaft als der allgemeine Capitalist auszahlt. Beide Seiten des Verhältnisses sind in eine vorgestellte Allgemeinheit erhoben, die Arbeit, als die Bestimmung, in welcher jeder gesezt ist, das Capital, als die anerkannte Allgemeinheit und Macht der Gemeinschaft.',
'共同性只是劳动的共同性以及由共同的资本——作为普遍的资本家的共同体——所支付的工资的平等的共同性。关系的两个方面被提高到想像的普遍性：劳动是为每个人设定的天职，而资本是共同体的公认的普遍性和力量。',[388],[321]),
]

if __name__ == '__main__':
    main(rows=ROWS, printed={('de_megai2',387):'387',('de_megai2',388):'388',
         ('zh_collected',320):'295',('zh_collected',321):'296'},
         batch=11, release='0.4.0-alpha7', reviewed_date='2026-10-03',
         doubts={'communism_de_011':['||IV|']},
         issue_overrides={'communism_de_011':{'||IV|':dict(kind='glyph_doubt',status='open',
             evidence_pages=['de_megai2:388'],reported_reading='IV页内标记的界符待核',
             note='PDF388在unnatürlichen与Einfachheit之间的标记暂转写为||IV|；左侧界符及罗马数字的具体字形仍待核。中文[IV]独立照录，不据译文确定德文标记。')}})
