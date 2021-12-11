import pandas as pd
import eel

### デスクトップアプリ作成課題
def charactor_search(word):
    print_txt:str
    # 検索対象取得
    df=pd.read_csv("./source.csv")
    source=list(df["name"])

    # 検索
    if word in source:
        print_txt = "『{}』はあります".format(word)
    else:
        print_txt = "『{}』はありません、追加します".format(word)
        source.append(word)
    
    # CSV書き込み
    df=pd.DataFrame(source)
    df.columns = ["name"]
    df.to_csv("./source.csv",encoding="utf_8-sig")
    eel.view_log_js(print_txt)
