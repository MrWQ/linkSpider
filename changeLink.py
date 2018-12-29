# -*- coding: utf-8 -*-
import re,requests
# //
#/
# ..
# .
# 不如一开始就把链接尾加上/
# 末尾有没有#/
GHeaders = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
# GStartUrlName = ''
# GStartUrlHead = ''

# 传入url获取url列表
def findLinks(url):
    reHtml = getHtml(url)
    urllist = []
    try:
        urllist = findLinksFromHtml(reHtml)
    except:
        print('reHtml 获取失败')
    return urllist
# 匹配正则返回url列表
def findLinksFromHtml(reHtml):
    pageUrlList = []
    # 获取链接
    pattern = re.compile(r'href="(.*?)"', re.S)
    pageUrlList1 = re.findall(pattern, reHtml)
    pageUrlList = pageUrlList + pageUrlList1
    pattern = re.compile(r"href='(.*?)'", re.S)
    pageUrlList2 = re.findall(pattern, reHtml)
    pageUrlList = pageUrlList + pageUrlList2
    # 获取资源
    pattern = re.compile(r'src="(.*?)"', re.S)
    pageUrlList1 = re.findall(pattern, reHtml)
    pageUrlList = pageUrlList + pageUrlList1
    pattern = re.compile(r"src='(.*?)'", re.S)
    pageUrlList2 = re.findall(pattern, reHtml)
    pageUrlList = pageUrlList + pageUrlList2
    # 获取js中的 链接
    pattern = re.compile(r'href = "(.*?)"', re.S)
    pageUrlList1 = re.findall(pattern, reHtml)
    pageUrlList = pageUrlList + pageUrlList1
    pattern = re.compile(r"href = '(.*?)'", re.S)
    pageUrlList2 = re.findall(pattern, reHtml)
    pageUrlList = pageUrlList + pageUrlList2

    pageUrlList = list(set(pageUrlList))  # 去重复
    return pageUrlList

# 获取html
def getHtml(url):
    try:
        reHtml = requests.get(url=url, headers=GHeaders, timeout=10).content.decode('utf-8')
    except:
        reHtml = requests.get(url=url, headers=GHeaders, timeout=10).text
    return (reHtml)

# 错误/无效链接处理
def removeErrorLink(urlList):
    errorList = []    #用来记录索引位置到末尾到距离   错误链接
    length = len(urlList)
    count = 0
    for count in range(0,length):
        if(len(urlList[count])==1):     #长度为1去掉 错误链接
            errorList.append(length-count)#记录当前索引位置到末尾到距离
            count = count+1
        # elif('.' not in urlList[count] ):   #去掉没.的
        #     errorList.append(length-count)#记录当前索引位置到末尾到距离
        #     count = count+1
        # elif(urlList[count][0]!='.' and urlList[count][1]!='/' and len(urlList[count])==2): #去掉./
        #     errorList.append(length-count)#记录当前索引位置到末尾到距离
        #     count = count+1
        elif(urlList[count]=='#' or urlList[count]=='/#' or urlList[count]=='/' or urlList[count]=='' or urlList[count]=='./'):  #去掉#
            errorList.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        elif(urlList[count][len(urlList[count])-1] == '='):     #去掉末尾为=
            errorList.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        elif(urlList[count][0]!='/' and len(urlList[count])==2):    #去掉长度为2，非/开头的
            errorList.append(length-count)#记录当前索引位置到末尾到距离
            count = count+1

        elif(urlList[count][0]=='.' and urlList[count][1]=='.' and urlList[count][2]=='.'):     #去掉...的
            errorList.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        elif('(' in urlList[count] or ')' in urlList[count] or '（' in urlList[count] or '）' in urlList[count] ):     #去掉有（）（）
            errorList.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        elif(len(urlList[count])>=11 and (urlList[count][10]==':' or urlList[count][10]=='：') ):     #去掉javascript:
            errorList.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        else:
            count = count+1
        #     去除错误链接
    for i in errorList:
        i = int(i)
        length = len(urlList)
        urlList.pop(length - i)
    removeNull(urlList)  # 去掉空值
    return urlList

# 去掉列表中的空值
def removeNull(urlList):
    urlList = list(urlList)
    if urlList != []:
        while '' in urlList:
            urlList.remove('')


