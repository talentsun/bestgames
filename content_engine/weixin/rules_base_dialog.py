# coding: utf8
from router import Router
from service import search_pb2
from message_builder import MessageBuilder, BuildConfig
import socket
from weixin.models import BaseDialog

default_sorry_wording = u'小每真是太笨了，没有理解您的意思[流泪]，求您一口盐汽水喷死小每吧'
def __search_dialogs(query):
    q = search_pb2.Query()
    q.query = query
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(q.SerializeToString(), ("127.0.0.1", 8038))
    r = s.recv(4196)
    resp = search_pb2.ResponseDialog()
    resp.ParseFromString(r)
    return resp
def match_dialogs(rule, info):
    resp = __search_dialogs(info.text)
    if resp.result == 0:
        for d in resp.dialogs:
            if d.rel > 0.8:
                return True
    return False

def _search_dialogs(rule, info):
    resp = __search_dialogs(info.text)
    if resp.result == 0:
        for d in resp.dialogs:
            if d.rel > 0.8:
                b = BaseDialog.objects.get(pk = d.qId)
                if b:
                    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, b.answer)
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, default_sorry_wording)
                

Router.get_instance().set({
    'name' : u'查找对话',
    'pattern': match_dialogs,
    'handler':_search_dialogs
})

