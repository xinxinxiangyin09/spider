import requests
from fake_useragent import UserAgent

url = "http://www.renren.com/972190340/profile"
# headers最常检查的字段Cookie Referer User-Agent
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Cookie":"anonymid=k09cupdl-l32fg0; depovince=GW; _r01_=1; jebe_key=0084bfe3-6e1b-4791-ad47-9fc050b6a389%7C149e44e102ffb24b85b5edd3011962f0%7C1567849350710%7C1%7C1567849357135; jebe_key=0084bfe3-6e1b-4791-ad47-9fc050b6a389%7C149e44e102ffb24b85b5edd3011962f0%7C1567849350710%7C1%7C1567849357149; ln_uact=13335116832; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; _de=8AD9FC70A71E3FD4C3FA66069D313EC3; JSESSIONID=abcj0IPeC9O1e-ld_0t0w; ick_login=2f6cafc7-8d2e-41f7-a4c2-cb19002c0254; jebecookies=e3427c7d-94a3-4338-b6d7-b345c96e3947|||||; p=51745638dcda408bf4f89ca3159f80750; first_login_flag=1; t=d5403be4d773eb5ed4c0960bee64030b0; societyguester=d5403be4d773eb5ed4c0960bee64030b0; id=972190340; xnsid=ec268139; loginfrom=syshome",
    "Host":"www.renren.com",
    "proxy-authorization":"Basic bnVsbCZudWxsOm51bGw=",
    "Referer":"http://www.renren.com/SysHome.do",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":UserAgent().random,
}

html = requests.get(url=url, headers=headers)
print(html.text)