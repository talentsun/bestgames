#coding: utf8
from router import Router
from django.db import transaction
from message_builder import MessageBuilder, BuildConfig
import traceback

from models import WeixinUser, RewardItem

default_sorry_wording = u'小每真是太笨了，没有理解您的意思[流泪]，求您一口盐汽水喷死小每吧'
rewardA = ('itune gift card', 40)
rewardB = ('android gift card', 40)
@transaction.commit_manually
def exchange(rule, info):
    global rewardA, rewardB
    try:
        user = WeixinUser.objects.get(uid=info.user)
    except:
        user = WeixinUser()
        user.uid = info.user
        user.integral = 0
        user.save()


    if info.text[-1] == 'A' or info.text[-1] == 'a':
        if user.integral >= rewardA[1]:
            try:
                item = RewardItem.objects.get(grade=1, state=0)
                user.integral -= rewardA[1]
                item.state = 1
                item.save()
                user.save()
                text = u"恭喜你得到了我们的%s %s, 你的剩余积分是%d, 欢迎继续参加我们的活动" % (rewardA[0], item.value, user.integral)

            except:
                traceback.print_exc()
                text = u"对不起，您想要的礼品暂时没有了，我们很快就会补货，明天再来看看吧"
        else:
            text = u"非常抱歉，我们的%s需要%d积分，你的积分只有%d，继续参加我们的活动赢取更多的积分把" % (rewardA[0], rewardA[1], user.integral)
    elif info.text[-1] == 'B' or info.text[-1] == 'b':
        if user.integral >= rewardB[1]:
            try:
                item = RewardItem.objects.get(grade=2, state=0)
                user.integral -= rewardB[1]
                item.state = 1
                item.save()
                user.save()
                text = u"恭喜你得到了我们的%s %s, 你的剩余积分是%d, 欢迎继续参加我们的活动" % (rewardB[0], item.value, user.integral)
            except:
                text = u"对不起，您想要的礼品暂时没有了，我们很快就会补货，明天再来看看吧"
        else:
            text = u"非常抱歉，我们的%s需要%d积分，你的积分只有%d，继续参加我们的活动赢取更多的积分吧" % (rewardB[0], rewardB[1], user.integral)
    else:
        text = default_sorry_wording

    transaction.commit()
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, text)


        
def start_exchange(rule, info):
    global rewardA, rewardB
    try:
        user = WeixinUser.objects.get(uid=info.user)
    except:
        user = WeixinUser()
        user.uid = info.user
        user.integral = 0
        user.save()

    text = u"我们的礼品有两种，一种是%s需要%d个积分，一种是%s需要%d个积分\n" % (rewardA[0], rewardA[1], rewardB[0], rewardB[1])
    text += u'回复"换#A"将换取%s，回复"换#B"将换取%s' % (rewardA[0], rewardB[0])
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, text)

Router.get_instance().set({
    'name' : u'换礼品',
    'pattern': u'^换礼品$',
    'handler':start_exchange
})
Router.get_instance().set({
    'name' : u'换具体奖',
    'pattern': u'^((换#(A|a))|(换#(B|b)))$',
    'handler':exchange
})
