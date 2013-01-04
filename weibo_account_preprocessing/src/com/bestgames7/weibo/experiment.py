#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
from follow import Bestgames
from follow import follow_v1
from follow import follow_v2
from follow import is_follow_v2
from follow import is_followed_by_v2
import time
from datetime import datetime
from db import *

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
        staging_cursor.execute('select uid from experiments where experiment=%s and followed_us=0 and followed_them=0 limit 300',(experiment))
        
        index=0
        for row in staging_cursor.fetchall():
            uid = row[0]
            access_token = Bestgames.ACCESS_TOKENS[index%8]
            if is_follow_v2(access_token, Bestgames.UID, uid):
                print '%d: %s is followed' % (index, uid)
                follow_them(experiment, uid)
            else:
                print '%d: follow %s' % (index, uid)
                if follow_v2(access_token, uid):
                    if is_follow_v2(access_token, Bestgames.UID, uid):
                        follow_them(experiment, uid)
                    else:
                        print '%d: follow %s failed' % (index, uid)
                time.sleep(15)
            index = index + 1
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
curve1 = [0.05, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.03, 0.04, 0.05, 0.05, 0.06, 0.06, 0.05, 0.06, 0.06, 0.06, 0.06, 0.06, 0.05, 0.06, 0.06, 0.07]

def addfans(experiment, curve):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute('select uid, version, data1, data2 from experiments where experiment=%s and followed_us=0 and followed_them=0',(experiment))
        
        index=0
        for row in staging_cursor.fetchall():
            hour_count = 600 * curve[datetime.today().time().hour]
            sleep_interval = 3600 / hour_count
            
            uid = row[0]
            version = int(row[1])
            if version == 1:
                if follow_v1(row[2], row[3], Bestgames.UID):
                    print '%d: %s followed us' % (index, uid)
                    follow_me(experiment, uid)
                else:
                    print '%d: %s failed' % (index, uid)
            elif version == 2:
                if follow_v2(row[2], Bestgames.UID):
                    print '%d: %s followed us' % (index, uid)
                    follow_me(experiment, uid)
                else:
                    print '%d: %s failed' % (index, uid)
            index = index + 1
            
            time.sleep(sleep_interval)
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()

def validate_experiment(experiment):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute('select uid from experiments where experiment=%s and followed_us=0 and followed_them=1',(experiment))
        
        index=0
        for row in staging_cursor.fetchall():
            uid = row[0]
            access_token=Bestgames.ACCESS_TOKENS[0]
            
            print '%d: process %s' % (index, uid)
            if not is_follow_v2(access_token, Bestgames.UID, uid):
                print '%d: %s unfollow them' % (index, uid)
                unfollow_them(experiment, uid)
            if is_followed_by_v2(access_token, Bestgames.UID, uid):
                print '%d: %s followed us' % (index, uid)
                follow_me(experiment, uid)
            time.sleep(0.1)
            index = index + 1
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
        staging_cursor.execute("update experiments set followed_them=1,followed_them_date=%s where experiment=%s and uid=%s",(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), experiment,uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
    db_follow_them(uid)
    
def unfollow_them(experiment, uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update experiments set followed_them=0 where experiment=%s and uid=%s",(experiment,uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
    db_unfollow_them(uid)

def follow_me(experiment, uid):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute("update experiments set followed_us=1,followed_us_date=%s where experiment=%s and uid=%s",(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), experiment,uid))
        staging_conn.commit()
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
    db_follow_me(uid)

if __name__ == '__main__':
    validate_experiment('refollow_rate-by-followers_count')
    execute_experiment('refollow_rate-by-followers_count')