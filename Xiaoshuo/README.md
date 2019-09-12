# 说明

> 爬取盗墓笔记全集

## 环境

- Ubuntu 18.0.4
- Python 3.6.5
- Scrapy 1.7.3

## 目标

- url：`http://www.daomubiji.com/`
- 抓取目标网站中盗墓笔记1-8中所有章节的所有小说的具体内容，保存到本地文件

## 分析

- 三级页面，首先考虑封装请求函数

## xpath表达式

- 一级页面的集链接：`//article[@class="article-content"]/a/@href`

  集名称：`//article[@class="article-content"]/a//h2/text()`

- 二级页面

  基准xpath：`//article`

  章节链接：`./a/@href`

  章节名：`./a/text()`

- 三级页面文章内容：`//article[@class="article-content"]//p/text()`

## 温馨提醒

该项目中已经集成了`run.py` 直接运行`run.py`即可,如果需要更改文件保存路径,请移步至`pipelines.py`中修改