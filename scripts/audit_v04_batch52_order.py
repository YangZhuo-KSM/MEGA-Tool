"""Read-only Mill reading order and literal source seam evidence for batch 52."""
import hashlib
import importlib
import json
import sys
from itertools import groupby
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus,index
from paris.reading import reading_pages
import append_v04_batch52 as recipe

def main():
    d=load_corpus(); u=index(d['units']); a=index(d['alignments'])
    recipe.extra_assertions(d,json.loads((ROOT/'data/extraction.json').read_text(encoding='utf-8')))
    order=[aid for p in reading_pages(d,'mill') for aid in p['alignment_ids']]
    assert len(order)==260 and set(order)=={f'mill_{n:03}' for n in range(1,261)}
    runs=[]
    for batch,items in groupby(order,key=lambda x:a[x]['review_batch']):
        ids=list(items)
        runs.append(dict(batch=batch,first=ids[0],last=ids[-1],count=len(ids),
            first_sequence=u[a[ids[0]]['de_ids'][0]]['sequence'],
            last_sequence=u[a[ids[-1]]['de_ids'][0]]['sequence']))
    assert [x['batch'] for x in runs]==[46,47,48,49,50,51,52,25,26,3,4,22,23,24]
    recipe_checked=[]
    for b in [46,47,48,49,50,51,52,25,26]:
        r=importlib.import_module(f'append_v04_batch{b}')
        ids=[]
        for section,n,label,de,zh,dp,zp in r.ROWS:
            if section!='mill': continue
            aid=f'mill_{n:03}'; ids.append(aid)
            for lang,text,pages in [('de',de,dp),('zh',zh,zp)]:
                v=u[f'mill_{lang}_{n:03}']
                assert v['text']==text
                assert [l['pdf_page'] for l in v['locations']]==pages
                assert v['sequence']==r.SEQUENCES[aid]
        assert ids==[x for x in order if a[x]['review_batch']==b]
        recipe_checked.append(dict(batch=b,groups=len(ids),body_locations_sequence='match'))
    # Explicit raw tails and heads: only whitespace may occur between them.
    # Line numbers refer to saved extraction, whose hash is retained below.
    pairs=[
      (131,132,('de_megaiv2',429,'die Zukunft, p. 50, 51.','Siehe p. sqq.'),
               ('zh_single',164,'而将来得不到补偿。(第50一51贝)','看一看以下各页')),
      (155,156,('de_megaiv2',433,'angewandt ist.« p. [103—]104.','Die erste und einzige Frage'),
               ('zh_single',168,'例。”(第[103]—104页)','因此,首要的和惟一的问题')),
      (179,180,('de_megaiv2',439,'nach seinem Belieben grösser oder kleiner.','Im ersten Fall öffnet'),
               ('zh_single',173,'愿使之增加或减少。”','在第一种情况下')),
      (203,204,('de_megaiv2',443,'Entwicklung des Geldwesens.','Im Creditwesen'),
               ('zh_single',177,'因素。','在信用业')),
      (227,228,('de_megaiv2',445,'der gesellschaftliche Genuß ist.','Indem das menschliche'),
               ('zh_single',180,'社会的活动和社会的享受。|','因为人的本质')),
      (251,252,('de_megaiv2',448,'wie er zum Preiß wird.','Das Verhältniß des Tausches'),
               ('zh_single',184,'应当在其他地方加以探讨。 Erwerbsarbeit','交换关系的前提')),
      (85,86,('de_megaiv2',453,'Waaren producirt hat. p. 251, 52.','»Zwei Sachen sind nöthig'),
             ('zh_single',189,'求。”(第251一252页)','“构成需求必须有两个条件')),
      (109,1,('de_megaiv2',455,'fremden gegenständlichen Eigennutz.','Du hast allerdings'),
              ('zh_single',191,'化的私利。','当然,你作为人')),
    ]
    seams=[]
    for left,right,*sides in pairs:
        aid,bid=f'mill_{left:03}',f'mill_{right:03}'
        assert order[order.index(aid)+1]==bid
        entry=dict(left=aid,right=bid,sides=[])
        for lang,(source,page,tail,head) in zip(['de','zh'],sides):
            raw=(ROOT/f'tmp/source_review/{source}/{page:04}.txt').read_text(encoding='utf-8')
            pos=raw.index(tail); end=pos+len(tail); start=raw.index(head,end)
            between=raw[end:start]
            # The margin's printed line number 10 precedes Du hast, not body text.
            assert not between.strip() or (left==109 and lang=='de' and between.strip()=='10')
            entry['sides'].append(dict(language=lang,source=source,pdf_page=page,
                printed_page=u[a[bid][lang+'_ids'][0]]['locations'][0]['printed_page'],
                left_tail=u[a[aid][lang+'_ids'][0]]['text'][-130:],
                right_head=u[a[bid][lang+'_ids'][0]]['text'][:130],
                left_raw_line=raw[:pos].count('\n')+1,right_raw_line=raw[:start].count('\n')+1,
                raw_boundary=raw[pos:start+len(head)],raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),
                gap='none; annotated text/margin explicitly excluded where applicable'))
        seams.append(entry)
    # New final group ends the last body line; only the facsimile intervenes.
    de448=(ROOT/'tmp/source_review/de_megaiv2/0448.txt').read_text(encoding='utf-8').splitlines()
    de450=(ROOT/'tmp/source_review/de_megaiv2/0450.txt').read_text(encoding='utf-8').splitlines()
    zh185=(ROOT/'tmp/source_review/zh_single/0185.txt').read_text(encoding='utf-8').splitlines()
    assert de448[41].strip()=='Leftensmittel zu erwerben.' and de448[42].strip()=='455'
    assert len(de448)==43 and de450[1].startswith('Je grösser, je ausgebildeter')
    assert zh185[13].strip()=='活资料。' and zh185[14].startswith('因此,在私有权关系的范围内')
    join=dict(left='mill_260',left_sequence=-29850,right='mill_062',right_sequence=-20000,
        de=dict(left_pdf=448,left_printed='455',left_lines=[33,42],
            tail=u['mill_de_260']['text'][-150:],right_pdf=450,right_printed='456',right_lines=[2,4],
            head=u['mill_de_062']['text'],intervening=recipe.EXTRA,
            evidence='448最后正文行后只有印刷页码455；449为XXX手稿影印；450首正文行即旧062，无其他正文。'),
        zh=dict(left_pdf=185,left_printed='175',left_lines=[6,14],
            tail=u['mill_zh_260']['text'][-150:],right_pdf=185,right_printed='175',right_lines=[15,16],
            head=u['mill_zh_062']['text'],
            evidence='185第14行“活资料。”后第15行直接起“因此”，红色读者批注未纳入正文。'))
    assert order[order.index('mill_260')+1]=='mill_062'
    report=dict(batch=52,passed=True,mill_groups=260,ordered_runs=runs,
        frontfill_recipes_checked=recipe_checked,boundary_evidence=seams,closing_join=join,
        scope='全穆勒260组阅读顺序与ID唯一性；46—52、25—26前补配方全文/位置/sequence重建；各前补批接缝原提取相邻行及本批5页图像。既有后段正文保护由52专项审计覆盖，未据页码跨度推定全书完整。',
        corpus_sha256=hashlib.sha256((ROOT/'data/corpus.json').read_bytes()).hexdigest())
    target=ROOT/'tmp/batch52-mill-order-audit.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(passed=True,mill_groups=260,ordered_runs=runs,closing_join=join,report=str(target)),ensure_ascii=False))

if __name__=='__main__': main()
