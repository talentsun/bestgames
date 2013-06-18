#coding:utf8
from state_machine import StateMachine
from message_builder import MessageBuilder, BuildConfig
import random, traceback, time
from models import WeixinUser
from utils import send_sms

import logging
logger = logging.getLogger('weixin')



class VerifyPhone(StateMachine):
    def __init__(self):
        StateMachine.__init__(self)
        self.stateId = 1
        pass

    def match(self, value, info):
        return True

    def start(self, info):
        value = {'state': 1, 'sendNum':0}
        self.store(info.user, value)
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u"使用积分商城进行积分换礼品需要进行身份验证。请输入您的手机号，小每会给您的手机号发送一个验证码，每个手机号只能验证一次")

    def checkPhoneNum(self, numStr):
        try:
            phoneNum = int(numStr)
            if len(numStr) == 11 and numStr[0] == '1':
                return True
        except:
            traceback.print_exc()
            pass
        return False

    def checkState1(self, value, info):
        if value['sendNum'] > 5:
            text = u"今天已经给你发送太多的短信了，明天再来吧"
            StateMachine.end(info.user)
        elif self.checkPhoneNum(info.text):
            try:
                user = WeixinUser.objects.get(phone=info.text)
                text = "这个手机号已经被使用了，请使用其他号码"
            except:
                user = None
            if user == None:
                verifyCode = str(random.randint(100000, 1000000))
                ret = send_sms(info.text, u"验证码是%s，15分钟内有效" % verifyCode)
                logger.debug("send sms return %s" % ret)
                value = {'state':2, 'phone':info.text, 'verifyCode':verifyCode, "sendTime":time.time(), 'sendNum':value['sendNum'] + 1}
                self.store(info.user, value)
                text = u'我们已经将验证码发送到%s，请将收到的验证码发送给我们就完成验证，如果2分钟内没有收到短信就请输入“重新发送”，我们将重新给你发送新的验证码，如果想换手机号，就请输入“换手机号”' % info.text
        else:
            text = u"请输入正确的手机号"
        return text

    def checkState2(self, value, info):
        if info.text == str(value['verifyCode']):
            StateMachine.end(info.user)
            user = WeixinUser.objects.filter(uid=info.user)[0]
            user.phone = value['phone']
            user.save()
            text = u'恭喜您，已经完成了验证，赶快回复“礼品”去积分商城选择礼品吧'
        elif info.text == u"重新发送":
            if time.time() < value['sendTime'] + 2 * 60:
                text = u"刚给您发送了短信，请耐心等候"
            elif value['sendNum'] > 5:
                text = u"今天已经给您发送了太多短信了，请明天再来吧"
                self.timeout = 12 * 3600
                self.store(info.user, value)
            else:
                verifyCode = random.randint(100000, 1000000)
                value['verifyCode'] = verifyCode
                ret = send_sms(info.text, u"验证码是%d，15分钟内有效" % verifyCode)
                logger.debug("send sms return %s" % ret)
                value['sendTime'] = time.time()
                value['sendNum'] += 1
                self.store(info.user, value)
                text = u"已经给您发送了一条短信，请查收"
        elif info.text == u"换手机号" or info.text == u"换手机":
            if time.time() < value['sendTime'] + 2 * 60:
                text = u'刚给你发送了短信，请2分钟后没收到，再“换手机号”'
            elif value['sendNum'] > 5:
                text = u'今天已经给你发送了太多短信了，请明天再来吧'
                self.timeout = 12 * 3600
                self.store(info.user, value)
            else:
                value['state'] = 1
                self.store(info.user, value)
                text = u"请输入新的手机号"
        else:
            text = u"您输入的验证码有误，请再看一下"
        return text

    def deal(self, value, info):
        state = value['state']
        if state == 1:
            text = self.checkState1(value, info)
        elif state == 2:
            text = self.checkState2(value, info)
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, text)

StateMachine.register(1, VerifyPhone())
