"""Reading and locator presentation; all research data remains read-only here."""
import html

import streamlit as st

from .annotations import unit_issues, annotated_html
from .citations import reference, reading_page_sources
from .clipboard import copy_button_html
from .corpus import index, aligned_units
from .locator import locate, snippets
from .reading import reading_pages, page_for_alignment, page_units
from .reviews import review_state
from .search import find_spans


def source_tools(data, unit, preview, key):
    ref=reference(data,unit)
    st.caption(ref['short'])
    if ref['markdown']:
        st.markdown(ref['markdown'])
        st.iframe(copy_button_html(ref['plain']),height='content')
    for note in ref['notes']:
        st.caption(note)
    e=ref['edition']
    if e.get('presentation'):
        st.caption('呈现方式：'+e['presentation'])
    for loc in ref['locations']:
        label=f'第{loc["printed_page"]}页' if unit['language']=='zh' else f'S. {loc["printed_page"]}'
        st.caption(label)
        preview(loc['source_id'],loc['pdf_page'],f'{key}_{loc["pdf_page"]}')
    if len(ref['locations'])>1:
        st.caption('该文本单元跨页；当前索引精度为整个单元，请在这些原页中核对命中字句。')


def request_jump(alignment_id, unit_id=None, query='', via=None, case=False, word=False):
    st.session_state['reading_jump']=dict(alignment_id=alignment_id,unit_id=unit_id,
                                        query=query,via=via,case=case,word=word)
    st.rerun()


def consume_jump(data):
    """Call before widgets are constructed, including the workspace selector."""
    if 'jump_alignment' in st.session_state:  # advanced page lookup compatibility
        st.session_state['reading_jump']=dict(alignment_id=st.session_state.pop('jump_alignment'))
    jump=st.session_state.pop('reading_jump',None)
    if jump:
        page=page_for_alignment(data,jump['alignment_id'])
        st.session_state.update(workspace='德中对读',section_id=page['section_id'],
            reading_page=page['id'],reader_query='',reader_issues_only=False,
            continuous_reading=False,reading_focus=jump)


def reading_unit(data, unit, query, case, word, preview, key, focused=False):
    issues=unit_issues(data,unit['id'])
    marked=annotated_html(unit['text'],find_spans(unit['text'],query,case,word),issues)
    st.caption(reference(data,unit)['short'])
    st.markdown(f'<div class="reader-text {"focused-text" if focused else ""}" lang="{unit["language"]}">{marked}</div>',unsafe_allow_html=True)
    for issue in issues:
        if issue['kind']=='semantic_doubt':
            st.warning(f'语义存疑 · 按底本照录：{issue["current_reading"]}。{issue["note"]}')
        else:
            st.warning(f'转录疑点：{issue["note"]} 当前：{issue["current_reading"]}；核对意见：{issue["reported_reading"]}')
    with st.expander('引用与原页'):
        source_tools(data,unit,preview,key)
        st.caption('文本记录：'+unit['id'])
        st.caption('文字经 AI 对照扫描页校订，仍可复核。' if unit.get('proofread_status')=='scan_checked_ai' else '文字尚待扫描页校订。')
        st.write(unit.get('transcription_note',''))


