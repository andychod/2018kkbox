# 文件說明<br>

## 1.訓練機器人模型   (bot_trainer.py)<br>
使用他須要安裝chatterbot和import os, json，同時需要將訓練資料集放在同目錄下的lyrics_list中。訓練完的模型預設會存在同一層目錄之下，名稱為database.sqlite3，下面是設定的程式碼<br>
```python
#設定機器人屬性
chatbot = ChatBot(
    "Andy",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3'
)
```
<br>
資料集的的格式為一首歌存成一個json檔，檔名為"歌名.json"。內容規格如下<br>

```json
[
    "歌詞1",
    "歌詞2",
    ...,
    "歌詞1",
]
```
比較怪的地方是需要在尾句再次放上第一句歌詞。<br>

## 2.對話機器人模型   (play.py)<br>
使用他只需要安裝chatterbot。然後因為此套件預設會隨著使用者的輸入自動增長模型內容，但在我們的專案中不能有這種情形發生，所以必須手動設定，將read_only參數設為True。以下為關鍵程式碼<br>
```python
chatbot = ChatBot(
    "Andy",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./database.sqlite3',
    read_only=True,
)
```