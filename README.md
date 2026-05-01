# kakeibo

[Zaim](https://zaim.net/) から家計データを取得し、カテゴリ別支出をグラフで可視化するツール。

## 機能

- Zaim API から指定期間の収支データを取得し Excel に保存
- カテゴリ別支出の円グラフ＋明細テーブルを HTML で出力

## 必要環境

- Python 3.10 以上
- [uv](https://docs.astral.sh/uv/)

## セットアップ

### 1. 依存パッケージのインストール

```bash
uv sync
```

### 2. Zaim API キーの取得

[Zaim デベロッパーページ](https://dev.zaim.net/) でアプリを登録し、Consumer Key / Consumer Secret を取得する。

### 3. アクセストークンの取得（初回のみ）

```bash
uv run ./src/get_token.py
```

ブラウザで Zaim の認証画面が開くので承認する。取得した以下の4つの値を `.env` に記載する。

### 4. `.env` ファイルの作成

プロジェクトルートに `.env` を作成する。

```
ZAIM_CONSUMER_KEY=<Consumer Key>
ZAIM_CONSUMER_SECRET=<Consumer Secret>
ZAIM_ACCESS_TOKEN=<Access Token>
ZAIM_ACCESS_TOKEN_SECRET=<Access Token Secret>
```

## Claude Code Skills

[Claude Code](https://claude.ai/code) を使うと、対話形式でより簡単に実行できる。

### `/show-kakeibo`

期間を会話で指定するだけでデータ取得＋グラフ生成を一括実行する。

```
/show-kakeibo
```

実行例：

```
> /show-kakeibo
開始日と終了日を教えてください。

> 開始日を2025年8月1日、終了日を8月31日にして

- 開始日：2025-08-01
- 終了日：2025-08-31
でよいですか？

> OK
→ get_table.py / visualize_table.py を順に実行してグラフを出力
```

### `/modify-code`

コーディング規約（`.claude/skills/modify-code/rules.md`）に従ってソースコードを自動修正する。

```
/modify-code src/get_table.py
```

対象ファイルを省略すると、IDE で開いているファイルが対象になる。

---

## 使い方

### データ取得

```bash
uv run ./src/get_table.py --start_date=YYYY-MM-DD --end_date=YYYY-MM-DD
```

`output/zaim_<start_date>_<end_date>.xlsx` に保存される。

### グラフ生成

```bash
uv run ./src/visualize_table.py --start_date=YYYY-MM-DD --end_date=YYYY-MM-DD
```

`output/pie_<start_date>_<end_date>.html` が生成され、ブラウザで自動的に開く。

### 実行例

```bash
# 2025年8月のデータを取得してグラフ化
uv run ./src/get_table.py --start_date=2025-08-01 --end_date=2025-08-31
uv run ./src/visualize_table.py --start_date=2025-08-01 --end_date=2025-08-31
```

## ファイル構成

```
kakeibo/
├── src/
│   ├── get_token.py        # アクセストークン取得（初回のみ）
│   ├── get_table.py        # Zaim API からデータ取得 → Excel 保存
│   └── visualize_table.py  # Excel を読み込んでグラフ生成
├── output/                 # 出力ファイル（.gitignore 対象）
│   ├── zaim_*.xlsx
│   └── pie_*.html
├── .env                    # 認証情報（.gitignore 対象）
└── pyproject.toml
```

## 対応カテゴリ

グラフに表示されるカテゴリは以下の通り。

| カテゴリID | 名称 |
|-----------|------|
| 101 | 食料品 |
| 102 | 日用品 |
| 108 | イベント |
| 199 | その他 |
