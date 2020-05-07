# -*- coding: utf-8 -*-
"""
Created on Fri May  1 22:14:33 2020

@author: Wenjie
"""


#web爬虫应用
#
 
#输入：url
#处理：request库函数获取页面信息，并将网页内容转换成为人能看懂的编码格式
#输出：访问海词人名网抓取全部英文中文名并将其写入到数据表english_chines_name

import requests                 #http library
from bs4 import BeautifulSoup   #xml parsing library
from MySqlAccess import MySqlAccess
nameList = []

def getHtmlText(url):
    try:
        req = requests.get(url, timeout=30)
        req.raise_for_status()  #如果状态码不是200， 抛出异常
        req.encoding = 'utf-8'
        return req.text
    except:   #抛出异常
        return ""

def getIndexList(soup):
    hrefList = []
    data = soup.find_all('div',class_="o_mlet")[0]
    adds = data.find_all('a')
    for addr in adds:
        hrefList.append(addr['href'])
    return hrefList

def getIndexPages(soup):
    indexPages = 1
    data = soup.find_all('div',class_="pager")[0]
    adds = data.find_all('a')
    for addr in adds:
        hrefDesc = addr.string
        if hrefDesc == "最后页":
            indexPages = int(addr['href'][-1:])
    return indexPages

def fillNameList(soup):
    data = soup.find_all('table',class_="enname-all")[0]
    rows = data.find_all('tr')
    for xrow in rows:
        cols = xrow.find_all('td')
        if len(cols) == 0:
            continue
        nameCols = []
        ix   = 0
        for xcol in cols:
            ix = ix + 1
            if ix == 1:
                colValue = xcol.find_all('a')[0].string
            elif ix == 2:
                colValue = xcol.find_all('em')[0]['title']
                if colValue is None or colValue == '':
                    colValue = '中性'
            elif ix == 3:
                colValue = xcol.find_all('i')[0].string
            elif ix == 5:
                colValue = xcol.find_all('bdo')[0].string
            elif ix == 6:
                colValue = xcol.find_all('span')[0]['class'][0][-1:]
            else:
                colValue = xcol.string
            if colValue is None:
                colValue = ""
            nameCols.append(colValue)
        #     print(ix,'-[',colValue,']',end='\t')
        # print()
        nameList.append(nameCols)

def printNameList():
    print("{:<30}{:<10}{:<15}{:<15}{:<20}{:<20}".format("English_Name","性别","Phonogram","中文","Resource","Popularity"))
    for nameRows in nameList:
        print("{:<30}{:<10}{:<15}{:<15}{:<20}{:<20}".format(nameRows[0],nameRows[1],nameRows[2],nameRows[3],nameRows[4],nameRows[5]))
        
def saveNameList(mySql):
    sql_str = """
                insert into english_chinese_name(english_name,gender,phonogram,chinese_name,name_resource,popularity)
                value(%s,%s,%s,%s,%s,%s)
              """
    for nameRows in nameList:
        mySql.exec_update_insert(sql_str,(nameRows[0],nameRows[1],nameRows[2],nameRows[3],nameRows[4],nameRows[5]))

def main():
    accs = MySqlAccess()
    accs.delete("delete from english_chinese_name")
    url  = 'http://ename.dict.cn'
    txt  = getHtmlText(url)
    soup = BeautifulSoup(txt, "lxml")
    ilst = getIndexList(soup)
    for link in ilst:
        if str(link).startswith("/list/"):
            surl = url + link
            stxt = getHtmlText(surl)
            # print(stxt)
            soup = BeautifulSoup(stxt,"lxml")
            page = getIndexPages(soup)
            for indx in range(page):
                print('url:',surl + '/' + str(indx+1))
                stxt = getHtmlText(surl + '/' + str(indx+1))
                soup = BeautifulSoup(stxt,"lxml")
                fillNameList(soup)
            # break
    printNameList()
    saveNameList(accs)
    accs.close()
    
main()