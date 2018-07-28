from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from chatterbot import ChatBot
from random import randint
import MySQLdb
import requests
import json
import multiprocessing
import time


botList = []
botnum = 700
while botnum < 1000:
    chatbot = ChatBot(
        "bot" + str(botnum),
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database='./Brain/'+str(botnum)+'.sqlite3',
        read_only=True,
    )
    botList.append(chatbot)
    botnum+=100


def job(index, msg,return_list):
    response = botList[index].get_response(msg)
    print("回應: " + response.text + "(" +str(response.confidence) +")")
    if(response.confidence >= 0.4):
        print({"confidence":response.confidence, "lys":response.text})
        queryy = "SELECT `kkboxID`, `Artists`,`SongName` FROM `LyricsData` WHERE `Lyrics` like '%"+response.text+"%'"
        print("queryy = " + queryy)
        cursor.execute(queryy)
        record = cursor.fetchone()
        kkboxID = record[0]
        Artists = record[1]
        SongName = record[2]
        return_list.append({"confidence":response.confidence,
            "kkboxID":kkboxID,"Artists":Artists,"Lry":response.text,"SongName":SongName})        

def SaveSongMsg(data):   
    print("in getSongID_andSave()")
    if(len(songIDList) == 0):
        insideData = {
            'ID':data['kkboxID'],
            'times':1,
            'Artists':data['Artists'],
            "Confidence":data['confidence']
        }
        songIDList.append(insideData)
    else:
        dd = [d for d in songIDList if d.get('ID')==data['kkboxID']]
        if(len(dd) == 0): #如果不存在
            insideData = {
                'ID':data['kkboxID'],
                'times':1,
                'Artists':data['Artists'],
                "Confidence":data['confidence']
            }
            songIDList.append(insideData)
        else:
            for i in range(len(songIDList)):
                if(songIDList[i]['ID'] == data['kkboxID']):
                    songIDList[i]['times'] = songIDList[i]['times'] + 1
                    break
    
def getBotResponse(msg):
    manager = multiprocessing.Manager()
    return_list = manager.list()
    pList = []
    for i in range(len(botList)):
        p = multiprocessing.Process(target=job, args=[i, msg,return_list])
        p.start()
        pList.append(p)
    for p in pList:
        p.join()
    for dd in return_list:
        SaveSongMsg(dd)
    return_list = sorted(return_list, key=lambda s: s['confidence'], reverse=True)
    print("return_list = "+ str(return_list))
    return return_list
        

def getSinger(msg):
    queryy = "SELECT `Artists` FROM `LyricsData` WHERE `Lyrics` like '%"+msg+"%'"
    cursor.execute(queryy)
    record = cursor.fetchone()
    return str(record[0])

def getSongCount(msg):
    return str(len(msg))

def getSongURL():
    print("In getSongURL")
    '''global songIDList
    songIDList = sorted(songIDList, key=lambda s: s['Confidence'], reverse=True)
    print(songIDList)
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
            print("URL~~ http://140.138.77.90:3005/youtubeLink/"+songIDList[i]['ID'])
            r = requests.get('http://140.138.77.90:3005/youtubeLink/' + songIDList[i]['ID'])
            rData = json.loads(r.text)
            urlList.append(rData["youtubeLink"])
    print("urlList = "+ str(urlList))'''
    return "~~give url~~"



def isNegation(msg):
    msg = msg.replace(" ","")
    if(msg=="不是"):
        return 1
    else:
        return 0
def isPositive(msg):
    msg = msg.replace(" ","")
    if(msg=="是"):
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
    msg = event.message.text
    global chooseArtist
    global whitelist
    global blacklist
    if(msg == "哈囉"):
        msg = "猜歌詞遊戲開始！！你可以任意地與機器人對話\n>>當想要bot給出歌曲時，請說「給我歌曲吧」\n>>若想重玩，請說「我要重玩」"
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= str(msg)))
    elif(msg.find("給我歌曲")!=-1):
        tempUrlList = getSongURL()
        print("給我歌曲 " + str(tempUrlList))
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= str(songIDList) + "\n\n白名單 " + str(whitelist) + "\n\n黑名單 " + str(blacklist)))
        '''tempUrlList = getSongURL()
        msg = ""
        for dd in tempUrlList:
            msg = msg + '\n\n' + dd
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= str(msg)))'''
    elif(msg.find("我要重玩")!=-1):
        songIDList.clear()
        whitelist.clear()
        blacklist.clear()
        chooseArtist = ""
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "沒問題!!\n\n猜歌遊戲，開始"))
    elif(isNegation(msg)==1):
        print("blackList: " + chooseArtist)
        blacklist.append(chooseArtist)
        chooseArtist = ""
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "ㄎㄎ，再給我一些提示吧"))
    elif(isPositive(msg)==1):
        print("whiteLisr: " + chooseArtist)
        whitelist.append(chooseArtist)
        chooseArtist = ""
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "哈哈，我們繼續~~"))
    else:
        # 非關鍵字類
        print("num = " + str(num))
        response = getBotResponse(msg)
        print("response = " + str(response))
        if(len(response)==0):
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text= "好難喔，再給我清楚一點的提示吧"))
        elif(num % 6 == 0):
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text= "恩恩，再給我一些提示"))
        elif(num % 6 == 1):
            print("chooseArtist = " + str(chooseArtist))
            chooseArtist = response[0]["Artists"]
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text= "你喜歡"+response[0]["Artists"]+"齁 (是/不是)"))           
        else:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text=response[0]["Lry"]))

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
    # 黑白名單
    whitelist = []
    blacklist = []
    chooseArtist = ""


    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)