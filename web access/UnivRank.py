#web爬虫学习 -- 分析
#获取页面信息
 
#输入：url
#处理：request库函数获取页面信息，并将网页内容转换成为人能看懂的编码格式
#输出：爬取到的内容

import requests                 #http library
from bs4 import BeautifulSoup   #xml parsing library
allUniv = []

def getHtmlText(url):
    try:
        req = requests.get(url, timeout=30)
        req.raise_for_status()  #如果状态码不是200， 抛出异常
        req.encoding = 'utf-8'
        return req.text
    except:   #抛出异常
        return ""

def fillUnivList(soup):
    data = soup.find_all("tr")
    for tr in data:
        ltd = tr.find_all("td")
        if len(ltd) == 0:
            continue
        singleUniv = []
        for td in ltd:
            singleUniv.append(str(td.string).strip())
        allUniv.append(singleUniv)
        
def printUnivList(num):
    print("{:^4}{:^30}{:^5}{:^8}{:^10}".format("排名","学校名称","省市","总分","规模培养"))
    for i in range(num):
        u=allUniv[i]
        print("{:^4}{:^30}{:^5}{:^8}{:^10}".format(u[0],u[1],u[2],u[3],u[6]))
        
def main():
    url  = 'https://movie.douban.com/chart'
    url  = 'http://www.baidu.com'
    url  = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    txt  = getHtmlText(url)
    soup = BeautifulSoup(txt, "html.parser")
    
    fillUnivList(soup)
    printUnivList(10)
    
main()