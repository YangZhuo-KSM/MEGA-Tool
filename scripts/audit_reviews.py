"""Summarize effective review states without changing user decisions."""
import sys
from collections import Counter
from datetime import datetime,timezone,timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus
from paris.reviews import load_reviews,review_state


def main():
    data=load_corpus()
    reviews=load_reviews()
    counts=Counter(review_state(data,a,reviews)[0] for a in data['alignments'])
    lines=['# 用户核验验收记录','',datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'),'',
        f'当前有效人工确认：{counts["manually_verified"]}/{len(data["alignments"])}；过期：{counts["stale"]}。',
        '','状态通过当前正文、页码、版本和来源的指纹计算；原始姓名/自由备注保留在本地data/reviews.json。','',
        '| 批次 | 组ID | 当前状态 |','| --- | --- | --- |']
    lines += [f'| {a["review_batch"]} | {a["id"]} | {review_state(data,a,reviews)[0]} |' for a in data['alignments']]
    lines += ['','## 转录待解决事项','']
    issues=[i for i in data.get('editorial_issues',[]) if i['status']=='open']
    lines += [f'- {i["unit_id"]}：{i["note"]}（{", ".join(i["evidence_pages"])}）' for i in issues] or ['无已登记的开放疑点。']
    retained=[i for i in data.get('editorial_issues',[]) if i['status']=='retained_as_source']
    lines += ['','## 语义存疑，按底本照录','']
    lines += [f'- {i["unit_id"]}：{i["current_reading"]}。{i["note"]}' for i in retained] or ['无已登记项。']
    lines += ['','对应关系已确认与文字疑点未解决可以同时存在。照录标注会持续显示，不因对应确认而消失；正式v0.1须补齐待审记录并处理开放疑点。']
    (ROOT/'docs/REVIEW_ACCEPTANCE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(dict(counts),f'open_issues={len(issues)}')


if __name__=='__main__': main()
