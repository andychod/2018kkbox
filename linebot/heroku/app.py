from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from chatterbot import ChatBot
from hanziconv import HanziConv
from random import randint
import MySQLdb
import requests
import json


chatbot = ChatBot(
    "Andy",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./Brain.sqlite3',
    read_only=True,
)


def getSinger(msg):
    queryy = "SELECT `Artists` FROM `LyricsData` WHERE `Lyrics` like '%"+msg+"%'"
    cursor.execute(queryy)
    record = cursor.fetchone()
    return str(record[0])

def getSongCount(msg):
    queryy = "SELECT `SongName` FROM `LyricsData` WHERE `Lyrics` like '%"+msg+"%'"
    cursor.execute(queryy)
    record = cursor.fetchone()
    return str(len(record[0]))

def getSongURL():
    # sort songIDList
    global songIDList
    songIDList = sorted(songIDList, key=lambda s: s['times'], reverse=True)
    size = len(songIDList)
    urlList = []
    if(size < 3):
        for dd in songIDList:
            print("ID = " + str(dd['ID']))
            r = requests.get('http://140.138.77.90:3005/youtubeLink/' + dd['ID'])
            rData = json.loads(r.text)
            urlList.append(rData["youtubeLink"])
    else:
        for i in range(3):
            r = requests.get('http://140.138.77.90:3005/youtubeLink/' + songIDList[i]['ID'])
            rData = json.loads(r.text)
            urlList.append(rData["youtubeLink"])
    return urlList

def getSongID_andSave(msg):
    queryy = "SELECT `kkboxID` FROM `LyricsData` WHERE `Lyrics` like '%"+msg+"%'"
    print("queryy = " + queryy)
    cursor.execute(queryy)
    record = cursor.fetchone()
    kkboxID = record[0]
    if(len(songIDList) == 0):
        insideData = {
            'ID':kkboxID,
            'times':1
        }
        songIDList.append(insideData)
    else:
        dd = [data for data in songIDList if data.get('ID')==kkboxID]
        if(len(dd) == 0): #如果不存在
            insideData = {
                'ID':kkboxID,
                'times':1
            }
            songIDList.append(insideData)
        else:
            for i in range(len(songIDList)):
                if(songIDList[i]['ID'] == kkboxID):
                    songIDList[i]['times'] = songIDList[i]['times'] + 1
                    break
    return kkboxID

def isNegation(msg):
    if(msg.find("不是喔")!=-1 or msg.find("不對ㄟ")!=-1 or msg.find("猜錯了")!=-1  or msg.find("並沒有")!=-1 or msg.find("沒有喔")!=-1):
        return 1
    else:
        return 0
def isPositive(msg):
    if(msg.find("對ㄟ")!=-1 or msg.find("被你猜中")!=-1 or msg.find("猜中")!=-1 or msg.find("賓果")!=-1):
        return 1
    else:
        return 0

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('1x3tkmuJT7Y+LORs2KNo3S+oRO06bxqGu0Ae8mhbyw4QxnKxMM/SrOrAEcxWRfgRcWX/yW/4Zo/GcUESjM2A628+jIgyguCjAQnMKyzaLvSmRl3SN8o+c6NrUFgDua/gFuNeL+akOpL/BML7rtJvLAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('459c943dbc44c451205d64803d3513a5')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    num = randint(1, 17)
    print("num = " + str(num))
    msg = event.message.text

    lys = chatbot.get_response(msg).text
    print("Log : seccessful~~~~")
    line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text= lys))

    '''if(msg == "哈囉"):
        msg = "猜歌詞遊戲開始！！你可以任意地與機器人對話\n>>當想要bot給出歌曲時，請說「給我歌曲吧」\n>>若想重玩，請說「我要重玩」"
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= str(msg)))
    elif(msg.find("給我歌曲")!=-1):
        tempUrlList = getSongURL()
        msg = ""
        for dd in tempUrlList:
            msg = msg + '\n\n' + dd
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= str(msg)))
    elif(msg.find("我要重玩")!=-1):
        songIDList.clear()
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "沒問題!!\n\n猜歌遊戲，開始"))
    elif(isNegation(msg)==1):
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "ㄎㄎ，再給我一些提示吧"))
    elif(isPositive(msg)==1):
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "哈哈，我們繼續~~"))
    elif(num % 6 == 0 ):
        lys = chatbot.get_response(msg).text
        lys = (lys.split(" "))[0]
        getSongID_andSave(lys)
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "恩恩，再給我一些提示"))
    elif(num % 6 == 1):
        lys = chatbot.get_response(msg).text
        lys = (lys.split(" "))[0]
        getSongID_andSave(lys)
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "你喜歡"+getSinger(lys)+"齁"))
    elif(num % 6 == 2):
        lys = chatbot.get_response(msg).text
        lys = (lys.split(" "))[0]
        getSongID_andSave(lys)
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "我猜，這首歌好像是"+getSongCount(lys)+"個字喔~~"))
    else:
        lys = chatbot.get_response(msg).text
        lys = (lys.split(" "))[0]
        response = lys
        getSongID_andSave(lys)
        line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text= response))'''

    '''if(msg.find("給我歌曲")!=-1):
        print("Bot: ~~給歌曲url~~")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "~~給歌曲url~~"))


    else:
        response = "是不是有這句阿:「" + chatbot.get_response(msg).text + "」"
        print("Bot:  是不是有這句阿:「" + response+"」")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= response))'''

    '''ss = chatbot.get_response(event.message.text)
    message = TextSendMessage(text= ss.text)
    line_bot_api.reply_message(event.reply_token, message)'''

import os
if __name__ == "__main__":
    db = MySQLdb.connect(host="140.138.77.90",
        user="visteam", passwd="RR10706b", db="kkbox2018",charset='utf8')
    cursor = db.cursor()

    # 存入歌曲的kkboxID
    songIDList = []
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)