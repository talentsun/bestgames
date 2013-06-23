#coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig
import traceback, time

from models import WeixinUser
from state_verify import *

default_sorry_wording = u'小每真是太笨了，没有理解您的意思[流泪]，求您一口盐汽水喷死小每吧'
def start_exchange(rule, info):
    print "start db", time.time()
    try:
        user = WeixinUser.objects.filter(uid=info.user)[0]
    except:
        traceback.print_exc()
        user = WeixinUser()
        user.src = info.sp
        user.uid = info.user
        user.integral = 0
        user.save()
    print "end db", time.time()

    if len(user.phone) == 0:
        return StateMachine.stateRoute[1].start(info)
    else:
        return BuildConfig(MessageBuilder.TYPE_GIFT_SHOP, None, user.id)

Router.get_instance().set({
    'name' : u'换礼品',
    'pattern': u'^(换礼品|礼品|换奖品|奖品|积分|积分商城)$',
    'handler':start_exchange
})
