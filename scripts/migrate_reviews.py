"""Repair legacy fingerprints with a preserved release as evidence. Stop the app before --apply."""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime,timezone,timedelta
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus,index
from paris.reviews import load_reviews,upgrade_legacy_record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    with ZipFile(args.baseline) as archive:
        names=[n for n in archive.namelist() if n.endswith('/data/corpus.json')]
        if len(names)!=1: raise ValueError('Expected one baseline corpus')
        baseline=json.loads(archive.read(names[0]))
    data=load_corpus()
    path=ROOT/'data/reviews.json'
    original=path.read_bytes()
    reviews=json.loads(original)
    alignments=index(data['alignments'])
    updated={aid:upgrade_legacy_record(data,alignments[aid],r,baseline) for aid,r in reviews.items()}
    changed=sum(updated[aid]!=r for aid,r in reviews.items())
    if args.apply and changed:
        stamp=datetime.now(timezone(timedelta(hours=8))).strftime('%Y%m%d-%H%M%S')
        backup=ROOT/'local_backups'/f'reviews-{stamp}.json'
        backup.parent.mkdir(exist_ok=True)
        with backup.open('xb') as handle: handle.write(original)
        assert hashlib.sha256(backup.read_bytes()).digest()==hashlib.sha256(original).digest()
        temp=path.with_suffix('.migration.tmp')
        temp.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if path.read_bytes()!=original: raise RuntimeError('Review file changed during migration; not replaced')
        os.replace(temp,path)
    print(f'{"Migrated" if args.apply else "Eligible"}: {changed}; preserved reviewer, note, timestamp and history.')


if __name__=='__main__': main()
