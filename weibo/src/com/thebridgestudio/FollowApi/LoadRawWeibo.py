#!/usr/local/bin/python2.7
import re
import MySQLdb

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from AccessInfo.models import Access

def GetAccessToken(info):
    accessTokenMatch = re.search(r'access_token";s:32:"([\.\w]+)"', info)
    if accessTokenMatch:
        return accessTokenMatch.group(1)
    return None


def GetOauthToken(info):
    oauthTokenMatch = re.search(r'oauth_token";s:32:"([\w]+)"', info)
    if oauthTokenMatch:
        return oauthTokenMatch.group(1)
    return None


def GetOauthTokenSecret(info):
    oauthTokenSecretMatch = re.search(r'oauth_token_secret";s:32:"([\w]+)"', info)
    if oauthTokenSecretMatch:
        return oauthTokenSecretMatch.group(1)
    return None

def ReadRAWData(limit, offset):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select fromuid, propdata from RAW_weibo_20110101_20121206 limit %d offset %d" % (limit, offset))
    for row in cursor.fetchall():
        uid = int(row[0])
        try:
            a = Access.objects.get(uid=uid)
            continue
        except:
            a = Access()
            a.uid = uid
            
        if 'access_token' in row[1]:
            a.version = 2
            a.data1 = GetAccessToken(row[1])
            if a.data1 == None:
                continue
            a.save()
        elif 'oauth_token' in row[1] and 'oauth_token_secret' in row[1]:
            a.version = 1
            a.data1 = GetOauthToken(row[1])
            a.data2 = GetOauthTokenSecret(row[1])
            if a.data1 == None or a.data2 == None:
                continue
            a.save()

    cursor.close()
    conn.close()
        
    


if __name__ == '__main__':
    ReadRAWData(1000000, 0)

    
