#!/usr/local/bin/python2.7

from django.core.management import setup_environ
from FollowApi import settings
setup_environ(settings)

from weibo import APIClient 
from AppValue import BGApp
from FriendShip import FriendShip

from Operations.models import Operation

import datetime, copy, sys, os, traceback

work_path = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    from Utils import *

    logger = InitLogger("unfollow", logging.DEBUG, work_path + "/log/unfollow.log")
    os.chdir(work_path)
    unfollowDay = datetime.date.today() - datetime.timedelta(days=3)
    ops = Operation.GetSomeDayOps(unfollowDay)
    client = APIClient(BGApp.app_key, BGApp.app_secret)
    client.set_access_token(BGApp.weico_token, time.time() + 90 * 24 *3600)
    for op in ops:
        logger.debug("unfollow %d state %d %s" % (op.opUid, op.state, op.actionTime))
        try:
            if FriendShip.CheckFollow(client, BGApp.dev_uid, op.opUid):
                logger.debug("unfollow %d" % op.opUid)
                FriendShip.Unfollow(client, op.opUid)
                op.state = 3#has been unfollowed
                op.save()
            else:
                logger.debug("%d not followed" % op.opUid)
        except:
            logger.debug(traceback.format_exc())

        time.sleep(60)
