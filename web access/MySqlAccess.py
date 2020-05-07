# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:18:12 2020

@author: Wenjie
"""

import MySQLdb
# import logging
# import sys

class MySqlAccess():
    def __init__(self, host="127.0.0.1", username="wenjie", password="wenjie1234", port=3306, database="python"):
        """类例化，处理一些连接操作"""
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database
        self.cursor = None
        self.connect = None
        
        #Connect to Mysql
        try:
            self.connect = MySQLdb.connect(self.host,self.username,self.password,self.database,port=self.port,charset='utf8')
            self.cursor  = self.connect.cursor()
        except Exception as e:
            print("Database Connect Error, Please Check the DB Configuration.")
            raise e
            
    def close(self):
        """结束查询和关闭连接"""
        self.connect.close()
        
    def create_table(self, sql_str):
        """创建数据表"""
        try:
            self.cursor.execute(sql_str)
        except Exception as e:
            print(e)
            
    def drop_table(self, sql_str):
        """删除数据表"""
        try:
            self.cursor.execute(sql_str)
        except Exception as e:
            print(e)
            
    def query_count(self, tab_name, where_sql="", args=None):
        """根据Where条件查询记录条数
            cursor   ： 连接光标
            where_sql： 查询条件
        """
        sql_str = "select count(*) from " + tab_name + " " + where_sql
        try:
            self.cursor.execute(sql_str, args)
            xcnt = self.cursor.fetchone()
            return xcnt[0]
        except Exception as e:
            print(e)
            return -1
            
    def query_formatrs(self, sql_str, args=None):
        """查询数据，返回一个列表，里面的每一行是一个字典，带字段名
            cursor ： 连接光标
            sql_str： 查询语句
        """
        try:
            self.cursor.execute(sql_str)
            rows = self.cursor.fetchall()
            ress = []
            for xrow in rows:
                ress.append(dict(zip(self.cursor.columns,xrow)))
            return ress
        except:
            return False
        
    def query(self, sql_str, args=None):
        """查询数据并返回
            cursor ： 连接光标
            sql_str： 查询语句
        """
        try:
            self.cursor.execute(sql_str, args)
            rows = self.cursor.fetchall()
            return rows
        except:
            return False
        
    def delete(self, sql_str, args=None):
        """删除数据并返回执行结果
            cursor ： 连接光标
            sql_str： 查询语句
        """
        try:
            res = self.cursor.execute(sql_str, args=args)
            self.connect.commit()
        except Exception as e:
            self.connect.close()
            print("Sql-Stmt:",sql_str,end='\n')
            print("Sql-Args:",args,end='\n')
            raise e
        return res
        
    def exec_update_insert(self, sql_str, args=None):
        """
            插入或更新记录，成功则返回最后id
        """
        try:
            self.cursor.execute(sql_str, args=args)
            self.connect.commit()
        except Exception as e:
            self.connect.close()
            print("Sql-Stmt:",sql_str,end='\n')
            print("Sql-Args:",args,end='\n')
            raise e
        return self.cursor.lastrowid