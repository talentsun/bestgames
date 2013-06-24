#coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig

from models import WeixinUser, UserAnswer
from portal.models import Puzzle
import datetime

default_sorry_wording = u'小每真是太笨了，没有理解您的意思[流泪]，求您一口盐汽水喷死小每吧'

def answer(rule, info):
    try:
        user = WeixinUser.objects.get(uid = info.user)
    except:
        user = WeixinUser()
        user.src = info.sp
        user.uid = info.user
        user.integral = 0
        user.save()

    return BuildConfig(MessageBuilder.TYPE_ANSWER, None, user.id)
    
Router.get_instance().set({
    'name' : u'答题',
    'pattern': u'^(答题|趣味答题)$',
    'handler': answer
})
