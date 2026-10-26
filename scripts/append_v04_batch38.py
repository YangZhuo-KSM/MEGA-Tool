"""Batch 38: profit 049--072, competition and large/small capitals."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(342, 39, 42), (343, 2, 42), (344, 2, 42), (345, 2, 22)], {
    # The shared line-number filter also strips this literal quantity at a page start.
    # Restore the scan's twenty grocers, not a marginal line number.
    343: [('||Vl| getheilt', '20 ||Vl| getheilt')],
}, join_page_hyphens=True)
ZH = stream('zh_collected', [(267, 26, 29), (268, 2, 26), (269, 2, 24), (270, 2, 19)], {
    267: [(';', '；'), ('。”(', '。”（')],
    268: [('373页)', '373页）'), (';', '；'), ('201页)', '201页）'), ('提髙', '提高'),
          ('<9', '69'), ('时候,', '时候，'), ('资本--般', '资本一般'), ('不谈,', '不谈，'),
          ('探吋', '探讨'), ('‘‘', '“'), ('因此,', '因此，')],
    269: [('。”(', '。”（'), ('斯密.', '斯密，'), ('196U97页〉', '196、197页）'),
          (':', '：'), ('325页)', '325页）'), ('呢?', '呢？'), ('増', '增'), ('（1)', '（1）'),
          ('（2)', '（2）'), ('(2)', '（2）'), (';', '；'), ('位置(营业)', '位置（营业）'),
          ('髙', '高'), ('対工人', '对工人')],
    270: [('降低.•/’', '降低。”'), ('斯密.', '斯密，'), ('增长.', '增长，'), ('而旦', '而且'),
          ('髙', '高'), (':', '：'), ('第⑽页', '第189页'), ('沩造', '伪造')],
})
DE_STARTS = [
    '„Wenn ζ. B.', 'Da wir nun schon wissen', 'AUeüi die Concurrenz', 'Die Entstehung vieler',
    'Die Concurrenz unter den', 'Die Accumulation, welche', 'Wü haben gehört', '|VIIl| Hienach',
    'Mit der Vermehrung der Capitaüen', 'Die Vermehrung der Capitaüen', '„In einem Lande',
    'Dieser Zustand', '„Die Proportion', 'Wie steht es nun', '„Mit der Vermehrung der Capitalien',
    'Der kleine Capitalist', 'Will dagegen', 'Ferner: Der grosse', 'Wenn aber der Fall',
    '„Damit, daß', '„Je mehr Reichthum', 'Wenn also diesem', 'In dieser Concurrenz', '|X| Ein wichtiger',
]
ZH_STARTS = [
    '“例如，一个城市', '既然我们已经知道', '但是，只有当资本', '只有通过多方面',
    '资本之间的竞争', '在私有制的统治下', '我们已经听说', '[VIII]由此可见',
    '随着资本的增长', '资本增长为大量', '“在财富达到', '这种状态', '“资本总额',
    '在这种日益扩大的', '“随着资本的增加', '因此，小资本家', '相反，如果大资本家',
    '其次，大资本家', '但是，如果说货币利息', '“随着使用资本', '“财富、工业',
    '如果像在所设想', '在这种竞争中', '[X]此外',
]
LABELS = [
    '杂货商人数与竞争', '竞争抵制垄断资本', '竞争需要资本分散', '多方面积累转为单方面积累',
    '竞争扩大资本积累', '私有制与资本集中', '资本规模与积累速度', '大资本积累更快',
    '利润下降与小资本家', '资本增长的财富前提', '低利润率与中等财产者', '国民经济学偏爱的状态',
    '资本收入与勤劳懒惰', '竞争中的资本使用问题', '资本增加利息下降与工资上涨',
    '小资本家的选择', '大资本排挤小资本', '批量进货与低价销售', '企业资本增加与利息下降',
    '使用资本的利润与价格', '财富增长与资本增殖', '小资本被大资本压垮',
    '竞争与商品质量低劣', '固定资本和流动资本的比例',
]
ROWS = rows('profit', 49, LABELS, DE, ZH, DE_STARTS, ZH_STARTS)
PRINTED = {('de_megai2', p): str(p) for p in range(342, 346)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in range(267, 271)})
SUSPECTS = ['ζ.', '||Vl|', 'Capitaüsten', 'wükt', 'consumnürenden', 'AUeüi', 'mögüch',
            'Capitaüen', 'natürüche', 'Wü', 'absichtüchen', 'accumuürt', 'semer', 'schneüer',
            '|VIIl|', 'wü', 'Capitaüst', 'gewöhnüche', 'ügend', 'interessüen', 'Verrriehrung',
            '||ΓΧ|', 'accumulili', '|X|']
DOUBTS = {f'{s}_de_{n:03}': [w for w in SUSPECTS if w in de] for s, n, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                          reported_reading='底本标记字形待复核',
                          note='扫描可见标记照录；罗马数字与界符转写保留待审。')
                  for w in words if '|' in w or w == 'ζ.'}
             for uid, words in DOUBTS.items()}
OVERRIDES['profit_de_049']['||Vl|']['evidence_pages'] = ['de_megai2:343']

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=38, release='0.4.0-alpha34',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES)
