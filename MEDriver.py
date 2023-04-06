# -*- config: utf-8 -*-

import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import config


class MEDriver:
    def __init__(self):
        # UserAgent設定
        options = webdriver.ChromeOptions()
        UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
        options.add_argument('--user-agent=' + UA)

        self.web = webdriver.Chrome(executable_path='C:/Users/manab/github_/chromedriver.exe')
        self.end_point = "https://moneyforward.com"

    def login(self, mail_address, password):
        if self.is_logged_in():
            return True

        url = "https://id.moneyforward.com/sign_in/email"

        self.web.get(url)
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

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div/ul/li/a/img")
        submit.click()
        time.sleep(2)

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[2]/input")
        submit.click()
        time.sleep(5)

        return self.is_logged_in()

    # ホーム/最新の入出金
    def fetch_newest_activities(self):
        self.to_page(self.end_point)

        dates      = self.web.find_elements_by_class_name("recent-transactions-date")
        categories = self.web.find_elements_by_class_name("recent-transactions-category")
        shops      = self.web.find_elements_by_class_name("recent-transactions-content")
        amounts    = self.web.find_elements_by_class_name("recent-transactions-amount")

        dates      = [d.text for d in dates]
        categories = [c.text for c in categories]
        shops      = [s.text for s in shops]
        amounts    = [a.text for a in amounts]

        data = dict(Date=dates, Category=categories, Shop=shops, Amount=amounts)

        return pd.DataFrame(data=data)


        # table_data = self.web.find_element_by_id("recent-transactions-table")
        # return table_data.text.split("\n")

    # ホーム/総資産
    def fetch_total_asset(self):
        self.to_page(self.end_point)

        return self.web.find_element_by_xpath('//*[@id="user-info"]/section/div[1]').text

    # 家計簿/月次推移/収支リスト
    def fetch_balances(self, institution_name=None):
        self.to_page(self.end_point + "/cf/monthly")


    # 予算/今月の予算
    def fetch_monthly_budget(self):
        pass

    # 口座/登録済み金融機関
    def fetch_financial_institutions(self):
        pass

    def is_logged_in(self):
        return self.web.title == "マネーフォワード ME"

    def to_page(self, url):
        if not self.is_logged_in():
            return False

        self.web.get(url)


if __name__ == '__main__':
    me = MEDriver()
    me.login(config.mail1, config.pw1)

    df = me.fetch_newest_activities()
    print(df)

    total = me.fetch_total_asset()
    print(total)
