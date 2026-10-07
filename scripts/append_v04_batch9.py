"""Finish the reading sequence of Privateigentum und Arbeit (batch 9)."""
from append_v04_batch6 import main

ROWS = [
('private_work',19,'重农学派对地产本质的理解',
'Die Physiokratie läugnet den besondren äusserlichen nur gegenständlichen Reichthum, indem sie die Arbeit für sein Wesen erklärt. Aber zunächst ist die Arbeit für sie nur das subjektive Wesen des Grundeigenthums (sie geht von der Art des Eigenthums aus, welche historisch als die herrschende und anerkannte erscheint); sie läßt nur das Grundeigenthum zum entäusserten Menschen werden.',
'重农学派既然把劳动宣布为财富的本质，也就否定了特殊的、外在的、仅仅是对象性的财富。但是，在重农学派看来，劳动首先只是地产的主体本质（重农学派是以那种在历史上占统治地位并得到公认的财产为出发点的）；他们认为，只有地产才成为外化的人。',[385],[317]),
('private_work',20,'农业与封建性质的扬弃',
'Sie hebt seinen Feudalcharakter auf, indem sie die Industrie (Agrikultur) für sein Wesen erklärt; aber sie verhält sich läugnend zur Welt der Industrie, sie erkennt das Feudalwesen an, indem sie die Agricultor für die einzige Industrie erklärt.',
'他们既然把生产（农业）宣布为地产的本质，也就消除了地产的封建性质；但是，就他们宣布农业是惟一的生产来说，他们对工业世界持否定态度，并且承认封建制度。',[385,386],[317]),
('private_work',21,'工业包含地产的主体本质',
'Es versteht sich, daß sobald nun das subjektive Wesen der im Gegensatz zum Grundeigenthum, d. h. als Industrie sich constituirenden Industrie —, gefaßt wird, dieses Wesen jenen seinen Gegensatz in sich einschließt. Denn wie die Industrie das aufgehobne Grundeigenthum, so umfaßt ihr subjektives Wesen zugleich sein subjektives Wesen.',
'十分明显，那种与地产相对立的、即作为工业而确立下来的工业的主体本质一旦被理解，那么这种本质同时也包含着自己的那个对立面。因为正像工业包含着已被扬弃了的地产一样，工业的主体本质也同时包含着地产的主体本质。',[386],[317]),
('private_work',22,'从农业劳动到一般劳动',
'Wie das Grundeigenthum die erste Form des Privateigenthums ist, wie die Industrie ihr blos als eine besondre Art des Eigenthums zunächst historisch entgegentritt — oder vielmehr der freigelaßne Sklave des Grundeigenthums ist — so wiederholt sich bei der wissenschaftlichen Erfassung des subjektiven Wesens des Privateigenthums, der Arbeit dieser Proceß und die Arbeit erscheint zunächst nur als Landbauarbeit, macht sich dann aber als Arbeit überhaupt geltend.',
'地产是私有财产的第一个形式，而工业在历史上最初仅仅作为财产的一个特殊种类与地产相对立——或者不如说它是地产的获得自由的奴隶——，同样，在科学地理解私有财产的主体本质，理解劳动时，这一过程也在重演。而劳动起初只作为农业劳动出现，后来才作为一般劳动得到承认。',[386],[318]),
('private_work',23,'工业资本与私有财产的客观形式',
'/|lll| Aller Reichthum ist zum industriellen Reichthum, zum Reichthum der Arbeit geworden und die Industrie ist die vollendete Arbeit, wie das Fabrikwesen das ausgebildete Wesen der Industrie, d. h. der Arbeit ist und das industrielle Capital die vollendete objektive Gestalt des Privateigenthums ist.',
'[III]一切财富都成了工业的财富，成了劳动的财富，而工业是完成了的劳动，正像工厂制度是工业的即劳动的发达的本质，而工业资本是私有财产的完成了的客观形式一样。',[386],[318]),
('private_work',24,'私有财产成为世界历史性的力量',
'— Wir sehn wie auch nun erst das Privateigenthum seine Herrschaft über den Menschen vollenden und in allgemeinster Form zur weltgeschichtlichen Macht werden kann. —',
'——我们看到，只有这时私有财产才能完成它对人的统治，并以最普遍的形式成为世界历史性的力量。——',[386],[318]),
]

if __name__ == '__main__':
    main(rows=ROWS, printed={('de_megai2',385):'385',('de_megai2',386):'386',
         ('zh_collected',317):'292',('zh_collected',318):'293'},
         batch=9, release='0.4.0-alpha5', reviewed_date='2026-10-03',
         doubts={'private_work_de_020':['Agricultor'],'private_work_de_023':['/|lll|']})
