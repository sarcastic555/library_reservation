# library_reservation

## 処理フロー
![slide_material](https://user-images.githubusercontent.com/29055397/103182685-bae73e80-48f0-11eb-9445-ef13c554fd40.png)

## 使い方
1. 準備
```bash
git clone https://github.com/sarcastic555/library_reservation.git
```

2. 環境変数の設定
```bash
export LIBRARY_RESERVATION="${PWD}"
export BOOKLOG_ID="***"
export BOOKLOG_PASSWORD="***"
export ICHIKAWA_LIBRARY_ID="***"
export ICHIKAWA_LIBRARY_PASSWORD="***"
export CULIL_API_KEY="***************"
export LINE_TOKEN_PERSONAL="********************"
export LINE_TOKEN_FOR_TEST="********************"
```

3. docker環境に入る
```bash
cd docker
source docker_build.sh
source docker_run.sh
```

4. ブックリストのダウンロード
```bash
python ./download_booklist.py --output_file ./list/booklog_data.csv
```

5. 貸し出し延長が必要か判定し必要なら延長手続きを実施
```bash
python extension_checker.py
```

6. 借りている本、予約している本のリストを作成
```bash
python ./create_owning_or_reserving_booklist.py --booklog_list_file list/booklog_data.csv --lend_output_file list/lend.csv --reserve_output_file list/reserve.csv
```

7. 1.でダウンロードしたブックリストを既読・未読即時利用可能・未読即時利用不可に分類  
```bash
python classify_list.py --booklog_data_file list/booklog_data.csv --lend_file list/lend.csv --reserve_file list/reserve.csv --output_not_found_file list/not_found.csv --output_no_reservation_file list/no_reservation.csv --output_has_reservation_file list/has_reservation.csv
```

8. 返却期限が迫っていればLINEで通知  
```bash
python ./send_line_message.py
```

9. 予約冊数の計算
```bash
python reserve_book_calculator.py --now_lend_file list/lend.csv --now_reserve_file list/reserve.csv --no_reservation_file list/no_reservation.csv --has_reservation_file list/has_reservation.csv --output_shortwait_reserve_size_file result/shortwait_reserve_size.csv --output_longwait_reserve_size_file result/longwait_reserve_size.csv --output_report_file result/report.html
```

10. 予約する本を決定
```bash
python reserve_book_selector.py --no_reservation_booklist_file list/no_reservation.csv --has_reservation_booklist_file list/has_reservation.csv --shortwait_reserve_book_num_file result/shortwait_reserve_size.csv --longwait_reserve_book_num_file result/longwait_reserve_size.csv --lend_file list/lend.csv --output_shortwait_reserve_list list/shortwait_reserve_list.csv --output_longwait_reserve_list list/longwait_reserve_list.csv
```

11. 予約バスケットをクリア
```bash
python ./clear_reserve_basket.py
```

12. 資料を予約  
```
python reserve_book.py --shortwait_reserve_list list/shortwait_reserve_list.csv --longwait_reserve_list list/longwait_reserve_list.csv
```

## ツール
フォーマッター
```
./formatter.sh
```
単体テスト
```
pytest
```
