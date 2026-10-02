"""Run: python -m streamlit run app.py --server.address 127.0.0.1"""
import csv
import html
import io
import json

import streamlit as st

from paris import __version__
from paris.corpus import load_corpus,index,aligned_units,context_units
from paris.search import find_spans,highlighted_html,search_units
from paris.pages import lookup_pages,units_on_page,render_page,missing_pages,page_label,alignments_on_page
from paris.compare import compare_texts,diff_html
from paris.stats import term_distribution
from paris.reviews import load_reviews,review_state,save_review
from paris.annotations import unit_issues,annotated_html
from paris.citations import reference
from paris.reader_ui import render_reader,render_locator,consume_jump,source_tools
from paris.research_ui import render_coverage,render_statistics,coverage_table
from paris.sampling import load_plan as load_sampling_plan

st.set_page_config(page_title='巴黎手稿 · 德中对读',page_icon='📖',layout='wide')
st.markdown('''<style>
.stApp {background:#f7f5ef;color:#253b34}
[data-testid="stSidebar"] {background:#e9eee8}
.block-container {max-width:1440px;padding-top:2.6rem}
h1,h2,h3 {font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif!important}
.reading {background:#fffdf7;border-top:3px solid #567766;padding:1.5rem 1.6rem;
 font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif;font-size:1.10rem;
 line-height:1.95;overflow-wrap:anywhere;white-space:pre-wrap;margin:0.8rem 0 1rem}
.reader-text {font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif;font-size:1.10rem;line-height:1.95;white-space:pre-wrap;overflow-wrap:anywhere;margin:.35rem 0 .7rem}
.group-heading {border-top:1px solid #d9dfd5;margin-top:1.2rem;padding:.55rem 0;font-size:.85rem;color:#52695d}
.group-heading small {color:#748578}
.focus-heading,.focused-text {border-left:3px solid #527e62;padding-left:.7rem}
.result-context {line-height:1.85;margin:.5rem 0;white-space:pre-wrap;overflow-wrap:anywhere}
.eyebrow {letter-spacing:.18em;font-size:.78rem;color:#61786c}
.subtle {color:#66786d;font-size:.92rem}
mark {background:#f4df94;color:#203a30;padding:0 .08rem;border-radius:2px}
.editorial-mark {text-decoration:underline dotted #975514;text-underline-offset:.25em;background:#fff0da}
ins {background:#d8eee0;color:#124b2a;text-decoration:underline}
del {background:#f7ddd7;color:#782d20;text-decoration:line-through}
[data-testid="stMetricValue"] {font-family:Georgia,serif}
</style>''',unsafe_allow_html=True)

try:
    data=load_corpus()
    reviews=load_reviews()
except (ValueError,OSError,KeyError) as exc:
    st.error(f'研究数据读取失败：{exc}')
    st.stop()

units=index(data['units'])
editions=index(data['editions'])
sources=index(data['sources'])
sections=index(data['sections'])
alignments=index(data['alignments'])
STATE_LABELS={'uncertain':'对应待你确认','automatically_aligned':'自动对齐 · 待核验','manually_verified':'对应已人工确认','stale':'文本已变更 · 需要重新确认'}


def citation(unit):
    return reference(data,unit)['short']


def preview(source_id,pdf_page,key):
    state_key=f'preview_open_{key}'
    opened=st.session_state.get(state_key,False)
    if st.button('收起这一原页' if opened else '查看原页',key=key):
        st.session_state[state_key]=not opened
        st.rerun()
    if st.session_state.get(state_key,False):
        try:
            st.image(render_page(sources[source_id],pdf_page),caption=editions.get(source_id,{}).get('short_title',source_id)+' · '+('；'.join(page_label(p) for p in lookup_pages(data,source_id,pdf_page,'pdf_page')) or '印刷页未定位'),width='stretch')
        except (OSError,ValueError,ImportError) as exc:
            st.info(str(exc))


