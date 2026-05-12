# 売り場ジェネレーター (Store Display Generator)

セブンイレブン冷凍ケース向けの売り場シミュレーター。
既存売り場の写真 + 新商品画像 + マスク(差し替える棚位置) → `gpt-image-1` で配置イメージを生成します。

MVP Phase 1 のスコープ:

- 売り場写真のアップロード(1024×1024 中央クロップ)
- 新商品画像の複数アップロード(参照画像として渡す)
- ブラシで「ここを差し替え」マスクを描画
- 配置指示テキスト
- `/api/generate` 経由で `gpt-image-1` 編集モード呼び出し
- 結果のプレビューとダウンロード

## セットアップ

```bash
cd store-display-generator
npm install
cp .env.example .env.local
# .env.local の OPENAI_API_KEY を埋める
npm run dev
# http://localhost:3000
```

## 環境変数

| 変数名 | 必須 | 説明 |
| --- | --- | --- |
| `OPENAI_API_KEY` | yes | OpenAI APIキー(gpt-image-1 利用権限が必要) |

## 構成

```
store-display-generator/
├── app/
│   ├── layout.tsx          ルートレイアウト
│   ├── page.tsx            メインUI(撮影/マスク/生成)
│   ├── globals.css         Tailwind ベース
│   └── api/generate/route.ts  gpt-image-1 編集モード呼び出し
├── lib/prompt.ts           プロンプトテンプレ
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.mjs
```

## マスクの扱い

OpenAI `images.edit` の仕様に従い、マスク PNG は以下:

- 透明ピクセル (alpha=0) → ここを編集
- 不透明ピクセル → 既存を保持

UI上では、ユーザーが赤色でなぞった箇所を「編集対象」として、送信前に透明アルファのマスク PNG に変換しています。

## 注意点・既知の制約

- gpt-image-1 はパッケージの文字や細部を改変する場合があります。プロンプトで強く保持を指示していますが、必ず生成結果を目視確認してください。
- 生成画像には「シミュレーション」である旨を表示しています。実店舗の確定売り場として使う前に、本部承認のフローを必ず通してください。
- 現状はサイズが 1024×1024 固定。将来 1536×1024 / 1024×1536 の縦横サイズ自動選択に拡張予定。

## ロードマップ

- [ ] 棚段の自動検出(段ごとに分割マスクを生成)
- [ ] 配置構造化UI(段×セル選択)
- [ ] 商品マスタ連携(現状は手動アップロード)
- [ ] 生成履歴・お気に入り保存
- [ ] PWA化(ホーム画面追加、オフライン UI)
- [ ] ハイブリッド合成モード(商品の物理合成 + AI 馴染ませ)
