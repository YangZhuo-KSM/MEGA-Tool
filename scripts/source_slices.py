"""Reproducible, scan-reviewed slices of the project's local extraction evidence.

Recipes retain page ranges, literal boundary anchors and explicit scan corrections.
No model-generated replacement paragraphs or book-wide page offsets are used.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def stream(source, pages, corrections=None, join_page_hyphens=False):
    evidence = json.loads((ROOT / 'data/extraction.json').read_text(encoding='utf-8'))
    text, positions, hashes = '', [], {}
    for number, first, last in pages:
        key = f'{source}:{number}'
        cache = ROOT / f'tmp/source_review/{source}/{number:04}.txt'
        raw = evidence.get(key)
        if raw is None:
            raw = cache.read_text(encoding='utf-8')
        elif cache.exists() and cache.read_text(encoding='utf-8') != raw:
            raise ValueError(f'Cached extraction differs from saved evidence: {key}')
        hashes[key] = hashlib.sha256(raw.encode('utf-8')).hexdigest()
        body = '\n'.join(raw.splitlines()[first - 1:last])
        if source.startswith('de_'):
            body = '\n'.join(re.sub(r'(^\s*\d{1,2}\s+|\s+\d{1,2}\s*$)', '', line)
                             for line in body.splitlines())
            body = re.sub(r'[-\u00ad]\s*\n\s*', '', body)
            body = ' '.join(body.split())
        else:
            body = re.sub(r'\s+', '', body)
        for old, new in (corrections or {}).get(number, []):
            if old not in body:
                raise ValueError(f'Scan correction not found on {key}: {old!r}')
            body = body.replace(old, new)
        if join_page_hyphens and source.startswith('de_') and text.endswith('-'):
            text = text[:-1]
            positions.pop()
            separator = ''
        else:
            separator = ' ' if source.startswith('de_') and text else ''
        text += separator
        positions.extend([number] * len(separator))
        text += body
        positions.extend([number] * len(body))
    return text, positions, hashes


def groups(source_stream, starts, end=None):
    text, positions, _ = source_stream
    offsets, cursor = [], 0
    for start in starts:
        at = text.find(start, cursor)
        if at < 0:
            raise ValueError(f'Slice boundary not found after {cursor}: {start!r}')
        offsets.append(at)
        cursor = at + len(start)
    stop = text.index(end, cursor) if end else len(text)
    result = []
    for left, right in zip(offsets, offsets[1:] + [stop]):
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        value = text[left:right]
        if not value:
            raise ValueError('Empty source slice')
        result.append((value, list(dict.fromkeys(positions[left:right]))))
    return result


def rows(section, first, labels, de_stream, zh_stream, de_starts, zh_starts,
         de_end=None, zh_end=None):
    de = groups(de_stream, de_starts, de_end)
    zh = groups(zh_stream, zh_starts, zh_end)
    if not len(labels) == len(de) == len(zh):
        raise ValueError('Different number of labels and source boundaries')
    return [(section, first + i, label, d[0], z[0], d[1], z[1])
            for i, (label, d, z) in enumerate(zip(labels, de, zh))]
