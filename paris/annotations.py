"""Source-faithful editorial marks, independent from text and search offsets."""
import html

VISIBLE_STATES={'open','retained_as_source'}


def unit_issues(data,unit_id):
    return [i for i in data.get('editorial_issues',[])
            if i['unit_id']==unit_id and i['status'] in VISIBLE_STATES]


def annotated_html(text,search_spans,issues):
    # Interval boundaries allow search and editorial marks to overlap safely.
    marks=[]
    for issue in issues:
        loc=issue.get('text_anchor')
        if loc and text[loc['start']:loc['end']]==loc['quote']:
            marks.append((loc['start'],loc['end'],issue['note']))
    bounds=sorted({0,len(text)}|{x for s,e in search_spans for x in (s,e)}
                  |{x for s,e,_ in marks for x in (s,e)})
    parts=[]
    for start,end in zip(bounds,bounds[1:]):
        chunk=html.escape(text[start:end])
        if any(s<=start and end<=e for s,e in search_spans):
            chunk=f'<mark>{chunk}</mark>'
        notes=[note for s,e,note in marks if s<=start and end<=e]
        if notes:
            title=html.escape('；'.join(notes),quote=True)
            chunk=f'<span class="editorial-mark" title="{title}">{chunk}</span>'
        parts.append(chunk)
    return ''.join(parts)
