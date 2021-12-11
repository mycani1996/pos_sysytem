import eel
import search
import pandas as pd
import os

#定数
SIZE_LIMIT = 1024 * 1024 * 1

@ eel.expose
def charactor_search(word):
    search.charactor_search(word)

# マスターファイル変更用関数
@ eel.expose
def change_source_file(path):
    result = file_check(path)
    if result == "":
        df = pd.read_csv(path)
        print(df.to_json())
        eel.out_order_list(df.to_json())
        df.to_csv("./master.csv",encoding="utf_8-sig", index = False)
        result = "更新完了"
    return result

def file_check(file_path):
    result:str
    result = ""
    try:
        file = open(file_path, mode='r',encoding="utf_8-sig")
    except FileNotFoundError:
        result = "ファイルが存在しません"
    else:
        file_size = os.path.getsize(file_path) 
        if file_path.endswith('.csv') == False:
            result = "csvファイルを選択してください"
        elif file_size > SIZE_LIMIT:
            result = "ファイルサイズは1MB以下にしてください"
        else:
            result = check_master_format(file_path)
        file.close()
    return result

def check_master_format(file_path):
    result:str
    result = ""
    df = pd.read_csv(file_path)
    if len(df.columns) != 3:
        result = "フォーマットエラー。列数を確認して下さい"
    return result

# 注文追加
# @ eel.expose
# def add_order(order):

