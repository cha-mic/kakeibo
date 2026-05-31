---
name: check-zaim-api
description: Zaim APIへのアクセスを確認する
disable-model-invocation: false
---

Zaim APIにアクセスできるかどうかを確認する。

1. 以下のコマンドを実行する:
   uv run ./src/check_api.py

2. 結果を以下の観点で報告する:
   - 「接続OK」が表示されればアクセス成功
   - 「接続NG」が表示された場合は理由を案内する
