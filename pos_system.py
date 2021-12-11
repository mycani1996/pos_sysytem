import eel
import common.common as common
import search
import eel_function
import pandas as pd
import datetime

# 定数を定義
SIZE_LIMIT = 1024 * 1024 * 1
now = datetime.datetime.now()
LOG_FILE_PATH = f'./log/log_{now.strftime("%Y%m%d_%H%M%S")}.log'
MASTER_FILE_PATH = './master.csv'
OUT_FILE_PATH = './receipt/{export_at}.txt'

### マスタークラス
class PosSystem:
    def __init__(self):
        self.master = []
        self.order = None

    def set_master(self,path):
        if common.file_check(path,".csv",SIZE_LIMIT):
            self.master = []
            df = pd.read_csv(path)
            # print(df.to_json())
            for item in df.itertuples():
                common.write_log(f"マスタテーブルに{item[2]}登録")
                self.master.append(Item(str(item[1]),item[2],int(item[3])))
            common.write_log("マスタ登録完了")
            eel.out_order_list(df.to_json())
            df.to_csv(MASTER_FILE_PATH,encoding="utf_8-sig",index=False)
            self.order = None
            
    def get_master(self,code):
        result_item = None
        for item in self.master:
            if item.get_code() == code:
                result_item = item
                break
        return result_item

    def set_order_Item(self,code,amount:int):
        name = None
        item = self.get_master(code)
        if self.order == None:
            common.write_log("オーダー初期化")
            self.order = Order()
        if item != None:
            common.write_log("オーダー追加処理開始")
            self.order.add_order_Item(item,amount)
        else:
            eel.alert_js("マスターにありません")
            
    def delete_Master(self,data):
        common.write_log("オーダー削除処理開始")
        self.order.delete_order_Item(data)
            
    def pay_master(self,deposit:int):
        common.write_log("会計処理開始")
        self.order.order_pay(deposit)

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price

    def get_code(self):
        return self.item_code

    def get_name(self):
        return self.item_name
            
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    deposit = 0
    order_price = 0
    order_count = 0
    def __init__(self):
        self.deposit = 0
        self.order_price = 0
        self.order_list=[]

    # 注文を追加
    def add_order_Item(self,item,amount:int):
        order_data = {"data":item,"amount":amount}
        self.order_list.append(order_data)
        common.write_log(f"{item.get_name()}を{amount}個注文に追加")
        self.total_val()

    # 注文を削除
    def delete_order_Item(self,data):
        for id in data:
            del self.order_list[id]
            common.write_log(f"注文{id}個目を削除")
        self.total_val()

    # 合計額を算出
    def total_val(self):
        self.order_price = 0
        for item in self.order_list:
            self.order_price += int(item["data"].get_price()) * int(item["amount"])
        common.write_log(f"合計額が{self.order_price}に変更")
        eel.out_total_price(self.order_price)

    # 支払い処理
    def order_pay(self,deposit:int):
        if (int(self.order_price) - int(deposit)) > 0:
            common.write_log("受領額不足")
            eel.alert_js("不足しています")
        else:
            common.write_log(f"受領額登録：{deposit}")
            self.deposit = deposit
            self.make_reciept()
    
    # レシート作成
    def make_reciept(self):
        time = datetime.datetime.now()
        reciept_text = "=======レシート=======\n"
        reciept_text += f'日時：{time.strftime("%Y/%m/%d_%H:%M:%S")}\n'
        reciept_text += "======購入リスト======\n"
        n = 0
        for item in self.order_list:
            n = n + 1
            price = int(item["data"].get_price()) * int(item["amount"])
            reciept_text += f'{n}. {item["data"].get_name()}×{item["amount"]}個：¥{price}\n'
        reciept_text += "========金額=========\n"
        reciept_text += f"合計額：¥{self.order_price}\n"
        reciept_text += f"お預かり金：¥{self.deposit}\n"
        reciept_text += f"お釣り{int(self.deposit) - int(self.order_price)}\n"
        reciept_text += "====================\n"
        out_file_path = OUT_FILE_PATH.format(export_at=time.strftime('%Y%m%d_%H%M%S'))
        with open(out_file_path,'w') as f:
            f.write(reciept_text)
            common.write_log("レシート出力完了")
            eel.alert_js("お買い上げありがとうございました")  



