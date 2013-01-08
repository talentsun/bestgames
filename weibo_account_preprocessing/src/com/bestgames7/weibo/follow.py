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

class Bestgames:
    UID = 3177187433
    ACCESS_TOKENS = ['2.00baJBTDqIR4cB04fca35e15ygoN_D',
                     '2.00baJBTDycMMdCd14db81f370tubtd',
                     '2.00baJBTDyWXWFCd18110ba2fdigGjC',
                     '2.00baJBTD0owgm_194216a0594XdWbB',
                     '2.00baJBTD634dZE99dade5113mZtTUE',
                     '2.00baJBTDNWR6xD01ac9160010KIVoL',
                     '2.00baJBTDtETxxB42857545e2PpruEC',
                     '2.00baJBTDHQFodEdad8aeb243rzkHWE']

def follow_v1(oauth_token, oauth_token_secret, uid):
    weiboClientV1 = APIClientV1(app_key, app_secret, OAuthToken(oauth_token, oauth_token_secret))
    
    successed = False
    
    try:
        weiboClientV1.post.friendships__create(source=app_key, user_id=uid)
        successed = True
    except Exception, e:
        print e
        
    return successed
        
def unfollow_v1(oauth_token, oauth_token_secret, uid):
    weiboClientV1 = APIClientV1(app_key, app_secret, OAuthToken(oauth_token, oauth_token_secret))
    
    successed = False
    
    try:
        weiboClientV1.post.friendships__destroy(source=app_key, user_id=uid)
        successed = True
    except Exception, e:
        print e
        
    return successed
        
def follow_v2(access_token_, uid_):
    weiboClientV2 = APIClientV2(app_key, app_secret)
    weiboClientV2.set_access_token(access_token_, time.time() + 90 * 24 * 3600)
    
    successed = False
    
    try:
        ret = weiboClientV2.post.friendships__create(uid=uid_)
        successed = True
    except Exception, e:
        print e
        
    return successed

def unfollow_v2(access_token_, uid_):
    weiboClientV2 = APIClientV2(app_key, app_secret)
    weiboClientV2.set_access_token(access_token_, time.time() + 90 * 24 * 3600)
    
    successed = False
    
    try:
        ret = weiboClientV2.post.friendships__destroy(uid=uid_)
        successed = True
    except Exception, e:
        print e
        
    return successed
        
def is_follow_v2(access_token_, source_uid_, target_uid_):
    weiboClientV2 = APIClientV2(app_key, app_secret)
    weiboClientV2.set_access_token(access_token_, time.time() + 90 * 24 * 3600)
    
    followed = False
    
    try:
        ret = weiboClientV2.get.friendships__show(access_token=access_token_, source_id=source_uid_, target_id=target_uid_)
        followed = ret.source.following
    except Exception,e:  
        print e
    
    return followed

def is_follow_v1(oauth_token, oauth_token_secret, source_uid_, target_uid_):
    weiboClientV1 = APIClientV1(app_key, app_secret, OAuthToken(oauth_token, oauth_token_secret))
    
    followed = False
    
    try:
        weiboClientV1.get.friendships__show(source=app_key, source_id=source_uid_, target_id=target_uid_)
        followed = ret.source.following
    except Exception, e:
        print e
        
    return followed

def is_followed_by_v1(oauth_token, oauth_token_secret, source_uid_, target_uid_):
    weiboClientV1 = APIClientV1(app_key, app_secret, OAuthToken(oauth_token, oauth_token_secret))
    
    followed = False
    
    try:
        ret = weiboClientV1.get.friendships__show(source=app_key, source_id=source_uid_, target_id=target_uid_)
        followed = ret.source.followed_by
    except Exception, e:
        print e
        
    return followed

def is_followed_by_v2(access_token_, source_uid_, target_uid_):
    weiboClientV2 = APIClientV2(app_key, app_secret)
    weiboClientV2.set_access_token(access_token_, time.time() + 90 * 24 * 3600)
    
    followed = False
    
    try:
        ret = weiboClientV2.get.friendships__show(access_token=access_token_, source_id=source_uid_, target_id=target_uid_)
        followed = ret.source.followed_by
    except Exception,e:  
        print e
    
    return followed