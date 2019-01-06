# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27
# @Author  : 素心
# @File    : bixin.py
# @Software: PyCharm
import requests as req
import os
#from multiprocessing import Pool

BASE_URL = "http://118.31.40.206:8888/api/moment/list?len=100&userid="


def get_json(url):
    res = req.get(url).json()
    images = res.get('Data')
    for image in images:
        yield {
            'title': image['content'],
            'images': image['imgs']
        }


def mkdir(path):
    path = path.strip()
    if path != '':
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        return path


def save(url, path):
    filename = os.path.basename(url)
    file = '/'.join((path, filename))
    res = req.get(url)
    with open(file, 'wb') as f:
        f.write(res.content)
        return filename


def main(uid):
    url = BASE_URL + str(uid)
    for item in get_json(url):
        dir = mkdir(item['title'])
        if dir != '' and dir != None:
            for image in item['images']:
                filename = save(image, dir)
                print('[%s] %s [OK]...' % (dir, filename))


if __name__ == '__main__':
    #pool = Pool()
    # pool.map(main, [i for i in range(10, 9300)])
    i=0
    while True:
        i+=1
        try:
            main(i)
        except Exception as e:
            print(e)
