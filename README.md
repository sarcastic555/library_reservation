# library_reservation

0. 準備
```bash
git clone https://github.com/sarcastic555/library_reservation.git
cd docker
source docker_build.sh
source docker_run.sh
```

1. ブックリストのダウンロード
```bash
python ./download_booklist.py --output_file ./list/booklog_data.csv
```

2. 貸し出し延長が必要か判定し必要なら延長手続きを実施
```bash
python extension_checker.py
```

3. 借りている本、予約している本のリストを作成
```bash
python ./create_owning_or_reserving_booklist.py --lend_output_file list/lend.csv --reserve_output_file list/reserve.csv
```

4. 1.でダウンロードしたブックリストを既読・未読即時利用可能・未読即時利用不可に分類  
3.の出力結果を利用
```bash
python3 classify_list.py --booklog_data_file list/booklog_data.csv --lend_file list/lend.csv --reserve_file list/reserve.csv --output_not_found_file list/not_found.csv --output_no_reservation_file list/no_reservation.csv --output_has_reservation_file list/has_reservation.csv
```

5. 返却期限が迫っていればLINEで通知  
3.の出力結果を利用
```bash
python ./send_line_message.py
```

6. 予約冊数の計算
```bash
python3 reserve_book_calculator.py --now_lend_file list/lend.csv --now_reserve_file list/reserve.csv --no_reservation_file list/no_reservation.csv --has_reservation_file list/has_reservation.csv --output_shortwait_reserve_size_file result/shortwait_reserve_size.csv --output_longwait_reserve_size_file result/longwait_reserve_size.csv --output_report_file result/report.html
```

7. 予約バスケットをクリア
```bash
python ./clear_reserve_basket.py
```

8. 読みたい本リストの中から資料を予約  
1.と4.の結果を利用
```
python ./reserve_book.py
```

# ツール
フォーマッター
```
./formatter.sh
```
単体テスト
```
pytest
```
