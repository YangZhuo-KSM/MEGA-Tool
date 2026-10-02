"""Validate relationships; optionally verify local source hashes and page counts."""
import argparse
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus
from paris.pages import resolve_source


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources',action='store_true')
    args=parser.parse_args()
    data=load_corpus()
    if args.sources:
        from pypdf import PdfReader
        for source in data['sources']:
            path=resolve_source(source)
            count=len(PdfReader(path).pages)
            if count!=source['pdf_page_count']:
                raise ValueError(f'{source["id"]}: actual page count {count}')
            print(f'{source["id"]}: SHA256 and {count} pages verified')
    print(f'Valid: {len(data["units"])} units, {len(data["alignments"])} alignments, {len(data["comparisons"])} comparisons, {len(data["page_map"])} page mappings')


if __name__=='__main__':
    main()
