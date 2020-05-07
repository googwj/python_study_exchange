# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:04:26 2020

@author: Wenjie
"""

#web爬虫应用
#
 
#输入：url
#处理：request库函数获取页面信息，并将网页内容转换成为人能看懂的编码格式
#输出：访问联合国中文官方网站，获取所有成员国名单

import requests                 #http library
from bs4 import BeautifulSoup   #xml parsing library
from MySqlAccess import MySqlAccess

memberList = []

def getHtmlText(url):
    try:
        req = requests.get(url, timeout=30)
        req.raise_for_status()  #如果状态码不是200， 抛出异常
        req.encoding = 'utf-8'
        return req.text
    except:   #抛出异常
        return ""

def fillMemberList(soup):
    mems = soup.find_all('span',class_='member-state-name')
    jdts = soup.find_all('span',class_='date-display-single')
    infs = soup.find_all('div',class_='collapse')
    cntr = len(mems)
    
    for ix in range(cntr):
        xmem = mems[ix].string.strip()
        xjdt = jdts[ix].string
        xinf = infs[ix]
        
        xsit = xinf.find_all('div',class_='site')[0].find_all('a')
        if len(xsit) == 0:
            xsit = ''
        else:
            xsit = xsit[0]['href']
            
        xadr = xinf.find_all('div',class_='mail')[0].find_all('a')
        if len(xadr) == 0:
            xadr = ''
        else:
            xadr = xadr[0].string
            if xadr is None:
                xadr = ''
            
        xphs = xinf.find_all('div',class_='phone')[0].find_all('li')
        xpho = ''
        for ipho in xphs:
            if xpho == '':
                xpho = ipho.string.strip()
            else:
                xpho = xpho + " & " + ipho.string.strip()
                
        xhol = xinf.find_all('div',class_='national-holiday')[0].string.strip()
        xenn = xinf.find_all('div',class_='chart')[0].find_all('a')[0].string[17:]
        xcms = xinf.find_all('div',class_='')[0].find_all('p')
        xcmm = ''
        for icmm in xcms:
            if xcmm == '':
                xcmm = icmm.get_text().strip()
            else:
                xcmm = xcmm + '\n' + icmm.get_text().strip()

        UnMember = []
        if xmem[-1:] == '*':
            xmem = xmem[0:-1]
        if int(xjdt[-2:]) < 45:
            xjdt = '20' + xjdt[-2:] + '-' + xjdt[3:5] + '-' + xjdt[0:2]
        else:
            xjdt = '19' + xjdt[-2:] + '-' + xjdt[3:5] + '-' + xjdt[0:2]
        UnMember.append(xmem)
        UnMember.append(xenn)
        UnMember.append(xjdt)
        UnMember.append(xhol)
        UnMember.append(xsit)
        UnMember.append(xadr)
        UnMember.append(xpho)
        UnMember.append(xcmm)
        
        memberList.append(UnMember)
        
def saveMemberList(mySql):
    sql_ins = """
                insert into un_member_states(country_chinese, country_english, joined_date, holiday, web_site, address, phone, comment)
                                       value(%s,              %s,              %s,          %s,      %s,       %s,      %s,    %s)
              """
    sql_upd = """
                update un_member_states
                   set joined_date = %s,
                       holiday     = %s,
                       web_site    = %s,
                       address     = %s,
                       phone       = %s,
                       comment     = %s
                 where country_chinese = %s
              """
    exe_all = 0
    upd_all = 0
    ins_all = 0
    for UnMember in memberList:
        exe_all = exe_all + 1
        print(str(exe_all+1)+"|",UnMember[0]+"|",UnMember[1]+"|",UnMember[2]+"|",UnMember[3]+"|",UnMember[4]+"|",UnMember[5]+"|",UnMember[6]+"|",UnMember[7]+"|")
        if mySql.query_count("un_member_states","where country_chinese = %s",(UnMember[0],)) < 1:
            ins_all = ins_all + 1
            mySql.exec_update_insert(sql_ins,(UnMember[0],UnMember[1],UnMember[2],UnMember[3],UnMember[4],UnMember[5],UnMember[6],UnMember[7]))
        else:
            upd_all = upd_all + 1
            mySql.exec_update_insert(sql_upd,(UnMember[2],UnMember[3],UnMember[4],UnMember[5],UnMember[6],UnMember[7],UnMember[0]))
            
    print("Total Processed:", exe_all)
    print("Total Inserted :", ins_all)
    print("Total Updated  :", upd_all)
    

def main():
    url  = 'https://www.un.org/zh/member-states/index.html'
    txt  = getHtmlText(url)                                 # Whole HTML Content
    soup = BeautifulSoup(txt, "lxml")
    mdat = soup.find_all('div',class_='view-content')[0]    # Main HTML Data
    
    fillMemberList(mdat)
    
    accs = MySqlAccess()
    saveMemberList(accs)
    accs.close()
    
main()