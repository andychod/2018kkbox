# 引入 ChatBot
from chatterbot import ChatBot

from chatterbot.trainers import ListTrainer

chatbot = ChatBot(
    "Andy",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3',
    read_only=True,
)


print("歌詞接龍，ready go!")
for i in range(20):
    msg = input("請輸入：")
    response = chatbot.get_response(msg)
    print("> " + response.text)