def show_unit(unit,query='',case=False,word=False,prefix='read'):
    st.caption(citation(unit))
    issues=unit_issues(data,unit['id'])
    marked=annotated_html(unit['text'],find_spans(unit['text'],query,case,word),issues)
    st.markdown(f'<div class="reading" lang="{unit["language"]}">{marked}</div>',unsafe_allow_html=True)
    proof_label='文字已由 AI 对照扫描页校订，待研究者复核' if unit.get('proofread_status')=='scan_checked_ai' else '文字尚待扫描页校订'
    st.caption(f'{unit["id"]} · {proof_label}')
    for issue in issues:
        if issue['kind']=='semantic_doubt':
            st.warning(f'语义存疑 · 按底本照录：{issue["current_reading"]}。{issue["note"]}')
            st.caption('橙色虚线标出照录位置；这是一条编辑说明，不是原书强调。来源：'+citation(unit))
        else:
            st.warning(f'转录疑点：{issue["note"]} 当前：{issue["current_reading"]}；核对意见：{issue["reported_reading"]}')
    with st.expander('原页与转录说明'):
        st.write(unit['transcription_note'])
        source_tools(data,unit,preview,f'{prefix}_{unit["id"]}')


def review_badge(alignment):
    state,record=review_state(data,alignment,reviews)
    text=STATE_LABELS[state]
    if state=='manually_verified':
        st.success(f'{text} · {record["reviewer"] if record else alignment["verified_by"]}')
    else:
        st.info(text)
    if record and record.get('note'):
        st.caption('核验备注：'+record['note'])


st.sidebar.markdown('### 巴黎手稿研究工具')
st.sidebar.caption('PARIS MANUSCRIPTS / 1844')
consume_jump(data)
mode=st.sidebar.radio('工作区',['德中对读','页码索引','版本比较','术语分布','覆盖清单','审核与资料'],key='workspace')
st.sidebar.divider()
st.sidebar.caption(f'{__version__} · 本地研究预览')
st.sidebar.caption('收录范围：精选样本。所有对应关系均有独立核验状态。')

st.markdown('<div class="eyebrow">PARIS MANUSCRIPTS · RESEARCH READER</div>',unsafe_allow_html=True)
st.title('巴黎手稿 · 德中对读')
st.caption('连续对读 · 词句定位 · 原页核查 · 论文引用')
verified=sum(review_state(data,a,reviews)[0]=='manually_verified' for a in data['alignments'])
c1,c2,c3=st.sidebar.columns(3)
c1.metric('已整理对照',len(data['alignments']))
c2.metric('已由你确认',verified)
c3.metric('已收录专题',len(data['sections']))
st.divider()

if mode=='德中对读':
    render_reader(data,reviews,preview)

