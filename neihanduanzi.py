#-*- coding:utf-8 -*-
import urllib2
import re

class Spider:

    def __init__(self):
        self.enable = True
        self.page = 1 #当前要爬去第几页

    def load_page(self, page):#发送内涵段子url请求，得到html源码
        url = "http://www.neihan8.com/article/list_5_"+ str(page) + ".html"         
        user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
        headers = {"User-Agent": user_agent}
        req = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(req)
        html = response.read()
        new_html = html.decode("gbk").encode("utf-8")

        #用正则表达式将new-html过滤 得到所有的段子
        # 所有的段子在<div class="f18 mb20">－－－－－</div>
        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)
        item_list = pattern.findall(new_html)
        return item_list

    def deal_one_page(self, item_list, page):
        '''
            处理一页的数据
        '''
        print "正在存储 第%d页的段子.." %(page)
        for item in item_list:
            item = item.replace("<p>", "").replace("</p>", "").replace("<br />", "")
            print item.replace("<p>", "").replace("</p>", "").replace("<br />", "")
            self.write_to_file(item)
        print "第%d 页的段子存储完毕.." %(page)

    def write_to_file(self, txt):
        f = open('./myStory.txt', 'a')
        f.write(txt)
        f.write('-----------------------------------------------')
        f.close()

    def do_work(self):
        '''
            提供跟用于交互的过程
            让爬虫去工作
        '''

        while self.enable:
            print "按回车继续"
            print "输出quit退出"
            command = raw_input()
            if (command == "quit"):
                self.enable = False
                break;
            item_list = self.load_page(self.page)
            self.deal_one_page(item_list, self.page)
            self.page += 1

if __name__ == "__main__":
    #创建一个spider对象
    mySpider = Spider()

    mySpider.do_work()





