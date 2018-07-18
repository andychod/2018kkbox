# 引入 ChatBot
from chatterbot import ChatBot

from random import randint

from chatterbot.trainers import ListTrainer

chatbot = ChatBot(
    "Andy",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3',
    read_only=True,
)


def getSinger(msg):
    # doing something
    return "[某某歌手]"

def getSongCount(msg):
    # doing something
    return "[n]"

def isNegation(msg):
    if(msg.find("不是喔")!=-1 or msg.find("不是喔")!=-1 or msg.find("猜錯了")!=-1 or msg.find("並沒有")!=-1):
        return 1
    else:
        return 0
def isPositive(msg):
    if(msg.find("對ㄟ")!=-1 or msg.find("被你猜中")!=-1 or msg.find("猜中")!=-1 or msg.find("賓果")!=-1):
        return 1
    else:
        return 0




print("猜歌詞遊戲，開始")
print("Bot: 我猜你心中一定想著某幾首歌吧？請你描述一下，我來猜猜看！")
for i in range(20):
    msg = input("Me : ")
    num = randint(1, 17)

    if(msg.find("給我歌曲")!=-1):
        print("Bot: ~~給歌曲url~~")
        break
    elif(isNegation(msg)==1):
        print("Bot: ㄎㄎ，再給我一些提示吧")
    elif(isPositive(msg)==1):
        print("Bot: 哈哈，我們繼續~~")
    elif(num % 4 == 0 ):
        print("Bot: 恩恩，再給我一些提示")
    elif(num % 4 == 1):
        print("Bot: 你喜歡"+getSinger(msg)+"齁")
    elif(num % 4 == 2):
        print("Bot: 我猜，這首歌好像是"+getSongCount(msg)+"個字喔~~")
    else:
        response = chatbot.get_response(msg)
        print("Bot:  是不是有這句阿:「" + response.text+"」")
