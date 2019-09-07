import requests
from fake_useragent import UserAgent
from hashlib import md5
import random
import time
import json


class YoudaoSpider(object):
    def __init__(self):
        pass

    # 计算请求需要的查询参数 salt sign ts
    def get_arg(self, word):
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0, 9))
        # 计算sign
        string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"

        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()

        return salt, ts, sign

    # 破解
    def attack_yd(self, word):
        salt, ts, sign = self.get_arg(word)
        # URL为"http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        headers = {
            "User-Agent": UserAgent().random,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "238",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "_ntes_nnid=9f31f72af3ae16407c983cbda613eb0f,1565342256644; OUTFOX_SEARCH_USER_ID_NCOO=1662276180.6007674; OUTFOX_SEARCH_USER_ID=131403599@223.255.15.21; JSESSIONID=aaaRsG27e2twd85qotj0w; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abcmSFqRefit665gDuk0w; ___rl__test__cookies=1567836263951",
            "Host": "fanyi.youdao.com",
            "Origin": "http://fanyi.youdao.com",
            "proxy-authorization": "Basic bnVsbCZudWxsOm51bGw=",
            "Referer": "http://fanyi.youdao.com/",
            "X-Requested-With": "XMLHttpRequest",
        }
        data = {
            "i": word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "ts": ts,
            "bv": "7e3150ecbdf9de52dc355751b074cf60",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        html = requests.post(url=url, headers=headers, data=data).text

        # 格式化json
        zhs = json.loads(html)
        # 提取翻译过的汉语
        zh = zhs["smartResult"]["entries"][1:]
        for i in zh:
            print(i.strip())

if __name__ == '__main__':
    while True:
        try:
            word = input("请输入翻译的单词:")
            spider = YoudaoSpider()
            spider.attack_yd(word)
        except KeyboardInterrupt:
            print("\n用户退出")
        except Exception:
            print("程序异常")
