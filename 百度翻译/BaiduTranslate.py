import requests
import re
import execjs

class BaiduTranslate(object):
    def __init__(self):
        self.get_url = "https://fanyi.baidu.com/"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "PSTM=1566478223; BIDUPSID=0CC61A0065AFFDEA58B0FD66090BD70B; BAIDUID=D7CAE55D8A7118B5B56D22F70DD4D8C9:FG=1; delPer=0; H_PS_PSSID=1434_21109_29522_29521_29721_29567_29220_26350; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; APPGUIDE_8_0_0=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1567998164,1568009412; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1568010523; __yjsv5_shitong=1.0_7_a71b978450b19d80ffa7e23252fdac0e1623_300_1568010515981_223.255.15.21_e9114107; yjs_js_security_passport=b4a73e6a9ca6c77eb314cfde6892b96bd47c909c_1568010520_js",
            "proxy-authorization": "Basic bnVsbCZudWxsOm51bGw=",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        }

    # 计算token,响应内容就有
    def get_token(self):
        html = requests.get(self.get_url, headers=self.headers).text
        # 正则解析较为方便
        pattern = re.compile("token: '(.*?)',", re.S)
        token = pattern.findall(html)[0]

        return token

    # 计算sign
    def get_sign(self, word):
        with open("/home/chancey/project/spider/work/百度翻译/node.js", "r") as f:
            js_data = f.read()
        execjs_obj = execjs.compile(js_data)
        sign = execjs_obj.eval('e("{}")').format(word)

        return sign

    # 获取翻译结果
    def get_result(self, word):
        token = self.get_token()
        sign = self.get_sign(word)
        # 将formdata定义成字典
        form_data = {
            "from": "en",
            "to": "zh",
            "query": "cta",
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token,
        }
        html_json = requests.post(url="https://fanyi.baidu.com/v2transapi", headers=self.headers, data=form_data).json()
        print(html_json)

if __name__ == '__main__':
    spider = BaiduTranslate()
    word = input("请输入单词:")
    result = spider.get_result(word)
    print(result)