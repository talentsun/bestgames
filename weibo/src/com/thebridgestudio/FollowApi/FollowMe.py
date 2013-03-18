#!/usr/bin/python
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
    for task in FollowMeTask.objects.filter(type=1, status = 0)[:number]:
        try:
            try:
                user = Access.objects.get(uid=task.uid)
            except:
                logger.error("not find access info for %d", task.uid)
                continue

            logger.debug("user %d" % user.uid)
            if user.version == 1:
                client = APIClientV1(BGApp.wdj_app_key, BGApp.wdj_app_secret, OAuthToken(user.data1, user.data2))
                client.post.friendships__create(source=BGApp.wdj_app_key, user_id = BGApp.dev_uid)
                task.status = 1
                task.save()
            elif user.version == 2:
                client = APIClientV2(BGApp.wdj_app_key, BGApp.wdj_app_secret)
                client.set_access_token(user.data1, time.time() + 90*24*3600)
                followed = FriendShip.Follow(client, BGApp.dev_uid)
                task.status = 1
                task.save()
            else:
                logger.debug("bad user version %d", user.version)
                task.status = 2
                task.save()
                continue
            time.sleep(60)
        except:
            task.status = 2
            task.save()
            logger.debug(traceback.format_exc())
            time.sleep(60)




if __name__ == '__main__':
    logger = InitLogger("follow_me", logging.DEBUG, "../log/follow_me.log")
    FollowMe(100, logger)








