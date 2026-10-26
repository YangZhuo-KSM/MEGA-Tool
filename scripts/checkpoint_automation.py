"""Refresh the same factual checkpoint in four recovery documents; retain their bodies."""
import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
BEGIN = '<!-- automation-checkpoint:start -->'
END = '<!-- automation-checkpoint:end -->'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True)
    parser.add_argument('--next', dest='next_step', required=True)
    parser.add_argument('--quota', required=True, help='Observed five-hour/weekly usedPercent, or unavailable')
    args = parser.parse_args()
    data = json.loads((ROOT / 'data/corpus.json').read_text(encoding='utf-8'))
    plan = json.loads((ROOT / 'data/sampling_plan.json').read_text(encoding='utf-8'))
    stamp = datetime.now(ZoneInfo('Asia/Hong_Kong')).isoformat(timespec='seconds')
    last = max(a['review_batch'] for a in data['alignments'])
    summary = (f'{stamp}（Asia/Hong_Kong）追加轮检查点：{args.phase}。\n\n'
               f'实际数据{data["release"]}：{len(data["alignments"])}组、{len(data["units"])}单元、'
               f'{len(data["page_map"])}映射、{len(data["sections"])}专题；'
               f'已执行批次至{last}，禁止重跑。最近实读额度（5小时/周已用）{args.quota}。\n\n'
               f'当前抽样文件{len(plan["recommended"])}/{len(plan["scope_ids"])}；'
               '是否已延续及审计以本检查点阶段为准。\n\n'
               f'下一项：{args.next_step}。本轮最多3批，额度门槛保持；'
               '下方为此前保存的基线和记录。')
    block = BEGIN + '\n' + summary + '\n' + END
    for name in ('Scope.md', 'To_do.md', 'Status.md', 'project_handoff.md'):
        path = ROOT / name
        original = path.read_text(encoding='utf-8')
        if BEGIN in original:
            start, stop = original.index(BEGIN), original.index(END) + len(END)
            updated = original[:start] + block + original[stop:]
        else:
            title, rest = original.split('\n', 1)
            updated = title + '\n\n' + block + '\n' + rest
        temp = path.with_suffix('.checkpoint.tmp')
        temp.write_text(updated, encoding='utf-8')
        temp.replace(path)
        assert block in path.read_text(encoding='utf-8')
    print(stamp, data['release'], 'four checkpoints saved', args.phase)


if __name__ == '__main__':
    main()
