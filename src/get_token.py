import pyzaim

def main():
    """OAuth 1.0a フローでアクセストークンを取得する。初回のみ実行。"""
    print("Hello from kakeibo!")
    pyzaim.get_access_token()


if __name__ == "__main__":
    main()