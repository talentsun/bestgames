#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*-

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from FollowMeTask.models import FollowMeTask
from AccessInfo.models import Access

from weibo import APIClient as APIClientV2
from weibo1 import APIClient as APIClientV1
from weibo1 import OAuthToken
from AppValue import BGApp
from FriendShip import FriendShip


from Utils import *

import datetime, time, traceback

def FollowMe(number, logger):
    followNum = 0
    for task in FollowMeTask.objects.filter(type=1, status = 0)[:number * 2]:
        try:
            if followNum > number:
                break
            try:
                user = Access.objects.get(uid=task.uid)
            except:
                logger.error("not find access info for %d", task.uid)
                continue

            logger.debug("user %d" % user.uid)
            if user.version == 1:
                client = APIClientV1(BGApp.wdj_app_key, BGApp.wdj_app_secret, OAuthToken(user.data1, user.data2))
                try:
                    tuser = client.post.users__show(source=BGApp.wdj_app_key, user_id=user.uid)
                except Exception, e:
                    print e
                    logger.debug(traceback.format_exc())
                    logger.debug("time out access token")
                    task.status = 2
                    task.save()
                    time.sleep(1)
                    continue
                client.post.friendships__create(source=BGApp.wdj_app_key, user_id = BGApp.dev_uid)
                task.status = 1
                task.save()
                followNum += 1
            elif user.version == 2:
                client = APIClientV2(BGApp.wdj_app_key, BGApp.wdj_app_secret)
                client.set_access_token(user.data1, time.time() + 90*24*3600)
                try:
                    tuser = client.get.users__show(uid=user.uid)
                except:
                    logger.debug(traceback.format_exc())
                    traceback.print_exc()
                    logger.debug("time out access token")
                    time.sleep(1)
                    task.status = 2
                    task.save()
                    continue
                followed = FriendShip.Follow(client, BGApp.dev_uid)
                task.status = 1
                followNum += 1
                task.save()
            else:
                logger.debug("bad user version %d", user.version)
                task.status = 2
                task.save()
                followNum += 1
                continue
            time.sleep(60)
        except:
            task.status = 2
            task.save()
            followNum += 1
            logger.debug(traceback.format_exc())
            traceback.print_exc()
            time.sleep(60)




if __name__ == '__main__':
    logger = InitLogger("follow_me", logging.DEBUG, "../log/follow_me.log")
    FollowMe(350, logger)








