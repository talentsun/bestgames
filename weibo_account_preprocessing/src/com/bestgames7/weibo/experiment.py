#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
from follow import bestgames_access_token
from follow import follow_v2
import time
import random

'''
(0,50]        200
[50,100)      200
[100,150)     200
[150,200)     200
[200,250)     200
[250,300)     200
[300,400)     200
[400,500)     200
[500,1000)    200
[1000,+)      200
'''
def build_experiment(experiment, configs):
    for config in configs:
        users = sample_users(config[0],config[1],config[2])
        for user in users:
            print 'add ' + user[0] + ' into ' + experiment
            save_user_to_experiment(experiment, user)

def sample_users(min_followers, max_followers, count):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    users = []
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute('select uid from users where followers_count >= %s and followers_count < %s limit 0,%s',(min_followers, max_followers, count))
        
        index=1
        for row in staging_cursor.fetchall():
            user = get_access_token(row[0])
            if user:
                users.append(user)
                print '%d: %s' % (index, user[0])
                index = index + 1
                
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
    return users

def get_access_token(uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    user = None
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute('select * from access_token where uid=%s',(uid))
        
        user = staging_cursor.fetchone()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
    return user

def save_user_to_experiment(experiment, user):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute('insert into experiments(experiment, uid, version, data1, data2, followed_them, followed_us, status) values(%s,%s,%s,%s,%s,0,0,0)',(experiment, user[0], user[1], user[2], user[3]))
        
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()

def execute_experiment(experiment):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute('select uid from experiments where experiment=%s and followed_us=0 and followed_them=0',(experiment))
        
        index=1
        for row in staging_cursor.fetchall():
            print '%d: follow %s' % (index, row[0])
            follow_v2(bestgames_access_token, row[0])
            follow_them(experiment, row[0])
            index = index + 1
            if index % 100 == 0:
                time.sleep(random.randint(0,2) * 1800)
            else:
                time.sleep(random.randint(1,10))
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
def follow_them(experiment, uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update experiments set followed_them=1 where experiment=%s and uid=%s",(experiment,uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()

if __name__ == '__main__':
    execute_experiment('refollow_rate-by-followers_count')