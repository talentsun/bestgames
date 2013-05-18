# coding: utf8
from router import Router
from service import draw_pb2
from message_builder import MessageBuilder, BuildConfig
import socket

default_sorry_wording = u'小每真是太笨了，没有理解您的意思[流泪]，求您一口盐汽水喷死小每吧'
def __draw(uid):
    q = draw_pb2.DrawQuery()
    q.uid = uid
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(q.SerializeToString(), ("127.0.0.1", 8040))
    r = s.recv(4196)
    resp = draw_pb2.DrawResp()
    resp.ParseFromString(r)
    return resp

def draw(rule, info):
    resp = __draw(info.user)
    text = u'小每真是太笨了，没有理解您的意思[流泪]，求您一口盐汽水喷死小每吧'
    if resp.result == 0:
        #错误处理，如果奖品没了，就告诉用户没中奖
        if resp.reward > 0 and len(resp.value) == 0:
            resp.reward = 0
        if resp.reward == -1:
            text = u'亲，您今天的抽奖机会已经用完了，感谢您的参与，明天再来吧！'
        elif resp.reward == 0:
            if resp.leftTimes > 0:
                text = u'亲，非常抱歉您没有中奖，不过您今天还有抽奖机会%d次，再接再厉哟' % resp.leftTimes
            else:
                text = u'亲，非常抱歉您没有中奖，您今天的抽奖机会也用完了，明天再来吧'
        elif resp.reward == 1:
            text = u'亲，您的运气实在是太棒了，您得到的冒险王为小每玩家准备的豪华大礼包，激活码是%s' % resp.value
            if resp.leftTimes > 0:
                text += u'，你还有%d次抽奖机会，接着爆发吧' % resp.leftTimes
            else:
                text += u'，赶紧去体验游戏吧。'
        elif resp.reward == 2:
            text = u'亲，您的运气实在是太棒了，您得到的冒险王为小每玩家准备的梦幻大礼包，激活码是%s' % resp.value
            if resp.leftTimes > 0:
                text += u'，你还有%d次抽奖机会，接着爆发吧' % resp.leftTimes
            else:
                text += u'，赶紧去体验游戏吧。'

    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, text)
            

    

Router.get_instance().set({
    'name' : u'抽奖',
    'pattern': u'冒险王',
    'handler':draw
})

