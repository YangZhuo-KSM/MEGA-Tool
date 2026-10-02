"""Ephemeral reading pages. Corpus groups and source pages are never rewritten."""
import math
import unicodedata

from .corpus import index


def visual_lines(text, width=62):
    """Estimate a desktop column in half-width character cells, including paragraphs.

    Wide CJK characters occupy two cells. A 12% wrap allowance accommodates
    German word boundaries and proportional fonts. This is not browser geometry.
    """
    return sum(max(1, math.ceil(sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1
                                   for c in line) * 1.12 / width))
               for line in text.split('\n'))


def group_height(group, units, width=62):
    sides=[sum(visual_lines(units[uid]['text'], width) + 2 for uid in group[field])
           for field in ('de_ids', 'zh_ids')]
    return max(sides) + 3  # group label and low-interference source controls


def reading_pages(data, section_id, budget=44, width=62):
    """Greedy, whole-group pagination in source sequence; oversized groups stand alone.

    The budget is estimated line rows, not a fixed number of paragraphs. Page
    numbers are scoped to a topic. Filtering and search never renumber pages.
    """
    if budget <= 0 or width <= 0:
        raise ValueError('Reading dimensions must be positive')
    units=index(data['units'])
    groups=sorted((a for a in data['alignments'] if a['section_id']==section_id),
                  key=lambda a:min(units[uid]['sequence'] for uid in a['de_ids']))
    pages=[]
    for group in groups:
        cost=group_height(group, units, width)
        if not pages or pages[-1]['estimated_lines'] + cost > budget:
            pages.append(dict(id=f'reading-{group["id"]}', number=len(pages)+1,
                              section_id=section_id, alignment_ids=[], estimated_lines=0))
        pages[-1]['alignment_ids'].append(group['id'])
        pages[-1]['estimated_lines']+=cost
    return pages


def page_for_alignment(data, alignment_id, **settings):
    group=index(data['alignments'])[alignment_id]
    return next(p for p in reading_pages(data, group['section_id'], **settings)
                if alignment_id in p['alignment_ids'])


def reading_targets(data, unit_id):
    """Return all direct groups, or explicit comparison bridges (never auto-align)."""
    direct=[dict(alignment_id=a['id'], via_comparison=None)
            for a in data['alignments'] if unit_id in a['de_ids']+a['zh_ids']]
    if direct:
        return direct
    targets=[]
    seen=set()
    for c in data['comparisons']:
        if unit_id not in c['left_ids']+c['right_ids']:
            continue
        partners=c['right_ids'] if unit_id in c['left_ids'] else c['left_ids']
        for a in data['alignments']:
            if set(partners).intersection(a['de_ids']+a['zh_ids']) and a['id'] not in seen:
                targets.append(dict(alignment_id=a['id'], via_comparison=c['id']))
                seen.add(a['id'])
    return targets


def page_units(data, page, language):
    units=index(data['units'])
    groups=index(data['alignments'])
    ids=dict.fromkeys(uid for aid in page['alignment_ids']
                      for uid in groups[aid][f'{language}_ids'])
    return [units[uid] for uid in ids]
