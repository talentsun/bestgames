#!/usr/local/bin/python2.7

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from weibo import APIClient 
from AppValue import BGApp

import datetime, copy, sys, os, time

from FriendShip import FriendShip


if __name__ == '__main__':
    client = APIClient(BGApp.app_key, BGApp.app_secret)
    client.set_access_token(BGApp.weico_token, time.time() + 90 * 24 *3600)
    ret = client.get.friendships__groups__members__ids(list_id=0, count=200)
    all_users = ret['users']
    next_cursor = ret['next_cursor']
    users = all_users;

    while next_cursor > 0:
        print len(all_users)
        ret = client.get.friendships__groups__members__ids(list_id=0, count=200, cursor=next_cursor)
        users = ret['users']
        next_cursor = ret['next_cursor']
        print next_cursor
        all_users.extend(users)

    print len(all_users)
    for id in all_users:
        print "unfollow id %d" % id
        try:
            FriendShip.Unfollow(client, id)
        except:
            pass
        time.sleep(60)
