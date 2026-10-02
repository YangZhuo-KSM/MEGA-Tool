"""Exact page mappings and local, hash-checked source previews."""
import hashlib
import io
import json
import threading
from functools import lru_cache
from pathlib import Path

from .corpus import ROOT

PDF_LOCK=threading.Lock()  # PDFium is not thread-safe across Streamlit sessions.


def lookup_pages(data, source_id, value, kind='printed_page'):
    if kind not in ('printed_page','pdf_page'):
        raise ValueError('Unknown page kind')
    value=str(value).strip()
    if kind=='pdf_page':
        if not value.isascii() or not value.isdecimal(): return []
        value=str(int(value))
    return [p for p in data['page_map'] if p['source_id']==source_id and p.get(kind) is not None and str(p[kind])==value]


def missing_pages(data,source_id,printed_page):
    return [p for p in data.get('missing_pages',[]) if p['source_id']==source_id and p['printed_page']==str(printed_page).strip()]


def page_label(page):
    return page.get('printed_page') or '无印刷页码'


def alignments_on_page(data,source_id,pdf_page):
    ids={u['id'] for u in units_on_page(data,source_id,pdf_page)}
    return [a for a in data['alignments'] if ids.intersection(a['de_ids']+a['zh_ids'])]


def units_on_page(data, source_id, pdf_page):
    return [u for u in data['units'] if any(p['source_id']==source_id and p['pdf_page']==pdf_page for p in u['locations'])]


@lru_cache(maxsize=16)
def file_hash(path, size, mtime_ns):
    with open(path,'rb') as handle:
        return hashlib.file_digest(handle,'sha256').hexdigest()


def resolve_source(source, root=ROOT):
    root=Path(root)
    config_path=root/'local_sources.json'
    overrides=json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
    path=Path(overrides[source['id']]) if source['id'] in overrides else root/'Asset_by_user'/source['file_name']
    if not path.is_absolute():
        path=root/path
    if not path.is_file():
        raise FileNotFoundError('尚未配置本地PDF；正文和页码仍可阅读。配置方法见README。')
    stat=path.stat()
    if file_hash(str(path),stat.st_size,stat.st_mtime_ns)!=source['sha256']:
        raise ValueError('PDF与页码索引所用文件不同；请核对版本并重新建立映射。')
    return path


def render_page(source, pdf_page):
    if not 1<=pdf_page<=source['pdf_page_count']:
        raise ValueError('PDF页序超出范围')
    path=resolve_source(source)
    import pypdfium2
    with PDF_LOCK:
        doc=pypdfium2.PdfDocument(str(path))
        try:
            if len(doc)!=source['pdf_page_count']:
                raise ValueError('实际PDF总页数与索引不一致')
            page=doc[pdf_page-1]
            bitmap=page.render(scale=1.7)
            try:
                image=bitmap.to_pil()
                out=io.BytesIO()
                image.save(out,format='PNG')
                return out.getvalue()
            finally:
                bitmap.close()
                page.close()
        finally:
            doc.close()
