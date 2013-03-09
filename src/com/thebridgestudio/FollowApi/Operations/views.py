# Create your views here.
# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json, logging
from django.views.decorators.csrf import csrf_exempt

import time
from AppValue import BGApp
from weibo import APIClient
from FriendShip import FriendShip


from Operations.models import Operation

def Follow(request):
    ops = Operation.objects.filter(state=0).order_by('addTime').reverse()[0:1]
    uids = []
    if len(ops) == 1:
        uid = ops[0].opUid
        client = APIClient(BGApp.app_key, BGApp.app_secret)
        client.set_access_token(BGApp.dev_token, time.time() + 90 * 24 *3600)
        if not FriendShip.CheckFollow(client, BGApp.dev_uid, uid):
            uids.append(uid)
        else:
            ops[0].state = 1
            ops[0].save()

    return HttpResponse(json.dumps(uids))

@csrf_exempt
def FinishFollow(request):
    logger = logging.getLogger('debug')
    logger.info("finish follow")
    if request.method == 'GET':
       jsonObj = request.GET
    else: 
       jsonObj = request.POST
    uidFinish = int(jsonObj['uid'])
    logger.debug("finish follow %d" % uidFinish)
    op = Operation.objects.get(opUid=uidFinish)
    op.state = 1
    op.save()
    return HttpResponse(json.dumps({'success': 'yes'}))

