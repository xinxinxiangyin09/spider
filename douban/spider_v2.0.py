'''
version : v2.0
本次升级可自定义搜索影片类型
'''

import requests

class DoubanSpider(object):
    def __init__(self):
        self.url = "https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start=0&limit={}"
        #正则批量处理headers
        self.headers = {
            'Accept': '*/*',
            # 'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'll="118371";bid=loa1jg0qURI;__utma=30149280.1704224511.1567767549.1567767549.1567767549.1;__utmc=30149280;__utmz=30149280.1567767549.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;__utmb=30149280.1.10.1567767549;__utma=223695111.1270134199.1567767597.1567767597.1567767597.1;__utmb=223695111.0.10.1567767597;__utmc=223695111;__utmz=223695111.1567767597.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/;ap_v=0,6.0;_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1567767599%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D;_pk_ses.100001.4cf6=*;__yadk_uid=T2F781IJEdpHOJ600jC0lKiwHGOcISOZ;_pk_id.100001.4cf6=104af536e3063e0b.1567767599.1.1567768968.1567767599.',
            'Host': 'movie.douban.com',
            'proxy-authorization': 'BasicbnVsbCZudWxsOm51bGw=',
            'Referer':'https://movie.douban.com/typerank?type_name=%E7%88%B1%E6%83%85&type=24&interval_id=10090&action=',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/76.0.3809.100Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
}

    # 请求+解析
    def get_film_info(self, url):
        html_json = requests.get(url=url, headers=self.headers).json()
        for film in html_json:
            # 名称
            name = film['title']
            # 评分
            score = film['score']

            print(name, score)

    def main(self):
        type_dict = {
            "剧情": 11,
            "喜剧": 24,
            "动作": 5,
            "爱情": 13,
            "科幻": 17
        }
        try:
            while True:
                type_name = input("请输入电影类型(剧情|喜剧|动作|爱情|科幻):")
                if type_name in type_dict:
                    limit = input("请输入电影数量:")
                    url = self.url.format(type_dict[type_name], limit)
                    self.get_film_info(url)
                else:
                    print(type_name,"不存在")
        except KeyboardInterrupt:
            print("\n用户退出")
        except Exception:
            print("程序异常")

if __name__ == '__main__':
    spider = DoubanSpider()
    spider.main()