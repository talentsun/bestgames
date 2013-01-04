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
    
if __name__ == '__main__':
    get_users_v2(49616,108697)