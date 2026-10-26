"""Batch 35: wages 073-096, through its source-visible section ending."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(336, 24, 42), (337, 2, 42), (338, 2, 22)], join_page_hyphens=True)
ZH = stream('zh_collected', [(260, 18, 29), (261, 2, 24), (262, 2, 21)], {
    260: [('查•劳顿', '查·劳顿'), ('<人口等问题的解决办法〉（1842年巴黎版)68—书',
          '《人口等问题的解决办法》（1842年巴黎版）⁶⁸一书'),
          ('保持6万这个数目', '保持6—7万这个数目'), ('平均要有丁考•，', '平均要有一名；'),
          ("('同°上", '（同上'), (',', '，'), ('((在英格兰', '（《在英格兰')],
    261: [('公布的关于爱尔兰的调查摘要>,1840年维也纳版）。"', '公布的关于爱尔兰的调查摘要》，1840年维也纳版）。”'),
          ('〈论贫困〉', '《论贫困》'), ('第36、37页)', '第36、37页）'), ('物•，', '物；'),
          (';', '；'), ('竞争‘••…', '竞争……'), (',', '，'), ('沩装', '伪装'), ('码?', '吗？'),
          ('呢？"', '呢？”'), ('页〉', '页）'), ('出OOOOO', '出'), ('。”(同上', '。”（同上'),
          ('人”0(同', '人”。（同'), ('醏博', '赌博')],
    262: [('）"这些利益〈即经济利益〉', '）“这些利益（即经济利益）'), ('力景', '力量'),
          ('平衡:', '平衡：'), ('按照科学的意见，等學是获得和平的惟一手段',
          '按照科学的意见，连绵不断的战争是获得和平的惟一手段'),
          (';', '；'), ('这种战争就叫作竞争，（同上，第23页°)°00000',
          '这种战争就叫作竞争。”（同上，第23页）'),
          ('凋集', '调集'), ('忠诚.', '忠诚，'), ('抛宑', '抛弃'),
          ('有些1:人毎天', '有些工人每天'), (',', '，'), ('调査', '调查'),
          ('短期內', '短期内'), ('劳动人口/(同上', '劳动人口。”（同上')],
})
DE_STARTS = [
    'Ch. Loudon', '«La moyenne vie', 'De manière', '«la population des misérables',
    "En 1821 la population", 'Die Nationalökonomie betrachtet',
    '« La population ouvrière', "«Pourquoi donc", 'Die grossen Ateüers',
    '« le travaüleur', 'La valeur du travaü', "Le travaü n'est susceptible",
    "||xrv| Le travail c'est", "Pour que la vie", 'Wenn die Arbeit also',
    'Das jetzige ökonomische', "«L'industrie est devenue", 'Les machines à',
    'Die Industrie befand', '« Ces intérêts', 'Der industrieüe Krieg',
    'Diese Völkerschaften', 'Je mehr die Arbeit', '|XV| «Nous avons',
]
ZH_STARTS = [
    '查·劳顿', '“这些不幸的马路天使', '因此，要使卖淫者保持', '“贫困的人口',
    '1821年爱尔兰', '国民经济学抽象地', '“出卖劳动的工人人口', '“为什么人们',
    '大工场宁可', '“工人在雇用', '如果劳动不是', '与真正的[商品]不同',
    '[XIV]劳动就是生命', '为了使人的生命', '可见，如果劳动', '现在的经济制度',
    '“工业成了战争', '单是加工棉花的机器', '工业直到现在', '“这些利益',
    '工业战争为了', '这些日益密集的工人', '加在他们身上的劳动', '[XV]“我们确信',
]
LABELS = [
    '劳顿的卖淫人数摘录', '卖淫者的平均寿命摘录', '死亡与持续补给的估算',
    '贫困人口与争夺生存', '爱尔兰人口增长比较', '劳动作为商品的经济学观念',
    '劳动商品理论与奴役', '劳动何以只被看作交换价值', '大工场选择妇女儿童劳动',
    '劳动买卖双方的自由差异', '不被出售的劳动失去价值', '劳动不能积累或储蓄',
    '劳动生命与食物交换', '生命商品化与奴隶制', '劳动商品的最不幸特性',
    '经济制度与工人和人的差别', '工业战争与商业赌博', '棉纺机器与手工劳动量',
    '工业的征服战争状态', '竞争作为持续战争', '工业军队与饥饿约束',
    '受雇保障与出卖力气', '长时间劳动与生存权利', '工业城市对农村人口的补给',
]
ROWS = rows('wages', 73, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(336, 339)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(260, 263)})
SUSPECTS = ['Heu', '14p', 'travaü', 'theüs', 'est-eUe', 'avoü', 'Ateüers', 'weü',
            'travaüleur', "s'ü", '||xrv|', 'ü', 'eme', 'unglückseeügsten', 'travaüler',
            'allem', 'eile', 'nécessaüement', 'üs', 'victoüe', 'équUibre', 'eUe',
            'obtenu', "s'appeUe", 'industrieüe', 'zahüeiche', 'reichheh', 'decimüen',
            'löstündiger', '|XV|', 'p.68,69.(']
DOUBTS = {f'{s}_de_{n:03}': [w for w in SUSPECTS if w in de]
          for s, n, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                           reported_reading='页内标记转写待复核', note='词内或页内标记照录，保留待审。')
                   for w in words if '|' in w} for uid, words in DOUBTS.items()}
ROW_NOTES = {f'wages_{n:03}': ('本组处于劳顿摘引范围，原始统计按底本保留。'
                             if n <= 75 else '本组处于比雷摘引及其周边评述范围，德方保留底本法文；摘引归属与中文来源注明。')
             for n in range(73, 97)}

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=35, release='0.4.0-alpha31',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         row_notes=ROW_NOTES, coverage_notes={'wages':
             '已从节首连续收录96句群至德印刷338/中文237节尾；首尾、衔接和注释的集中审计仍待完成，全文分母未登记。'})
