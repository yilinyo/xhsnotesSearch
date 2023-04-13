import csv
import hashlib
from urllib import parse
import requests
from bs4 import BeautifulSoup

import json
from lxml import etree


def get_x_sign(api):
    x_sign = "X"
    m = hashlib.md5()
    m.update((api + "WSUDD").encode())
    x_sign = x_sign + m.hexdigest()
    return x_sign


# 配置你的 代理 ip池
# def get_proxy():
#     # 提取ip

#     return proxies


def spider(keyword, authorization, d_page, sort_by='general', ):
    """
    :param authorization:
    :param keyword:
    :param d_page: 页数
    :param sort_by: general：综合排序，hot_desc：热度排序
    :return:
    """
    host = 'https://www.xiaohongshu.com'
    url = '/fe_api/burdock/weixin/v2/search/notes?keyword={}&sortBy={}' \
          '&page={}&pageSize=20&prependNoteIds=&needGifCover=true'.format(parse.quote(keyword),
                                                                          sort_by,
                                                                          d_page + 1)
    # page 从0开始, 所以这里+1

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Referer': 'https://servicewechat.com',
        'Authorization': authorization,  # 在这里填入抓到的header
        'X-Sign': get_x_sign(url)
    }

    # proxies = {'http': "http://{}".format(get_proxy())}
    # 记得使用代理池

    resp = requests.get(url=host + url, headers=headers, timeout=5)
    if resp.status_code == 200:
        res = json.loads(resp.text)
        return res['data']['notes'], res['data']['totalCount']
    else:
        print('Fail:{}'.format(resp.text))


# 拿到帖子 id
def getlistByName(keyword, authorization_, sorted_way="general"):
    notes = []

    # 拿到所有 的 文章id 只取20 页
    for i in range(0, 20):

        tmp = spider(keyword, authorization_, d_page=i, sort_by=sorted_way)
        print(tmp[0])
        if (len(tmp[0]) <= 0):
            break
        else:
            notes.extend(tmp[0])

    ids = []

    for note in notes:
        ids.append(note['id'])

    print("检索到相关笔记 " + len(ids).__str__() + "篇")

    return ids


# 获取文章信息返回

def getInfo(ids):
    # proxys = get_proxy()
    infolist = []
    for id in ids:

        url = "https://www.xiaohongshu.com/explore/" + id

        headers = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Connection": "keep-alive",
            "Host": "www.xiaohongshu.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"

        }

        resp = requests.get(url, headers=headers)

        # 中文解码

        resp.encoding = resp.apparent_encoding
        html = resp.text

        soup = BeautifulSoup(html, 'lxml')

        json_str = soup.find(attrs={'type': 'application/ld+json'}).text

        # 去除换行 等字符 不然 json无法解析 ,Windows 正常 ，Linux 异常
        json_str = json_str.replace('\n', '').replace('\r\n', '')
        # print(url)
        info_dic = json.loads(json_str, strict=False)
        info_dic['link'] = url
        # 小红书有反爬机制短时间重复 会有些数据获取不到 数据为空的就过滤掉
        if info_dic['name'] != '':
            infolist.append(info_dic)
    print("本次有效爬取到相关笔记 " + len(infolist).__str__() + "篇")
    return infolist


# 保存为csv文件，data只接受列表嵌套列表，列表嵌套元组数据
def saveCsvFile(data, keyName):
    f = open(keyName + '.csv ', 'w', newline='', encoding="utf-8")
    csv_write = csv.writer(f)
    for i in range(len(data)):
        csv_write.writerow(data[i])
    f.close()
    print("保存完闭，文件在此文件夹当前目录~~~")
    print("如果检索笔记和实际保存笔记数目不一致可以尝试重试或更换ip~~~~")


# 转换为 csv 格式
def toCsv(infolist, keyname):
    listlist = [['链接地址', '标题', '内容']]

    for info in infolist:
        name = info['name']

        link = info['link']
        description = info['description']
        listinfo = [link, name, description]
        listlist.append(listinfo)
    saveCsvFile(listlist, keyname)


if __name__ == "__main__":
    # 参数
    # 检索关键字
    keyName = "Python"
    # 微信小程序 小红书header 认证头 小程序自行 抓包Authorization ，是一串 wxmp.xxxxxxxx的数据
    authorization = ""
    # 排序方式可选  general：综合排序 (默认)，或hot_desc：热度排序
    sortedWay = "general"

    # 执行函数

    idList = getlistByName(keyName, authorization, sortedWay)

    toCsv(getInfo(idList), keyName)
