#coding:utf8
from state_machine import StateMachine
from message_builder import MessageBuilder, BuildConfig
import random, traceback, time


StateMachine.register(1, VerifyPhone())

class VerifyPhone(StateMachine):
    def __init__(self):
        StateMachine.__init__(self)
        pass

    def match(self, value, info):
        return True

    def start(self, info):
        value = {'state': 1, 'sendNum':0}
        StateMachine.store(info.user, value)
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, u"为了保证礼品能平等的发放到游戏玩家手中，我们需要用户进行真实性确认，请输入你的手机号，我们会给这个手机号发送一个验证码，每个手机号只能用一次")

    def checkPhoneNum(self, numStr):
        try:
            phoneNum = int(numStr)
            if numStr.len == 11 and numStr[0] == '1':
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
                text = "这个电话号码已经被使用了，请使用其他号码"
            except:
                user = None
            if user == None:
                #verifyCode = random.randint(100000, 1000000)
                verifyCode = '123321'
                value = {'state':2, 'phone':info.text, 'verifyCode':verifyCode, "sendTime":time.time(), 'sendNum':1}
                StateMachine.store(info.user, value)
                text = u"我们已经将验证码发送到%s，请将收到的验证码发送给我们就完成验证，如果2分钟内没有收到短信就请输入'重新发送'，我们将重新给你发送新的验证码，如果想换手机号，就请输入'换手机号'" % info.text)
        else:
            text = u"请输入正确的手机号"
        return text

    def checkState2(self, value, info):
        if info.text == value['verifyCode']:
            StateMachine.end(info.user)
            user = WeixinUser.objects.get(uid=info.user)
            user.phone = value['phone']
            user.save()
            text = u"恭喜您，已经完成了验证，赶快去选择礼品吧"
        elif info.text == u"重新发送":
            if time.time() < value['sendTime'] + 2 * 60:
                text = u"刚给你发送了短信，请耐心等候"
            elif value['sendNum'] > 5:
                text = u"今天已经给你发送了太多短信了，请明天再来吧"
                self.timeout = 12 * 3600
                StateMachine.store(info.user, value)
            else:
                verifyCode = "123456"
                value = (2, value[1], verifyCode, time.time)
                value['sendNum'] += 1
                StateMachine.store(info.user, value)
                text = u"亲，又给你发送了一条短信，请查收"
        elif info.text == u"换手机号":
            if time.time() < value['sendTime'] + 2 * 60:
                text = u"刚给你发送了短信，请2分钟后没收到，再换手机号"
            elif value['sendNum'] > 5:
                text = u"今天已经给你发送了太多短信了，请明天再来吧"
                self.timeout = 12 * 3600
                StateMachine.store(info.user, value)
            else:
                value['state'] = 1
                StateMachine.store(info.user, value)
        else:
            text = u"您输入的验证码有误，请再看一下"
        return text

    def deal(self, value, info):
        state = value['state']
        if state == 1:
            text = self.checkState1(value, info)
        elif state == 2:
            text = self.checkState2(value, info)
        return BuildConfig(MesssageBuilder.TYPE_RAW_TEXT, None, text)
