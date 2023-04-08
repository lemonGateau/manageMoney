# -*- config: utf-8 -*-
import sys
sys.path.append('../notifybot')

import pandas as pd
import matplotlib.pyplot as plt
from MEDriver import MEDriver
from line_notify_bot import LineNotifyBot
import config


class MEClient:
    def __init__(self, mail_address, password):
        self.driver = MEDriver(mail_address, password)
        self.lineNotifyBot = LineNotifyBot(config.ACCESS_TOKEN)

    def fetch_financial_account_names(self):
        df = self.driver.fetch_account_statuses()
        # df = df.reset_index()

        f = plt.figure(figsize=(df.shape[1], df.shape[0]))
        a = f.gca()
        a.axis("off")

        a.table(cellText=df.values,
                 colLabels=df.columns,
                 loc="center",
                 bbox=[0,0,1,1])

        plt.tight_layout()
        plt.savefig("C:\\Users\\manab\\github_\\manageMoney\\pngs\\df1.png")

        # self.lineNotifyBot.send(message="df", image="C:\\Users\\manab\\github_\\manageMoney\\pngs\\df1.png")
        # plt.show()

        # self.lineNotifyBot.send(message=df.to_markdown())

if __name__ == '__main__':
    meC = MEClient(config.mail1, config.pw1)
    meC.fetch_financial_account_names()
