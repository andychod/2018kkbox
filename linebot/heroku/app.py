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
    if(msg.find("不是喔")!=-1 or msg.find("不是喔")!=-1 or msg.find("猜錯了")!=-1  or msg.find("並沒有")!=-1 or msg.find("沒有喔")!=-1):
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

    if(msg.find("給我歌曲")!=-1):
        print("Bot: ~~給歌曲url~~")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "~~給歌曲url~~"))
    elif(isNegation(msg)==1):
        print("Bot: ㄎㄎ，再給我一些提示吧")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "ㄎㄎ，再給我一些提示吧"))
    elif(isPositive(msg)==1):
        print("Bot: 哈哈，我們繼續~~")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "哈哈，我們繼續~~"))
    elif(num % 4 == 0 ):
        print("Bot: 恩恩，再給我一些提示")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "恩恩，再給我一些提示"))
    elif(num % 4 == 1):
        lys = chatbot.get_response(msg).text
        print("Bot: 你喜歡"+getSinger(lys)+"齁")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "你喜歡"+getSinger(lys)+"齁"))
    elif(num % 4 == 2):
        lys = chatbot.get_response(msg).text
        print("Bot: 我猜，這首歌好像是"+getSongCount(lys)+"個字喔~~")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= "我猜，這首歌好像是"+getSongCount(lys)+"個字喔~~"))
    else:
        response = "是不是有這句阿:「" + chatbot.get_response(msg).text + "」"
        print("Bot:  是不是有這句阿:「" + response+"」")
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text= response))

    '''ss = chatbot.get_response(event.message.text)
    message = TextSendMessage(text= ss.text)
    line_bot_api.reply_message(event.reply_token, message)'''


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