# //转换
def changeLink1(urlList,head):
    headList4 = []  # 用来记录索引位置到末尾到距离    //开头的链接
    length = len(urlList)
    count = 0
    for count in range(0, length):
        if (urlList[count][0] == '/' and urlList[count][1] == '/'):  # //开头的转换
            headList4.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        else:
            count = count + 1
    # //开头的转换
    for i in headList4:
        i = int(i)
        length = len(urlList)
        urlList[length - i] = head  +  urlList[length-i]
    removeNull(urlList)  # 去掉空值
    return urlList

# /转换
def changeLink2(urlList,url,head,name):
    headList2 = []  # 用来记录索引位置到末尾到距离    /开头的链接  /favicon.ico 的加头和域名
    length = len(urlList)
    count = 0
    for count in range(0, length):
        if (urlList[count][0] == '/' and urlList[count][1] != '/'):  # /开头的链接
            headList2.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        else:
            count = count + 1
    #    /开头的转换
    for i in headList2:
        i = int(i)
        length = len(urlList)

        temp = urlList[length - i]
        urlList[length - i] = head + '//' + name + temp
    removeNull(urlList)  # 去掉空值
    return urlList

# ../转换
def changeLink3(urlList,url):
    headList3 = []  # 用来记录索引位置到末尾到距离    ../开头的链接
    length = len(urlList)
    count = 0
    for count in range(0, length):
        if (urlList[count][0] == '.' and urlList[count][1] == '.' and urlList[count][2] == '/'):  # ../开头的转换
            headList3.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        else:
            count = count +1
    #   ..开头的转换
    for i in headList3:
        i = int(i)
        length = len(urlList)
        value = urlList[length - i]
        # urlList[length - i]#每一个都是../开头
        try:
            urlList[length - i] = link3ToTrueLink2(url,link3ToTrueLink1(value))
        except:
            urlList[length - i] = ''
    removeNull(urlList)  # 去掉空值
    return urlList

#         判断link3
def ifLink3(url):
    if (url[0] == '.' and url[1] == '.' and url[2] == '/'):  # ../开头
        return True
    else:
        return False

#       去一次../
def removeLink3(url):
    url = url[3:]
    return url

#   计算link3 返回列表 ../的数目 和有效值 例如：[3,'a.html']
def link3ToTrueLink1(url):
    try:
        count = 0
        cL = []
        while (ifLink3(url) == True):
            url = removeLink3(url)
            count = count + 1
        cL.append(count)
        cL.append(url)
        return cL
    except:
        return []

#   计算link3 返回真正链接有效链接  http://baidu.com/a.html
def link3ToTrueLink2(url,tureLink1):
    try:
        count1 = tureLink1[0]   #数目
        value = tureLink1[1]    #有效值
        uList = url.split('/')
        tempstr =''
        for count in range(0,len(uList)-1-count1):
            tempstr = tempstr + uList[count] +'/'
        value = tempstr + value
        return value
    except:
        return ''

# ./转换
def changeLink4(urlList,url):
    headList1 = []  # 用来记录索引位置到末尾到距离    ./开头的链接 ./favicon.ico 的加头和域名
    length = len(urlList)
    count = 0

    for count in range(0, length):
        if (urlList[count][0] == '.' and urlList[count][1] == '/'):  # ./开头的链接转换
            headList1.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        else:
            count = count + 1
    #     ./开头的转换
    for i in headList1:
        i = int(i)
        length = len(urlList)
        # 去掉.    取./后面的值
        temp = urlList[length - i][2:]
        urlList[length - i] = url + temp
    removeNull(urlList)  # 去掉空值
    return urlList

