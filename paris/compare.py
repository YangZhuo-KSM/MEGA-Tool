"""Literal same-language differences. No judgment of translation quality."""
import difflib
import html
import re


def tokens(text,language):
    return list(text) if language=='zh' else re.findall(r'\w+|\s+|[^\w\s]',text,flags=re.UNICODE)


def compare_texts(left,right,language):
    a,b=tokens(left,language),tokens(right,language)
    return [dict(kind=tag,left=''.join(a[i:j]),right=''.join(b[k:l]))
            for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes()]


def diff_html(changes,side):
    parts=[]
    for change in changes:
        value=html.escape(change[side])
        tag=change['kind']
        if tag!='equal' and value:
            element='del' if side=='left' else 'ins'
            value=f'<{element}>{value}</{element}>'
        parts.append(value)
    return ''.join(parts)
