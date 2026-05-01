---
name: show-kakeibo
description: 家計簿を表示する
disable-model-invocation: true
---

家計簿を表示する．

1. 対話を通して家計簿を作成する開始日(start_data)と終了日(end_date)を決定する．形式はYYYY-MM-DD
2. 決定した開始日，終了日の確認をとる．
3. 決定した引数をもとに以下のコマンドを実行
  uv run ./src/get_table.py --start_date=開始日 --end_date=終了日

4. 以下のコマンドを実行
  uv run ./src/visualize_table.py --start_date=開始日 --end_date=終了日

5. /clear を実行する
---

## 使い方

Claude Code上で以下を入力するだけで実行されます。
/show-kakeibo
