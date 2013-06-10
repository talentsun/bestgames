#coding:utf8
from state_machine import StateMachine
from message_builder import MessageBuilder, BuildConfig
import random, traceback, time
from models import Gift, GiftItem, WeixinUser


StateMachine.register(1, VerifyPhone())

class Exchange(StateMachine):
    def __init__(self):
        StateMachine.__init__(self)
        pass

    def match(self, value, info):
        return True


    def start(self, info):
        value = {'state':1}
        StateMachine.store(info.user, value)
        text = u"我们为玩家准备的礼品有：\r\n"
        for item in Gift.objects.all():
            itemNum = GiftItem.objects.filter(state = 0, grade=item).count()
            text += "输入%d即可兑换%s，需要积分%d，剩余%d个\r\n" % (item.pk, item.integral, itemNum)
        return BuildConfig(MesssageBuilder.TYPE_RAW_TEXT, None, text)


    def deal(self, value, info):
        try:
            user = WeixinUser.objects.get(uid=info.user)
        except:
            user = WeixinUser()
            user.uid = info.user
            user.integral = 0
            user.phone = ''
            user.save()
        state = value['state']
        if state == 1:
            try:
                itemId = int(info.text)
                gift = Gift.objects.get(id=itemId)
                if user.integral > gift.integral:
                    giftItem = GiftItem.objects.get(grade = gift, state = 0)
                    text = u"恭喜你兑换到了%s，礼品码是%s" % (gift.name, giftItem.value)
                    giftItem.state = 1
                    giftItem.save()
                    StateMachine.end(info.user)
                else:
                    text = u"你的积分%d小于礼品所需的积分%d，继续努力吧少年" % (user.integral, gift.integral)
            except:
                text = u"你想要的礼品没有了，我们会快速补货的，请兑换其他的礼品或者明天再来吧"
            return BuildConfig(MesssageBuilder.TYPE_RAW_TEXT, None, text)
        else:
            StateMachine.end(info.user)
            raise Exception, "state bad %d" % state
