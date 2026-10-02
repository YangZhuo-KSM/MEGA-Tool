"""Third manuscript continuation; local PDF384 and Chinese PDF315–316."""
from append_v04_batch6 import main

ROWS = [
('private_work',7,'外在异化与异化活动',
'Was früher sich Aüsserlichsein, reale Entäusserung d[es] Menschen, ist nur zur That der Entäusserung, zur Veräusserung geworden.',
'以前是自身之外的存在——人的真正外化——的东西，仅仅变成外化的行为，变成外在化。',[384],[315]),
('private_work',8,'国民经济学原则的展开',
'Wenn also jene Nationalökonomie unter dem Schein der Anerkennung des Menschen, seiner Selbstständigkeit, Selbsttätigkeit, etc beginnt und wie sie in das Wesen d[es] Menschen selbst das Privateigenthum versezt, nicht mehr durch die lokalen, nationalen etc Bestimmungen des Privateigenthums als eines ausser ihr existirenden \\\\ Wesens bedingt sein kann, also eine kosmopolitische, allgemeine, jede Schranke, jedes Band umwerfende Energie entwickelt, um sich als die einzige Politik, Allgemeinheit, Schranke und Band an die Stelle zu setzen — so muß sie bei weitrer Entwicklung diese Scheinheiligkeit abwerfen, in ihrem ganzen Cynismus hervortreten und sie thut dieß, indem sie — unbekümmert um alle scheinbaren Widersprüche, worin diese Lehre sie verwickelt — viel einseitiger, darum schärfer und consequenter die Arbeit als das einzige Wesen des Reichthums entwickelt, die Consequenzen dieser Lehre im Gegensatz zu jener ursprünglichen Auffassung vielmehr als Menschenfeindliche nachweist und endlich dem lezten, individuellen, natürlichen, unabhängig von der Bewegung der Arbeit existirenden Dasein des Privateigenthums und Quelle des Reichthums — der Grundrente, diesen schon ganz nationalökonomisch gewordnen und daher gegen die Nationalökonomie widerstandsunfähigen Ausdruck des Feudaleigenthums — den Todesstoß giebt.',
'因此，如果上述国民经济学是从表面上承认人、人的独立性、自主活动等等开始，并由于把私有财产移入人自身的本质中而能够不再受制于作为存在于人之外的本质的私有财产的那些地域性的、民族的等等的规定，从而发挥一种世界主义的、普遍的、推毁一切界限和束缚的能量，以便自己作为唯一的政策、普遍性、界限和束缚取代这些规定，——那么国民经济学在它往后的发展过程中必定抛弃这种伪善性，而表现出自己的十足的昔尼克主义⁹²。它也是这样做的——它不在乎这种学说使它陷入的那一切表面上的矛盾，它十分片面地，因而也更加明确和彻底地发挥了关于劳动是财富的惟一本质的论点，然而它表明，这个学说的结论与上述原来的观点相反，不如说是敌视人的；最后，它还致命地打击了私有财产和财富源泉的最后的个别的、自然的、不依赖于劳动运动的存在形式即地租，打击了这种已经完全成了经济的东西因而对国民经济学无法反抗的封建所有制的表现。',[384],[315,316]),
('private_work',9,'从斯密到李嘉图和穆勒',
'(Schule des Ricardo.) Nicht nur wächst der Cynismus der Nationalökonomie relativ von Smith über Say bis zu Ricardo, Mill etc; insofern die Consequenzen der Industrie den leztern entwickelter und widerspruchsvoller vor die Augen treten; sondern auch positiv gehn sie immer und mit Bewußtsein weiter in der Entfremdung gegen d[en] Menschen als ihr Vorgänger, aber nur, weil ihre Wissenschaft sich consequenter und wahrer entwickelt.',
'（李嘉图学派。）从斯密经过萨伊到李嘉图、穆勒等等，国民经济学的昔尼克主义不仅相对地增长了——因为工业所造成的后果在后面这些人面前以更发达和更充满矛盾的形式表现出来——，而且肯定地说，他们总是自觉地在排斥人这方面比他们的先驱者走得更远，但是，这只是因为他们的科学发展得更加彻底、更加真实罢了。',[384],[316]),
('private_work',10,'现实矛盾与原则的本质',
'Indem sie das Privateigenthum in seiner thätigen Gestalt zum Subjekt machen, also zugleich d[en] Menschen zum Wesen und zugleich den Menschen als ein Unwesen zum Wesen machen, so entspricht der Widerspruch der Wirklichkeit vollständig dem widerspruchsvollen Wesen, das sie als Princip erkannt haben.',
'因为他们使具有活动形式的私有财产成为主体，就是说，既使人成为本质，又同时使作为某种非存在物[Unwesen]的人成为本质，所以现实中的矛盾就完全符合他们视为原则的那个充满矛盾的本质。',[384],[316]),
('private_work',11,'工业现实与分裂的原则',
'Die zerrißne ||n| Wirklichkeit der Industrie bestätigt ihr in sich zerrißnes Princip, weit entfernt, es zu widerlegen.',
'支离破碎的[II]工业现实不仅没有推翻，相反，却证实了他们的自身支离破碎的原则。',[384],[316]),
('private_work',12,'分裂状态的原则',
'Ihr Princip ist ja das Princip dieser Zerrissenheit.',
'他们的原则本来就是这种支离破碎状态的原则。',[384],[316]),
]

if __name__ == '__main__':
    main(rows=ROWS, printed={('de_megai2',384):'384',('zh_collected',315):'290',('zh_collected',316):'291'},
         batch=7, release='0.4.0-alpha3', doubts={'private_work_de_007':['sich Aüsserlichsein'],
         'private_work_de_011':['||n|']})
