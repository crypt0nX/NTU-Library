import requests
import json


def hitokoto():
    try:
        url = "https://v1.hitokoto.cn/"

        r = requests.get(url)
        data = json.loads(r.text)
        if data['from_who'] != None:
            return '「\n\t' + data['hitokoto'] + "\t\n」\n" + "\t"+"      ———" + data['from_who'] +"："+ data['from']
        else:
            return '「\n\t' + data['hitokoto'] + "\t\n」\n" + "\t"+ "     ———" + data['from']
    except Exception:
        return "出错啦🎉🎉"

hitokoto()
