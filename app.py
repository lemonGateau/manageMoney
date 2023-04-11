import os
import datetime
from flask import *
import config
from MeClient import MeClient


app = Flask(__name__)

key = os.urandom(21)
app.secret_key = key


# トップページ
@app.route("/")
def index():
    try:
        total_asset = app.me_client.extract_total_asset()
        df_balances, balance_period = app.me_client.extract_total_balances()
        df_recents = app.me_client.extract_recent_transactions()
    except:
        return redirect(url_for("login"))

    return render_template("index.html",
                           total_asset=total_asset,
                           balance_period=balance_period,
                           df_balances=df_balances,
                           df_recents=df_recents
                           )

@app.route("/login")
def login():
    app.me_client = MeClient(config.mail1, config.pw1)

    return redirect(url_for("index"))

@app.route("/balances")
def balances():
    try:
        df_balances = app.me_client.extract_monthly_balances()
    except:
        return redirect(url_for("login"))

    return render_template("balances.html",
                           df_balances=df_balances)

@app.route("/budgets")
def budgets():
    try:
        df_budgets, period = app.me_client.extract_monthly_budgets()
    except:
        return redirect(url_for("login"))

    return render_template("budgets.html",
                           period=period,
                           df_budgets=df_budgets)

@app.route("/financial_accounts")
def financial_accounts():
    try:
        df_accounts = app.me_client.extract_account_statuses()
    except:
        return redirect(url_for("login"))

    return render_template("financial_accounts.html",
                           df_accounts=df_accounts)


#トップページへの再アクセスパス
@app.route("/reload")
def reload():
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host="127.0.0.85", port=7200, debug=True)
