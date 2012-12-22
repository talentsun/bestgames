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
bestgames_wdj_access_token = '2.00baJBTDqIR4cB04fca35e15ygoN_D'
bestgames_papa_access_token = '2.00baJBTDycMMdCd14db81f370tubtd'
bestgames_putao_access_token = '2.00baJBTDyWXWFCd18110ba2fdigGjC'
bestgames_moji_access_token = '2.00baJBTD0owgm_194216a0594XdWbB'
bestgames_oi_access_token = '2.00baJBTD634dZE99dade5113mZtTUE'
bestgames_163reader_access_token = '2.00baJBTDNWR6xD01ac9160010KIVoL'
bestgames_qyer_access_token = '2.00baJBTDtETxxB42857545e2PpruEC'
bestgames_appchina_access_token = '2.00baJBTDDtVnrCa15211823dh0Y2SB'
bestgames_taoshenbian_access_token = '2.00baJBTDHQFodEdad8aeb243rzkHWE'
bestgames_duokan_access_token = '2.00baJBTDr0QrYC68c1438955yaf41C'

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