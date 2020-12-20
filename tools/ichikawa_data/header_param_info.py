class HeaderParamInfo:
  header = {
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':
            'gzip, deflate, br',
        'Accept-Language':
            'ja,en-US;q=0.9,en;q=0.8',
        'Cache-Control':
            'no-cache',
        'Connection':
            'keep-alive',
        'Host':
            'www.library.city.ichikawa.lg.jp',
        'Origin':
            'https://www.library.city.ichikawa.lg.jp',
        'Sec-Fetch-Dest':
            'document',
        'Sec-Fetch-Mode':
            'navigate',
        'Sec-Fetch-Site':
            'same-origin',
        'Sec-Fetch-User':
            '?1',
        'Pragma':
            'no-cache',
        'Upgrade-Insecure-Requests':
            '1',
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
  search_params = {
        'chk_catph': '11 31',
        'chk_catph': '13 33',
        'chk_catph': '14 34',
        'chk_catph': '15 35',
        'chk_catph': '17 37',
        'cmb_column1': 'title',
        'txt_word1': '',
        'cmb_like1': '2',
        'cmb_unit1': '0',
        'cmb_column2': 'author',
        'txt_word2': '',
        'cmb_like2': '2',
        'cmb_unit2': '0',
        'cmb_column3': 'publisher',
        'txt_word3': '',
        'cmb_like3': '2',
        'cmb_unit3': '0',
        'cmb_column4': 'subject',
        'txt_word4': '',
        'cmb_like4': '2',
        'cmb_unit4': '0',
        'cmb_column5': 'ndc',
        'txt_word5': '',
        'cmb_like5': '1',
        'cmb_unit5': '0',
        'cmb_column6': 'p_title',
        'txt_word6': '',
        'cmb_like6': '2',
        'cmb_unit6': '0',
        'cmb_column7': 'p_publisher',
        'txt_word7': '',
        'cmb_like7': '2',
        'cmb_unit7': '0',
        'chk_hol1tp': '00',
        'chk_hol1tp': '80',
        'chk_hol1tp': '20',
        'chk_hol1tp': '50',
        'chk_hol1tp': '90',
        'chk_hol1tp': '30',
        'chk_hol1tp': '40',
        'chk_hol1tp': '10',
        'chk_hol1tp': '11',
        'chk_hol1tp': '12',
        'chk_hol1tp': '13',
        'chk_hol1tp': '70',
        'chk_hol1tp': '72',
        'chk_hol1tp': '75',
        'chk_hol1tp': '76',
        'chk_hol1tp': '61',
        'chk_hol1tp': '62',
        'chk_hol1tp': '63',
        'chk_hol1tp': '64',
        'chk_hol1tp': '65',
        'chk_hol1tp': '66',
        'chk_hol1tp': '67',
        'chk_hol1tp': '68',
        'chk_hol1tp': '69',
        'chk_hol1tp': '60',
        'chk_hol1tp': '71',
        'chk_hol1tp': '73',
        'chk_hol1tp': '74',
        'chk_hol1tp': '77',
        'txt_stpubdate': '',
        'txt_edpubdate': '',
        'cmb_volume_column': 'volume',
        'txt_stvolume': '',
        'txt_edvolume': '',
        'cmb_code_column': 'isbn',
        'txt_code': '0000000000000',
        'txt_lom': '',
        'txt_cln1': '',
        'txt_cln2': '',
        'txt_cln3': '',
        'chk_area': '01',
        'chk_area': '02',
        'chk_area': '03',
        'chk_area': '04',
        'chk_area': '05',
        'chk_area': '06',
        'chk_area': '07',
        'chk_area': '11',
        'chk_area': '41',
        'chk_area': '42',
        'cmb_order': 'crtdt',
        'opt_order': '1',
        'opt_pagesize': '10',
        'submit_btn_searchDetailSelAr': '所蔵検索'
    }
    # hid_sessionはあとで上書きするので暫定的に"0000000"で初期化しておく
  reserve_params = {
        "hid_session": "0000000",
        "chk_rsvbib": "",
        "submit_btn_rsv_basket": "予約かご",
        "cmb_oder": "title",
        "opt_oder": "1",
        "opt_pagesize": "10",
        "chk_check": "0",
        "cmb_oder": "title",
        "opt_oder": "1",
        "opt_pagesize": "10"
    }
  basket_submit_params = {
        "hid_session": "00000000",
        "hid_aplph": "W",
        "cmb_area": "02",
        "view-title": "T170P68001",
        "txt_year": "9999",
        "cmb_month": "12",
        "cmb_day": "31",
        "chk_check": "1101897016",
        "submit_btn_reservation": "通常予約する"
    }
  basket_delete_params = {
        "hid_session": "00000000",
        "hid_aplph": "W",
        "cmb_area": "02",
        "view-title": "T170P68001",
        "txt_year": "9999",
        "cmb_month": "12",
        "cmb_day": "31",
        "submit_btn_delete": "削除"
    }
  basket_delete_confirm_params = {"hid_session": "00000000", "submit_btn_delete": "削除"}
  confirm_params = {
        "hid_session": "00000000",
        "hid_aplph": "W",
        "submit_btn_confirm": "予約する"
    }
  mypage_params = {"dispatch": "/opac/mylibrary.do", "every": "1"}
  extend_params = {
        "hid_session": "00000000",
        "idx": "0",
        "submit_btn_extend": "/T170P11011",
        "opt_pagesize": "10",
        "opt_pagesize": "10"
    }
  extend_confirm_params = {
        "hid_session": "00000000",
        "hid_lenid": "0001501174",
        "submit_btn_confirm": "貸出延長する"
    }