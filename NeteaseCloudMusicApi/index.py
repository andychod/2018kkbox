# 引入 requests 模組
import requests
import json


def GetSongId(songname):
    getSongId = requests.get('http://140.138.150.36:3000/search?keywords=' + songname)
    getSongId = json.loads(getSongId.text)
    songId = getSongId['result']['songs'][0]['id']
    return songId


def GetLyric(songId, jsondata):
    # step2 取得歌詞
    try:
        lyr = requests.get('http://140.138.150.36:3000/lyric?id=' + str(songId))
        lyric = json.loads(lyr.text)
        lyric = lyric['lrc']['lyric']
        for mylyric in lyric.split('\n'):
            r = mylyric.find(']')
            if(len(mylyric)>(r+1)):
                substr = mylyric[r+1:]
                if(substr[0]!=' ' and substr.find('：')== -1):
                    jsondata.append(substr)
                    print(substr)
        # 存檔起來
        with open(songname + '.json', 'w', encoding="utf8") as outfile:
            json.dump(jsondata, outfile, ensure_ascii=False,indent=4,)

    except:
        print("~~~~ <"+songname+"> :查無結果~~~~")



# main function()

with open('SongName.json', 'r', encoding="utf8") as f:
    songnameList = json.load(f)
for songname in songnameList:
    print(songname + ": ")

    # step1 取得歌曲id
    songId = GetSongId(songname)

    jsondata = []

    # step2 取得歌詞
    GetLyric(songId,jsondata)


