import eel
import common.desktop as desktop
import common.common as common
from pos_system import PosSystem
import eel_function
import pandas as pd
import datetime

# 定数を定義
APP_NAME="html"
END_POINT="index.html"
SIZE=(700,600)
MASTER_FILE_PATH = './master.csv'
OUT_FILE_PATH = './receipt/{export_at}.txt'

# 初期マスタ設定用
@eel.expose
def set_master_item(path):
    if path == "init":
        path = MASTER_FILE_PATH
    global order_master
    order_master = PosSystem()
    order_master.set_master(path)

# 注文追加用
@eel.expose
def add_order(code,amount:int):
    global order_master
    order_master.set_order_Item(code,amount)

# 注文削除用
@eel.expose
def delete_order(data):
    global order_master
    # print(data)
    order_master.delete_Master(data)

# 会計用
@eel.expose
def payment(deposit_price:int):
    global order_master
    order_master.pay_master(deposit_price)

if __name__ == "__main__":
    common.write_log("start")
    desktop.start(APP_NAME,END_POINT,SIZE)
    # main()