elif mode=='页码索引':
    render_locator(data,preview)
    if st.toggle('高级页码核验（含 PDF 页序）',key='advanced_pages'):
        st.subheader('在书页与 PDF 之间定位')
        st.caption('只查询已建立的逐页映射；未收录页不推算。原件发生变化时需重新核对映射。')
        sid=st.selectbox('来源文件',list(sources),key='mapping_source',format_func=lambda k:editions[k]['short_title'])
        kind=st.radio('已知的是',['印刷页','PDF页序'],key='mapping_kind',horizontal=True)
        value=st.text_input('输入页码',key='mapping_value',placeholder='例如 364；前言可用罗马数字或带星号页码')
        if value.strip():
            found=lookup_pages(data,sid,value,'printed_page' if kind=='印刷页' else 'pdf_page')
            absent=missing_pages(data,sid,value) if kind=='印刷页' else []
            for missing in absent:
                st.warning(f'已确认缺页：印刷页 {missing["printed_page"]}。{missing["note"]} 无可用PDF页序，不能预览。')
                st.caption('缺页依据：'+missing['evidence'])
            if not found and not absent:
                st.info('该页尚无已核对的映射。请保留印刷页与PDF页序的区别，不使用估算偏移。')
            for loc in found:
                st.success(f'印刷页 {page_label(loc)} ↔ PDF 第 {loc["pdf_page"]} 页')
                if loc.get('note'): st.caption(loc['note'])
                for u in units_on_page(data,sid,loc['pdf_page']):
                    st.write(f'{u["id"]} · {u["label"]}')
                for a in alignments_on_page(data,sid,loc['pdf_page']):
                    if st.button('打开对读：'+a['label'],key=f'jump_{loc["pdf_page"]}_{a["id"]}'):
                        st.session_state['jump_alignment']=a['id']
                        st.rerun()
                preview(sid,loc['pdf_page'],f'index_{sid}_{loc["pdf_page"]}')
        with st.expander('查看当前来源全部映射'):
            rows=[{'印刷页':page_label(p),'PDF页序':p['pdf_page'],'页类型':p.get('page_kind','正文'),'核对':p.get('status','未记录'),'说明':p.get('note','')} for p in data['page_map'] if p['source_id']==sid]
            st.dataframe(rows,hide_index=True)
            st.download_button('导出当前来源页码表',json.dumps({'source':sources[sid],'page_map':[p for p in data['page_map'] if p['source_id']==sid],'missing_pages':[p for p in data.get('missing_pages',[]) if p['source_id']==sid]},ensure_ascii=False,indent=2),file_name=f'{sid}-pages.json',mime='application/json')
        with st.expander('按PDF页序浏览原文件'):
            st.caption('可查看未建索引的PDF页。浏览不会自动认定印刷页码，也不会新增映射。')
            browse_page=st.number_input('PDF页序（从1开始）',min_value=1,max_value=sources[sid]['pdf_page_count'],value=1,step=1,key=f'browse_{sid}')
            mapped=lookup_pages(data,sid,browse_page,'pdf_page')
            if mapped: st.caption('已记录印刷页：'+'；'.join(page_label(p) for p in mapped))
            else: st.caption('该PDF页尚未建立印刷页映射。')
            preview(sid,browse_page,f'browse_preview_{sid}_{browse_page}')
    

elif mode=='版本比较':
    st.subheader('查看同语种文本差异')
    st.caption('红色删除线为左侧独有内容，绿色下划线为右侧新增内容；不判断哪种表述更优。')
    if not data['comparisons']:
        st.info('比较功能已就绪；已核对的同语种比较样本尚未录入。')
    else:
        comparisons=index(data['comparisons'])
        cid=st.selectbox('比较位置',list(comparisons),format_func=lambda k:comparisons[k]['label'])
        c=comparisons[cid]
        l=[units[i] for i in c['left_ids']]
        r=[units[i] for i in c['right_ids']]
        changes=compare_texts('\n\n'.join(u['text'] for u in l),'\n\n'.join(u['text'] for u in r),l[0]['language'])
        st.info(c['note'])
        if all(p['kind']=='equal' for p in changes):
            st.success('这组转录文本相同。')
        for col,side,group in zip(st.columns(2,gap='large'),['left','right'],[l,r]):
            with col:
                st.markdown(f'### {editions[group[0]["edition_id"]]["short_title"]}')
                for u in group:
                    st.caption(citation(u))
                st.markdown(f'<div class="reading">{diff_html(changes,side)}</div>',unsafe_allow_html=True)
        st.download_button('导出差异明细',json.dumps(changes,ensure_ascii=False,indent=2),file_name=f'{cid}.json',mime='application/json')

elif mode=='术语分布':
    render_statistics(data,reviews,show_unit)

elif mode=='覆盖清单':
    render_coverage(data,reviews)

