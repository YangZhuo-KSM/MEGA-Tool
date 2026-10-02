"""Auditable term counts within the selected, explicitly partial corpus."""
from collections import Counter
from .search import search_units
from .reviews import review_state
from .citations import reference


def term_distribution(units,query,case_sensitive=False,whole_word=False):
    hits=search_units(units,query,case_sensitive,whole_word)
    counts=Counter()
    for h in hits:
        counts[h['unit']['section_id']]+=h['count']
    return dict(counts),hits


def research_distribution(data,reviews,queries,language='de',edition_ids=None,section_ids=None,
                          primary_only=True,confirmed_only=False,case_sensitive=False,whole_word=False):
    """Count distinct units in an explicit scope; export every hit with its citation."""
    queries=list(dict.fromkeys(q.strip() for q in queries if q.strip()))
    states={a['id']:review_state(data,a,reviews)[0] for a in data['alignments']}
    relations={u['id']:[a['id'] for a in data['alignments'] if u['id'] in a['de_ids']+a['zh_ids']] for u in data['units']}
    selected=[u for u in data['units'] if u['language']==language
        and (edition_ids is None or u['edition_id'] in edition_ids)
        and (section_ids is None or u['section_id'] in section_ids)
        and (not primary_only or u.get('role','primary')=='primary')
        and (not confirmed_only or any(states[aid]=='manually_verified' for aid in relations[u['id']]))]
    summary=[]; rows=[]
    # Report zero counts for in-scope sections as well, so absence is auditable.
    for query in queries:
        counts,hits=term_distribution(selected,query,case_sensitive,whole_word and language=='de')
        for section in data['sections']:
            if section_ids is not None and section['id'] not in section_ids: continue
            scoped=[u for u in selected if u['section_id']==section['id']]
            summary.append(dict(query=query,section_id=section['id'],section=section['title'],
                                count=counts.get(section['id'],0),units=len(scoped)))
        for hit in hits:
            u=hit['unit']; ref=reference(data,u)
            rows.append(dict(query=query,unit_id=u['id'],section_id=u['section_id'],edition_id=u['edition_id'],
                count=hit['count'],spans=hit['spans'],citation=ref['plain'],source=ref['short'],
                citation_notes=ref['notes'],text=u['text'],alignment_ids=relations[u['id']],
                review_states=[states[aid] for aid in relations[u['id']]],proofread_status=u.get('proofread_status')))
    return dict(scope=dict(language=language,edition_ids=edition_ids,section_ids=section_ids,
        primary_only=primary_only,confirmed_only=confirmed_only,case_sensitive=case_sensitive,whole_word=whole_word,
        units=len(selected),queries=queries,note='仅当前筛选的已收录文本；不同查询独立计数，不可相加当作唯一词数。'),summary=summary,hits=rows)
