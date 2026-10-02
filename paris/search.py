"""Literal Unicode search, preserving character positions in the source text."""
import html
import unicodedata


def normalize(text, case_sensitive=False):
    """Return normalized text and (start, end) source spans for each character.

    A combining mark belongs to the preceding base character. One original ß
    becomes two search characters ('ss'), both pointing back to the same span.
    Runs of whitespace become one space. Original text is never modified.
    """
    result, mapping = [], []
    i = 0
    while i < len(text):
        end = i + 1
        if text[i].isspace():
            while end < len(text) and text[end].isspace():
                end += 1
            chunk = ' '
        else:
            while end < len(text) and unicodedata.combining(text[end]):
                end += 1
            chunk = unicodedata.normalize('NFC', text[i:end])
            if not case_sensitive:
                chunk = chunk.casefold()
        result.extend(chunk)
        mapping.extend([(i, end)] * len(chunk))
        i = end
    return ''.join(result), mapping


def find_spans(text, query, case_sensitive=False, whole_word=False):
    haystack, mapping = normalize(text, case_sensitive)
    needle = normalize(query.strip(), case_sensitive)[0]
    if not needle:
        return []
    spans, start = [], 0
    while (pos := haystack.find(needle, start)) >= 0:
        end = pos + len(needle)
        before = pos > 0 and (haystack[pos-1].isalnum() or haystack[pos-1]=='_')
        after = end < len(haystack) and (haystack[end].isalnum() or haystack[end]=='_')
        if not whole_word or not (before or after):
            span = (mapping[pos][0], mapping[end-1][1])
            if span not in spans:
                spans.append(span)
        start = end  # Non-overlapping occurrences, shared by search and statistics.
    return spans


def highlighted_html(text, spans):
    """Escape source HTML before inserting highlights; merge overlapping spans."""
    merged = []
    for start, end in sorted(spans):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start,end))
    parts, pos = [], 0
    for start,end in merged:
        parts.extend([html.escape(text[pos:start]), '<mark>',html.escape(text[start:end]),'</mark>'])
        pos=end
    parts.append(html.escape(text[pos:]))
    return ''.join(parts)


def search_units(units, query, case_sensitive=False, whole_word=False):
    hits=[]
    for unit in units:
        spans=find_spans(unit['text'],query,case_sensitive,whole_word)
        if spans:
            hits.append(dict(unit=unit,spans=spans,count=len(spans)))
    return hits
