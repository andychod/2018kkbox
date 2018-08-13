# 引入 ChatBot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
# 開檔讀檔用
import json


#設定機器人屬性
chatbot = ChatBot(
    "Brain",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='brenchmark.sqlite3'
)
chatbot.set_trainer(ListTrainer)
#chatbot.set_trainer(ChatterBotCorpusTrainer)
# 讀檔
with open('trainData.json', 'r',encoding="'utf-8-sig'") as f:
    file = json.load(f)
    f.close()
chatbot.train(file)
print('訓練  完成 ~~')
