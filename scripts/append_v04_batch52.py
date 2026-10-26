"""Batch 52: close the Mill front-fill seam without duplicating mill_062."""
from append_v04_batch6 import main
from append_v04_batch22 import ROUTES
from source_slices import rows, stream

DE = stream('de_megaiv2', [(448,8,42)])
ZH = stream('zh_single', [(184,12,26),(185,1,14)], {
    184: [('课生','谋生'),('东四','东西'),('于头','手头'),('目然','自然'),
          ('促便','促使'),('多万面','多方面'),('越是单方面的','越是单方面的，')],
    185: [('陷人','陷入'),('票赋','禀赋'),('课生','谋生'),('包含看','包含着'),
          ('活动的目的而','活动的目的，而'),('活看','活着'),('课取','谋取')],
})
ZH = (ZH[0].replace(',', '，').replace(';', '；').replace(':', '：'), ZH[1], ZH[2])
DE_STARTS = ['Das Verhältniß des Tausches','Dieß Verhältniß der entfremdeten',
    'In jener rohen Gestalt','Jeder tauscht daher','Die Arbeit war allerdings',
    'Durch den Tausch','Das Product wird als Werth','Je vielseitiger die Production',
    'In der Erwerbsarbeit liegt:']
ZH_STARTS = ['交换关系的前提','异化劳动的这种关系','在上面说到的',
    '因此，其中任何一人','诚然，劳动','通过交换','产品是作为价值',
    '生产越是多方面的','在谋生的劳动中']
LABELS = ['交换与直接谋生的劳动','异化劳动关系的顶点','物物交换的初始生产',
    '产品余额的交换','生活来源与个人存在','劳动的目的与收入来源',
    '为交换价值生产','生产多样化与谋生劳动','谋生劳动的四项规定']
ROWS = rows('mill',252,['马克思评注：'+x for x in LABELS],DE,ZH,DE_STARTS,ZH_STARTS)
PRINTED = {('de_megaiv2',448):'455',('zh_single',184):'174',('zh_single',185):'175'}
SEQUENCES = {f'mill_{n:03}': -29858+i for i,n in enumerate(range(252,261))}
NOTES = {f'mill_{n:03}':'此组为马克思对穆勒摘录的评注。' for n in range(252,261)}
NOTES['mill_252'] += '起于中文PDF184第12行，上一行红色Erwerbsarbeit为读者批注，未纳入正文。'
NOTES['mill_256'] += '德文扫描在Subsist与enzquelle间可见词内空格，照录并标疑点。'
NOTES['mill_259'] += '中文完整长句跨PDF184—185，保留页末逗号。'
NOTES['mill_260'] += '完整保留四项规定及编号；德PDF449为影印插页，正文接旧mill_062（德450/中185），本批在此收束。'
DOUBTS = {'mill_de_256':['Subsist enzquelle'],
          'mill_de_260':['gesellschaftliehen','Leftensmittel']}
OVERRIDES = {uid:{word:dict(kind='glyph_doubt',status='open',
    reported_reading='按扫描照录，待研究者核查',
    note=('原页Subsist与enzquelle间可见空格，按可见排布保留；未合并为规范拼写。'
          if word=='Subsist enzquelle' else
          '原页可见异常字形，按扫描照录；未依据语义改为常见拼写。'),
    evidence_pages=['de_megaiv2:448']) for word in words} for uid,words in DOUBTS.items()}
EXTRA = [dict(source_id='de_megaiv2',pdf_page=449,printed_page=None,page_kind='illustration',
    status='scan_checked_ai',checked_by='Codex',checked_at='2026-10-24',
    note='逐页核图：穆勒摘录手稿第XXX页影印及图题，无可见印刷页码；不作新正文，不推算编号。')]
SCAN_PAGES = dict(de_megaiv2=[448,449,450],zh_single=[184,185])
NEXT_START = dict(joined_existing=True,id='mill_062',sequence=-20000,
    de_pdf=450,de_line=2,de_printed='456',de_anchor='Je grösser, je ausgebildeter',
    zh_pdf=185,zh_line=15,zh_printed='175',zh_anchor='因此，在私有权关系的范围内',
    instruction='已接既有后段，勿重复追加；由协调核实整体范围及报告。')

def extra_assertions(data,evidence):
    from paris.corpus import index
    from paris.reading import reading_pages
    u=index(data['units'])
    order=[aid for p in reading_pages(data,'mill') for aid in p['alignment_ids']]
    expected=([f'mill_{n:03}' for n in range(110,261)]+
              [f'mill_{n:03}' for n in range(62,110)]+[f'mill_{n:03}' for n in range(1,62)])
    assert order==expected and len(set(order))==260
    assert [u[f'mill_de_{n:03}']['sequence'] for n in range(110,261)]==list(range(-30000,-29849))
    assert u['mill_de_251']['text'].endswith('wie er zum Preiß wird.')
    assert u['mill_zh_251']['text'].endswith('应当在其他地方加以探讨。')
    assert u['mill_de_252']['text']==DE[0][:DE[0].index(DE_STARTS[1])].strip()
    assert u['mill_zh_252']['text']=='交换关系的前提是劳动成为直接谋生的劳动。'
    assert u['mill_de_256']['text'].find('Subsist enzquelle')>=0
    assert [x['pdf_page'] for x in u['mill_zh_259']['locations']]==[184,185]
    assert '越是单方面的，他的劳动' in u['mill_zh_259']['text']
    assert u['mill_de_260']['text'].endswith('Leftensmittel zu erwerben.')
    assert u['mill_zh_260']['text'].endswith('他活着只是为了谋取生活资料。')
    assert all(x in u['mill_de_260']['text'] for x in ['1)','2)','3)','4)'])
    assert all(x in u['mill_zh_260']['text'] for x in ['(1)','(2)','(3)','(4)'])
    assert u['mill_de_062']['text'].startswith(NEXT_START['de_anchor'])
    assert u['mill_zh_062']['text'].startswith(NEXT_START['zh_anchor'])
    assert all('Erwerbsarbeit' not in u[f'mill_zh_{n:03}']['text'] for n in range(252,261))
    assert all('还是费尔巴哈逻辑' not in u[f'mill_zh_{n:03}']['text'] for n in range(252,261))
    assert [x for x in data['page_map'] if x['source_id']=='de_megaiv2' and x['pdf_page']==449]==EXTRA
    assert not any(x['pdf_page']==449 for v in data['units'] for x in v['locations'] if x['source_id']=='de_megaiv2')
    if evidence:
        from pathlib import Path
        assert evidence['de_megaiv2:449']==Path('tmp/source_review/de_megaiv2/0449.txt').read_text(encoding='utf-8')

if __name__=='__main__':
    assert len(ROWS)==9
    main(rows=ROWS,printed=PRINTED,batch=52,release='0.4.0-alpha48',reviewed_date='2026-10-24',
         source_by_section=ROUTES,sequence_overrides=SEQUENCES,doubts=DOUBTS,
         issue_overrides=OVERRIDES,row_notes=NOTES,extra_page_maps=EXTRA,
         coverage_notes={'mill':'第46—52批前补mill_110—260已接旧mill_062，顺序为110—260、062—109、001—061；旧ID及sequence保留。正文首尾与批次接缝证据见第52批验收，全文分母仍待整体审计。'})
