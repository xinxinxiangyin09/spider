'''
腾讯招聘的职位信息爬取,异步加载
'''

from fake_useragent import UserAgent
import requests
import csv

class TencentSpider(object):
    def __init__(self):
        self.headers = {"User-Agent": UserAgent().random}
        self.base_url = "https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex={}&pageSize=10"
        self.info_url = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?&postId={}"

    # 请求页面
    def get_page(self, url):
        '''
        后边会有多次返回的页面,故而在这里直接封装函数
        :param url:
        :return:
        '''
        res = requests.get(url, headers=self.headers).json()
        return res

    # 请求职位列表,提取 岗位名称 岗位职责 岗位要求 岗位城市
    def parse_base_page(self, url):
        #解析一级页面,获取postID,用以构造详情页面的链接
        html = self.get_page(url)
        for item in html["Data"]["Posts"]:
            info_html = self.get_page(self.info_url.format(item["PostId"]))# 构造详情页面的URL
            job_name = str(info_html["Data"]["RecruitPostName"]).strip()
            job_addr = str(info_html["Data"]["LocationName"]).strip()
            job_content = str(info_html["Data"]["Responsibility"]).strip()
            job_require = str(info_html["Data"]["Requirement"]).strip()

            info = [job_name, job_addr, job_content, job_require]
            print(job_name, job_addr)
            self.write_info(info)

    def write_info(self, info):
        with open("jobs.csv", "a+") as f:
            write = csv.writer(f)
            write.writerow(info)

    def main(self):
        try:
            number = int(input("请输入职位页数(每页10岗):"))
            for page in range(1, number+1):
                url = self.base_url.format(page)
                self.parse_base_page(url)
        except ValueError:
            print("请输入纯数字")
        except KeyboardInterrupt:
            print("用户退出")
        except Exception:
            print("程序异常")

if __name__ == '__main__':
    spider = TencentSpider()
    spider.main()
