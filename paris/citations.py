"""User-specified citation styles, separate from verified edition metadata.

No template changes source years or their verification status. Binding is by
source id, checked against the text's edition; never guessed from a page number.
"""
from .corpus import index

MEGA_TITLE='Marx－Engels－Gesamtausgabe (MEGA²)'
BIBLIOGRAPHY={
    'de_megai2': dict(short_title='MEGA² I/2', volume='Ⅰ/2', place='Berlin',
        publisher='Dietz Verlag', year=1982, language='de',
        template=f'Marx: *{MEGA_TITLE}*, Ⅰ/2, Berlin: Dietz Verlag, 1982. S.{{page}}.'),
    'de_megaiv2': dict(short_title='MEGA² IV/2', volume='Ⅳ/2', place='Berlin',
        publisher='Dietz Verlag', year=1982, language='de',
        template=f'Marx: *{MEGA_TITLE}*, Ⅳ/2, Berlin: Dietz Verlag, 1982. S.{{page}}.'),
    'zh_single': dict(short_title='《1844年经济学哲学手稿》', volume='', place='北京',
        publisher='人民出版社', year=2000, language='zh',
        template='马克思：《1844年经济学哲学手稿》，北京：人民出版社2000年版，第{page}页。'),
    'zh_collected': dict(short_title='《马克思恩格斯全集》第3卷', volume='3', place='北京',
        publisher='人民出版社', year=2002, language='zh',
        template='《马克思恩格斯全集》第3卷，北京：人民出版社2002年，第{page}页。'),
}


def format_pages(labels, language='de'):
    """Only adjacent canonical decimal labels form ranges; preserve other labels."""
    labels=list(dict.fromkeys(str(p) for p in labels if p is not None))
    result=[]
    def numeric(s):
        return s.isascii() and s.isdecimal() and str(int(s))==s
    i=0
    while i < len(labels):
        end=i
        while (end+1 < len(labels) and numeric(labels[end]) and numeric(labels[end+1])
               and int(labels[end+1])==int(labels[end])+1):
            end+=1
        result.append(labels[i] if end==i else labels[i]+('–' if language=='de' else '—')+labels[end])
        i=end+1
    return (', ' if language=='de' else '、').join(result)


def mapped_locations(data, unit):
    """Resolve each exact stored location through the existing per-page map.

    Using both labels and PDF addresses disambiguates repeated printed labels.
    Unmapped locations are not inferred; callers expose the missing information.
    """
    edition=index(data['editions'])[unit['edition_id']]
    records={(p['source_id'],p['pdf_page'],p.get('printed_page')):p for p in data['page_map']}
    result=[]
    for loc in unit.get('locations',[]):
        if loc['source_id']!=edition['source_id']:
            raise ValueError('文本来源与版本不一致')
        record=records.get((loc['source_id'],loc['pdf_page'],loc.get('printed_page')))
        if record is not None and record not in result:
            result.append(record)
    return result


def reference(data, unit):
    edition=index(data['editions'])[unit['edition_id']]
    config=BIBLIOGRAPHY.get(edition['source_id'])
    locations=mapped_locations(data,unit)
    complete=len(locations)==len({(p['source_id'],p['pdf_page'],p.get('printed_page'))
                                 for p in unit.get('locations',[])}) and bool(locations)
    pages=format_pages([p.get('printed_page') for p in locations],edition['language'])
    named=bool(pages) and all(p.get('printed_page') is not None for p in locations)
    short_title=config['short_title'] if config else edition['short_title']
    short=short_title+' · '+(('S. '+pages if edition['language']=='de' else '第'+pages+'页')
                             if pages else '来源页待定位')
    if not complete: short+=' · 定位未完整'
    citation=config['template'].format(page=pages) if config and complete and named else ''
    notes=[]
    if config and str(config['year'])!=str(edition['year']):
        notes.append(f'按用户指定模板引用年份 {config["year"]}；本地底本元数据年份为 {edition["year"]}，两者有差异，尚待研究者决定。')
    if edition['source_id']=='zh_single':
        notes.append('引用采用用户指定的2000年版格式；原书版权页书目信息尚未独立核验。')
    if not citation:
        notes.append('来源页或引用模板不完整，暂不生成可复制引用。')
    return dict(short=short, markdown=citation, plain=citation.replace('*'+MEGA_TITLE+'*',MEGA_TITLE),
                locations=locations, notes=notes, edition=edition)


def reading_page_sources(data, units):
    """Summaries by edition; deduplicate labels but retain exact page mapping below."""
    by_edition={}
    for unit in units:
        by_edition.setdefault(unit['edition_id'],[]).extend(unit.get('locations',[]))
    result=[]
    for eid,locations in by_edition.items():
        unique=list({(p['source_id'],p['pdf_page']):p for p in locations}.values())
        result.append(reference(data,dict(edition_id=eid,locations=unique))['short'])
    return result
