# -*- coding: utf-8 -*-
# 引入 ChatBot
from chatterbot import ChatBot
from random import randint
import json
import threading
# 黑白名單
chatbot = ChatBot(
        "bot",
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database='brenchmark.sqlite3',
        read_only=True,
)

def checkSame(s1 ,s2):
        s1 = s1.replace(" ", "")
        s2 = s2.replace(" ", "")
        return (s1 == s2)

# 讀取測試檔
with open('測試.json', 'r',encoding="'utf-8-sig'") as f:
    TestFile = json.load(f)

print("Brenchmark 開始!!")

errorlist = []
report = {
        "準確歌詞": 0,
        "有缺歌詞": 0,
        "模糊歌詞": 0
}
for data in TestFile:
        response = chatbot.get_response(data['input']).text
        if(checkSame(response,data['ans'])):
                print("測資" + str(data['id']) + "("+data['type']+ ") OK")
        else:
                print("測資" + str(data['id']) + "("+data['type']+ ") error~~~")
                print("\tinput: " + data['input'])
                print("\toutput: " + response)
                print("\tans: " + data['ans'])
                xx = {
                        "input": data['input'],
                        "output": response,
                        "answer": data['ans']
                }
                errorlist.append(xx)
                report[data['type']] +=1

print("\n結果分析:")
print("準確歌詞錯誤數: "+ str(report['準確歌詞']) + "/10")
print("有缺歌詞錯誤數: "+ str(report['有缺歌詞']) + "/10")
print("模糊歌詞錯誤數: "+ str(report['模糊歌詞']) + "/10")

if len(errorlist) > 0:
        print("\n<產生錯誤報表>")
        with open('errorReport.json', 'w',encoding="utf-8") as f:
                json.dump(errorlist, f, ensure_ascii=False,indent=4)
                f.close()




