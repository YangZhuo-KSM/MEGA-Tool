"""Batch 36: first 24 groups of the profit-of-capital section."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(338, 23, 39), (339, 3, 43), (340, 2, 32)], join_page_hyphens=True)
ZH = stream('zh_collected', [(263, 2, 17), (264, 2, 23), (265, 2, 23)], {
    263: [('[I]—、资本', '[I]一、资本'), ('(1)', '（1）'), ('。”(萨伊', '。”（萨伊'),
          ('所有者7', '所有者？'), ('的-•切产品', '的一切产品')],
    264: [('鈎买', '购买'), ('页）OOOOO', '页）'), ('(2)', '（2）'), ('第191页)', '第191页）'),
          ('嬴利', '赢利'), ('一样的、其次', '一样的。其次'), ('比例/’', '比例。”'), ('蓣付', '预付')],
    265: [('179,180', '179、180'), ('稍确', '精确'), (';', '；'), ('第180、181页)', '第180、181页）'),
          ('含理', '合理'), ('最髙', '最高'), ('除丁', '除了'), ('剰余', '剩余'),
          ('惰况', '情况'), ('[III]最Ä的', '[III]最高的'), ('仅眵', '仅够'), ('湖口', '糊口'), (',', '，')],
})
DE_STARTS = [
    '|l| Gewinn des Capitals.', '„Wenn das Capital selbst', 'Wie wird man Proprietair',
    'Durch das positive Recht', 'Was erwirbt man', '„Einer, der', 'Das Capital ist also',
    'Wir werden später sehn', 'Was ist das Capital?', '«Une certaine quantité',
    'Capital ist aufgespeicherte', '2) fonds, Stock', '2) Der Gewinn des Capitals.',
    'Warum verlangt der Capitalist', 'Er hätte kern Interesse', 'Der Capitalist zieht also',
    'Welches Verhältniß hat nun', 'Wenn es schon schwer', 'So unmöglich es nun ist',
    'Die Proportion, welche', 'Welches ist die niedrigste', 'Die niedrigste Taxe',
    '|lll| Die höchste Taxe', 'Ausser allen Vortheilen',
]
ZH_STARTS = [
    '资本的利润[I]一、资本', '“尽管资本本身', '人怎样成为生产基金', '根据实在法',
    '人们依靠资本', '“例如，继承了大宗财产', '因此，资本是对劳动', '下面我们首先将看到',
    '什么是资本？', '“一定量的积蓄', '资本是积蓄的劳动', '（2）基金，资金',
    '二、资本的利润', '为什么资本家要求', '如果资本家从出卖工人', '因此，资本家赚得',
    '利润和资本的比例', '如果说确定一定地点', '尽管精确地确定', '通常的利息率',
    '什么是最低的利润率', '资本的最低的普通利润率', '[III]最高的普通利润率', '资本家除了',
]
LABELS = [
    '资本私有权的基础问题', '继承与立法', '生产基金与产品所有权', '实在法的回答',
    '继承财产获得什么权力', '财富赋予购买和控制权', '资本对劳动及产品的支配',
    '资本家支配劳动与资本支配资本家', '什么是资本', '积蓄和储存的劳动', '资本是积蓄劳动',
    '基金成为资本的条件', '资本利润与监督劳动', '利润为何与资本成比例', '雇用劳动的资本动机',
    '工资与预付原料上的利润', '追问利润与资本比例', '利润日常波动的原因',
    '以货币利息判断利润', '利息率与纯利润率', '最低和最高利润率问题', '最低普通利润率',
    '最高普通利润率与工资地租', '竞争小与高于自然价格',
]
ROWS = rows('profit', 1, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(338, 341)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(263, 266)})
NEW_SECTIONS = [dict(id='profit', title='资本的利润', work='1844年经济学哲学手稿',
                     manuscript='第一手稿', aliases=['Gewinn des Capitals', 'Gewinn des Kapitals'],
                     coverage='节首连续24句群')]
SUSPECTS = ['|l|', 'ζ.', 'Capitaüst', 'Capitaüsten', 'travaü', 'Π', 'Manuf acturarbeit',
            'Düektion', 'Capitaüen', 'Verhältruß', '||ll|', 'kern', 'avancüten', 'eme',
            'Salaüe', '|lll|']
DOUBTS = {f'{s}_de_{n:03}': [w for w in SUSPECTS if w in de]
          for s, n, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                           reported_reading='底本位置标记或字形待复核',
                           note='扫描可见形式照录；不据译文或常用引文统一。')
                   for w in words if '|' in w or w in ('ζ.', 'Π')}
             for uid, words in DOUBTS.items()}

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=36, release='0.4.0-alpha32',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         new_sections=NEW_SECTIONS, coverage_updates={'profit': ['profit']},
         coverage_notes={'profit': '节首连续24句群，德印刷338—340/中文238—240，停在市场价高于自然价的引入句末；商业秘密等后文待续。'})
