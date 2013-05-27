# Create your views here.
# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json, logging
from django.views.decorators.csrf import csrf_exempt

import time
from datetime import datetime, timedelta
from AppValue import BGApp
from weibo import APIClient
from FriendShip import FriendShip


from Operations.models import Operation

def Follow(request):
    ops = Operation.objects.filter(state=1).order_by('addTime').reverse()[0:1]
    uids = []
    if len(ops) == 1:
        if ops[0].addTime < datetime.now() - timedelta(days = 1):
            return HttpResponse(json.dumps(ops[0]))

        uid = ops[0].opUid
        client = APIClient(BGApp.app_key, BGApp.app_secret)
        client.set_access_token(BGApp.dev_token, time.time() + 90 * 24 *3600)
        if not FriendShip.CheckFollow(client, uid, BGApp.dev_uid):
            uids.append(uid)
            ops[0].state = 2
            ops[0].save()

    return HttpResponse(json.dumps(uids))

@csrf_exempt
def FinishFollow(request):
    logger = logging.getLogger("debug")
    logger.info("finish follow")
    if request.method == 'GET':
       jsonObj = request.GET
    else: 
       jsonObj = request.POST
    uidFinish = int(jsonObj['uid'])
    op = Operation.objects.get(opUid=uidFinish)
    op.state = 2
    op.save()
    return HttpResponse(json.dumps({'success': 'yes'}))