# 字母或数字开头  基本上是正常链接
def changeLink5(urlList,url,head):
    headList1 = []  # 用来记录索引位置到末尾到距离
    length = len(urlList)
    count = 0
    for count in range(0, length):
        value = urlList[count][0]   #首字母
        if (value>='a' and value<='z' ):  # 小写字母开头的链接转换
            # 去掉http开头的
            if value == 'h':
                if len(urlList[count])>= 7:
                    value = urlList[count][0:7]
                    if value == 'http://' or value == 'https:/':
                        count = count + 1
                    else:
                        headList1.append(length - count)
                        count = count + 1
                else:
                    headList1.append(length - count)
                    count = count + 1
            else:
                headList1.append(length - count)
                count = count + 1
        elif (value>='A' and value<='Z' ):  # 大写字母开头的链接转换
            headList1.append(length - count)
            count = count + 1
        elif (value>='0' and value<='9' ):  # 数字开头的链接转换
            headList1.append(length - count)
            count = count + 1
        else:
            count = count + 1
    #     正常链接转换
    for i in headList1:
        i = int(i)
        length = len(urlList)
        temp = urlList[length-i]
        value = getValue(url)
        valuelist = value.split('/')
        if len(valuelist) <=1 :
            pass
        else:
            value = ''
            for c in range(0,len(valuelist) -1 ):
                value = value+ '/' + valuelist[c]

        urlList[length - i] = head + '/' + value + '/' + temp
    removeNull(urlList)  # 去掉空值
    return urlList

# ?a=cc/a/b/c.html转换
def changeLink6(urlList):
    headList1 = []  # 用来记录索引位置到末尾到距离
    length = len(urlList)
    count = 0
    for count in range(0, length):
        value = urlList[count]
        value = removeTail(value)
        if '?' in value:
            try:
                valueList = value.split('?')
                value = valueList[1]
            except:
                value = ''
            if (value == '' or '/' in value):
                headList1.append(length - count)  # 记录当前索引位置到末尾到距离
                count = count + 1
            else:
                count = count + 1
        else:
            count = count + 1


    #     ?/开头的去掉
    for i in headList1:
        i = int(i)
        length = len(urlList)
        urlList.pop(length - i)
    removeNull(urlList)  # 去掉空值
    return urlList

# 去掉不同域名
def removeDiffererntName(urlList,NAME):
    headList1 = []  # 用来记录索引位置到末尾到距离
    length = len(urlList)
    count = 0
    for count in range(0, length):
        value = urlList[count]
        valueName = getName(value)
        if NAME not in valueName:   #如果不包含起始域名
            headList1.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        else:
            count = count + 1
    #     去掉不同域名
    for i in headList1:
        i = int(i)
        length = len(urlList)
        urlList.pop(length - i)
    removeNull(urlList)  # 去掉空值
    return urlList

# 返回响应为200的url列表
def urllistCheck(urlList):
    headList1 = []  # 用来记录索引位置到末尾到距离
    length = len(urlList)
    count = 0
    for count in range(0, length):
        value = urlList[count]
        valueStat = requests.get(value,headers = GHeaders,timeout=20).status_code
        # print(value)
        # print(valueStat)
        # print(type(valueStat))
        if (valueStat != 200):
            headList1.append(length - count)  # 记录当前索引位置到末尾到距离
            count = count + 1
        else:
            count = count + 1
    #     去掉不同域名
    for i in headList1:
        i = int(i)
        length = len(urlList)
        urlList.pop(length - i)
    removeNull(urlList)  # 去掉空值
    return urlList

# 末尾加/
def addTail(url):
    lastValue = url[len(url)-1]
    ul = url.split('/')
    value = ul[len(ul)-1]
    if lastValue == '#':
        url = url[0:len(url)-1]
    elif lastValue == '/':
        pass
    elif('.' in value):
        pass
    else:
        url = url + '/'
    return url

# 末尾去掉/
def removeTail(url):
    lastValue = url[len(url)-1]
    if lastValue == '#' or lastValue == '/':
        url = url[0:len(url)-1]
    else:
        pass
    return url

#获取域名
def getName(url):
    try:
        return url.split('/')[2]
    except:
        return ''

# 去头去尾获取链接有效值
def getValue(url):
    url = removeTail(url)
    try:
        url = url.split('//')[1]
    except:
        url = ''
    return url

#获取头
def getHead(url):
    url = removeTail(url)
    try:
        url = url.split('//')[0]
    except:
        url = ''
    return url


if __name__ =='__main__':

    a=['loginImages/timg.png','/captcha/LifSKUVKaxRptog.png','lib/jquery.form.js','/action/findpwd.html']
    u = 'https://www.5169888.com/action/login.jsp'
    print(a)
    print(u)
    print(changeLink5(a,u,'http:'))
    a = changeLink2(a, u, 'http:', getName(u))  # 处理/
    print(a)
    urllistCheck(a)