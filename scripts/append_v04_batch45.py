"""Batch 45: the preface from manuscript III, 14 complete sentence groups."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2',[(325,3,28),(326,2,33)],{
    326:[('theoretische 1 o Revolution','theoretische Revolution')],
},join_page_hyphens=True)
ZH = stream('zh_collected',[(244,3,15),(245,2,20),(246,2,6),(247,2,3)],{
    244:[('批判。39','批判。³⁹'),('批判。56','批判。⁵⁶'),('国民经济学42','国民经济学⁴²'),
          ('范围3','范围。')],
    245:[('著作。S»','著作。⁵⁸'),('〈二十一印张〉','《二十一印张》'),
          ('（德法年鉴〉','《德法年鉴》'),('<国民经济学批判大纲〉','《国民经济学批判大纲》'),
          ('。59在','。⁵⁹在'),('要点','要点。①'),('批判《。','批判⁶¹。'),
          ('〈现象学〉','《现象学》'),('〈逻辑学)62','《逻辑学》⁶²'),('说,','说，')],
    246:[('意ÎR的','意识的')],
    247:[('场合*3','场合⁶³')],
})
DE_STARTS = [
    '|XXXIX| Vorrede.','Bei der Ausarbeitung','Ueberdem hätte','Ich werde daher',
    'Man findet aus diesem Grunde','Dem mit der Nationalökonomie','Es versteht sich von selbst',
    'Die Inhaltsvollen','Ausserdem verdankt','Von Feuerbach datirt','Je geräuschloser',
    'Das Schlußkapitel','// Genau angesehn','Diese interessante Gerechtigkeit',
]
ZH_STARTS = [
    '[XXXIX]我在','在加工整理','此外，由于需要探讨','因此，我打算',
    '由于这个原因','我用不着向熟悉','不消说，','但是，德国人在这门科学',
    '此外，对国民经济学的批判','从费尔巴哈起','费尔巴哈的著作越',
    '我认为，本著作的最后一章','仔细考察起来','历史现在仍然指派',
]
LABELS = [
    '法学国家学批判的预告','思辨批判与材料批判','材料多样性和格言式叙述','分册批判和整体联系',
    '本著作的国民经济学范围','经验分析与批判研究','法国英国及德国社会主义著作','赫斯与恩格斯的研究',
    '费尔巴哈对实证批判的奠基','人道主义和自然主义批判','费尔巴哈著作的理论革命',
    '黑格尔批判与批判的神学家','神学批判与哲学超验性','哲学消极解体与历史判决',
]
ROWS = rows('preface',1,LABELS,DE,ZH,DE_STARTS,ZH_STARTS)
PRINTED = {('de_megai2',325):'325',('de_megai2',326):'326',
           ('zh_collected',244):'219',('zh_collected',245):'220',
           ('zh_collected',246):'221',('zh_collected',247):'222'}
NEW_SECTIONS = [dict(id='preface',title='序言（第三手稿）',work='1844年经济学哲学手稿',
                     manuscript='第三手稿',aliases=['Vorrede','Vorrede (aus Heft III)'],
                     coverage='正文节首至节尾14个句群，注释范围待集中审计')]
SUSPECTS = ['|XXXIX|','hegeVsehen','phüosophie','||','f ür','||XL|','Ungrühdlichkeit',
            '//','Verf aulungsprozeß','/']
DOUBTS = {f'{s}_de_{n:03}':[w for w in SUSPECTS if w in de] for s,n,_,de,*_ in ROWS}
OVERRIDES = {uid:{w:dict(kind='glyph_doubt',status='open',
    reported_reading='可见页内界符或异常字形待复核',
    note='照录扫描可见形式，保留原页标记；不按现代词形或中文译文静默改写。')
    for w in ws} for uid,ws in DOUBTS.items()}
ROW_NOTES = {
    'preface_006':'中文PDF244的①指向原手稿删文脚注，脚注正文留在原页。',
    'preface_008':'中文PDF245的①为本卷页码参照；两侧正文均接续到恩格斯摘要及本著作要点。',
    'preface_009':'中文PDF245的②指向删文脚注；正文与脚注分开。',
    'preface_012':'中文PDF246的①指向长篇删文，跨页正文不拼入该脚注。',
    'preface_014':'中文PDF247的①指向序言末删文；正文至末句，脚注全文仍在原页。',
}

if __name__ == '__main__':
    assert len(ROWS) == 14  # preface ends here; keep whole sentences and chapter boundary
    main(rows=ROWS,printed=PRINTED,batch=45,release='0.4.0-alpha41',reviewed_date='2026-10-21',
         doubts=DOUBTS,issue_overrides=OVERRIDES,new_sections=NEW_SECTIONS,
         coverage_updates={'preface':['preface']},row_notes=ROW_NOTES,
         coverage_notes={'preface':'正文从节首连续14个句群至节尾；注释/删文范围及14项首尾衔接待集中审计，全文分母未建立'})
