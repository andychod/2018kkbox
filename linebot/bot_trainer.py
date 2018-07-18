# 引入 ChatBot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
# 開檔讀檔用
import os
import json

# 傳入檔案名，回傳整份檔案內容
def getOntLyric(filename):
    with open('lyrics_list\\'+ filename, 'r', encoding="utf8") as f:
        data = json.load(f)
    return data

#設定機器人屬性
chatbot = ChatBot(
    "Andy",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3'
)
chatbot.set_trainer(ListTrainer)
#chatbot.set_trainer(ChatterBotCorpusTrainer)

path = "D:\DATA\line_bot\lyrics_list" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称

for filename in files:
    trainArray = getOntLyric(filename)
    print(trainArray)
    chatbot.train(trainArray)

