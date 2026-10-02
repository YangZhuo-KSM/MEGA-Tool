"""Rebuild the curated seed dataset from reviewed PDF text caches.

This is an editorial seed, not an automatic aligner. Curated Chinese readings and
German OCR corrections were initially proposed by Codex; some were later found
unsupported (see docs/TRANSCRIPTION_REVIEW.md). Never use this command to overwrite later
researcher edits: it refuses to overwrite an existing corpus unless --force.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from inspect_sources import FILES

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'tmp' / 'source_review'

# Each tuple: editorial navigation label, German start anchor, next anchor,
# German PDF pages, Chinese PDF pages, Chinese text transcribed from the scan.
ALIENATION = [
('竞争与垄断', 'Eben weil', 'Wir haben also jezt', [364], [292],
 '正因为国民经济学不理解运动的联系，所以才把例如竞争的学说同垄断的学说，行业自由的学说同同业公会的学说，地产分割的学说同大地产的学说重新对立起来。因为竞争、行业自由、地产分割仅仅被阐述和理解为垄断、同业公会和封建所有制的偶然的、蓄意的、强制的结果，而不是必然的、不可避免的、自然的结果。'),
('异化与货币制度', 'Wir haben also jezt', 'Versetzen wir uns', [364], [292],
 '因此，我们现在必须弄清楚私有制，贪欲和劳动、资本、地产三者的分离之间，交换和竞争之间，人的价值和人的贬值之间，垄断和竞争等等之间，这全部异化和货币制度之间的本质联系。'),
('虚构的原始状态', 'Versetzen wir uns', 'Wir gehn von', [364], [292],
 '不要像国民经济学家那样，当他想说明什么的时候，总是置身于一种虚构的原始状态。这样的原始状态什么问题也说明不了。⁷⁶国民经济学家只是使问题堕入五里雾中。他把应当加以推论的东西即两个事物之间的例如分工和交换之间的必然关系，假定为事实、事件。神学家也是这样用原罪来说明恶的起源，就是说，他把他应当加以说明的东西假定为一种具有历史形式的事实。'),
('从经济事实出发', 'Wir gehn von', 'Der Arbeiter wird', [364], [292],
 '我们且从当前的经济事实出发。'),
('物的增值与人的贬值', 'Der Arbeiter wird', 'Dieß Factum', [364], [292],
 '工人生产的财富越多，他的产品的力量和数量越大，他就越贫穷。⁷⁷工人创造的商品越多，他就越变成廉价的商品。物的世界的增值同人的世界的贬值成正比。劳动生产的不仅是商品，它生产作为商品的劳动自身和工人，而且是按它一般生产商品的比例生产的。'),
('劳动的对象化', 'Dieß Factum', 'Die Verwirklichung der Arbeit erscheint so', [364,365], [292,293],
 '这一事实无非是表明：劳动所生产的对象，即劳动的产品，作为一种异己的存在物，作为不依赖于生产者的力量，同劳动相对立。劳动的产品是固定在某个对象中的、物化的劳动，这就是劳动的对象化。劳动的现实化就是劳动的对象化。在国民经济学假定的状况中，劳动的这种现实化表现为工人的非现实化⁷⁸，对象化表现为对象的丧失和被对象奴役，占有表现为异化、外化⁷⁹。'),
('对象的丧失', 'Die Verwirklichung der Arbeit erscheint so', 'In der Bestimmung', [365], [293],
 '劳动的现实化竟如此表现为非现实化，以致工人非现实化到饿死的地步。对象化竟如此表现为对象的丧失，以致工人被剥夺了最必要的对象——不仅是生活的必要对象，而且是劳动的必要对象。甚至连劳动本身也成为工人只有通过最大的努力和极不规则的中断才能加以占有的对象。对对象的占有竟如此表现为异化，以致工人生产的对象越多，他能够占有的对象就越少，而且越受自己的产品即资本的统治。'),
('产品成为独立力量', 'In der Bestimmung', '|XXHl|', [365], [293],
 '这一切后果包含在这样一个规定中：工人对自己的劳动的产品的关系就是对一个异己的对象的关系。因为根据这个前提，很明显，工人在劳动中耗费的力量越多，他亲手创造出来反对自身的、异己的对象世界的力量就越强大，他自身、他的内部世界就越贫乏，归他所有的东西就越少。宗教方面的情况也是如此。人奉献给上帝的越多，他留给自身的就越少。⁸⁰工人把自己的生命投入对象；但现在这个生命已不再属于他而属于对象了。因此，这种活动越多，工人就越丧失对象。凡是成为他的劳动的产品的东西，就不再是他自身的东西。因此，这个产品越多，他自身的东西就越少。工人在他的产品中的外化，不仅意味着他的劳动成为对象，成为外部的存在，而且意味着他的劳动作为一种与他相异的东西不依赖于他而在他之外存在，并成为同他对立的独立力量；意味着他给予对象的生命是作为敌对的和相异的东西同他相对立。'),
('考察对象化', '|XXHl|', 'Der Arbeiter kann', [365], [293,294],
 '[XXIII]现在让我们来更详细地考察一下对象化，工人的生产，并且考察对象即工人产品在对象化中的异化、丧失。'),
('自然界与劳动材料', 'Der Arbeiter kann', 'Wie aber die Natur', [365], [294],
 '没有自然界，没有感性的外部世界，工人什么也不能创造。它是工人的劳动得以实现、工人的劳动在其中活动、工人的劳动从中生产出和借以生产出自己的产品的材料。'),
('劳动与生活资料', 'Wie aber die Natur', 'Je mehr also', [365,366], [294],
 '但是，自然界一方面在这样的意义上给劳动提供生活资料，即没有劳动加工的对象，劳动就不能存在，另一方面，也在更狭隘的意义上提供生活资料，即维持工人本身的肉体生存的手段。'),
('生活资料的双重丧失', 'Je mehr also', 'Nach dieser doppelten', [366], [294],
 '因此，工人越是通过自己的劳动占有外部世界、感性自然界，他就越是在两个方面失去生活资料：第一，感性的外部世界越来越不成为属于他的劳动的对象，不成为他的劳动的生活资料；第二，感性的外部世界越来越不给他提供直接意义的生活资料，即维持工人的肉体生存的手段。'),
]

MILL = [
('需要与产品的权力', 'Du hast allerdings', 'Wenn ich mehr', [455], [191],
 '当然，你作为人同我的产品有一种人的关系；你需要我的产品；因此，我的产品对你来说是作为你的愿望和你的意志的对象而存在的。但是，你的需要、你的愿望、你的意志对我的产品来说却是软弱无力的需要、愿望和意志。换句话说，你的人的因而也就是同我的人的产品必然有内在联系的本质，并不是你支配这种产品的权力，并不是你对这种产品的所有权，因为我的产品所承认的不是人的本质的特性，也不是人的本质的权力。相反，你的需要、你的愿望、你的意志是使你依赖于我的纽带，因为它们使你依赖于我的产品。它们根本不是一种赋予你支配我的产品的权力的手段，倒是一种赋予我支配你的权力的手段！'),
('剩余产品与相互承认', 'Wenn ich mehr', 'Der Austausch vermittelt', [455,456], [191,192],
 '如果我生产的物品超过了我自己能够直接消费的，那么，我的剩余产品是精确地估计到你的需要的。我只是在表面上多生产了这种物品。实际上我生产了另一种物品，即我想以自己的剩余产品来换取的、你所生产的物品，这种交换在我思想上已经完成了。因此，我同你的社会关系，我为你的需要所进行的劳动只不过是假象，我们的相互补充，也只是一种以相互掠夺为基础的假象。在这里，掠夺和欺骗的企图必然是秘而不宣的，因为我们的交换无论从你那方面或从我这方面来说都是利己的，因为每一个人的私利都力图超过另一个人的私利，所以我们就不可避免地要设法相互欺骗。我认为我的物品对你的物品所具有的权力的大小，当然需要得到你的承认，才能成为真正的权力。但是，我们相互承认对方对自己物品的权力，这却是一场斗争。在这场斗争中，谁更有毅力，更有力量，更高明，或者说，更狡猾，谁就胜利。如果身强力壮，我就直接掠夺你。如果用不上体力了，我们就相互讹诈，比较狡猾的人就欺骗不太狡猾的人。就整个关系来说，谁欺骗谁，这是偶然的事情。双方都进行观念上和思想上的欺骗，也就是说，每一方都已在自己的判断中欺骗了对方。'),
('交换的中介', 'Der Austausch vermittelt', 'Die einzig verständliche', [456], [192],
 '总之，双方的交换必然是以每一方生产的和占有的物品为中介的。当然，我们彼此同对方产品的观念上的关系是我们彼此的需要。但是，现实的、实际的、真正的、在事实上实现的关系，只是彼此排斥对方对自己产品的占有。在我心目中，惟一能向你对我的物品的需要提供价值、身份、实效的，是你的物品，即我的物品的等价物。因此，我们彼此的产品是满足我们彼此的需要的手段、中介、工具、公认的权力。因此，你的需求和你所占有的等价物，对我来说是具有同等意义的、相同的术语；你的需求只有在对我具有意义和效用时，才具有效用，从而具有意义。如果单纯地把你看作一个没有这种交换工具的人，那么，你的需求从你这方面来说是得不到满足的愿望，而在我看来则是实现不了的幻想。可见，你作为人，同我的物品毫无关系，因为我自己同我的物品也不具有人的关系。但是，手段是支配物品的真正的权力。因此，我们彼此把自己的产品看作一个人支配另一个人而且也支配自己的权力，这就是说，我们自己的产品顽强地不服从我们自己，它似乎是我们的财产，但事实上我们是它的财产。我们自己被排斥于真正的财产之外，因为我们的财产排斥他人。'),
('人的语言与物的语言', 'Die einzig verständliche', 'Allerdings:', [456], [193],
 '我们彼此进行交谈时所用的惟一可以了解的语言，是我们的彼此发生关系的物品。我们不懂得人的语言了，而且它已经无效了；它被一方看成并理解为请求、哀诉，[XXXIII]从而被看成屈辱，所以使用它时就带有羞耻和被唾弃的感情；它被另一方理解为不知羞耻或神经错乱，从而遭到驳斥。我们彼此同人的本质相异化已经达到了这种程度，以致这种本质的直接语言在我们看来成了对人类尊严的侮辱，相反，物的价值的异化语言倒成了完全符合理所当然的、自信的和自我认可的人类尊严的东西。'),
('目的与手段', 'Allerdings:', 'Unser wechselseitiger', [456,457], [193],
 '当然，在你心目中，你的产品是攫取我的产品从而满足你的需要的工具、手段。但是，在我心目中，它是我们交换的目的。相反，对我来说，你是生产那在我看来是目的的物品的手段和工具，而你对我的物品也具有同样的关系。但是，（1）我们每个人实际上把自己变成了另一个人心目中的东西；你为了攫取我的物品实际上把自己变成了手段、工具、你自己的物品的生产者。（2）你自己的物品对你来说仅仅是我的物品的感性的外壳，潜在的形式，因为你的生产意味着并表明想谋取我的物品的意图。这样，你为了你自己而在事实上成了你的物品的手段、工具，你的愿望则是你的物品的奴隶，你像奴隶一样从事劳动，目的是为了你所愿望的对象永远不再给你恩赐。如果我们被物品弄得相互奴役的状况在发展的初期实际上就表现为统治和被奴役的关系，那么这仅仅是我们的本质关系的粗陋的和直率的表现。'),
('彼此的价值', 'Unser wechselseitiger', 'Gesezt wir hätten', [457], [193],
 '对我们来说，我们彼此的价值就是我们彼此拥有的物品的价值。因此，在我们看来，一个人本身对另一个人来说是某种没有价值的东西。'),
('假定我们作为人进行生产', 'Gesezt wir hätten', 'Unsere Productionen', [457], [193,194],
 '假定我们作为人进行生产。在这种情况下，我们每个人在自己的生产过程中就双重地肯定了自己和另一个人：（1）我在我的生产中使我的个性和我的个性的特点对象化，因此我既在活动时享受了个人的生命表现，又在对产品的直观中由于认识到我的个性是对象性的、可以感性地直观的因而是毫无疑问的权力而感受到个人的乐趣。（2）在你享受或使用我的产品时，我直接享受到的是：既意识到我的劳动满足了人的需要，从而使人的本质对象化，又创造了与另一个人的本质的需要相符合的物品。（3）对你来说，我是你与类之间的中介，你自己认识到和感觉到我是你自己本质的补充，是你自己不可分割的一部分，从而我认识到我自己被你的思想和你的爱所证实。（4）在我个人的生命表现中，我直接创造了你的生命表现，因而在我个人的活动中，我直接证实和实现了我的真正的本质，即我的人的本质，我的社会的本质。'),
('反映本质的镜子', 'Unsere Productionen', 'Dieß Verhältniß wäre', [457], [194],
 '我们的产品都是反映我们本质的镜子。'),
('关系的相互性', 'Dieß Verhältniß wäre', 'Betrachten wir die verschiedenen', [457], [194],
 '情况就是这样：你那方面所发生的事情同样也是我这方面所发生的事情。'),
('考察不同因素', 'Betrachten wir die verschiedenen', 'Meine Arbeit wäre', [458], [194],
 '让我们来考察一下在我们的假定中出现的不同因素。'),
('自由的生命表现', 'Meine Arbeit wäre', 'Zweitens:', [458], [194],
 '我的劳动是自由的生命表现，因此是生活的乐趣。在私有制的前提下，它是生命的外化，因为我劳动是为了生存，为了得到生活资料。我的劳动不是我的生命。'),
('劳动与个性', 'Zweitens:', 'Nur als das', [458], [194,195],
 '第二：因此，我在劳动中肯定了自己的个人生命，从而也就肯定了我的个性的特点。劳动是我真正的、活动的财产。在私有制的前提下，我的个性同我自己外化到这种程度，以致这种活动为我所痛恨，它对我来说是一种痛苦，更正确地说，只是活动的假象。因此，劳动在这里也仅仅是一种被迫的活动，它加在我身上仅仅是由于外在的、偶然的需要，而不是由于内在的必然的需要。'),
]

CORRECTIONS = {
 'de_megai2': [('ζ. B.', 'z. B.'), ('ConSequenzen', 'Consequenzen'),
    ('Verwirküchung', 'Verwirklichung'), ('Arbeitsgegenstande', 'Arbeitsgegenstände'),
    ('Voraussetzimg', 'Voraussetzung'), ('|XXHl|', '|XXIII|'), ('Lebensnüttel', 'Lebensmittel')],
 'de_megaiv2': [('Eigentümlichkeit', 'Eigenthümlichkeit'), ('Deiner Produktion', 'Deiner Production'),
    ('bioser', 'bloser'), ('besizt', 'besitzt'), ('Verhältniß to', 'Verhältniß'),
    ('Gesezt wir', 'Gesetzt wir')],
}

# The supplied PDF reads "trete Lebensäusserung". Keep that reading.
# A contextually plausible alternative belongs in an editorial note, never here.


def page_text(source, page):
    return (CACHE / source / f'{page:04}.txt').read_text(encoding='utf-8')


def german_stream(source, pages):
    """Remove known running heads, page labels and marginal line counters only."""
    chunks = []
    for number in pages:
        lines = page_text(source, number).splitlines()[1:]
        lines = [x for x in lines if not re.fullmatch(r'\s*\d+\s*', x)]
        lines = [re.sub(r'^\s*(?:5|10|15|20|25|30|35|40)\s+', '', x) for x in lines]
        lines = [re.sub(r'\s+(?:5|10|15|20|25|30|35|40)\s*$', '', x) for x in lines]
        chunks.append('\n'.join(lines))
    text = '\n'.join(chunks)
    # Only join hyphens at a printed line break. In-line hyphens are preserved.
    text = re.sub(r'[-\u00ad]\s*\n\s*', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'data' / 'corpus.json'
    if target.exists() and not args.force:
        parser.error('Corpus exists; refusal to overwrite researcher changes')
    now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')
    sources = []
    editions = []
    info = [
      ('de_megai2','de',508,'MEGA² I.2','Werke · Artikel · Entwürfe. März 1843 bis August 1844',1982,'Dietz Verlag Berlin','Inge Taubert (Leitung); Deana Bauer; Bernhard Dohm','1982','Zweite Wiedergabe'),
      ('zh_collected','zh',825,'中文全集第3卷','马克思恩格斯全集 第三卷',2002,'人民出版社','中共中央马克思恩格斯列宁斯大林著作编译局','第2版',''),
      ('de_megaiv2','de',574,'MEGA² IV.2','Exzerpte und Notizen. 1843 bis Januar 1845',1981,'Dietz Verlag Berlin','Nelly Rumjanzewa (Leitung); Bernhard Dohm; Swetlana Nasarowa; Eleonora Safronowa; Ljudmila Welitschanskaja','1981',''),
      ('zh_single','zh',236,'中文单行本（2000）','1844年经济学哲学手稿',2000,'人民出版社','中共中央马克思恩格斯列宁斯大林著作编译局','第3版，2004年10月重印',''),
    ]
    for sid,lang,count,short,title,year,publisher,editor,edition,presentation in info:
        path = ROOT / 'Asset_by_user' / FILES[sid]
        sources.append(dict(id=sid,file_name=FILES[sid],pdf_page_count=count,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        editions.append(dict(id=sid,source_id=sid,language=lang,short_title=short,title=title,year=year,publisher=publisher,editor=editor,translator=editor if lang=='zh' else None,edition=edition,presentation=presentation,metadata_status='title_text_checked'))
    sections = [dict(id='alienation', title='异化劳动和私有财产', work='1844年经济学哲学手稿', manuscript='第一手稿',aliases=['Entfremdete Arbeit und Privateigentum'], coverage='精选连续12组，非全文'),
        dict(id='mill',title='詹姆斯·穆勒《政治经济学原理》一书摘要',work='巴黎笔记',manuscript='穆勒笔记',aliases=['穆勒评注','穆勒批注','穆勒笔记'],coverage='评注部分精选连续12组，非全文')]
    corpus = dict(schema_version=1, release='0.1.0-preview',editions=editions,sources=sources,sections=sections,units=[],alignments=[],page_map=[],comparisons=[],corrections=[],coverage=[
        dict(id='manuscript1',title='第一手稿',state='部分收录',detail='异化劳动精选12组'),
        dict(id='manuscript2',title='第二手稿',state='未收录',detail='后续逐节整理'),
        dict(id='manuscript3',title='第三手稿',state='未收录',detail='后续逐节整理'),
        dict(id='mill',title='穆勒评注',state='部分收录',detail='评注精选12组')])
    evidence = {}
    page_map = {}
    for sec, rows, de, zh, all_pages in [('alienation',ALIENATION,'de_megai2','zh_collected',range(364,367)),('mill',MILL,'de_megaiv2','zh_single',range(455,459))]:
        stream = german_stream(de, all_pages)
        for n,(label,start,end,de_pages,zh_pages,zh_text) in enumerate(rows,1):
            a = stream.index(start)
            b = stream.index(end,a+len(start))
            raw_de = stream[a:b].strip()
            text_de = raw_de
            for old,new in CORRECTIONS[de]:
                text_de = text_de.replace(old,new)
            for sid,lang,pages,text,raw in [(de,'de',de_pages,text_de,raw_de),(zh,'zh',zh_pages,zh_text,None)]:
                uid = f'{sec}_{lang}_{n:03}'
                locations=[]
                for p in pages:
                    printed = str(p if sid=='de_megai2' else p+8 if sid=='de_megaiv2' else p-25 if sid=='zh_collected' else p-10)
                    # These explicit reviewed pages use these local offsets only.
                    # The application never extrapolates an offset to other pages.
                    key=f'{sid}:{p}'
                    evidence[key]=page_text(sid,p)
                    loc=dict(source_id=sid,printed_page=printed,pdf_page=p)
                    locations.append(loc)
                    page_map[key]=dict(**loc,status='scan_checked_ai',checked_by='Codex',checked_at=now)
                unit=dict(id=uid,edition_id=sid,language=lang,section_id=sec,sequence=n,label=label,text=text,locations=locations,
                    proofread_status='scan_checked_ai',proofread_by='Codex',proofread_at=now,evidence_pages=[f'{sid}:{p}' for p in pages],
                    transcription_note='纯文本阅读转录：合并排版断行，不复现字重/斜体；保留旧拼写、手稿位置符号及中文注号。导航标题由项目添加。原页为最终核对依据。')
                corpus['units'].append(unit)
                corpus['corrections'].append(dict(unit_id=uid,method='scan_review_ai',reviewed_by='Codex',reviewed_at=now,
                    extracted_reading=raw,corrected_text=text,evidence_pages=unit['evidence_pages'],
                    note='德文保留机械去页眉/行号后的提取稿；中文按扫描页逐段转录，原始OCR全文见extraction.json对应页。'))
            corpus['alignments'].append(dict(id=f'{sec}_{n:03}',section_id=sec,label=label,de_ids=[f'{sec}_de_{n:03}'],zh_ids=[f'{sec}_zh_{n:03}'],status='uncertain',proposed_by='Codex',verified_by=None,verified_at=None,review_batch=(n-1)//6+1+(0 if sec=='alienation' else 2),note='AI拟定对应，待研究者逐批确认。'))
    corpus['page_map']=list(page_map.values())
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(corpus,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (target.parent/'extraction.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Saved {len(corpus["alignments"])} pending alignments, {len(corpus["units"])} units, {len(page_map)} reviewed page mappings.')


if __name__=='__main__':
    main()
