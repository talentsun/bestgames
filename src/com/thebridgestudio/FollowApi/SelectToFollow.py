#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from AccessInfo.models import Access
from FollowMeTask.models import FollowMeTask

from weibo import APIClient as APIClientV2
from AppValue import BGApp
from FriendShip import FriendShip

from Utils import *

import datetime, time, traceback


def GetLatestTweetTime(client, uid):
    tweets = client.get.statuses__user_timeline(uid=uid, count=10, trim_user=1)
    tweets = tweets['statuses']
    if len(tweets) == 0:
        return None
    else:
        timeStr = tweets[0].created_at
        timeStr = timeStr[:-11] + timeStr[-5:]
        return datetime.datetime.strptime(timeStr, "%a %b %d %H:%M:%S %Y")
def GetNumber(client, uid):
    userInfo = client.get.users__show(uid=uid)
    return userInfo
def SelectToFollow1(logger, client, num):
    now = datetime.datetime.now()
    allnum = 0
    rightnum = 0
    for a in Access.objects.all():
        try:
            allnum += 1
            if num == 0:
                break
            num -= 1
            try:
                task = FollowMeTask.objects.get(uid=a.uid)
                continue
            except:
                task = FollowMeTask()
            logger.debug("deal with %d" % a.uid)
            time.sleep(1)
            lastTime = GetLatestTweetTime(client, a.uid)
            if lastTime == None:
                continue
            secs = (now - lastTime).total_seconds()
            if secs > 3600 * 24 * 30:
                logger.debug("one month not write tweet")
                continue
            userInfo = GetNumber(client, a.uid)
            followerNum = userInfo['followers_count']
            friendNum = userInfo['friends_count']
            location = userInfo['location']
            if followerNum < friendNum and followerNum > 60 and followerNum < 150 and u'北京' not in location and u'其他' not in location:
                task.uid = a.uid
                task.status = 0
                task.type = 1
                rightnum += 1
                task.save()
                logger.debug("add to task %u" % task.uid)
        except:
            logger.debug(traceback.format_exc())


if __name__ == '__main__':
    logger = InitLogger("select_to_follow", logging.DEBUG, "../log/select_to_follow.log")
    client = APIClientV2(BGApp.wdj_app_key, BGApp.wdj_app_secret)
    client.set_access_token(BGApp.wdj_me_token, time.time() + 90 * 24 * 3600)
    SelectToFollow1(logger, client, -1)

