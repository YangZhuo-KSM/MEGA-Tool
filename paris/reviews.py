"""Researcher reviews are separate, atomic records bound to exact content."""
import hashlib
import json
import os
import tempfile
from datetime import datetime,timezone,timedelta
from pathlib import Path

from .corpus import ROOT,index


def fingerprint(data,alignment,*,version=2):
    units=index(data['units'])
    selected=[units[i] for i in alignment['de_ids']+alignment['zh_ids']]
    edition_ids={u['edition_id'] for u in selected}
    payload=dict(de_ids=alignment['de_ids'],zh_ids=alignment['zh_ids'],
        units=[{k:u[k] for k in ('id','text','locations','edition_id')} for u in selected],
        editions=[e for e in data['editions'] if e['id'] in edition_ids],
        sources=[s for s in data['sources'] if s['id'] in {e['source_id'] for e in data['editions'] if e['id'] in edition_ids}])
    if version==1:
        payload.pop('sources')
    elif version!=2:
        raise ValueError('Unknown fingerprint version')
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def upgrade_legacy_record(data,alignment,record,baseline):
    """Migrate only with a preserved pre-review corpus and matching exact content."""
    if record.get('fingerprint')==fingerprint(data,alignment):
        return record
    old_alignment=index(baseline['alignments']).get(alignment['id'])
    if (not old_alignment or record.get('fingerprint_version',1)!=1
        or record.get('fingerprint')!=fingerprint(data,alignment,version=1)
        or fingerprint(baseline,old_alignment)!=fingerprint(data,alignment)):
        raise ValueError(f'{alignment["id"]}: 内容或来源与旧快照不一致，不能迁移确认')
    result=dict(record)
    result['history']=record.get('history',[])+[{k:v for k,v in record.items() if k!='history'}]
    result['fingerprint']=fingerprint(data,alignment)
    result['fingerprint_version']=2
    result['migration']={'at':datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),
        'reason':'旧服务使用不含sources的指纹；与核验前快照核对正文、页码、版本和来源全部一致。'}
    return result


def load_reviews(path=None):
    path=Path(path) if path else ROOT/'data'/'reviews.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def review_state(data,alignment,reviews):
    record=reviews.get(alignment['id'])
    if record:
        if record.get('fingerprint')!=fingerprint(data,alignment):
            return 'stale',record
        return record['status'],record
    return alignment['status'],None


def save_review(data,alignment,reviewer,note,status='manually_verified',path=None):
    if not reviewer.strip():
        raise ValueError('请填写核验人')
    if status not in ('manually_verified','uncertain'):
        raise ValueError('无效核验状态')
    if status=='manually_verified' and not alignment['zh_ids']:
        raise ValueError('缺少中文，无法确认对应关系')
    path=Path(path) if path else ROOT/'data'/'reviews.json'
    reviews=load_reviews(path)
    old=reviews.get(alignment['id'])
    record=dict(status=status,reviewer=reviewer.strip(),note=note.strip(),
        reviewed_at=datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),
        fingerprint=fingerprint(data,alignment),fingerprint_version=2,history=(old.get('history',[])+[{k:v for k,v in old.items() if k!='history'}]) if old else [])
    reviews[alignment['id']]=record
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,temp=tempfile.mkstemp(dir=path.parent,suffix='.tmp')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as handle:
            json.dump(reviews,handle,ensure_ascii=False,indent=2)
            handle.write('\n')
        os.replace(temp,path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    return record
