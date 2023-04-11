# -*- config: utf-8 -*-
import sys
sys.path.append('../notifybot')

import time
import pandas as pd
import matplotlib.pyplot as plt
from MeDriver import MeDriver
from line_notify_bot import LineNotifyBot
from df_func import df_to_png
import config


class MeClient:
    def __init__(self, mail_address, password):
        self.driver = MeDriver(mail_address, password)
        self.lineNotifyBot = LineNotifyBot(config.ACCESS_TOKEN)

        self.png_path = "C:\\Users\\manab\\github_\\manageMoney\\pngs\\df1.png"

    def extract_total_asset(self):
        return self.driver.fetch_total_asset()

    def extract_total_balances(self):
        return self.driver.fetch_total_balances()

    def extract_recent_transactions(self):
        df = self.driver.fetch_recent_transactions()

        try:
            return df[["利用日", "店舗", "金額"]]
        except:
            return None

    def extract_account_statuses(self):
        return self.driver.fetch_account_statuses()

    def extract_monthly_total_balances(self):
        df = self.driver.fetch_total_balances()

        try:
            df = df.set_index("分類")
            df = df.transpose()
        except:
            return None

        return df[["収入合計", "支出合計", "収支合計"]]

    def extract_monthly_balances(self, columns=[]):
        df = self.driver.fetch_monthly_balances()

        df = df.transpose()

        if not columns:
            columns = list(df.columns)

        df = df[columns].transpose()

        return df
        """
        except:
            return None
        """

    def extract_monthly_budgets(self, offset_month=0):
        if not (type(offset_month) in (str, int)):
            return None

        df, period = self.driver.fetch_monthly_budgets(offset_month)

        return df, period

    def send_df(self, df, header=None, message="df", plot_index=False):
        if df is None or df.empty:
            return

        if header is None:
            df_to_png(df, plot_index=plot_index, png_path=self.png_path)
        else:
            df_to_png(df, plot_index=plot_index, header=header, png_path=self.png_path)

        self.lineNotifyBot.send(message=message, image=self.png_path)


if __name__ == '__main__':
    mes = list()

    mes.append(MeClient(config.mail1, config.pw1))
    # mes.append(MeClient(config.mail2, config.pw2))
    # mes.append(MeClient(config.mail3, config.pw3))
    # mes.append(MeClient(config.mail4, config.pw4))

    for me in mes:
        _ = me.extract_total_asset()
        _ = me.extract_total_balances()
        _ = me.extract_recent_transactions()
        _ = me.extract_account_statuses()
        _ = me.extract_monthly_total_balances()
        _ = me.extract_monthly_balances()
        print(_)
        _ = me.extract_monthly_budgets()
        _ = me.extract_monthly_budgets(offset_month=3)
        time.sleep(5)
