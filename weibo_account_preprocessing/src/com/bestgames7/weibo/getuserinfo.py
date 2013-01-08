#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
from weibo1 import APIClient
from weibo1 import OAuthToken
from weibo import APIClient as APIClientV2
import time
from datetime import datetime,timedelta,date
from follow import unfollow_v1,unfollow_v2,Bestgames,is_followed_by_v1, is_followed_by_v2
from db import *

app_key = '1483181040'
app_secret = '6f503ed72723bacf9f4a0f4902b62c24'

def get_user_info_v1(uid, oauth_token, oauth_token_secret):
    weiboClientV1 = APIClient(app_key, app_secret, OAuthToken(oauth_token, oauth_token_secret))
    user = None
    
    try:
        user = weiboClientV1.post.users__show(source=app_key, user_id=uid)
    except Exception, e:
        print e
    
    return user

def save_user_info(user_info, token_version, token_data1, token_data2):
    if not user_info:
        return
    
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        if token_version == 2:
            staging_cursor.execute('insert into users(uid, verified, followers_count, statuses_count, friends_count, screen_name, name, favourites_count, gender, token_version, token_data1, rel_followed_me, rel_followed_them) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, 2, %s, 0, 0)',
                                         (int(user_info.id),int(user_info.verified),int(user_info.followers_count),int(user_info.statuses_count),int(user_info.friends_count),user_info.screen_name,user_info.name,int(user_info.favourites_count),user_info.gender, token_data1))
        elif token_version == 1:
            staging_cursor.execute('insert into users(uid, verified, followers_count, statuses_count, friends_count, screen_name, name, favourites_count, gender, token_version, token_data1, token_data2, rel_followed_me, rel_followed_them) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s, 0, 0)',
                                         (int(user_info.id),int(user_info.verified),int(user_info.followers_count),int(user_info.statuses_count),int(user_info.friends_count),user_info.screen_name,user_info.name,int(user_info.favourites_count),user_info.gender, token_data1, token_data2))
        staging_conn.commit()
    except Exception,e:
        print e
    
    staging_cursor.close()
    staging_conn.close()
    
def get_user_info_v2(uid_, access_token_):
    weiboClientV2 = APIClientV2(app_key, app_secret)
    weiboClientV2.set_access_token(access_token_, time.time() + 90 * 24 * 3600)
    
    user = None
    
    try:
        user = weiboClientV2.get.users__show(access_token=access_token_, uid=uid_)
    except Exception, e:
        print e
    
    return user

def exists(uid):
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo')
    except Exception, e:
        print e
    
    exists = False
    try:
        cursor = conn.cursor()
        count = cursor.execute('select * from users where uid=%s' % uid)
        exists = count > 0
    except Exception,e:
        print e
    
    cursor.close()
    conn.close()
    
    return exists

def get_users_v1(offset, limit):
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo')
    except Exception, e:
        print e
    
    try:
        cursor = conn.cursor()
        cursor.execute('select * from access_token where version=1 limit %d,%d' % (offset, limit))
        index=1
        for row in cursor.fetchall():
            print '%d: process %s' % (index, row[0])
            if (not exists(row[0])):
                save_user_info(get_user_info_v1(row[0], row[2],row[3]), 1, row[2], row[3])
                time.sleep(0.36)
            else:
                print row[0] + ' exists'
            index = index + 1
    except Exception,e:
        print e
        sys.exit()
    
    cursor.close()
    conn.close()
    
def get_users_v2(offset, limit):
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo')
    except Exception, e:
        print e
    
    try:
        cursor = conn.cursor()
        cursor.execute('select * from access_token where version=2 limit %d,%d' % (offset, limit))
        index=1
        for row in cursor.fetchall():
            print '%d: process %s' % (index, row[0])
            if (not exists(row[0])):
                save_user_info(get_user_info_v2(row[0], row[2]), 2, row[2], None)
                time.sleep(0.36)
            else:
                print row[0] + ' exists'
            index = index + 1
    except Exception,e:
        print e
        sys.exit()
    
    cursor.close()
    conn.close()
    
def update_users():
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo')
    except Exception, e:
        print e
    
    try:
        cursor = conn.cursor()
        cursor.execute('select uid, token_version, token_data1, token_data2, rel_followed_them, rel_followed_them_date, rel_followed_me from users where rel_followed_them=1 or rel_followed_me=1')
        index=1
        for row in cursor.fetchall():
            uid = row[0]
            token_version = row[1]
            token_data1 = row[2]
            token_data2 = row[3]
            rel_followed_them = row[4]
            rel_followed_them_date = row[5]
            rel_followed_me = row[6]
            
            print '%d: process %s' % (index, row[0])
            if rel_followed_them == 1:
                #unfollow users followed and not refollow a week ago
                need_unfollow = False
                if rel_followed_them_date is not None:
                    if (date.today() - rel_followed_them_date.date()).days >= 7:
                        need_unfollow = True
                else:
                    need_unfollow = True
                if need_unfollow:
                    print 'unfollow %s because of timeout' % (uid)
                    unfollow_v2(Bestgames.ACCESS_TOKENS[0], uid)
                    db_unfollow_them(uid)
                    
            if rel_followed_me == 1:
                need_unfollow = False
                if token_version == 1:
                    if not is_followed_by_v1(token_data1, token_data2, Bestgames.UID, uid):
                        need_unfollow = True
                elif token_version == 2:
                    if not is_followed_by_v2(token_data1, Bestgames.UID, uid):
                        need_unfollow = True
                if need_unfollow:
                    print 'update %s bescause they unfollow me' % (uid)
                    db_unfollow_me(uid)
            index = index + 1
    except Exception,e:
        print e
        sys.exit()
    
    cursor.close()
    conn.close()
    
if __name__ == '__main__':
    update_users()