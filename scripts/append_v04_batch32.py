"""Batch 32: wages opening, including the genuine Chinese illustration gap."""
from append_v04_batch6 import main
from source_slices import rows, stream

DE = stream('de_megai2', [(327, 4, 31), (328, 2, 42), (329, 2, 42), (330, 2, 42)],
            {329: [('o fortschreitet', 'fortschreitet')]}, join_page_hyphens=True)
ZH = stream('zh_collected', [(248, 4, 20), (249, 2, 26), (252, 2, 23),
                             (253, 2, 24), (254, 2, 23)], {
    248: [('养家湖口', '养家糊口'), ('“普通人即', '“普通人”⁶⁴即')],
    249: [(',', '，'), ('傾向', '倾向'), ('鼉大的', '最大的'), ('束溥', '束缚'),
          ('屈脤', '屈服'), (';', '；'), ('这样:', '这样：'), ('提髙', '提高')],
    252: [('步于', '步子'), ('廉利', '赢利'), ('(1)', '（1）'),
          ('®', '①'), ('[111](2)', '[III]（2）'), ('提髙', '提高'), (',', '，')],
    253: [('悄况', '情况'), ('才可能:（《)', '才可能：（α）'),
          ('①•，就是说', '①，就是说'),
          ('芏人', '工人'), ('（ß)', '（β）'), ('(7)', '（γ）'),
          ('~部分', '一部分'), (';', '；'), (',', '，')],
    254: [('提髙', '提高'), (';', '；'), ('増', '增'), (',', '，'), ('(3广', '（3）“')],
})
DE_STARTS = [
    '|l| Arbeitslohn.', 'Für d[en] Arbeiter also', 'Die niedrigste',
    'Die Nachfrage nach Menschen', 'Ueberbietet die Quantität', 'Bei der Gravitation',
    '|Π| Die zufälligen', 'Der Arbeiter braucht nicht', 'Ferner: Die Arbeitspreisse',
    'Ein andrer Nachtheil', 'Ueberhaupt ist zu bemerken', 'Der Arbeiter muß nicht nur',
    'Nehmen wir die 3', '1) Ist der Reichthum', '|lll| 2) Nehmen',
    'Einmal: Die Erhöhung', 'Dabei kürzen', 'Ferner: Wann befindet',
    'ß) Die Häufung', '7) In einer Gesellschaft', 'Also selbst in dem Zustand',
    '|V| Die Erhöhung', 'Das sind die Folgen', 'Endlich aber muß',
]
ZH_STARTS = [
    '[I]工资决定于', '因此，资本、地租和劳动', '最低的和惟一必要的',
    '对人的需求必然', '如果供给的量超过需求', '因此，当市场价格',
    '[II]市场价格', '当资本家赢利时', '其次，劳动价格', '工人还有一个不利的方面',
    '总之，应当看到', '工人不仅必须', '我们列举社会', '（1）如果社会财富',
    '[III]（2）现在', '首先，工资的提高', '这就缩短了工人的寿命',
    '其次，社会在什么时候', '（β）资本的积累', '（γ）在福利增长',
    '由此可见，即使在对工人', '[V]工资的提高', '这就是对工人最有利', '然而说到底',
]
LABELS = [
    '工资与资本工人的斗争', '三者分离对工人的后果', '最低工资与生存',
    '人的需求与工人商品化', '供求和自然价格', '资本流动与工人损失',
    '市场波动对工资的影响', '资本家盈亏与工人', '工资和生活资料价格',
    '劳动价格的行业差别', '生存与资本收益的差别', '谋求工作本身的斗争',
    '社会的三种主要状态', '财富衰落中的工人', '财富增长中的工人',
    '工资提高与过度劳动', '工人寿命与劳动力补给', '财富增长与积累劳动',
    '资本积累分工和机器劳动', '资本集中与资本家转为工人', '有利社会状态的后果',
    '工资提高分工和生产过剩', '增长财富的后果', '财富顶点的工人处境问题',
]
ROWS = rows('wages', 1, LABELS, DE, ZH, DE_STARTS, ZH_STARTS,
            de_end='3) „In einem Land', zh_end='（3）“在财富')
PRINTED = {('de_megai2', p): str(p) for p in range(327, 331)}
PRINTED.update({('zh_collected', p): str(p - 25) for p in [248, 249, 252, 253, 254]})
NEW_SECTIONS = [dict(id='wages', title='工资', work='1844年经济学哲学手稿',
                     manuscript='第一手稿', aliases=['Arbeitslohn'], coverage='首批24句群')]
EXTRA = [dict(source_id='zh_collected', pdf_page=p, printed_page=None, page_kind=kind,
              status='scan_checked_ai', checked_by='Codex', checked_at='2026-10-19', note=note)
         for p, kind, note in [
             (250, 'illustration', '已查看：笔记本I第1页手稿影印及图题，无可见印刷页码；不推算为225。'),
             (251, 'blank', '已查看：无正文、图题和印刷页码，仅纸面和扫描边缘；不推算为226。')]]
SUSPECTS = ['|l|', '|Π|', '|lll|', '||lV|', '|V|', 'Capitaüsten', 'Capitaüst',
            'industrieüe', 'Vortheüe', 'Capitalüiteresse', 'aüeüi', 'wesentüche',
            'schädüche', 'Famüie', 'Theü', 'redueirt', 'gravitili', 'Centraipunkt',
            'desMarktpreisseszum', 'verwirkHchen', 'woüen', 'voüständig', 'aüer',
            'voUziehn', 'weü', 'wüd', 'GeseUschaft', 'Capitaüen', 'semen',
            'Theüung', 'rem', 'aUen', 'SteUung', '7)', "mit'"]
DOUBTS = {f'{section}_de_{number:03}': [w for w in SUSPECTS if w in de]
          for section, number, _, de, *_ in ROWS}
OVERRIDES = {uid: {w: dict(kind='glyph_doubt', status='open',
                           reported_reading='底本界符或分项字形待定向复核',
                           note='保留扫描当前形式；不按译文统一字形。')
                   for w in words if '|' in w or w == '7)'} for uid, words in DOUBTS.items()}

if __name__ == '__main__':
    assert len(ROWS) == 24
    main(rows=ROWS, printed=PRINTED, batch=32, release='0.4.0-alpha28',
         reviewed_date='2026-10-19', doubts=DOUBTS, issue_overrides=OVERRIDES,
         new_sections=NEW_SECTIONS, coverage_updates={'wages': ['wages']}, extra_page_maps=EXTRA,
         coverage_notes={'wages': '节首连续24句群，德印刷327—330/中文223—224、227—229；正文待续。中文PDF250插图、251空白已分别登记。'})
