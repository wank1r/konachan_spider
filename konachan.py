import json
import requests
import re
import os
import time


class Konachan:
    '''爬取konachan网站图片'''
    def __init__(self, page, tags):
        self.page = page  # 网址页码
        self.tags = tags  # 标签（可以理解为关键词搜索，具体看网址就明白了）
        self.img_suess = 0  # 下载成功的图片数量
        self.img_fail = 0  # 下载失败的图片数量
        self.starttime = time.time()  # 下载开始时间
        self.s = requests.session()
        self.result = None  # 每页的下载链接
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        }

    def spider(self):
        '''拿到每页的下载链接'''
        url = 'https://konachan.com/post?page={}&tags={}'.format(self.page, self.tags)
        while True:
            try:
                response = self.s.get(url=url, headers=self.headers,timeout=2)
            except Exception:
                print('获取图片ID超时')
                continue
            else:
                break

        # 正则去匹配
        self.result = re.findall(r'<a class="directlink .*?" href="(.*?)">', response.content.decode('utf-8'))
        print('第{}页链接拿到啦！共{}张图片'.format(self.page, len(self.result)))


    def download(self):
        '''
        下载一页的图片
        :return: 
        '''
        imgnum = 1  # 每页的图片序号
        for img in self.result:
            # 图片的id
            # img_id = re.findall(r'https://konachan.com/.*?/(.*?)/Konachan.com', img)[0]
            dirs = './{}'.format(self.tags)
            if not os.path.exists(dirs):  # 如果文件夹不存在则创建
                os.makedirs(dirs)
            filename = '{}/{}-{}.jpg'.format(dirs, self.page, imgnum)
            for i in range(3):
                fail = 1  # 局部变量，重试次数
                try:
                    res = self.s.get(img, headers=self.headers, timeout=2)
                except Exception:
                    print("{}下载超时，正在第{}次重试".format(img, fail))
                    fail += 1
                    continue
                else:
                    break
            if fail == 3:
                print("{}下载超时".format(img))
                imgnum += 1
                self.img_fail += 1
                continue


            with open(filename, 'wb') as f:
                f.write(res.content)
                print("{}-{}下载完成".format(self.page, imgnum))
            imgnum += 1
            self.img_suess += 1
    def run(self):
        for i in range(int(input('需要下载多少页（一页普遍21张）:'))):  # 需要下载多少页
            self.spider()
            self.download()
            self.page += 1
        print('成功下载{}张，失败{}张'.format(self.img_suess, self.img_fail))
        end = time.time()
        self.spend = end - self.starttime
        hour = self.spend // 3600
        minu = (self.spend - 3600 * hour) // 60
        sec = self.spend - 3600 * hour - 60 * minu
        print('总耗时{}小时{}分{}秒'.format(int(hour), int(minu), sec))
if __name__ == '__main__':
    page = int(input('从第几页开始下载：'))
    tags = str(input('标签内容：'))
    k = Konachan(page, tags)
    k.run()