def render_reader(data, reviews, preview):
    sections=index(data['sections'])
    units=index(data['units'])
    groups=index(data['alignments'])
    section_id=st.sidebar.selectbox('研究专题',list(sections),key='section_id',format_func=lambda k:'穆勒评注' if k=='mill' else sections[k]['title'])
    query=st.sidebar.text_input('查找本专题德文或中文',key='reader_query',placeholder='Arbeit / 劳动 / 一段原文')
    case=st.sidebar.checkbox('区分大小写',False,key='reader_case')
    word=st.sidebar.checkbox('完整词匹配（德文）',False,key='reader_word')
    issues_only=st.sidebar.checkbox('仅看有转录标注的阅读页',False,key='reader_issues_only')
    pages=reading_pages(data,section_id)
    candidates=[]
    for page in pages:
        ids=[uid for aid in page['alignment_ids'] for uid in groups[aid]['de_ids']+groups[aid]['zh_ids']]
        matches=not query.strip() or any(find_spans(units[uid]['text'],query,case,word and units[uid]['language']=='de') for uid in ids)
        if matches and (not issues_only or any(unit_issues(data,uid) for uid in ids)):
            candidates.append(page)
    if not candidates:
        st.info('当前专题的已收录文本中没有命中。可缩短词语，或关闭完整词匹配、转录标注筛选。')
        return
    ids=[p['id'] for p in candidates]
    page_index={p['id']:p for p in pages}
    if st.session_state.get('reading_page') not in ids:
        st.session_state['reading_page']=ids[0]
    selected=st.sidebar.selectbox('阅读页（本专题）',ids,key='reading_page',format_func=lambda k:f'阅读页 {page_index[k]["number"]} · {len(page_index[k]["alignment_ids"])}组对照')
    continuous=st.sidebar.toggle('连续浏览本专题',key='continuous_reading')
    st.sidebar.caption('阅读页为界面分页；筛选保留页内前后文，页号不随检索改变。连续浏览从所选页开始。')
    page=page_index[selected]
    position=ids.index(selected)
    def turn(delta):
        st.session_state['reading_page']=ids[position+delta]
        st.session_state.pop('reading_focus',None)
    nav=st.columns([1,2,1])
    nav[0].button('← 上一阅读页',key='reading_prev',disabled=position==0,on_click=turn,args=(-1,))
    nav[1].caption(f'{sections[section_id]["title"]} · 阅读页 {page["number"]} / {len(pages)}')
    nav[2].button('下一阅读页 →',key='reading_next',disabled=position==len(ids)-1,on_click=turn,args=(1,))
    st.caption(sections[section_id]['coverage']+'。页与页仅连续呈现已收录样本，不代表原著全文连续覆盖。')
    focus=st.session_state.get('reading_focus',{})
    if focus.get('alignment_id') in page['alignment_ids']:
        st.info('已定位：'+groups[focus['alignment_id']]['label']+'。目标组以绿色边线标出。')
        if focus.get('via'):
            st.caption('通过已有版本比较关系跳到主读位置；该版本比较关系仍待研究者复核。下面保留本次命中的版本文本。')
            with st.expander('检索命中的比较版本',expanded=True):
                u=units[focus['unit_id']]
                reading_unit(data,u,focus.get('query',''),focus.get('case',False),focus.get('word',False),preview,'bridge_'+u['id'],True)
    shown=candidates[position:] if continuous else [page]
    for current in shown:
        st.subheader(f'阅读页 {current["number"]}')
        for col,language,title in zip(st.columns(2,gap='large'),['de','zh'],['德文原文','中文译文']):
            with col:
                st.markdown(f'**{title}**')
                st.caption('；'.join(reading_page_sources(data,page_units(data,current,language))) or '来源页待定位')
        for aid in current['alignment_ids']:
            group=groups[aid]
            focused=focus.get('alignment_id')==aid
            state,record=review_state(data,group,reviews)
            state_text={'manually_verified':'对应已人工确认','uncertain':'对应待确认','stale':'原确认已过期','automatically_aligned':'自动对齐 · 待确认'}[state]
            st.markdown(f'<div class="group-heading {"focus-heading" if focused else ""}">{html.escape(group["label"])} <small>· {state_text}</small></div>',unsafe_allow_html=True)
            de,zh=aligned_units(data,group)
            for col,items in zip(st.columns(2,gap='large'),[de,zh]):
                with col:
                    if not items: st.info('该段对应中文尚未收录。')
                    for unit in items:
                        q=query or (focus.get('query','') if focused else '')
                        c=case if query else focus.get('case',False)
                        w=word if query else focus.get('word',False)
                        reading_unit(data,unit,q,c,w and unit['language']=='de',preview,
                                     f'read_{aid}_{unit["id"]}',focused)
            if len(de)>1 or len(zh)>1:
                st.caption(f'本组对应 {len(de)} 个德文单元 / {len(zh)} 个中文单元，完整展示同组上下文。')
            with st.expander('本组记录 · '+aid):
                import json
                if record and record.get('note'):
                    st.caption('核验备注：'+record['note'])
                st.download_button('导出本组文本与来源',json.dumps(dict(alignment=group,de=de,zh=zh,
                    review=reviews.get(aid),effective_review_state=state,
                    editorial_issues=[i for u in de+zh for i in unit_issues(data,u['id'])]),ensure_ascii=False,indent=2),
                    file_name=f'{aid}.json',mime='application/json',key='export_'+aid)
    if not continuous:
        bottom=st.columns([1,2,1])
        bottom[0].button('← 上一阅读页',key='reading_prev_bottom',disabled=position==0,on_click=turn,args=(-1,))
        bottom[1].caption(f'阅读页 {page["number"]} / {len(pages)} · 本专题')
        bottom[2].button('下一阅读页 →',key='reading_next_bottom',disabled=position==len(ids)-1,on_click=turn,args=(1,))


def render_locator(data, preview):
    st.subheader('用词句找到原书位置')
    st.caption('检索当前已收录的德文与中文，包括比较版本。引用与定位精度为文本单元；跨页单元列出所有涉及页码。')
    query=st.text_area('输入德文或中文词、短语或文段',key='locator_query',height=90)
    from .citations import BIBLIOGRAPHY
    sid=st.selectbox('限定来源',['all']+[s['id'] for s in data['sources']],key='locator_source',
                    format_func=lambda k:'全部来源' if k=='all' else BIBLIOGRAPHY[k]['short_title'])
    case=st.checkbox('检索区分大小写',key='locator_case')
    word=st.checkbox('仅完整德文词',key='locator_word')
    if not query.strip():
        st.info('输入记得的词句，即可查询版本、印刷页和引用。')
        return
    # Whole-word boundaries are useful for German; Chinese words have no spaces.
    hits=locate(data,query,None if sid=='all' else sid,case,word)
    st.caption(f'{len(hits)} 个候选文本单元 · {sum(h["count"] for h in hits)} 处命中')
    if not hits: st.info('当前已收录语料中没有命中。可尝试较短片段或检查底本拼写。')
    for hit in hits:
        unit=hit['unit']
        st.markdown('#### '+hit['reference']['short'])
        st.caption(f'{unit["label"]} · {unit["id"]} · {hit["count"]}处命中')
        for snippet in snippets(unit['text'],hit['spans']):
            st.markdown(f'<div class="result-context">{snippet}</div>',unsafe_allow_html=True)
        source_tools(data,unit,preview,'result_'+unit['id'])
        for target in hit['targets']:
            label=('跳到对应主读位置' if target['via_comparison'] else '跳转到对读位置')+f' · 阅读页 {target["page"]["number"]}'
            if target['via_comparison']:
                st.caption('此结果属于比较版本，入口依据已有、待复核的版本比较关系。')
            if st.button(label,key=f'locate_{unit["id"]}_{target["alignment_id"]}'):
                request_jump(target['alignment_id'],unit['id'],query,target['via_comparison'],case,word)
        if not hit['targets']:
            st.caption('此文本尚未建立德中对应，暂无阅读页入口。')
        st.divider()
