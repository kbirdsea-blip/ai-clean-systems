# Ai Clean Systems コーポレートサイト

清掃・特殊清掃・高圧洗浄（横浜・神奈川全域）のコーポレートサイト。
単一HTML（`index.html`）で完結する静的サイト。

## ファイル構成
```
ai-clean-systems-site/
├── index.html          サイト本体（自己完結：base64画像 + Google Fonts のみ外部依存）
├── README.md           このファイル（公開手順）
├── REQUEST.md          サカリヤラボチーム宛の依頼書
├── DESIGN-BRIEF.md     Canvaデザイン依頼の要件書
└── .gitignore
```

## ローカルで確認する
```bash
open index.html
# もしくは簡易サーバーで
python3 -m http.server 8080
# → http://localhost:8080/
```

## GitHub Pages で公開する手順

### 1. GitHub リポジトリを作成
```bash
# gh CLI を使う場合（推奨）
cd ai-clean-systems-site
gh repo create ai-clean-systems --public --source=. --remote=origin --push
```

または GitHub 上で空のリポジトリを手動で作り、
```bash
git remote add origin https://github.com/<OWNER>/ai-clean-systems.git
git branch -M main
git push -u origin main
```

### 2. GitHub Pages を有効化
Web UIから：
- `Settings` → `Pages`
- **Source**: `Deploy from a branch`
- **Branch**: `main` / `/ (root)` → `Save`
- 1〜2分で公開される：`https://<OWNER>.github.io/ai-clean-systems/`

もしくは CLIで：
```bash
gh api -X POST repos/<OWNER>/ai-clean-systems/pages \
  -f source[branch]=main -f source[path]=/
```

### 3. （任意）カスタムドメイン設定
`ai-clean-systems.com` を持っている場合：
```bash
echo "ai-clean-systems.com" > CNAME
git add CNAME && git commit -m "Add CNAME" && git push
```
ドメイン側で CNAME レコードを `<OWNER>.github.io` に向ける。

## デプロイ更新フロー
```bash
# 変更 → コミット → push すれば自動反映
git add -A && git commit -m "update: <内容>" && git push
```

## 外部依存
- Google Fonts（Noto Sans JP / Barlow Condensed）… オフライン不可だが、Pages運用なら問題なし
- 画像は全て base64 インライン埋め込み済み

## 注意点
- `index.html` のメールアドレス (`info@ai-clean-systems.com`) と電話番号 (`000-0000-0000`) は仮値。本番公開前に差し替え。
- スライド等の JS は全て HTML 内にインライン。外部 JS ファイルは不要。
