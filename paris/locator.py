"""Text -> printed source location -> optional reading destination, without writes."""
from .search import search_units, highlighted_html
from .citations import reference
from .reading import reading_targets, page_for_alignment


def locate(data, query, source_id=None, case_sensitive=False, whole_word=False):
    editions={e['id']:e for e in data['editions']}
    candidates=[u for u in data['units'] if source_id is None
                or editions[u['edition_id']]['source_id']==source_id]
    results=[]
    hits=[]
    for unit in candidates:
        hits.extend(search_units([unit],query,case_sensitive,whole_word and unit['language']=='de'))
    for hit in hits:
        unit=hit['unit']
        targets=reading_targets(data,unit['id'])
        for target in targets:
            target['page']=page_for_alignment(data,target['alignment_id'])
        results.append(dict(**hit, reference=reference(data,unit), targets=targets))
    return results


def snippets(text, spans, margin=70):
    """All occurrence contexts, with overlapping windows merged and offsets intact."""
    windows=[]
    for start,end in spans:
        left,right=max(0,start-margin),min(len(text),end+margin)
        if windows and left <= windows[-1][1]:
            windows[-1]=(windows[-1][0],max(right,windows[-1][1]))
        else:
            windows.append((left,right))
    return [('…' if left else '')+highlighted_html(text[left:right],
             [(max(left,a)-left,min(right,b)-left) for a,b in spans if a<right and b>left])
             +('…' if right<len(text) else '') for left,right in windows]
