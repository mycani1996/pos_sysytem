import eel
import pandas as pd
import os
import datetime
import common.common as common

# 定数定義
now = datetime.datetime.now()
LOG_FILE_PATH = f'./log/log_{now.strftime("%Y%m%d_%H%M%S")}.log'

## ログ機能用関数
def write_log(log_str):
    now_log = datetime.datetime.now()
    with open(LOG_FILE_PATH, mode='a+') as log_file:
        log_file.writelines(f"{str(now_log)}:{str(log_str)}\n")

## ファイルチェック
def file_check(path,type,size):
    result = True
    result_text:str
    result_text = "エラー"
    try:
        file = open(path, mode='r',encoding="utf_8-sig")
    except FileNotFoundError:
        result_text = "ファイルが存在しません"
        result = False
    else:
        file_size = os.path.getsize(path) 
        if path.endswith(type) == False:
            result_text = "csvファイルを選択してください"
            result = False
        elif file_size > size:
            result_text = "ファイルサイズは1MB以下にしてください"
            result = False
        elif check_master_format(path) == False:
            result_text = "フォーマットエラー"
            result = False
        file.close()
    if result == False:
        eel.alert_js(result_text)
    return result

def check_master_format(path):
    result = True
    df = pd.read_csv(path)
    if len(df.columns) != 3:
        result = False
    return result