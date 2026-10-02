"""Extract selected source pages for review. Page numbers are one-based.

Example: python scripts/inspect_sources.py de_megai2 363 369 --render
Original PDFs are never modified. Evidence is written under tmp/source_review.
"""
import argparse
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    'de_megai2': 'MEGA² I.2. Karl Marx. Artikel, Entwürfe. März 1843 bis August 1844.pdf',
    'de_megaiv2': 'MEGA² IV.2 - Karl Marx - Friedrich Engels - Exzerpte und Notizen. 1843 bis Januar 1845.pdf',
    'zh_collected': '《马克思恩格斯全集》第３卷，北京：人民出版社，2002年版.pdf',
    'zh_single': '【含穆勒评注】1844 Manuscript.pdf',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', choices=FILES)
    parser.add_argument('start', type=int)
    parser.add_argument('end', type=int)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'Asset_by_user' / FILES[args.source]
    reader = PdfReader(path)
    if not 1 <= args.start <= args.end <= len(reader.pages):
        parser.error('Invalid one-based PDF page range')
    out = ROOT / 'tmp' / 'source_review' / args.source
    out.mkdir(parents=True, exist_ok=True)
    renderer = None
    if args.render:
        import pypdfium2
        renderer = pypdfium2.PdfDocument(str(path))
    for number in range(args.start, args.end + 1):
        text = reader.pages[number - 1].extract_text() or ''
        (out / f'{number:04}.txt').write_text(text, encoding='utf-8')
        if renderer is not None:
            page = renderer[number - 1]
            bitmap = page.render(scale=2.0)
            bitmap.to_pil().save(out / f'{number:04}.png')
            bitmap.close()
            page.close()
        print(f'{args.source} PDF {number}: {len(text)} characters')
    if renderer is not None:
        renderer.close()


if __name__ == '__main__':
    main()
