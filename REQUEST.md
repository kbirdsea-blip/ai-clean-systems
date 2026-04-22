# 依頼書｜サカリヤラボチーム御中

## 概要
Ai Clean Systems（清掃・特殊清掃・高圧洗浄／横浜・神奈川全域）のコーポレートサイトを立ち上げたい。
本フォルダに一式のサイト素材を同梱しているので、下記2点の対応をお願いしたい。

---

## ① GitHub で閲覧できるように立ち上げ
- **ホスティング方式**：GitHub Pages（Public リポジトリ + main ブランチ `/` 直下）
- **希望リポジトリ名**：`ai-clean-systems`（orgかアカウントは任せます）
- **公開 URL イメージ**：`https://<org-or-user>.github.io/ai-clean-systems/`
- **引き継ぐもの**：本フォルダ（`ai-clean-systems-site/`）全体。`git init` 済み／コミット済み。
- **手順は** [`README.md`](./README.md) **に記載。**

カスタムドメイン（例：`ai-clean-systems.com`）が確保できるようなら、CNAME 設定までお願いできるとありがたい。
不要なら `<user>.github.io/ai-clean-systems/` のままでOK。

---

## ② Canva でデザイン生成
現状の `index.html` は **base64 画像で仮組み** している。
ヒーロー／サービスカード／施工ギャラリー等の画像を Canva で差し替えたい。

- **詳細な要件**：[`DESIGN-BRIEF.md`](./DESIGN-BRIEF.md) にまとめてある。
- **希望**：Canva 上に専用ブランドキットを作成し、今後も同じトーンで素材を量産できるようにしておいてほしい。
- **納品形式**：PNG または WebP（`assets/` 以下に格納 → HTML の base64 を差し替え）。

---

## ③ 別パターン（Pattern A）もブラッシュアップ
`pattern-a/index.html` に、別案のHTMLが入っている（施工ギャラリー無し版／431KB）。
こちらも同じトーンでブラッシュアップして公開してほしい。

- **現在の公開URL**：
  - メイン（Pattern B）：`https://kbirdsea-blip.github.io/ai-clean-systems/`
  - Pattern A：`https://kbirdsea-blip.github.io/ai-clean-systems/pattern-a/`
- **依頼内容**：
  - 2案を見比べた上で、最終的に1案に統合 or 両案を残すかを提案してほしい
  - 画像差し替え（DESIGN-BRIEF.md と同じ要件）
  - コピー・レイアウトのリファイン
  - 両案とも `index.html` を差し替えるだけで反映される構造

---

## スケジュール感
- まず ① GitHub Pages 公開を優先。公開 URL が出たら共有してほしい。
- ② デザインは公開後に差し替えていく形でOK。

## 連絡事項
- サイト内のメール：`info@ai-clean-systems.com`
- サイト内の電話番号：`000-0000-0000`（**仮置き**。確定したら連絡します）
- どちらも本番化前に差し替える必要があることを念頭に置いておいてください。

よろしくお願いします。
