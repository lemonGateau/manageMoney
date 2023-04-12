# -*- config: utf-8 -*-

import datetime
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import config


class MeDriver:
    def __init__(self, mail_address, password):
        # UserAgent設定
        options = webdriver.ChromeOptions()
        UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
        options.add_argument('--user-agent=' + UA)

        self.web = webdriver.Chrome(executable_path='C:/Users/manab/github_/chromedriver.exe')
        self.end_point = "https://moneyforward.com"

        self.login(mail_address, password)

    def login(self, mail_address, password):
        if self._is_logged_in():
            return True

        url = "https://id.moneyforward.com/sign_in/email"

        self.web.get(url)
        mail_form = self.web.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div[1]/section/form/div[2]/div/input")
        mail_form.send_keys(mail_address)
        time.sleep(0.1)

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div[1]/section/form/div[2]/div/div[3]/input")
        submit.click()
        time.sleep(1)

        pw_form = self.web.find_element_by_xpath("/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/input[2]")
        pw_form.send_keys(password)
        time.sleep(0.1)

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]/input")
        submit.click()
        time.sleep(1)

        if self._is_logged_in():
            return True

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div/ul/li/a/img")
        submit.click()
        time.sleep(1)

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[2]/input")
        submit.click()

        return self._is_logged_in()

    # ホーム/総資産
    def fetch_total_asset(self):
        self._to_page(self.end_point)

        return self.web.find_element_by_xpath('//*[@id="user-info"]/section/div[1]').text

    # ホーム/収支
    def fetch_total_balances(self):
        self._to_page(self.end_point)

        period = self.web.find_element_by_xpath('//*[@id="cf-info"]/div/h2[1]').text

        data = list()
        table = self.web.find_elements_by_class_name("js-monthly_total")
        for row in table:
            data.append(row.text.split())

        columns = ["内容", "合計金額"]
        df = pd.DataFrame(data, columns=columns)

        return df, period

    # ホーム/最新の入出金
    def fetch_recent_transactions(self):
        self._to_page(self.end_point)

        data = list()
        table = self.web.find_elements_by_class_name("recent-transactions-row")
        for row in table:
            data.append(row.text.split())

        columns=["利用日", "分類", "店舗", "金額"]

        return pd.DataFrame(data, columns=columns)

    # ホーム/明細
    def fetch_account_statuses(self):
        """ todo: カード、銀行などで場合分け """
        self._to_page(self.end_point)

        try:
            accounts = self.web.find_elements_by_class_name("heading-accounts")
            amounts  = self.web.find_elements_by_class_name("amount")
        except:
            return None

        data = list()
        for account, amount in zip(accounts, amounts):
            name, update = account.text.split("\n")
            amount, *_   = amount.text.split("\n")

            update = update.replace("取得日時", "")[1:-1]

            data.append([name, amount, update])

        columns = ["内容", "金額", "更新日時"]

        return pd.DataFrame(data, columns=columns)

    # 家計簿/月次推移/収支リスト
    def fetch_monthly_balances(self):
        self._to_page(self.end_point + "/cf/monthly")

        periods = self.web.find_element_by_xpath('//*[@id="monthly_list"]/tbody/tr[1]')
        periods = periods.text.split()
        periods.insert(0, "分類")

        data = list()
        for i in range(30):
            try:
                balance = self.web.find_element_by_xpath(f'//*[@id="monthly_list"]/tbody/tr[{i+2}]')
            except:
                break
            data.append(balance.text.split())


        return pd.DataFrame(data, columns=periods)

    # 予算/今月の予算
    def fetch_monthly_budgets(self, offset_month=0):
        ''' offset_month = 0: 今月, 1: 前月...'''
        self._to_page(self.end_point + "/spending_summaries" + "?offset_month=" + str(offset_month))

        period = self.web.find_element_by_xpath('//*[@id="budgets-progress"]/div/section/div/div/div').text

        data = list()
        for i in range(30):
            try:
                row = self.web.find_element_by_xpath(f'//*[@id="budgets-progress"]/div/section/table/tbody/tr[{i+1}]')
            except:
                break
            data.append(row.text.split("\n"))

        columns=["分類", "支出", "予算"]
        df = pd.DataFrame(data, columns=columns)

        return df, period

    def _is_logged_in(self):
        return self.web.title == "マネーフォワード ME"

    def _to_page(self, url):
        if not self._is_logged_in():
            return False

        self.web.get(url)
        time.sleep(1)   # 動的な要素で、表示に若干必要だから（fetch_monthly_budget()の予算など）

    # 各金融機関の最新情報に更新
    def _reload_assets(self):
        pass



if __name__ == '__main__':
    mes = list()
    mes.append(MeDriver(config.mail1, config.pw1))
    # mes.append(MeDriver(config.mail2, config.pw2))
    # mes.append(MeDriver(config.mail3, config.pw3))
    # mes.append(MeDriver(config.mail4, config.pw4))

    time.sleep(1)
    for me in mes:
        print("\n\n")

        print("fetch_total_asset")
        total = me.fetch_total_asset()
        print(total)
        print("\n")

        print("fetch_total_balances")
        df, period = me.fetch_total_balances()
        print(period)
        print(df)
        print("\n")

        print("fetch_recent_transactions")
        df1 = me.fetch_recent_transactions()
        print(df1)
        print("\n")

        print("fetch_account_statuses")
        df2 = me.fetch_account_statuses()
        print(df2)
        print("\n")

        print("fetch_monthly_balances")
        df3 = me.fetch_monthly_balances()
        print(df3)
        print("\n")

        print("fetch_monthly_budget")
        df4, period = me.fetch_monthly_budgets()
        print(period)
        print(df4)
        print("\n")

        print("fetch_monthly_budget(offset_month=2)")
        df5, period = me.fetch_monthly_budgets(offset_month=2)
        print(period)
        print(df5)
        print("\n\n")


    """
    # indexに登録パターン
    for row in table:
        name, *data = row.text.split()
        df.loc[name] = data
    """