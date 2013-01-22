#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
from datetime import datetime

def db_follow_them(uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update users set rel_followed_them=1, rel_followed_them_date=%s where uid=%s",(datetime.today().strftime('%Y-%m-%d %H:%M:%S'),uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
def db_unfollow_them(uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update users set rel_followed_them=-1, rel_unfollowed_them_date=%s where uid=%s",(datetime.today().strftime('%Y-%m-%d %H:%M:%S'),uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
def db_unfollow_me(uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update users set rel_followed_me=-1, rel_unfollowed_me_date=%s where uid=%s",(datetime.today().strftime('%Y-%m-%d %H:%M:%S'),uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()

def db_follow_me(uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update users set rel_followed_me=1, rel_followed_me_date=%s where uid=%s",(datetime.today().strftime('%Y-%m-%d %H:%M:%S'),uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()

def db_task_processed(task, uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update tasks set state=1,timestamp=%s where name=%s and uid=%s",(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), task, uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()