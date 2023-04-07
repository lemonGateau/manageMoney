# -*- config: utf-8 -*-

import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import config


class MEDriver:
    def __init__(self, mail_address, password):
        # UserAgent設定
        options = webdriver.ChromeOptions()
        UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'
        options.add_argument('--user-agent=' + UA)

        self.web = webdriver.Chrome(executable_path='C:/Users/manab/github_/chromedriver.exe')
        self.end_point = "https://moneyforward.com"

        self.login(mail_address, password)

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

        if self.is_logged_in():
            return True

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div/ul/li/a/img")
        submit.click()
        time.sleep(2)

        submit = self.web.find_element_by_xpath("/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[2]/input")
        submit.click()
        time.sleep(5)

        return self.is_logged_in()

    # ホーム/最新の入出金
    def fetch_current_transactions(self):
        self.to_page(self.end_point)

        dates      = self.web.find_elements_by_class_name("recent-transactions-date")
        categories = self.web.find_elements_by_class_name("recent-transactions-category")
        shops      = self.web.find_elements_by_class_name("recent-transactions-content")
        amounts    = self.web.find_elements_by_class_name("recent-transactions-amount")

        dates      = [d.text for d in dates]
        categories = [c.text for c in categories]
        shops      = [s.text for s in shops]
        amounts    = [a.text for a in amounts]

        data = dict(Category=categories, Shop=shops, Amount=amounts)

        return pd.DataFrame(data=data, index=dates)

        # table_data = self.web.find_element_by_id("recent-transactions-table")
        # return table_data.text.split("\n")

    # ホーム/総資産
    def fetch_total_asset(self):
        self.to_page(self.end_point)

        return self.web.find_element_by_xpath('//*[@id="user-info"]/section/div[1]').text

    # ホーム/明細
    def fetch_account_statuses(self):
        """ todo: カード、銀行などで場合分け """
        self.to_page(self.end_point)

        accounts = list()
        amounts  = list()

        for i in range(30):
            try:
                accounts.append(self.web.find_element_by_xpath(f'//*[@id="registered-accounts"]/ul/li[{i+3}]/div'))
                amounts.append(self.web.find_element_by_xpath(f'//*[@id="registered-accounts"]/ul/li[{i+3}]/ul[1]'))
            except:
                break

        names  = list()
        updates  = list()
        values = list()

        for account, amount in zip(accounts, amounts):
            name, update = account.text.split("\n")
            amount, *_   = amount.text.split("\n")

            names.append(name)
            updates.append(update)
            values.append(amount)

        data = dict(Update=updates, Value=values)

        return pd.DataFrame(data=data, index=names)


    # 家計簿/月次推移/収支リスト
    def fetch_total_balances(self):
        self.to_page(self.end_point + "/cf/monthly")

        periods = self.web.find_element_by_xpath('//*[@id="monthly_list"]/tbody/tr[1]')
        periods = periods.text.split(" ")

        income = self.web.find_element_by_class_name("in_sum")
        outgo  = self.web.find_element_by_class_name("out_sum")
        total  = self.web.find_element_by_class_name("total")

        names = ["", "", ""]
        names[0], *incomes = income.text.split(" ")
        names[1], *outgos  = outgo.text.split(" ")
        names[2], *totals  = total.text.split(" ")

        return pd.DataFrame(data=[incomes, outgos, totals], columns=periods, index=names)

    # 家計簿/月次推移/収支リスト
    def fetch_category_balances(self):
        self.to_page(self.end_point + "/cf/monthly")

        periods = self.web.find_elements_by_xpath('//*[@id="monthly_list"]/tbody/tr[1]')


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
    mes = list()
    mes.append(MEDriver(config.mail1, config.pw1))
    # mes.append(MEDriver(config.mail2, config.pw2))
    # mes.append(MEDriver(config.mail3, config.pw3))

    for me in mes:
        print("\n\n")

        df = me.fetch_current_transactions()
        print(df)
        print("\n")

        total = me.fetch_total_asset()
        print(total)
        print("\n")

        df2 = me.fetch_account_statuses()
        print(df2)
        print("\n")

        df3 = me.fetch_total_balances()
        print(df3)
        print("\n")

        print("\n\n")

