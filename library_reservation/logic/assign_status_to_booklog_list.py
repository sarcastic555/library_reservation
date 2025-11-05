# docker compose  up -d --build
# docker exec -it python-app poetry run python3 library_reservation/logic/assign_status_to_booklog_list.py

import pandas as pd
from tqdm import tqdm


import sys
sys.path.append("/src/library_reservation")
print(f"{sys.path=}")

import culil.get_book_status

columns = ["サービスID", "アイテムID", "13桁ISBN", "カテゴリ", "評価", "読書状況", "レビュー", "タグ", "読書メモ(非公開)",
           "登録日時", "読了日", "タイトル", "作者名", "出版社名", "発行年", "ジャンル", "ページ数", "価格"]

df = pd.read_csv("booklog20251104093236.csv", encoding="Shift_JIS", header=None, names=columns)
df["13桁ISBN"] = df["13桁ISBN"].fillna(-1).astype(int).astype(str)

def get_library_status(isbn: str) -> str:
    status_dict = culil.get_book_status.get_book_status(isbn, "Tokyo_Koto")
    exist = False
    short_waiting = False
    for status in status_dict.values():
        if status == culil.get_book_status.BookStatus.borrow_available:
            short_waiting = True
        exist = True
    if not exist:
        print(f"ISBN: {isbn} -> Status: not_found")
        return "not_found"
    elif short_waiting:
        print(f"ISBN: {isbn} -> Status: short_waiting")
        return "short_waiting"
    else:
        print(f"ISBN: {isbn} -> Status: long_waiting")
        return "long_waiting"

try:
    df = df[df["読書状況"] == "読みたい"]
    print(f"{df=}")

    tqdm.pandas(desc="Processing")
    df["library_status"] = df["13桁ISBN"].progress_apply(lambda x: get_library_status(x))

    df = df[["タイトル", "読書状況", "13桁ISBN", "library_status"]]

    df_short_waiting = df[df["library_status"] == "short_waiting"]
    df_long_waiting = df[df["library_status"] == "short_waiting"]

    df_short_waiting.to_csv("short_waiting.csv", index=None)
except KeyboardInterrupt:
    print("\n処理が中断されました。終了します。")
    sys.exit(0)