else:
    st.subheader('分批审核与来源')
    st.caption('文字经过AI对照扫描页整理。对应关系由你确认；保存时绑定文本和页码，内容变化后原确认自动失效。')
    suggested = {}
    try:
        sampling = load_sampling_plan(data)
    except (ValueError, OSError, KeyError) as exc:
        st.warning(str(exc)); sampling = None
    if sampling:
        suggested = {r['alignment_id']:r['reasons'] for r in sampling['recommended']}
        done = sum(review_state(data,alignments[k],reviews)[0]=='manually_verified' for k in suggested)
        st.info(f'本轮建议核查 {len(suggested)}/{len(sampling["scope_ids"])} 组，已逐组确认 {done}/{len(suggested)}。未抽中组保持未人工核对，不随样本通过而自动确认。')
        with st.expander('人工抽样标准与清单'):
            st.markdown('普通文本按专题、来源版本及长短段分层，暂取20%且每层至少2组；另补跨页、照录疑点、多单元对应的代表组，未解决疑点单列。比例是试运行规则，不是统计质量保证。')
            st.markdown('每个抽中组检查两侧原页：无漏字/漏句/重复/错序，否定词和术语忠实，对应起止完整，版本与页码准确。发现影响研究的错误，先保留待审，扩大同页及同类检查；用于论文引用的片段另行逐条核对。')
            st.dataframe([{'组ID':k,'选中理由':'；'.join(v)} for k,v in suggested.items()],hide_index=True)
            st.download_button('下载本轮抽样清单',json.dumps(sampling,ensure_ascii=False,indent=2),file_name='sampling-plan.json',mime='application/json')
    sampled_only=st.toggle('只看建议核查组',key='sampled_only',disabled=not bool(suggested))
    batch=st.selectbox('审核批次',sorted({a['review_batch'] for a in data['alignments']}),format_func=lambda x:f'第{x}批 · {sum(a["review_batch"]==x for a in data["alignments"])}组')
    for a in [a for a in data['alignments'] if a['review_batch']==batch and (not sampled_only or a['id'] in suggested)]:
        with st.expander(f'{a["id"]} · {a["label"]}'):
            if a['id'] in suggested: st.caption('核查理由：'+'；'.join(suggested[a['id']]))
            review_badge(a)
            de,zh=aligned_units(data,a)
            for col,group in zip(st.columns(2,gap='large'),[de,zh]):
                with col:
                    for u in group:
                        show_unit(u,prefix='review')
            with st.form(f'review_form_{a["id"]}'):
                reviewer=st.text_input('核验人',key=f'name_{a["id"]}')
                note=st.text_area('核验说明',key=f'note_{a["id"]}')
                decision=st.selectbox('结论',['确认对应','保留待审'],key=f'decision_{a["id"]}')
                checked=st.checkbox('我已查看本组原文、译文与来源页码',key=f'checked_{a["id"]}')
                if st.form_submit_button('保存我的核验'):
                    if not checked:
                        st.error('请先核对本组文本和页码。')
                    else:
                        try:
                            save_review(data,a,reviewer,note,'manually_verified' if decision=='确认对应' else 'uncertain')
                            st.rerun()
                        except (ValueError,OSError) as exc:
                            st.error(str(exc))
    st.markdown('### 收录范围')
    st.dataframe(coverage_table(data,reviews),hide_index=True)
    primary_units=[u for u in data['units'] if u.get('role','primary')=='primary']
    checked_units=sum(u.get('proofread_status')=='scan_checked_ai' for u in primary_units)
    st.caption(f'当前主读样本：{len(primary_units)} 个文本单元，AI扫描校订 {checked_units}/{len(primary_units)}；人工对应确认 {verified}/{len(data["alignments"])}。全文总段落数尚未建立，不报告全文覆盖百分比。')
    st.markdown('### 版本与资料')
    for e in data['editions']:
        with st.expander(e['short_title']):
            st.json(e)
            st.write('来源文件：'+sources[e['source_id']]['file_name'])
    st.caption('标题标签为项目导航文字。纯文本转录不复现字重和斜体，中文注号保留；需要研究排版和手稿符号时请查看原页。')
