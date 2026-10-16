# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ページ余白を少し狭めて広く使う
for s in doc.sections:
    s.left_margin = Cm(1.8); s.right_margin = Cm(1.8)
    s.top_margin = Cm(1.5); s.bottom_margin = Cm(1.5)

# 既定フォント
style = doc.styles['Normal']
style.font.name = 'Yu Gothic'
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Yu Gothic')

# ===== カラーパレット =====
NAVY   = '1F3B5C'
BLUE   = '2E5E8C'
GREEN  = '2E7D32'
LGREEN = 'E6F4EA'   # 追記ボックス背景
LGRAY  = 'EEF1F5'   # 原案ボックス背景
LBLUE  = 'DDE8F3'   # ステップ背景
ORANGE = 'E8821E'
WHITE  = 'FFFFFF'
LINE   = 'C9D3DF'

def H(hexstr):
    return RGBColor.from_string(hexstr)

def set_font(run, name='Yu Gothic', size=None, bold=None, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if size is not None: run.font.size = Pt(size)
    if bold is not None: run.font.bold = bold
    if color is not None: run.font.color.rgb = H(color)

def shade(el, hexcolor):
    """段落 or セルの背景塗り"""
    pr = el.get_or_add_tcPr() if el.tag.endswith('}tc') else el.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hexcolor)
    pr.append(shd)

def cell_shade(cell, hexcolor):
    shade(cell._tc, hexcolor)

def set_cell_borders(cell, color=LINE, sz=6):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz))
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), color)
        borders.append(e)
    tcPr.append(borders)

def no_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top','left','bottom','right','insideH','insideV'):
        e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'),'none')
        borders.append(e)
    tblPr.append(borders)

def cell_margins(cell, top=60, bottom=60, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement('w:tcMar')
    for k,v in (('top',top),('bottom',bottom),('start',left),('end',right)):
        e = OxmlElement(f'w:{k}'); e.set(qn('w:w'), str(v)); e.set(qn('w:type'),'dxa')
        m.append(e)
    tcPr.append(m)

def p_run(cell, text, size=10.5, bold=False, color=None, align=None,
          space_after=0, space_before=0, first=True):
    p = cell.paragraphs[0] if (first and not cell.paragraphs[0].runs) else cell.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    if align: p.alignment = align
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, color=color)
    return p

def spacer(pts=6):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(''); set_font(run, size=pts)
    return p

# =========================================================
# タイトルバナー
# =========================================================
banner = doc.add_table(rows=1, cols=1)
banner.alignment = WD_TABLE_ALIGNMENT.CENTER
no_borders(banner)
c = banner.cell(0,0)
cell_shade(c, NAVY); cell_margins(c, top=200, bottom=200, left=200, right=200)
p_run(c, '仲町台店　売場改善コンサルティング提案書', size=20, bold=True,
      color=WHITE, align=WD_ALIGN_PARAGRAPH.CENTER, first=True)
p_run(c, '― 弁当依存からの脱却と、時間帯別売場の立て直し ―', size=11,
      color='C7D6E8', align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4)

info = doc.add_paragraph(); info.alignment = WD_ALIGN_PARAGRAPH.RIGHT
info.paragraph_format.space_before = Pt(4)
r = info.add_run('原案：仲町台店 小泉店長　／　ブラッシュアップ版　　作成日：2026年6月7日')
set_font(r, size=9, color='666666')

# =========================================================
# 全体方針（囲みボックス）
# =========================================================
spacer(4)
mb = doc.add_table(rows=1, cols=1); no_borders(mb)
c = mb.cell(0,0); cell_shade(c, LGRAY); set_cell_borders(c, color=NAVY, sz=4)
cell_margins(c, top=140, bottom=140, left=160, right=160)
p_run(c, '🎯 全体方針', size=12, bold=True, color=NAVY)
p_run(c, '沈んでいる弁当を無理に伸ばすのではなく、獅子ヶ谷店の成功パターン'
         '（弁当を絞り、チルド弁当・調理麺の売場を拡大）を仲町台店へ横展開する。'
         '「勝ち筋に乗せる」判断を軸に、時間帯別（朝帯・夜帯）の立て直しと'
         '発注精度の向上を並行して進める。', size=10.5, space_before=4)

# =========================================================
# セクション部品
# =========================================================
def section_bar(num, title, color=BLUE):
    spacer(6)
    t = doc.add_table(rows=1, cols=2); no_borders(t)
    t.columns[0].width = Cm(1.1); t.columns[1].width = Cm(16)
    # 番号バッジ
    cnum = t.cell(0,0); cell_shade(cnum, NAVY); cell_margins(cnum,40,40,40,40)
    cnum.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_run(cnum, str(num), size=14, bold=True, color=WHITE,
          align=WD_ALIGN_PARAGRAPH.CENTER)
    # タイトル
    ctit = t.cell(0,1); cell_shade(ctit, color); cell_margins(ctit,60,60,160,60)
    ctit.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_run(ctit, title, size=12.5, bold=True, color=WHITE)

