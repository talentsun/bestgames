#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from weibo1 import APIClient as APIClientV1
from weibo1 import OAuthToken
from weibo import APIClient as APIClientV2
import time

app_key = '1483181040'
app_secret = '6f503ed72723bacf9f4a0f4902b62c24'

bestgames_uid = 3177187433
bestgames_access_token = '2.00baJBTDqIR4cB04fca35e15ygoN_D'

def follow_v1(oauth_token, oauth_token_secret, uid):
    weiboClientV1 = APIClientV1(app_key, app_secret, OAuthToken(oauth_token, oauth_token_secret))
    
    try:
        weiboClientV1.post.friendships__create(source=app_key, user_id=uid)
    except Exception, e:
        print e
        
def unfollow_v1(oauth_token, oauth_token_secret, uid):
    weiboClientV1 = APIClientV1(app_key, app_secret, OAuthToken(oauth_token, oauth_token_secret))
    
    try:
        weiboClientV1.post.friendships__destroy(source=app_key, user_id=uid)
    except Exception, e:
        print e
        
def follow_v2(access_token_, uid_):
    weiboClientV2 = APIClientV2(app_key, app_secret)
    weiboClientV2.set_access_token(access_token_, time.time() + 90 * 24 * 3600)
    
    try:
        weiboClientV2.post.friendships__create(uid=uid_)
    except Exception, e:
        print e

def unfollow_v2(access_token_, uid_):
    weiboClientV2 = APIClientV2(app_key, app_secret)
    weiboClientV2.set_access_token(access_token_, time.time() + 90 * 24 * 3600)
    
    try:
        weiboClientV2.post.friendships__destroy(uid=uid_)
    except Exception, e:
        print e