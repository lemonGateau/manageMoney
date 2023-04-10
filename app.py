import os
import datetime
from flask import *


app = Flask(__name__)

key = os.urandom(21)
app.secret_key = key

#空き情報を表示するトップページ
@app.route("/", methods=["POST", "GET"])
def index():
    if (request.method == "GET"):
        now_location = "東京駅"
    if (request.method == "POST"):
        now_location = request.form["now_location"]

    return render_template("index.html", parkA = A, parkB = B, parkC = C, map = map, distance_all = distance_all)


@app.route("/park/<string:park_name>")
def show_park(park_name):
    seki.read_seki()
    if not seki.parks:
        return redirect(url_for("index"))
    
    park = park_name

    if(park == 'A'):
        park_info = seki.parks[0]
    if(park == 'B'):
        park_info = seki.parks[1]
    if(park == 'C'):
        park_info = seki.parks[2]

    session["park_name"] = park_name

    return render_template("parkInfo.html", park_name = park, park_info = park_info, len = len(park_info))

@app.route("/check")
def check():
    return render_template("check.html")

@app.route("/cancell", methods=["POST"])
def cancell():
    r.ReserveData.r_num = request.form["r_num"]
    park_name = r.to_park_name(r.ReserveData.r_num)
    file_name = r.to_file_name(r.ReserveData.r_num)

    res = r.find_reserve(file_name, r.ReserveData.r_num)

    # 予約番号が見当たらない場合
    if res is None:
        return render_template("check.html")

    r.ReserveData.r_park = res[2]

    return render_template("cancell.html", r_num=r.ReserveData.r_num, park_name=park_name, name=res[1], park=res[2], month=res[3], day=res[4], hour=res[5], minute=res[6])


@app.route("/cancell_complete", methods=["POST"])
def cancell_complete():
    park_name = r.to_park_name(r.ReserveData.r_num)
    file_name = r.to_file_name(r.ReserveData.r_num)

    seki.empty_seki(park_name, r.ReserveData.r_park)
    r.cancell_reserve(r.ReserveData.r_num)

    return render_template("cancell_complete.html")


@app.route("/reserve")
def hello_world():
    park_name = session.get("park_name")
    if(park_name == 'A'):
        num = 0
    elif(park_name == 'B'):
        num = 1
    elif(park_name == 'C'):
        num = 2
    
    return render_template("reserve.html",a="予約情報を入力してください",park_name=park_name, park_size = len(seki.parks[num]), park_info = seki.parks[num])

@app.route("/result", methods=["POST"])
def information_cheak():
    r.ReserveData.r_name =request.form["r_name"]
    r.ReserveData.r_park=int(request.form["r_park"])
    afterminute=int(request.form["afterminute"])
   
    r.error_check(afterminute)

    return render_template("result.html",name=r.ReserveData.r_name,park=r.ReserveData.r_park,month=r.ReserveData.r_month,day=r.ReserveData.r_day,hour=r.ReserveData.r_hour,minute=r.ReserveData.r_minute,success_message="success_message",park_name=session.get("park_name"))
    """
    else:
        return render_template("result.html",error_message="入力情報に間違いがあります.駐車番号や日付の入力に間違いがないかご確認ください" )
    """

@app.route("/pay_select")
def select():
    return render_template("pay_select.html")

@app.route("/enter_pay", methods=["POST"])
def select_pay_method():
    pay_method = request.form["pay_method"]

    if pay_method == "credit_card":
        return render_template("enter_pay.html")

    if pay_method == 2:
        return render_template("enter_pay2.html")

    if pay_method == 3:
        return render_template("enter_pay3.html")

@app.route("/result_pay", methods=["POST"])
def enter_pay_info():
    card_num = request.form["card_num"]
    secret_num = request.form["secret"]
    valid_month = request.form["month"]
    valid_year = request.form["year"]

    if pay.error_check():
        # card_num[:4]で上4桁のみ渡す
        return render_template("result_pay.html", park_name=session.get("park_name"), name=r.ReserveData.r_name, park=r.ReserveData.r_park, \
        month=r.ReserveData.r_month, date=r.ReserveData.r_day, hour=r.ReserveData.r_hour, minute=r.ReserveData.r_minute, top4=card_num[:4], success_message="success_message")


@app.route("/complete", methods=["POST"])
def complete():
    reserve_com=int(request.form["reserve_com"])

    if(reserve_com ==1):
        park_name = session.get("park_name")

        # 空きなら予約（リロードによる2重書き込み対策）
        if seki.is_empty(park_name, r.ReserveData.r_park):
            seki.fill_seki(park_name, r.ReserveData.r_park)
            r.add_information(park_name)

    return render_template("/complete.html", r_num=r.ReserveData.r_num)


#トップページへの再アクセスパス
@app.route("/reload")
def reload():
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(debug=True)
