import argparse
import os
import webbrowser

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

CATEGORY_NAMES: dict[int, str] = {
    101: "食料品",
    102: "日用品",
    108: "イベント",
    199: "その他",
}

OUTPUT_DIR: str = os.path.join(os.path.dirname(__file__), "..", "output")

def load_payments(start_date: str, end_date: str) -> pd.DataFrame:
    """Excelファイルから支払いデータを読み込んでフィルタリングする。

    Args:
        start_date (str): 取得開始日 "YYYY-MM-DD"
        end_date (str): 取得終了日 "YYYY-MM-DD"

    Returns:
        pd.DataFrame: 支払いデータのDataFrame
    """
    excel_path: str          = "{}/zaim_{}_{}.xlsx".format(OUTPUT_DIR, start_date, end_date)
    df:         pd.DataFrame = pd.read_excel(excel_path)
    df["date"] = pd.to_datetime(df["date"])
    mask: pd.Series = (
        (df["mode"] == "payment")
        & (df["date"] >= start_date)
        & (df["date"] <= end_date)
    )
    return df[mask]


def plot_category_pie(df: pd.DataFrame, start_date: str, end_date: str) -> str:
    """カテゴリ別支出の円グラフと明細テーブルをHTMLファイルとして出力する。

    Args:
        df (pd.DataFrame): 支払いデータのDataFrame
        start_date (str): 集計開始日 "YYYY-MM-DD"
        end_date (str): 集計終了日 "YYYY-MM-DD"

    Returns:
        str: 出力したHTMLファイルのパス。データが空の場合は空文字列
    """
    df: pd.DataFrame = df[df["category_id"].isin(CATEGORY_NAMES)].copy()
    if df.empty:
        print("対象カテゴリのデータがありません")
        return ""

    df["category"] = df["category_id"].map(CATEGORY_NAMES)

    summary: pd.Series = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    table_df: pd.DataFrame = (
        df[["date", "category", "name", "amount"]]
        .sort_values(["date", "category"])
        .assign(
            date=lambda d: d["date"].dt.strftime("%Y-%m-%d"),
            amount=lambda d: d["amount"].map("{:,}円".format),
        )
    )

    fig: go.Figure = make_subplots(
        rows=1, cols=2,
        specs=[[
            {"type": "pie"},
            {"type": "table"},
        ]],
        column_widths=[0.45, 0.55],
    )

    custom_text: list[str] = [f"{v:,}円" for v in summary.values]
    fig.add_trace(
        go.Pie(
            labels=summary.index,
            values=summary.values,
            text=custom_text,
            textinfo="label+text+percent",
            hovertemplate="%{label}<br>%{value:,}円 (%{percent})<extra></extra>",
        ),
        row=1, col=2,
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["日付", "カテゴリ", "品名", "金額"],
                fill_color="#4C72B0",
                font=dict(color="white", size=13),
                align="center",
            ),
            cells=dict(
                values=[
                    table_df["date"],
                    table_df["category"],
                    table_df["name"],
                    table_df["amount"],
                ],
                align=["center", "center", "left", "right"],
                height=24,
            ),
        ),
        row=1, col=1,
    )

    fig.update_layout(
        title=f"カテゴリ別支出　{start_date} ～ {end_date}",
        height=700,
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path: str = os.path.abspath(os.path.join(OUTPUT_DIR, f"pie_{start_date}_{end_date}.html"))
    fig.write_html(out_path)
    return out_path


def main() -> None:
    """コマンドライン引数を解析してカテゴリ別支出グラフを生成する。"""
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--start_date", required=True, help="開始日 YYYY-MM-DD")
    parser.add_argument("--end_date",   required=True, help="終了日 YYYY-MM-DD")
    args: argparse.Namespace = parser.parse_args()

    df:  pd.DataFrame = load_payments(args.start_date, args.end_date)
    out: str          = plot_category_pie(df, args.start_date, args.end_date)
    if out:
        print(f"保存しました: {out}")
        webbrowser.open(f"file:///{out}")


if __name__ == "__main__":
    main()
