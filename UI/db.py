# -*- coding: utf-8 -*-
import sqlite3

#  id 省 市 姓名 电话 学术职称 医学职称  医院大名 医院小名 科室 擅长 简介
table_items ='ID,SHENG,SHI,NAME,PHONE,XUESHUZHICHENG,YIXUEZHICHENG,YIYUAN_DAMING,YIYUAN_XIAOMING,KESHI,SHANCHANG,JIANJIE'

conn = sqlite3.connect('doctor_info1.5.db')

def create_db():
    conn.execute('CREATE TABLE  IF NOT EXISTS DOCTOR  (ID INTEGER PRIMARY KEY AUTOINCREMENT, SHENG TEXT NOT NULL,NAME TEXT NOT NULL,SHI TEXT NOT NULL,PHONE TEXT NOT NULL,XUESHUZHICHENG TEXT NOT NULL,YIXUEZHICHENG TEXT NOT NULL,YIYUAN_DAMING TEXT NOT NULL,YIYUAN_XIAOMING TEXT NOT NULL,KESHI TEXT NOT NULL,SHANCHANG TEXT NOT NULL,JIANJIE TEXT NOT NULL) ')
    conn.commit()

#查询全部的
def show_all_doctor():
    cursor = conn.execute('SELECT %s FROM DOCTOR  order by ID LIMIT 0,50' % table_items )
    return cursor

#按照条件进行查询
def show_like_doctor(condition):
    if (condition ==None or len(condition)==0):
        return show_all_doctor()
    else:   
        sql ='SELECT %s FROM DOCTOR  WHERE %s  order by ID LIMIT 0,50' % (table_items,condition);
        print sql 
        cursor = conn.execute(sql)
        return cursor

#插入数据
def insert_doctor(name,phone,yiyuan_daming,yiyuan_xiaoming,keshi,shanchang):
    conn.execute("INSERT INTO DOCTOR (%s) VALUES (NULL,'%s','%s','%s','%s','%s','%s')" % (table_items,name,phone,yiyuan_daming,yiyuan_xiaoming,keshi,shanchang))
    conn.commit()
    
# 插入   'name,phone,类型的数据'
def insert_doctor_by_info(info):
    print info
    sql ="INSERT INTO DOCTOR (%s) VALUES (NULL,'%s')" % (table_items,info.replace('__',"','"));
    print sql
    conn.execute(sql)
    conn.commit()
    
    
#删除
def detele_doctor(id):
#     print id
    sql ='delete from doctor where id =%s' % id;
    conn.execute(sql)
    conn.commit()
    
    
    
    
    