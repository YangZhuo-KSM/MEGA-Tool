"""Coverage and scoped, reproducible term research surfaces."""
import csv
import io
import json
import streamlit as st
from .coverage import load_plan,coverage_rows,WORKS
from .stats import research_distribution
from .reader_ui import request_jump
from .reading import reading_targets
from .corpus import index


def coverage_table(data,reviews):
    rows=coverage_rows(data,reviews,load_plan(data))
    def ratio(n,d): return f'{n}/{d}（{n/d:.0%}）' if d else '尚无收录'
    return [dict(手稿=WORKS[r['work']],题目=r['title'],状态=r['state'],已收录对应组=r['groups'],
        全文收录比例='分母未建立' if r['collected_ratio'] is None else f'{r["collected_ratio"]:.0%}',
        已收录文本AI扫描校订=ratio(r['scan_checked'],r['units']),人工对应确认=ratio(r['confirmed'],r['groups']),
        德文目录起始页=r['de_start'] or '待定位',中文目录起始页=r['zh_start'] or '待定位') for r in rows]


def render_coverage(data,reviews):
    plan=load_plan(data); rows=coverage_rows(data,reviews,plan)
    st.subheader('研究语料覆盖清单')
    st.caption(plan['basis'])
    cols=st.columns(3)
    cols[0].metric('已开始整理的目录项',f'{sum(r["groups"]>0 for r in rows)}/{len(rows)}')
    checked=sum(r['scan_checked'] for r in rows); unit_count=sum(r['units'] for r in rows)
    cols[1].metric('已收录文本 · AI扫描校订',f'{checked}/{unit_count}')
    confirmed=sum(r['confirmed'] for r in rows); groups=sum(r['groups'] for r in rows)
    cols[2].metric('已收录对应 · 人工确认',f'{confirmed}/{groups}')
    st.info('目录项开始整理只表示已有片段。全文单元总数尚未建立，因此不报告全文收录百分比。AI扫描校订与人工对应确认分别统计。')
    st.dataframe(coverage_table(data,reviews),hide_index=True)
    st.caption('目录起始页来自目录图像，用于安排整理；并不表示该节所有页已建立原页映射。')
    for row in rows:
        if row['groups']:
            a=next(a for a in data['alignments'] if a['section_id'] in row['section_ids'])
            if st.button(f'阅读已收录部分：{row["title"]}',key='coverage_'+row['id']):
                request_jump(a['id'])
    st.download_button('导出覆盖清单与计算依据',json.dumps(dict(plan=plan,coverage=rows,
        denominator_note='checked_ratio分母为已收录文本单元；confirmed_ratio分母为已收录对应组；全文分母未知时collected_ratio=null。'),ensure_ascii=False,indent=2),
        file_name='research-coverage.json',mime='application/json')


def render_statistics(data,reviews,show_unit):
    st.subheader('术语在已收录文本中的分布')
    st.caption('选择语言、版本、专题和核验范围；各查询独立进行字面计数，每个文本单元只计一次。结果仅代表已收录范围。')
    language=st.selectbox('统计语言',['de','zh'],format_func=lambda k:'德文' if k=='de' else '中文',key='stats_language')
    editions=index(data['editions']); sections=index(data['sections']); units=index(data['units'])
    choices=[e['id'] for e in data['editions'] if e['language']==language]
    selected_editions=st.multiselect('统计版本',choices,default=choices,key='stats_editions_'+language,format_func=lambda k:editions[k]['short_title'])
    selected_sections=st.multiselect('统计专题',list(sections),default=list(sections),key='stats_sections',format_func=lambda k:sections[k]['title'])
    queries=st.text_area('词语或短语（每行一项）',value='Arbeit' if language=='de' else '劳动',key='stats_queries_'+language)
    primary=st.checkbox('仅主读版本，排除比较副本',True,key='stats_primary')
    confirmed=st.checkbox('仅已有有效人工对应确认的文本',False,key='stats_confirmed')
    case=st.checkbox('统计区分大小写',False,key='stats_case')
    word=st.checkbox('仅完整德文词',False,key='stats_word',disabled=language=='zh')
    report=research_distribution(data,reviews,queries.splitlines(),language,selected_editions,selected_sections,
                                 primary,confirmed,case,word and language=='de')
    st.caption(f'本次范围：{report["scope"]["units"]} 个文本单元，{len(report["scope"]["queries"])} 项独立查询。不同查询可能重叠，不把各查询之和当作唯一词数。')
    if not primary: st.info('已包含比较版本：同一内容的不同出版版本分别计数，导出按edition_id区分。')
    st.dataframe([{'查询':r['query'],'专题':r['section'],'出现次数':r['count'],'范围内文本单元':r['units']} for r in report['summary']],hide_index=True)
    if not report['hits']: st.info('当前范围无命中。可调整查询或筛选；空结果也可导出。')
    output=io.StringIO(newline='')
    columns=['query','unit_id','section_id','edition_id','count','citation','source','citation_notes','text','spans','alignment_ids','review_states','proofread_status']
    writer=csv.DictWriter(output,fieldnames=columns); writer.writeheader()
    for row in report['hits']:
        writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in row.items()})
        u=units[row['unit_id']]
        with st.expander(f'{row["query"]} · {u["label"]} · {row["count"]}次 · {editions[u["edition_id"]]["short_title"]}'):
            show_unit(u,row['query'],case,word and language=='de',prefix=f'stats_{report["scope"]["queries"].index(row["query"])}')
            for target in reading_targets(data,u['id']):
                if st.button('到对读位置',key=f'stats_jump_{report["scope"]["queries"].index(row["query"])}_{u["id"]}_{target["alignment_id"]}'):
                    request_jump(target['alignment_id'],u['id'],row['query'],target['via_comparison'],case,word and language=='de')
    st.download_button('导出逐条命中 CSV',('\ufeff'+output.getvalue()).encode('utf-8'),file_name='term_hits.csv',mime='text/csv')
    st.download_button('导出查询条件、分布与原文 JSON',json.dumps(report,ensure_ascii=False,indent=2),file_name='term_research.json',mime='application/json')
