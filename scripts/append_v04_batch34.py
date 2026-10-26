"""Batch 34: scan-reviewed Schulz/Pecqueur excerpts in the wages section."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(333, 20, 41), (334, 2, 42), (335, 3, 43), (336, 2, 23)],
            join_page_hyphens=True)
ZH = stream('zh_collected', [(257, 23, 26), (258, 2, 29), (259, 2, 33), (260, 2, 17)], {
    257: [('[VIII]"', '[VIII]“')],
    258: [('生活得奸', '生活得好'), ('收人的', '收入的'), ('但是.', '但是，'),
          ('[rx]', '[IX]'), ('情况下.', '情况下，'),
          ('（舒尔茨（生产运动〉66第65页)', '（舒尔茨《生产运动》⁶⁶第65页）'),
          ('提髙', '提高'), ('三分之―', '三分之一'), ('第65、66页〉', '第65、66页）'),
          ('"国民要想', '“国民要想'), ('榷神', '精神'), ('贏得', '赢得'), ('■-个', '一个')],
    259: [('生产郁门', '生产部门'), ('精沖', '精神'), ('计算过.', '计算过，'),
          ('利益•尽管', '利益……尽管'), ('民士说', '民来说'), ('无已。"', '无已。”'),
          ('伹是,', '但是，'), ('梢神', '精神'), ('较髙', '较高'), ('表明丁', '表明了'),
          ('[X]]', '[XI]'), ('。”(同上', '。”（同上'),
          (',', '，'), ('女工:', '女工：'), (';', '；'), ('第71、72页〉', '第71、72页）'),
          ('13-18', '13—18'), ('[XI】]', '[XII]'), ('阶缀', '阶级'),
          ('(舒尔茨(生产运动〉', '（舒尔茨《生产运动》')],
    260: [('•做资本家', '‘做资本家'), ('一軸工作', '一种工作'), ('第60页)', '第60页）'),
          ('〈社会经济[和政治经济]的新理论〉67', '《社会经济[和政治经济]的新理论》⁶⁷'),
          (';', '；'), ('第409、410页)', '第409、410页）'),
          ('“出租自己的劳动"，“出借自己的劳动换取利息代替别人劳动"。',
           '“出租自己的劳动”，“出借自己的劳动换取利息”，“代替别人劳动”。'),
          ('“出租劳动材料"，“出借劳动材料换取利息”让别人代替自己劳动”。',
           '“出租劳动材料”，“出借劳动材料换取利息”，“让别人代替自己劳动”。'),
          ('一无所有者以各种各样的形式卖淫（同上', '一无所有者以各种各样的形式卖淫。”（同上')],
})
DE_STARTS = [
    '|Vin| „Das läßt', 'Ueberdies ist die Grösse', 'Endüch ist noch',
    '„Allein selbst', 'Der Samojede', 'Aber die Nationalökonomie',
    '„Ein Volk', 'Verrichtet doch jezt', 'War nun früher', 'Aber auch über',
    'Man hat in Frankreich', '„Der Uebergang', 'Nach der Natur der Sache',
    '„Für die Zukunft', '„In den englischen', 'Auch in den nordamerikanischen',
    '„In den von Dampf', '„Lord Broughams', '«Pour vivre donc', 'Domestiques',
    '„louer son travail"', '„louer la matière', '|xm| «cette constitution', '«la prostitution',
]
ZH_STARTS = [
    '[VIII]“可以肯定地说', '此外，工人的工资多少', '最后，还应注意过去',
    '“然而，即使所谓', '靠鲸油和腐鱼', '但是，国民经济学', '“国民要想',
    '的确，今天由于', '如果说为了满足', '但是，在我们甚至', '法国有人计算过',
    '“从复合的手工劳动', '根据事物的本性', '“但是，在各国人民', '“在英国的纺纱厂',
    '1833年在北美', '“1835年，在拥有', '“布鲁姆勋爵', '“于是，为了生活',
    '佣人——工钱', '“出租自己的劳动”', '“出租劳动材料”', '[XIII]“这种经济制度', '“一无所有者',
]
LABELS = [
    '舒尔茨论工资平均数', '收入与就业的持续性', '机器与劳动时间延长',
    '相对贫困与绝对贫困', '需要变化与福利比较', '劳动动物的经济学观念',
    '精神发展需要自由时间', '生产率与自然力', '生产率与精神活动余暇',
    '节省时间的分配', '五小时劳动与工厂持续劳动', '手工劳动分解与机器',
    '单调操作与工人死亡率', '自然力成为人的奴仆', '英国工厂男女就业',
    '女工就业与经济地位', '童工与机械改进', '成为资本家的劝告',
    '无产者依赖所有者', '不同劳动报酬名称', '出租劳动与代替劳动',
    '出租材料与雇用他人', '低贱职业与经济制度', '无所有者卖淫与捡破烂',
]
ROWS = rows('wages', 49, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(333, 337)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(257, 261)})
SUSPECTS = ['|Vin|', '||IX|', '||x|', 'Fabrik||Xl|arbeiter', 'Besei||XIl|tigung', '|xm|',
            'spe züische', 'spezüische', 'Vorbüdung', 'einträgücher', 'schneü', 'faüen',
            'zahüeichste', 'erwübt', 'freüich', 'AUein', 'Mülion', 'oberflächüchen', 'wül',
            'weü', 'Endüch', 'engüschen', 'gebüeben', 'Arbeitstbier', 'gemessen', 'Gemessen',
            'nachtheiügfür', 'Theüung', 'zahüeichere', 'Nachtheüe', 'Sterbüchkeit', 'wükenden',
            'seüi', 'männüche', 'Druden', 'weibüchen', 'SteUung', 'endüch', 'Freiüch',
            'wüken', 'aUe', 'aUmähüge', 'AUeüi', 'Capitaüsten', 'SchulzBew.']
DOUBTS = {f'{s}_de_{n:03}': [w for w in SUSPECTS if w in de]
          for s, n, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                           reported_reading='页内标记或界符待核',
                           note='按来源可见形式保留，含词内标记；未据译文改写。')
                   for w in words if '|' in w} for uid, words in DOUBTS.items()}
ROW_NOTES = {f'wages_{n:03}': ('本组位于舒尔茨摘引范围；保留底本引号和引文来源。'
                             if n <= 66 else '本组位于贝魁尔摘引范围；德方保留原法文，语言字段仍为德文底本主读栏。')
             for n in range(49, 73)}
ROW_NOTES['wages_054'] = '本组为引文间的正文评述，保留与周边舒尔茨摘引的界限。'

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=34, release='0.4.0-alpha30',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         row_notes=ROW_NOTES, coverage_notes={'wages':
             '节首连续72句群，至德印刷336/中文235贝魁尔摘引“捡破烂者”处；劳顿摘引及余文待续。'})
