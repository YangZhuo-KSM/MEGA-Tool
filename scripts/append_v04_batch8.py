"""Third manuscript, physiocracy: German PDF385; Chinese PDF316–317."""
from append_v04_batch6 import main

ROWS = [
('private_work',13,'魁奈与重农主义的过渡',
'Die physiokratische Lehre von Dr. Quesnay bildet den Uebergang aus dem Mercantilsystem zu Adam Smith. Die Physiokratie ist unmittelbar die nationalökonomische Auflösung des Feudaleigenthums, aber darum eben so unmittelbar die nationalökonomische Umwandlung, Wiederherstellung desselben, nur daß seine Sprache nun nicht mehr feudal, sondern ökonomisch wird.',
'魁奈医生的重农主义学说是从重商主义体系到亚当·斯密的过渡。重农学派直接是封建所有制在国民经济学上的解体，但正因为如此，它同样直接是封建所有制在国民经济学上的变革、恢复，不过它的语言这时不再是封建的，而是经济学的了。',[385],[316]),
('private_work',14,'土地与财富的对象',
'Aller Reichthum wird aufgelöst in die Erde und den Landbau; (Agrikultur) die Erde ist noch nicht Capital, sie. ist noch eine besondre Daseinsweise desselben, die in ihrer und um ihrer natürlichen Besonderheit willen gelten soll; aber die Erde ist doch ein allgemeines natürliches Element, während das Merkantüsystem nur das edle Metall als Existenz des Reichthums kennt. Der Gegenstand des Reichthums, seine Materie, hat also sogleich die höchste Allgemeinheit innerhalb der Naturgrenze, — insofern er noch als Natur unmittelbar gegenständlicher Reichthum ist — erhalten.',
'全部财富被归结为土地和耕作（农业）。土地还不是资本，它还是资本的一种特殊的存在形式，这种存在形式应当在它的自然特殊性中并且由于它的这种自然特殊性而起作用。但是，土地毕竟是一种普遍的自然要素，而重商主义体系只知道贵金属是财富的存在。因此，财富的对象、财富的材料立即获得了自然界范围之内的最高普遍性，因为它们作为自然界仍然是直接对象性的财富。',[385],[316]),
('private_work',15,'农业作为劳动的特殊形式',
'Und die Erde ist nur durch die Arbeit, die Agrikultur für den Menschen. Also wird schon das subjektive Wesen des Reichthums in die Arbeit versezt. Aber zugleich ist die Agricultur die einzig produktive Arbeit. Also ist die Arbeit noch nicht in ihrer Allgemeinheit und Abstraktion gefaßt, sie ist noch an ein besondres Naturelement als ihre Materie gebunden, sie ist daher auch nur noch in einer besonderen Naturbestimmten Daseinsweise erkannt.',
'而土地只有通过劳动、耕种才对人存在。因而财富的主体本质已经移入劳动中。但是，农业同时是惟一的生产的劳动。因此，劳动还不是从它的普遍性和抽象性上被理解的，它还是同一种作为它的材料的特殊自然要素结合在一起，因而，它也还是仅仅在一种特殊的、自然规定的存在形式中被认识的。',[385],[316,317]),
('private_work',16,'土地与劳动的因素关系',
'Sie ist daher erst eine bestimmte, besondre Entäusserung d[es] Menschen, wie ihr Product auch als ein bestimmter, — mehr noch der Natur als ihr selbst anheimfallender Reichthum — gefaßt ist. Die Erde wird hier noch als von Menschen unabhängiges Naturdasein anerkannt, noch nicht als Capital, d. h. als ein Moment der Arbeit selbst. Vielmehr erscheint die Arbeit als ihr Moment.',
'因此，劳动不过是人的一种特定的、特殊的外化，正像劳动产品还被理解为一种特定的财富——与其说来源于劳动本身，不如说来源于自然界的财富。在这里，土地还被看作不依赖于人的自然存在，还没有被看作资本，就是说，还没有被看作劳动本身的因素。相反，劳动却表现为土地的因素。',[385],[317]),
('private_work',17,'财富的普遍本质与抽象劳动',
'Indem aber der Fetischismus des alten äusserlichen nur als Gegenstand existirenden Reichthums auf ein sehr einfaches Naturelement reducirt und sein Wesen schon, wenn auch erst theilweise auf eine besondre Weise, in seiner subjektiven Existenz anerkannt ist, ist der nothwendige Fortschritt, daß das allgemeine Wesen des Reichthums erkannt und daher die Arbeit in ihrer vollständigen Absolutheit, d. h. Abstraktion, zum Princip erhoben wird.',
'但是，因为这里把过去的外在的仅仅作为对象存在的财富的拜物教归结为一种极其简单的自然要素，而且已经承认——虽然只是部分地、以一种特殊的方式承认——财富的本质就在于财富的主体存在，所以，认出财富的普遍本质，并因此把具有完全绝对性即抽象性的劳动提高为原则，是一个必要的进步。',[385],[317]),
('private_work',18,'一般劳动作为财富的本质',
'Es wird der Physiokratie bewiesen, daß die Agrikultur in ökonomischer Hinsicht, also d[er] einzig berechtigten von keiner andern Industrie verschieden sei, also nicht eine bestimmte Arbeit, eine an ein besondres Element II gebundne, eine besondre Arbeitsäusserung, sondern die Arbeit überhaupt das Wesen des Reichthums sei.',
'人们向重农学派证明，从经济学观点即惟一合理的观点来看，农业同任何其他一切生产部门毫无区别，因此，财富的本质不是某种特定的劳动，不是与某种特殊要素结合在一起的、某种特殊的劳动表现，而是一般劳动。',[385],[317]),
]

if __name__ == '__main__':
    main(rows=ROWS, printed={('de_megai2',385):'385',('zh_collected',316):'291',('zh_collected',317):'292'},
         batch=8, release='0.4.0-alpha4', reviewed_date='2026-10-03',
         doubts={'private_work_de_014':['sie.', 'Merkantüsystem'], 'private_work_de_018':['Element II gebundne']})
