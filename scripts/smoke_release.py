"""Run from an extracted package to check imports, both topics, tools, and missing PDFs."""
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus
from streamlit.testing.v1 import AppTest

data=load_corpus()
at=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
assert not at.exception
assert int(at.metric[0].value)==len(data['alignments'])
for section in data['sections']:
    at.sidebar.selectbox[0].select(section['id']).run()
    assert not at.exception
    assert at.sidebar.selectbox[1].value.startswith('reading-'+section['id'])
if not (ROOT/'Asset_by_user').exists() and not (ROOT/'local_sources.json').exists():
    next(b for b in at.button if b.key.startswith('read_')).click().run()
    assert not at.exception
    assert any('尚未配置本地PDF' in x.value for x in at.info)
for mode in ['页码索引','版本比较','术语分布','覆盖清单','审核与资料']:
    at.sidebar.radio[0].set_value(mode).run(timeout=30)
    assert not at.exception,mode
print(f'PASS: {len(data["alignments"])} alignments; {len(data["sections"])} topics; 6 workspaces; root={ROOT}')
