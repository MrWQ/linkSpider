# -*- coding: utf-8 -*-
#深度优先爬取链接的爬虫

import requests,re
from changeLink import *

GHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
GUrlValueList = []  #有效值列表，用于查重复
GUrlList = []       #总列表，剩余要爬取的链接
GStartUrlName = ''  #起始链接的域名
GStartUrlHead = ''  #起始链接的头

def linkSpider():
    global GUrlList
    global GHeaders
    global GUrlValueList
    while (len(GUrlList)>0):
        url = GUrlList.pop()
        url = addTail(url)
        urlValue = getValue(url)
    #     判断是否已经爬取
        if urlValue in GUrlValueList:
            pass
        else:
            GUrlValueList.append(urlValue)  #添加进已爬取的列表
            print('当前爬取链接：' + url)
            # 传人url 获取url列表
            GUrlList = GUrlList + findLinks(url)  # 去重复
            # 去除错误链接
            GUrlList = removeErrorLink(GUrlList)
            # 纠正 // / ../ ./ 四种格式链接
            GUrlList = changeLink1(GUrlList,GStartUrlHead)                                    #处理//
            GUrlList = changeLink2(GUrlList,url,GStartUrlHead,GStartUrlName)    #处理/
            GUrlList = changeLink3(GUrlList,url)                                #处理../
            # GUrlList = changeLink4(GUrlList,url)                              #处理./   有问题
            GUrlList = changeLink5(GUrlList,url,GStartUrlHead)                  #处理正常链接
            GUrlList = changeLink6(GUrlList)                                    #处理?a/a
            GUrlList = removeDiffererntName(GUrlList,GStartUrlName)             #处理不同域名
            GUrlList = urllistCheck(GUrlList)                                   # 处理返回不是200的
            print(GUrlList)


if __name__ =='__main__':

    startUrl = 'https://www.baidu.com'

    GStartUrlName = getName(startUrl)
    GStartUrlHead = getHead(startUrl)
    GUrlList.append(startUrl)
    linkSpider()
    print(GUrlValueList)

