from fake_useragent import UserAgent
import requests
from lxml import etree
import pymysql

from config import * # 自定义配置文件

headers = {
    "User-Agent": UserAgent().random
}

def get_ip_list(url):
    html = requests.get(url=url, headers=headers).text
    parse_html = etree.HTML(html)
    r_list = parse_html.xpath('//tr[@class="odd"]')

    ip_list = []
    for r in r_list:
        ip = r.xpath('./td[2]/text()')[0].strip()
        port = r.xpath('./td[3]/text()')[0].strip()
        type = r.xpath('./td[6]/text()')[0].strip()

        # 构建proxy参数
        proxy = {type: type + "://" + ip + ":" + port}

        ip_save = clean(proxy)
        ip_list.append(ip_save)
    print("写入数据库")
    write_db(ip_list)

def clean(proxy):

    test_url = "http://www.httpbin.org/get"
    res = requests.get(url=test_url, headers=headers, proxies=proxy)
    if res.status_code == 200:
        print(proxy, "OK")
        return str(proxy)


def write_db(ip_list):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, charset='utf8')
    cursor = db.cursor()

    ins = "insert into proxy(content) value (%s)"
    try:
        cursor.executemany(ins, ip_list)
        db.commit()
    except:
        print("数据库写入错误")
        pass

    cursor.close()
    db.close()


if __name__ == '__main__':
    url = "https://www.xicidaili.com/nn/{}"
    try:
        page = int(input("请输入页数:"))
        for i in range(1, page+1):
            url = url.format(i)
            print("正在爬取第{}页".format(i))
            get_ip_list(url)
    except ValueError:
        print("请输入纯数字!")
    except KeyboardInterrupt:
        print("用户退出")


