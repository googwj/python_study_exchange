# -*- coding: utf-8 -*-
"""
Created on Sun May  3 02:44:06 2020

@author: Wenjie
"""


import  MySQLdb

# 打开数据库连接
def openDataBase():
    url  = 'localhost'
    port = 3306
    user = 'wenjie'
    pswd = 'wenjie1234'
    dbnm = 'python'
    wsdb = MySQLdb.connect(url,user, pswd,dbnm,port=port,charset='utf8')
    return wsdb

# 关闭数据库连接
def closeDataBase(wsdb):
    wsdb.close()
    
# 使用cursor()方法获取操作游标 
def getCursor(wsdb):
    return wsdb.cursor()
    
# 使用execute方法执行SQL语句
def execCursorSQL(cursor,sqlStmt):
    cursor.execute(sqlStmt)
    
wsdb    = openDataBase()

cursor  = getCursor(wsdb)
sqlStmt = "select version()"
sqlStmt = "drop table if exists english_chinese_name"
execCursorSQL(cursor,sqlStmt)
sqlStmt = """
            create table english_chinese_name(
                english_name  CHAR(30) NOT NULL,
                gender        CHAR(10) NOT NULL,
                phonogram     CHAR(30),
                chinese_name  CHAR(30),
                name_resource CHAR(30),
                popularity    INT(1)
            )
          """
execCursorSQL(cursor,sqlStmt)

sqlStmt = """
            insert into english_chinese_name(english_name,gender,phonogram,chinese_name,name_resource,popularity)
            value(%s,%s,%s,%s,%s,%d)
          """
try:
    execCursorSQL(cursor,sqlStmt)
    wsdb.commit()
except:
    wsdb.rollback()
    
sqlStmt = "select * from english_chinese_name"
execCursorSQL(cursor,sqlStmt)

data    = cursor.fetchone()
print("Inquiry Result:", data)

    
sqlStmt = "delete from english_chinese_name"
try:
    execCursorSQL(cursor,sqlStmt)
    wsdb.commit()
except:
    wsdb.rollback()

data    = cursor.fetchone()
print("Inquiry Result:", data)

closeDataBase(wsdb)