"""Build portable source archives using an explicit allowlist; never ship local PDFs/reviews."""
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus,validate
from paris import __version__


def build(stage):
    data=copy.deepcopy(load_corpus())
    if stage=='stage0':
        selected=[]
        data['sections']=[s for s in data['sections'] if s['id'] in ('alienation','mill')]
        for section in data['sections']:
            selected += [a for a in data['alignments'] if a['section_id']==section['id']][:3]
        data['alignments']=selected
        ids={uid for a in selected for uid in a['de_ids']+a['zh_ids']}
        data['units']=[u for u in data['units'] if u['id'] in ids]
        data['editorial_issues']=[i for i in data.get('editorial_issues',[]) if i['unit_id'] in ids]
        data['comparisons']=[]
        pages={(p['source_id'],p['pdf_page']) for u in data['units'] for p in u['locations']}
        data['page_map']=[p for p in data['page_map'] if (p['source_id'],p['pdf_page']) in pages]
        for section in data['sections']:
            section['coverage']='阶段0检查点：精选3组，非全文'
        for item in data['coverage']:
            if item['id'] in ('manuscript1','mill'):
                item['detail']='阶段0检查点：精选3组'
        data['release']=f'{__version__}-stage0-checkpoint'
    errors=validate(data)
    if errors:
        raise ValueError('\n'.join(errors))
    name=f'paris-manuscripts-{data["release"] if stage=="stage0" else __version__}'
    output=ROOT/'dist'/f'{name}.zip'
    output.parent.mkdir(exist_ok=True)
    files=[ROOT/p for p in ('app.py','start.ps1','requirements.txt','requirements-dev.txt',
        'local_sources.example.json','README.md','LICENSE','.gitignore','.streamlit/config.toml','pytest.ini','data/coverage_plan.json')]
    if stage!='stage0' and (ROOT/'data/sampling_plan.json').exists():
        files.append(ROOT/'data/sampling_plan.json')
    for folder in ('paris','scripts','docs','tests'):
        files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts
                     and p.suffix in ('.py','.md','.jpg','.png')
                     and 'reviews' not in p.relative_to(ROOT).parts
                     and p.name not in ('REVIEW_ACCEPTANCE.md','original-pages.jpg','windows-exe-original.png','USER_CONTRIBUTIONS_README_HANDOFF.md')
                     and not p.name.endswith('.local.md'))
    if stage=='stage0':
        files=[p for p in files if 'tests' not in p.relative_to(ROOT).parts and 'reviews' not in p.relative_to(ROOT).parts]
    with ZipFile(output,'w',ZIP_DEFLATED) as z:
        for p in sorted(set(files)):
            if stage=='stage0' and p==ROOT/'data/coverage_plan.json':
                plan=json.loads(p.read_text(encoding='utf-8'))
                available={s['id'] for s in data['sections']}
                for item in plan['items']:
                    item['section_ids']=[sid for sid in item['section_ids'] if sid in available]
                z.writestr(f'{name}/data/coverage_plan.json',json.dumps(plan,ensure_ascii=False,indent=2))
                continue
            z.write(p,f'{name}/{p.relative_to(ROOT).as_posix()}')
        z.writestr(f'{name}/data/corpus.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        if stage!='stage0':
            z.write(ROOT/'data/extraction.json',f'{name}/data/extraction.json')
        z.writestr(f'{name}/CHECKPOINT.md',
            '# 包内数据范围\n\n'+('本包是在当前实现上组装的阶段0六组数据检查点，每专题3组；不是历史旧代码版本。'
             ' README与状态文件介绍主工作区预览；本包以此说明及corpus.json为准。'
             '不附全量专用测试与审核包；使用scripts/smoke_release.py验收。\n' if stage=='stage0' else
             f'本包包含{len(data["alignments"])}组对照。用户审核记录仅保留在本地，不进入源码包；解压后的确认数量因此可能与原工作区不同。没有完整PDF、个人路径配置或虚拟环境。\n'))
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix('.zip.sha256').write_text(f'{digest}  {output.name}\n',encoding='ascii')
    print(f'{output.name}: {len(data["alignments"])} alignments, sha256={digest}')
    return output


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=['stage0','preview','all'],default='preview')
    args=parser.parse_args()
    for stage in (['stage0','preview'] if args.stage=='all' else [args.stage]):
        build(stage)
