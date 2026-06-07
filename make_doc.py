# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# 既定フォント（日本語）
style = doc.styles['Normal']
style.font.name = 'Yu Gothic'
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Yu Gothic')

NAVY = RGBColor(0x1F, 0x3B, 0x5C)
GREEN = RGBColor(0x2E, 0x7D, 0x32)

def set_jp_font(run, name='Yu Gothic', size=None, bold=None, color=None):
    run.font.name = name
    r = run._element
    r.rPr.rFonts.set(qn('w:eastAsia'), name)
    if size: run.font.size = Pt(size)
    if bold is not None: run.font.bold = bold
    if color is not None: run.font.color.rgb = color

def heading(text, size=13, color=NAVY, space_before=10, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    set_jp_font(run, size=size, bold=True, color=color)
    return p

def body(text, size=10.5, bold=False, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    if indent: p.paragraph_format.left_indent = Cm(indent)
    run = p.add_run(text)
    set_jp_font(run, size=size, bold=bold)
    return p

def bullet(text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    if level: p.paragraph_format.left_indent = Cm(0.75 + level*0.75)
    run = p.add_run(text)
    set_jp_font(run, size=10.5)
    return p

# ===== タイトル =====
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('仲町台店　売場改善コンサルティング提案書')
set_jp_font(r, size=18, bold=True, color=NAVY)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('～ 弁当依存からの脱却と時間帯別売場の立て直し ～')
set_jp_font(r, size=11, bold=False, color=GREEN)

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = info.add_run('原案：仲町台店　小泉店長　／　ブラッシュアップ版　　作成日：2026年6月7日')
set_jp_font(r, size=9)

doc.add_paragraph()

# ===== 0. 全体方針 =====
heading('■ 全体方針')
body('沈んでいる弁当を無理に伸ばす方向ではなく、獅子ヶ谷店の成功パターン（弁当を絞り、'
     'チルド弁当・調理麺の売場を拡大する）を仲町台店へ横展開する。'
     '「勝ち筋に乗せる」判断を軸に、時間帯別（朝帯・夜帯）の立て直しと発注精度の向上を並行して進める。')

# ===== 1 =====
heading('1. 基本方針：弁当 → チルド弁当・調理麺へのシフト')
body('原案（小泉店長）：沈む弁当を伸ばすのではなく、獅子ヶ谷のように弁当を縮め、'
     'チルド弁当・調理麺の売場を伸ばす。', bold=True)
body('【ブラッシュアップ・追記】')
bullet('「縮める」前に根拠数値を取る。弁当の時間帯別販売数・廃棄数・売価値入を1～2週間ログ化し、削る分類・フェイスを数字で決定する（感覚で減らすと欠品クレーム→客離れになりやすい）。')
bullet('置き換え後の売場割（什器の段数）を先に図面化する。弁当を◯フェイス減らし、チルド弁当◯／調理麺◯へ振り替える棚割を確定してから発注を動かす。')
bullet('獅子ヶ谷との差分を確認する。客層・立地（仲町台＝住宅＋通勤客、駅近）の違いを踏まえ、丸コピーではなくチルドの構成比を仲町台向けに微調整する。')

# ===== 2 =====
heading('2. 朝帯の立て直し')
body('原案（小泉店長）：おにぎり・サンド等のアイテム見直し、売場拡充、フェイスアップの徹底。'
     'ブリトーセール等を活用し朝の販売を伸ばす。レジ前でプライチの小物チョコ等を展開しプラスワンを目指す。'
     'フライヤーの品揃え確認。', bold=True)
body('【ブラッシュアップ・追記】')
bullet('フェイスアップを時間帯ルール化する。朝ピーク前（例 6:30／7:30／8:30）の前出し・補充を時間指定でルーティン化し、作業割当表に落とす。')
bullet('プラスワン施策を具体化する。レジ前プライチ（小物チョコ等）に加え、コーヒー＋ベーカリー／おにぎり＋汁物のセット声掛けを実施。コーヒーマシン稼働率は朝の客単価に直結する。')
bullet('ホットスナックは「焼き上がり・温め完了時刻の見える化」。朝ピークに合わせて逆算し、POP（焼きたて時刻）で誘導する。')
bullet('欠品ゼロを最優先。朝の欠品はそのまま売上ロス。主力おにぎり・サンドの基準在庫を引き上げ、朝便基準で発注を見直す。')

# ===== 3 =====
heading('3. 夜帯の立て直し')
body('原案（小泉店長）：フライヤーの拡充。揚げ止め時間の確認と、その時の品揃え。'
     'デイリー（チル弁・麺類・サラダ・惣菜）の品揃え数の見直し。セールがあれば上手に活用する。', bold=True)
body('【ブラッシュアップ・追記】')
bullet('揚げ止め時間の確認に加え、閉店◯時間前から売れ筋2～3品に絞って揚げるルールにする。廃棄を抑えつつ品切れ感を出さない。')
bullet('デイリーは「単品大量」より「少量多品目」で見切り前提の構成に。値引き（見切り）開始時間とルールを明文化し、廃棄前に売り切る。')
bullet('夜の客層（仕事帰りの夕食まとめ買い）に合わせ、惣菜＋主食＋一品（サラダ・汁物）の関連陳列を行う。')

# ===== 4 =====
heading('4. 廃棄・発注の見直し（曜日別対策）')
body('原案（小泉店長）：①月曜日の廃棄＝土日の発注を見直し、値引きのタイミングを早める。'
     '②木曜日の廃棄＝新規商品の影響か？　残り具合を見て値引きタイミングを考える。', bold=True)
body('【ブラッシュアップ・追記】')
bullet('曜日別の発注カーブを作る。曜日別・時間帯別の販売実績で発注基準値を分ける（住宅地寄りなら土日の買われ方が平日と別物になりやすい）。')
bullet('月曜の廃棄が多い主因は土曜夜～日曜の発注過多。土曜最終便・日曜朝便の数量を実績ベースで再設定する。ただし日曜を絞りすぎると月曜朝が品薄になるため、両端をセットで管理する。')
bullet('値引き（見切り）のタイミングを早める基準を時刻で明文化する（例：閉店◯時間前で◯％）。担当者の判断任せにせず、誰がやっても同じ動きになるようにする。')
bullet('木曜の廃棄は新規商品の動きを単品で検証する。導入週の販売実績を1～2週分追い、「定着しない新規」は発注数を絞るか早めの見切りに切り替える。新規の山と既存商品の発注が重なって過多にならないよう調整する。')

# ===== 5 フライヤー声掛け =====
heading('5. フライヤー販売の強化（声掛けの仕組み化）')
body('原案（小泉店長）：フライヤーの販売をもっと伸ばす。セール時はもちろん、新規商品の時も'
     'いかに声掛けができるか。主体者が先頭に立って声掛けをし、スタッフも声掛けできるようにする。', bold=True)
body('【ブラッシュアップ・追記】')
bullet('主体者（店長・社員）が先頭で声掛けの「お手本」を見せ、トークの型（ひと言フレーズ）を決めてクルーに共有する。誰でも言える短い言葉にするのが定着のコツ。')
bullet('声掛けのタイミングをルール化する。揚げたて直後・レジ会計時・ピーク前など「いつ声を掛けるか」を作業の中に組み込む。')
bullet('新規商品は導入初週が勝負。POP＋試食的アピール＋声掛けをセットで実施し、立ち上がりを早める。')
bullet('結果を見える化する。フライヤーの日別販売数を掲示し、声掛け強化日と通常日の差をクルーと共有してモチベーションにつなげる。')

# ===== 6 追加提案 =====
heading('6. 全体への追加提案（実行マネジメント）')
bullet('優先順位と期限を付ける：①朝帯 → ②弁当シフト → ③夜帯 → ④発注精度の順で、各2週間スパンで着手する（4テーマ同時着手は現場が回らない）。')
bullet('数値目標（KPI）を1つずつ設定：朝帯売上前年比／チルド弁当＋調理麺の売上構成比／デイリー廃棄率／客単価。「やった・やってない」でなく数字で振り返る。')
bullet('作業の標準化：フェイスアップ・揚げ止め・見切りはすべて「誰が・いつ・何を」の作業割当に落とし込み定着させる。')
bullet('クルー共有：方針を朝礼やノートで全クルーに周知する。特に「弁当を絞る理由」は欠品クレーム対応のためにも全員で共有する。')

# ===== KPI表 =====
heading('7. KPI管理表（記入例）')
table = doc.add_table(rows=1, cols=4)
table.style = 'Light Grid Accent 1'
hdr = table.rows[0].cells
heads = ['項目', '指標(KPI)', '現状', '目標']
for c, h in zip(hdr, heads):
    para = c.paragraphs[0]
    run = para.add_run(h)
    set_jp_font(run, size=10, bold=True)
rows = [
    ['朝帯', '朝帯売上 前年比', '', '＋％'],
    ['売場シフト', 'チルド弁当＋調理麺 構成比', '', '％'],
    ['夜帯', 'デイリー廃棄率', '', '％以下'],
    ['廃棄', '月・木曜の廃棄金額', '', '円以下'],
    ['フライヤー', '日別販売数', '', '個'],
    ['全体', '客単価', '', '円'],
]
for rd in rows:
    cells = table.add_row().cells
    for c, v in zip(cells, rd):
        run = c.paragraphs[0].add_run(v)
        set_jp_font(run, size=10)

doc.save('/home/user/ai-clean-systems/仲町台店_コンサル提案書.docx')
print('saved')
