from api import base
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Koto(base.Base):
    def __init__(self, user_id: str, user_password: str) -> None:
        self.login(user_id, user_password)

    def login(self, user_id: str, user_password: str) -> None:
        self.driver = webdriver.Remote(
          command_executor = 'http://selenium:4444/wd/hub',
          options = webdriver.ChromeOptions()
        )
        self.driver.get('https://www.koto-lib.tokyo.jp/opw/OPW/OPWUSERCONF.CSP')
        time.sleep(10)
        user_id_text_box = self.driver.find_element(By.XPATH, value='//*[@id="LoginCheck"]/div[2]/div/div[2]/div[3]/input')
        user_id_text_box.send_keys(user_id)
        user_password_text_box = self.driver.find_element(By.XPATH, value='//*[@id="LoginCheck"]/div[2]/div/div[2]/div[5]/input')
        user_password_text_box.send_keys(user_password)
        time.sleep(10)
        submit_button = self.driver.find_element(By.XPATH, value='//*[@id="LoginCheck"]/div[2]/div/div[2]/div[7]/input')
        submit_button.click()
        time.sleep(10)

    def get_borrow_list(self) -> pd.DataFrame:
        self.driver.get('https://www.koto-lib.tokyo.jp/opw/OPW/OPWUSERINFO.CSP')
        time.sleep(10)
        total_borrow_num = int(self.driver.find_element(By.XPATH, value='//*[@id="contents"]/div[2]/div/ul/li[1]/a/h3/span').text)
        print(f"{total_borrow_num=}")
        df = pd.DataFrame()
        for i in range(total_borrow_num):
            title = self.driver.find_element(By.XPATH, value=f'//*[@id="ContentLend"]/form/div[2]/table/tbody/tr[{2*i+2}]/td[3]/a').text
            book_id = self.driver.find_element(By.XPATH, value=f'//*[@id="ContentLend"]/form/div[2]/table/tbody/tr[{2*i+2}]/td[5]').text
            extension_available = self.driver.find_element(By.XPATH, value=f'//*[@id="ContentLend"]/form/div[2]/table/tbody/tr[{2*i+2}]/td[2]').text
            return_date = self.driver.find_element(By.XPATH, value=f'//*[@id="ContentLend"]/form/div[2]/table/tbody/tr[{2*i+2}]/td[8]').text
            #//*[@id="ContentLend"]/form/div[2]/table/tbody/tr[8]/td[2]
            s = pd.Series({
              "title": title,
              "book_id": book_id,
              "extension_available": extension_available,
              "return_date": return_date,
            })
            print(f"{s=}")
            df = pd.concat([df, s.to_frame().T], ignore_index=True)
        print(f"{df=}")
        return df

    def push_extension_button(self, book_id: str) -> None:
        borrow_list = self.get_borrow_list()
        # 入力されたbook_idに相当する本の行番号を取得
        index = borrow_list.index[borrow_list["book_id"] == book_id].tolist()[0]
        button = self.driver.find_element(By.XPATH, value=f'//*[@id="ContentLend"]/form/div[2]/table/tbody/tr[{2*index+2}]/td[2]/button')
        button.click()
        time.sleep(10)
        # 確認画面で了承する
        button = self.driver.find_element(By.XPATH, value=F'//*[@id="modal-footter"]/input[1]')
        button.click()
        time.sleep(10)

    def __del__(self) -> None:
        self.driver.quit()