def gensan_box(text):
    """店長原案ボックス"""
    t = doc.add_table(rows=1, cols=1); no_borders(t)
    c = t.cell(0,0); cell_shade(c, LGRAY); set_cell_borders(c, color=LINE, sz=4)
    cell_margins(c, top=80, bottom=80, left=160, right=140)
    p_run(c, '📋 店長原案', size=9.5, bold=True, color='555555')
    p_run(c, text, size=10.5, space_before=2)

def tsuiki_box(items):
    """追記・ブラッシュアップ ボックス（箇条書き）"""
    t = doc.add_table(rows=1, cols=1); no_borders(t)
    c = t.cell(0,0); cell_shade(c, LGREEN)
    set_cell_borders(c, color='B7DFC2', sz=4)
    cell_margins(c, top=80, bottom=80, left=160, right=140)
    p_run(c, '✨ 追記・ブラッシュアップ', size=9.5, bold=True, color=GREEN)
    for it in items:
        p = c.add_paragraph(); p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        run = p.add_run('▸ '); set_font(run, size=10.5, bold=True, color=GREEN)
        run2 = p.add_run(it); set_font(run2, size=10.5)

# =========================================================
# 1
# =========================================================
section_bar(1, '基本方針：弁当 → チルド弁当・調理麺へのシフト')
gensan_box('沈む弁当を伸ばすのではなく、獅子ヶ谷のように弁当を縮め、'
           'チルド弁当・調理麺の売場を伸ばす。')
tsuiki_box([
  '「縮める」前に根拠数値を取る。弁当の時間帯別販売数・廃棄数・売価値入を1～2週間ログ化し、削る分類・フェイスを数字で決定する。',
  '置き換え後の売場割（什器の段数）を先に図面化。弁当を◯フェイス減らし、チルド弁当◯／調理麺◯へ振り替える棚割を確定してから発注を動かす。',
  '獅子ヶ谷との差分を確認。立地（仲町台＝住宅＋通勤客・駅近）の違いを踏まえ、丸コピーせずチルド構成比を仲町台向けに微調整する。',
])

# =========================================================
# 2
# =========================================================
section_bar(2, '朝帯の立て直し', color=BLUE)
gensan_box('おにぎり・サンド等のアイテム見直し、売場拡充、フェイスアップの徹底。'
           'ブリトーセール等で朝の販売を伸ばす。レジ前でプライチの小物チョコ等を'
           '展開しプラスワンを目指す。フライヤーの品揃え確認。')
tsuiki_box([
  'フェイスアップを時間帯ルール化。朝ピーク前（例 6:30／7:30／8:30）の前出し・補充を時間指定でルーティン化し作業割当表へ。',
  'プラスワンを具体化。レジ前プライチに加え「コーヒー＋ベーカリー」「おにぎり＋汁物」のセット声掛け。コーヒーマシン稼働率は客単価に直結。',
  'ホットスナックは焼き上がり時刻を見える化。朝ピークに合わせ逆算し、POP（焼きたて時刻）で誘導。',
  '欠品ゼロを最優先。主力おにぎり・サンドの基準在庫を引き上げ、朝便基準で発注を見直す。',
])

# =========================================================
# 3
# =========================================================
section_bar(3, '夜帯の立て直し', color=BLUE)
gensan_box('フライヤーの拡充。揚げ止め時間の確認と、その時の品揃え。'
           'デイリー（チル弁・麺類・サラダ・惣菜）の品揃え数の見直し。'
           'セールがあれば上手に活用する。')
tsuiki_box([
  '揚げ止め時間の確認に加え、閉店◯時間前から売れ筋2～3品に絞って揚げる。廃棄を抑えつつ品切れ感を出さない。',
  'デイリーは「単品大量」より「少量多品目」で見切り前提の構成に。値引き開始時間とルールを明文化し廃棄前に売り切る。',
  '夜の客層（仕事帰りの夕食まとめ買い）に合わせ、惣菜＋主食＋一品（サラダ・汁物）の関連陳列を行う。',
])

# =========================================================
# 4
# =========================================================
section_bar(4, '廃棄・発注の見直し（曜日別対策）', color=ORANGE)
gensan_box('①月曜日の廃棄＝土日の発注を見直し、値引きのタイミングを早める。'
           '②木曜日の廃棄＝新規商品の影響か？　残り具合を見て値引きタイミングを考える。')
tsuiki_box([
  '曜日別の発注カーブを作る。曜日別・時間帯別の販売実績で発注基準値を分ける（土日の買われ方は平日と別物になりやすい）。',
  '月曜の廃棄の主因は土曜夜～日曜の発注過多。土曜最終便・日曜朝便の数量を実績ベースで再設定。絞りすぎて月曜朝が品薄にならないよう両端をセット管理。',
  '値引き（見切り）を早める基準を時刻で明文化（例：閉店◯時間前で◯％）。担当者の判断任せにしない。',
  '木曜の廃棄は新規商品を単品で検証。導入週の実績を1～2週追い、定着しない新規は発注を絞るか早めの見切りに切り替える。',
])

