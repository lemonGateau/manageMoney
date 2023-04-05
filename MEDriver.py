# -*- config: utf-8 -*-

import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class MEDriver:
    def __init__(self):
        # UserAgent設定
        options = webdriver.ChromeOptions()
        UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
        options.add_argument('--user-agent=' + UA)

        self.web = webdriver.Chrome(executable_path='C:/Users/manab/github_/chromedriver.exe')

    def login(self, mail_address, password):
        url = "https://id.moneyforward.com/sign_in/email"

        self.web .get(url)
        mail_form = self.web.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div[1]/section/form/div[2]/div/input")
        mail_form.send_keys(mail_address)
        time.sleep(1)

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div[1]/section/form/div[2]/div/div[3]/input")
        submit.click()
        time.sleep(2)

        pw_form = self.web.find_element_by_xpath("/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/input[2]")
        pw_form.send_keys(password)
        time.sleep(1)

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]/input")
        submit.click()
        time.sleep(2)

    # ホーム/最新の入出金
    def fetch_newest_accout_activities(self,count=5):
        pass

    # ホーム/総資産
    def fetch_assets(self, institution_name=None):
        pass

    # 家計簿/月次推移/収支リスト
    def fetch_balances(self, institution_name=None):
        pass

    # 予算/今月の予算
    def fetch_monthly_budget(self):
        pass

    # 口座/登録済み金融機関
    def fetch_financial_institutions(self):
        pass


if __name__ == '__main__':
    mail = "mikancisco@gmail.com"
    pw   = "aw38M9s82#"

    me = MEDriver()
    me.login(mail, pw)

    time.sleep(10)