# 透過網易api抓取歌詞的程式
<br>
需要安裝的套件: requests

## index.py說明<br>
此程式執行時，需要有SongName.json在同一層目錄下，讀取其歌名並透過網易api取得歌詞，然後會在目錄下生成對應歌名的json檔。<br>
要注意的是，生成的內容是簡體中文，還需進行下一步的簡轉繁

## SongName.json說明
其格式為 : ["歌名A", "歌名B", ...]