# =========================================================
# 5 フライヤー
# =========================================================
section_bar(5, 'フライヤー販売の強化（声掛けの仕組み化）', color=ORANGE)
gensan_box('フライヤーの販売をもっと伸ばす。セール時はもちろん、新規商品の時も'
           'いかに声掛けができるか。主体者が先頭に立って声掛けをし、'
           'スタッフも声掛けできるようにする。')
tsuiki_box([
  '主体者（店長・社員）が先頭で声掛けのお手本を見せ、トークの型（ひと言フレーズ）を決めてクルーへ共有。短い言葉が定着のコツ。',
  '声掛けのタイミングをルール化（揚げたて直後・レジ会計時・ピーク前など）し、作業の中に組み込む。',
  '新規商品は導入初週が勝負。POP＋アピール＋声掛けをセットで実施し立ち上がりを早める。',
  'フライヤーの日別販売数を掲示し、声掛け強化日と通常日の差をクルーと共有してモチベーションにつなげる。',
])

# =========================================================
# 6 実行ロードマップ（ビジュアル）
# =========================================================
section_bar(6, '実行ロードマップ（優先順位）', color=GREEN)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
r = p.add_run('4テーマ同時着手は現場が回らない。各2週間スパンで順に着手する。')
set_font(r, size=10.5)

steps = ['STEP1\n朝帯の\n立て直し', 'STEP2\n弁当→チルド\nへのシフト',
         'STEP3\n夜帯の\n立て直し', 'STEP4\n発注精度\n・廃棄削減']
road = doc.add_table(rows=1, cols=7); no_borders(road)
road.alignment = WD_TABLE_ALIGNMENT.CENTER
widths = [Cm(3.4), Cm(0.8)]*3 + [Cm(3.4)]
for i, w in enumerate(widths):
    road.columns[i].width = w
colseq = [GREEN, BLUE, BLUE, NAVY]
si = 0
for i in range(7):
    cell = road.cell(0,i)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    if i % 2 == 0:
        cell_shade(cell, colseq[si]); cell_margins(cell,60,60,40,40)
        for j, line in enumerate(steps[si].split('\n')):
            p_run(cell, line, size=(10 if j==0 else 11), bold=True, color=WHITE,
                  align=WD_ALIGN_PARAGRAPH.CENTER, first=(j==0),
                  space_after=0)
        si += 1
    else:
        p_run(cell, '➜', size=16, bold=True, color='999999',
              align=WD_ALIGN_PARAGRAPH.CENTER)

# =========================================================
# 7 KPI表
# =========================================================
section_bar(7, 'KPI管理表（記入例）', color=GREEN)
table = doc.add_table(rows=1, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
heads = ['項目', '指標（KPI）', '現状', '目標']
hw = [Cm(2.6), Cm(7.2), Cm(2.8), Cm(3.0)]
for i,w in enumerate(hw): table.columns[i].width = w
for c, h in zip(table.rows[0].cells, heads):
    cell_shade(c, NAVY); set_cell_borders(c, color=WHITE, sz=4)
    cell_margins(c,50,50,100,100)
    p_run(c, h, size=10, bold=True, color=WHITE)
rows = [
    ['朝帯', '朝帯売上　前年比', '', '＋　％'],
    ['売場シフト', 'チルド弁当＋調理麺　売上構成比', '', '　％'],
    ['夜帯', 'デイリー廃棄率', '', '　％以下'],
    ['廃棄', '月・木曜の廃棄金額', '', '　円以下'],
    ['フライヤー', '日別販売数', '', '　個'],
    ['全体', '客単価', '', '　円'],
]
for ri, rd in enumerate(rows):
    cells = table.add_row().cells
    bg = 'FFFFFF' if ri % 2 == 0 else 'F2F6FA'
    for ci,(c, v) in enumerate(zip(cells, rd)):
        cell_shade(c, bg); set_cell_borders(c, color=LINE, sz=4)
        cell_margins(c,50,50,100,100)
        p_run(c, v, size=10, bold=(ci==0),
              color=(NAVY if ci==0 else None))

# =========================================================
# フッター注記
# =========================================================
spacer(6)
fb = doc.add_table(rows=1, cols=1); no_borders(fb)
c = fb.cell(0,0); cell_shade(c, LBLUE); cell_margins(c,80,80,160,160)
p_run(c, '💡 運用のポイント', size=10, bold=True, color=NAVY)
p_run(c, '「やった／やってない」ではなく数字で振り返る。'
         'フェイスアップ・揚げ止め・見切り・声掛けはすべて'
         '「誰が・いつ・何を」の作業割当に落とし込み、朝礼やノートで全クルーに共有して定着させる。',
      size=10, space_before=2)

doc.save('/home/user/ai-clean-systems/仲町台店_コンサル提案書.docx')
print('saved')
