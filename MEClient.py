# -*- config: utf-8 -*-
import sys
sys.path.append('../notifybot')

import time
import pandas as pd
import matplotlib.pyplot as plt
from MEDriver import MEDriver
from line_notify_bot import LineNotifyBot
from df_func import df_to_png
import config


class MEClient:
    def __init__(self, mail_address, password):
        self.driver = MEDriver(mail_address, password)
        self.lineNotifyBot = LineNotifyBot(config.ACCESS_TOKEN)

        self.png_path = "C:\\Users\\manab\\github_\\manageMoney\\pngs\\df1.png"

    def send_total_asset(self):
        total_asset = self.driver.fetch_total_asset()

        self.lineNotifyBot.send(message=f"収入 = {total_asset}")

        return total_asset

    def send_current_transactions(self):
        df = self.driver.fetch_current_transactions()

        if df.empty:
            self.lineNotifyBot(message="直近の入出金はありません")
            return

        df = df[["店舗", "金額"]]

        df_to_png(df, plot_index=True, header=df.columns, png_path=self.png_path)

        self.lineNotifyBot.send(message="最新の入出金", image=self.png_path)

        return df

    def send_account_statuses(self):
        df = self.driver.fetch_account_statuses()

        if df.empty:
            return

        df_to_png(df, plot_index=True, header=df.columns, png_path=self.png_path)

        self.lineNotifyBot.send(message="金融明細", image=self.png_path)

        return df

    def send_monthly_total_balances(self):
        df = self.driver.fetch_monthly_balances()

        if df.empty:
            return

        df = df.transpose()
        df = df[["収入合計", "支出合計", "収支合計"]]

        df_to_png(df, plot_index=True, header=df.columns, png_path=self.png_path)

        self.lineNotifyBot.send(message="収支", image=self.png_path)

        return df

    def send_monthly_balance(self):
        pass

    def send_monthly_budgets(self, offset_month=0):
        if not (type(offset_month) in (str, int)):
            return None

        period, df = self.driver.fetch_monthly_budgets(offset_month)
        if df.empty:
            return

        period = period.replace("-", "~")
        df_to_png(df, plot_index=True, header=df.columns, png_path=self.png_path)

        self.lineNotifyBot.send(message=period, image=self.png_path)

        return df


if __name__ == '__main__':
    mes = list()

    mes.append(MEClient(config.mail1, config.pw1))
    # mes.append(MEClient(config.mail2, config.pw2))
    # mes.append(MEClient(config.mail3, config.pw3))
    # mes.append(MEClient(config.mail4, config.pw4))

    for me in mes:
        _ = me.send_total_asset()
        _ = me.send_current_transactions()
        _ = me.send_account_statuses()
        _ = me.send_monthly_total_balances()
        _ = me.send_monthly_budgets()
        _ = me.send_monthly_budgets(offset_month=3)
        time.sleep(5)
