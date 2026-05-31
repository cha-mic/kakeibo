import os

from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def main():
    session = OAuth1Session(
        os.environ.get("ZAIM_CONSUMER_KEY"),
        client_secret=os.environ.get("ZAIM_CONSUMER_SECRET"),
        resource_owner_key=os.environ.get("ZAIM_ACCESS_TOKEN"),
        resource_owner_secret=os.environ.get("ZAIM_ACCESS_TOKEN_SECRET"),
    )

    resp = session.get("https://api.zaim.net/v2/home/user/verify")
    print("ステータス:", resp.status_code)

    if resp.status_code == 200:
        name = resp.json().get("me", {}).get("name", "不明")
        print(f"接続OK - ユーザー名: {name}")
    elif resp.status_code == 401:
        print("接続NG - 認証情報が正しくありません。.env の ZAIM_ACCESS_TOKEN / ZAIM_ACCESS_TOKEN_SECRET を確認してください")
    else:
        print("接続NG -", resp.text)


if __name__ == "__main__":
    main()
