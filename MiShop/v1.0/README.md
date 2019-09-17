# 爬取小米应用商店

## 环境

- Ubuntu 19.0.4

- Python 3.6.5

## 第三方库

- requests 2.22.0

- lxml 4.4.1

## 目标

- 获取分栏的实用工具

- 获取所有的APP名和简介

- 写入CSV文件

## 分析

- 异步加载

- API:http://app.mi.com/categotyAllListApi?page={}&categoryId=5&pageSize=30

## 数据提取

- APP名称XPATH:`//div[@class="intro-titles"]/h3/text()`

- APP简介XPATH:`//p[@class="pslide"][1]/text()`

## 结果展示

![](http://wx4.sinaimg.cn/mw690/007WoGSoly1g72ilxxyssj31du0hj4ez.jpg)
