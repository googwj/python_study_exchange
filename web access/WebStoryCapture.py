# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:59:36 2020

@author: Wenjie
"""

#web爬虫应用
#
 
#输入：url
#处理：request库函数获取页面信息，并将网页内容转换成为人能看懂的编码格式
#输出：访问书趣阁网站，并抓取鬼吹灯的全部小说内容

import requests                 #http library
from bs4 import BeautifulSoup   #xml parsing library
from urllib.parse import urljoin #Splice current url with relevant url
from MySqlAccess import MySqlAccess

bookTitle = []
chapterList = []

def getHtmlText(url):
    try:
        req = requests.get(url, timeout=30)
        req.raise_for_status()  #如果状态码不是200， 抛出异常
        req.encoding = 'utf-8'
        return req.text
    except:   #抛出异常
        return ""

def loadBookTitle(soup):
    cover = soup.find('div',class_='cover')
    cover = cover.find('img')['src']
    sname = soup.find('h2').string
    small = soup.find('div',class_='small').find_all('span')
    authr = small[0].string[3:]
    clazz = small[1].string[3:]
    stats = small[2].string[3:]
    words = small[3].string[3:]
    intro = soup.find('div',class_='intro').find_all('span')
    xintr = ''
    for _intr in intro:
        if not _intr.has_attr('class'):
            zintr = ''
        else:
            zintr = _intr['class'][0]
        if zintr != 'showall':
            xintr = xintr + _intr.string
    intro = xintr
    bookTitle.append(sname)
    bookTitle.append(authr)
    bookTitle.append(clazz)
    bookTitle.append(stats)
    bookTitle.append(words)
    bookTitle.append(cover)
    bookTitle.append(intro)
    print(bookTitle)
    
def loadChapterList(soup, url):
    chaps = soup.find_all('dt')[1].next_siblings
    for _chap in chaps:
        if repr(_chap) == r"'\n'":
            continue
        alink = _chap.find('a')
        ahref = urljoin(url, alink['href'])
        title = alink.string
        xlink = []
        xlink.append(title)
        xlink.append(ahref)
        # print(xlink)
        chapterList.append(xlink)
        

        
def loadChapterContent():
    for xlink in chapterList[0:5]:
        title = xlink[0]
        cpurl = xlink[1]
        ctext = getHtmlText(cpurl)
        csoup = BeautifulSoup(ctext,"lxml").find('div',id='content', class_='showtxt')
        print("Chapter Name:",title)
        print("Chapter Url:",cpurl)
        print("Chapter Content:")
        for _cstr in csoup.strings:
            _istr = eval(repr(_cstr))
            if _istr.strip() == cpurl:
                break
            print(_cstr)

def main():
    url  = 'http://www.shuquge.com/txt/8403/index.html'     # 汉鼎
    url  = 'http://www.shuquge.com/txt/76615/index.html'    # 鬼吹灯
    url  = 'http://www.shuquge.com/txt/9160/index.html'     # 红楼梦
    txt  = getHtmlText(url)                                 # Whole HTML Content
    soup = BeautifulSoup(txt, "lxml")
    head = soup.find('div',class_='info')     # Story Header
    body = soup.find('div',class_='listmain') # Story Content
    
    loadBookTitle(head)
    loadChapterList(body, url)
    loadChapterContent()
    
    accs = MySqlAccess()
    # saveMemberList(accs)
    # accs.close()
    
main()