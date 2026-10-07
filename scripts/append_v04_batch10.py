"""First six reading groups of Privateigentum und Kommunismus; append once."""
from append_v04_batch6 import main

ROWS = [
('communism',1,'无产和有产的对立',
'X ad. p. XXXIX. Aber der Gegensatz von Eigenthumslosigkeit und Eigenthum ist ein noch indifferenter, nicht in seiner thätigen Beziehung, seinem innern Verhältniß, noch nicht als Widerspruch gefaßter Gegensatz, solange er nicht als der Gegensatz der Arbeit und des Capitals begriffen wird.',
'× 补入第XXXIX页。但是，无产和有产的对立，只要还没有把它理解为劳动和资本的对立，它还是一种无关紧要的对立，一种没有从它的能动关系上、它的内在关系上来理解的对立，还没有作为矛盾来理解的对立⁹³。',[386],[319]),
('communism',2,'私有财产的矛盾关系',
'Auch ohne die fortgeschrittne Bewegung des Privateigenthums, im alten Rom, in der Türkei etc kann dieser Gegensatz in der ersten Gestalt sich aussprechen. So erscheint er noch nicht als durch das Privateigenthum selbst gesezt. Aber die Arbeit, das subjektive Wesen des Privateigenthums, als Ausschliessung des Eigenthums und das Capital, die objektive Arbeit als Ausschliessung der Arbeit ist das Privateigenthum als sein entwickeltes Verhältniß des Widerspruchs, darum ein energisches, zur Auflösung treibendes Verhältniß.',
'这种对立即使没有私有财产的前进运动也能以最初的形式表现出来，如在古罗马、土耳其等。因此，它还不表现为由私有财产本身设定的对立。但是，作为财产之排除的劳动，即私有财产的主体本质，和作为劳动之排除的资本，即客体化的劳动，——这就是作为上述对立发展到矛盾关系的、因而促使矛盾得到解决的能动关系的私有财产。',[386],[319]),
('communism',3,'自我异化的扬弃与资本',
'xx ad ibidem Die Aufhebung der Selbstentfremdung macht denselben Weg, wie die Selbstentfremdung. Erst wird das Privateigenthum nur in seiner objektiven Seite, — aber doch die Arbeit als sein Wesen — betrachtet. Seine Daseinsform ist daher das Capital, das „als solches“ aufzuheben ist. (Proudhon.)',
'×× 补入同一页。自我异化的扬弃同自我异化走的是一条道路。最初，对私有财产只是从它的客体方面来考察，——但是劳动仍然被看成它的本质。因此，它的存在形式就是“本身”应被消灭的资本。（蒲鲁东。）',[387],[319]),
('communism',4,'傅立叶与圣西门的劳动观点',
'Oder die besondre Weise der Arbeit — als nivellirte, parcellirte und darum unfreie Arbeit wird als die Quelle der Schädlichkeit des Privateigenthums und seines Menschenentfremdeten Daseins gefaßt—Fourier, der d[en] Physiokraten entsprechend auch wieder die Landbauarbeit wenigstens als die ausgezeichnete faßt, während St. Simon im Gegensatz die Industriearbeit als solche für das Wesen erklärt und nun auch die alleinige Herrschaft der Industriellen und die Verbesserung der Lage der Arbeiter begehrt.',
'或者，劳动的特殊方式，即划一的、分散的因而是不自由的劳动，被理解为私有财产的有害性的和它同人相异化的存在的根源——傅立叶，他和重农学派一样，也把农业劳动看成至少是最好的劳动，⁹⁴而圣西门则相反，他把工业劳动本身说成本质，因此他渴望工业家独占统治，渴望改善工人状况。①',[387],[319,320]),
('communism',5,'共产主义的最初形式',
'Der Communismus endlich ist der positive Ausdruck des aufgehobnen Privateigenthums, zunächst das allgemeine Privateigenthum. Indem er dieß Verhältniß in seiner Allgemeinheit faßt, ist er 1) in seiner ersten Gestalt nur eine Verallgemeinerung und Vollendung desselben; als solche zeigt er sich in doppelter Gestalt:',
'最后，共产主义是扬弃了的私有财产的积极表现；起先它是作为普遍的私有财产出现的。共产主义是从私有财产的普遍性来看私有财产关系，因而共产主义\n（1）在它的最初的形式中不过是这种关系的普遍化和完成。⁹⁵这样的共产主义以双重的形式表现出来：',[387],[320]),
('communism',6,'占有目的与工人规定的推广',
'einmal ist die Herrschaft des sachlichen Eigenthums so groß ihm gegenüber, daß er alles vernichten will, was nicht fähig ist, als Privateigenthum von allen besessen [zu] werden; er will auf gewaltsame Weise v[on] Talent, etc abstrahiren, der physische, unmittelbare Besitz gilt ihm als einziger Zweck des Lebens und Daseins; die Bestimmung des Arbeiters wird nicht aufgehoben, sondern auf alle Menschen ausgedehnt; || das Verhältniß des Privateigenthums bleibt das Verhältniß der Gemeinschaft zur Sachenwelt;',
'首先，物质的财产对它的统治力量如此之大，以致它想把不能被所有人作为私有财产占有的一切都消灭；它想用强制的方法把才能等等抛弃。在它看来，物质的直接的占有是生活和存在的惟一目的；工人这个规定并没有被取消，而是被推广到一切人身上；私有财产关系仍然是共同体同实物世界的关系；',[387],[320]),
]

if __name__ == '__main__':
    main(rows=ROWS, printed={('de_megai2',386):'386',('de_megai2',387):'387',
         ('zh_collected',319):'294',('zh_collected',320):'295'},
         batch=10, release='0.4.0-alpha6', reviewed_date='2026-10-03', doubts={},
         new_sections=[dict(id='communism',title='私有财产和共产主义',
             aliases=['Privateigentum und Kommunismus','共产主义'],
             coverage='本节开头6个连续句群')],
         coverage_updates={'communism':['communism']})
