import argparse
import os

import pandas as pd
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

ZAIM_BASE_URL:   str = "https://api.zaim.net/v2"
OUTPUT_DIR:      str = os.path.join(os.path.dirname(__file__), "..", "output")
ZAIM_PAGE_LIMIT: int = 200


def _get_session() -> OAuth1Session:
    """Zaim APIへのOAuth1認証済みセッションを返す。

    Returns:
        OAuth1Session: 認証済みセッション
    """
    return OAuth1Session(
        os.environ.get("ZAIM_CONSUMER_KEY"),
        client_secret=os.environ.get("ZAIM_CONSUMER_SECRET"),
        resource_owner_key=os.environ.get("ZAIM_ACCESS_TOKEN"),
        resource_owner_secret=os.environ.get("ZAIM_ACCESS_TOKEN_SECRET"),
    )


def get_money_records(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Zaimから収支データを取得してDataFrameで返す。

    Args:
        start_date: 取得開始日 "YYYY-MM-DD"
        end_date:   取得終了日 "YYYY-MM-DD"

    Returns:
        収支レコードのDataFrame。列の主なものは以下:
            date, mode (payment/income/transfer), amount,
            category, genre, place, name, comment
    """
    session: OAuth1Session = _get_session()
    records: list[dict]    = []
    page:    int           = 1

    while True:
        resp = session.get(
            ZAIM_BASE_URL + "/home/money",
            params={
                "mapping": 1,
                "start_date": start_date,
                "end_date": end_date,
                "limit": ZAIM_PAGE_LIMIT,
                "page": page,
            },
        )
        print(resp.status_code, resp.url)
        resp.raise_for_status()
        money: list[dict] = resp.json().get("money", [])
        if not money:
            break
        records.extend(money)
        page += 1

    df: pd.DataFrame = pd.DataFrame(records)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

    return df

def save_to_excel(df: pd.DataFrame, start_date: str, end_date: str) -> str:
    """DataFrameをExcelファイルとして保存する。

    Args:
        df (pd.DataFrame): 保存するデータ
        start_date (str): 取得開始日 "YYYY-MM-DD"
        end_date (str): 取得終了日 "YYYY-MM-DD"

    Returns:
        str: 保存先のファイルパス
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename: str = f"zaim_{start_date}_{end_date}.xlsx"
    path:     str = os.path.join(OUTPUT_DIR, filename)
    df.to_excel(path, index=False)
    return path

def main() -> None:
    """コマンドライン引数を解析してZaimデータを取得・保存する。"""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="開始日と終了日")
    parser.add_argument("--start_date", default="2026-04-01")
    parser.add_argument("--end_date",   default="2026-05-01")
    args: argparse.Namespace = parser.parse_args()

    df:   pd.DataFrame = get_money_records(args.start_date, args.end_date)
    print(df)
    path: str = save_to_excel(df, args.start_date, args.end_date)
    print(f"保存しました: {path}")

if __name__ == "__main__":
    main()