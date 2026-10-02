"""Export readable review batches without altering confirmation state."""
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus,index,aligned_units
from paris.reviews import load_reviews,review_state
from paris.annotations import unit_issues


def main():
    data=load_corpus()
    editions=index(data['editions'])
    reviews=load_reviews()
    out=ROOT/'docs'/'reviews'
    out.mkdir(parents=True,exist_ok=True)
    for batch in sorted({a['review_batch'] for a in data['alignments']}):
        parts=[f'# 第{batch}批德中对应核对\n',
            '每组检查：文字是否忠实于指定扫描页、对应范围是否完整、版本与页码是否准确。导航标题由项目添加。\n',
            '当前文字经AI扫描校订；每组状态见下方。可在应用“审核与资料”逐组保存，或向Codex明确反馈组ID及结论。\n']
        for a in [a for a in data['alignments'] if a['review_batch']==batch]:
            parts.append(f'## {a["id"]} · {a["label"]}\n')
            parts.append(f'状态：{review_state(data,a,reviews)[0]}\n')
            de,zh=aligned_units(data,a)
            for group in [de,zh]:
                for u in group:
                    e=editions[u['edition_id']]
                    refs='；'.join(f'印刷{p["printed_page"]} / PDF第{p["pdf_page"]}页' for p in u['locations'])
                    parts.extend([f'**{e["short_title"]}（{e["year"]}） · {u["id"]}**\n',refs+'\n',u['text']+'\n'])
                    for issue in unit_issues(data,u['id']):
                        label='语义存疑 · 按底本照录' if issue['kind']=='semantic_doubt' else '转录疑点'
                        parts.append(f'> {label}：{issue["current_reading"]}。{issue["note"]}\n')
            checked='x' if review_state(data,a,reviews)[0]=='manually_verified' else ' '
            parts.append(f'- [{checked}] 已核对对应关系与来源\n\n核验人／日期／修改意见以本地审核记录为准。\n')
        (out/f'batch-{batch:02}.md').write_text('\n'.join(parts),encoding='utf-8')
    print(f'Exported {len({a["review_batch"] for a in data["alignments"]})} review batches; no confirmation state changed.')


if __name__=='__main__':
    main()
