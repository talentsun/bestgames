#coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig

from models import WeixinUser, UserAnswer
from portal.models import Puzzle

default_sorry_wording = u'小每真是太笨了，没有理解您的意思[流泪]，求您一口盐汽水喷死小每吧'



def answer(rule, info):
    puzzleId = int(info.text[:-2])
    option = info.text[-1]
    if option == 'A' or option == 'a':
        option = 0
    elif option == 'B' or option == 'b':
        option = 1
    elif option == 'C' or option == 'c':
        option = 2
    elif option == 'D' or option == 'd':
        option = 3
    else:
        text = u'非常抱歉，无法识别你的答案'
        return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, text)

    try:
        user = WeixinUser.objects.get(uid = info.user)
    except:
        user = WeixinUser()
        user.uid = info.user
        user.integral = 0
        user.save()
    try:
        puzzle = Puzzle.objects.get(pk = puzzleId)
    except:
        puzzle = None
    if puzzle == None:
        text = u"非常抱歉没找到第%d题" % puzzleId
    else:
        try:
            userAnswer = UserAnswer.objects.get(questionId = puzzleId, userId = user.pk)
        except:
            userAnswer = None
        if userAnswer:
            text = u'第%d题你已经答过了，再回答其他的题吧' % puzzleId
        else:
            userAnswer = UserAnswer()
            userAnswer.questionId = puzzle
            userAnswer.userId = user
            userAnswer.userOption = option
            if option == puzzle.right:
                user.integral += 5
                text = u'恭喜你，你答对了，太牛了，你现在的积分是%d, 回复"换礼品"换取礼品吧' % user.integral
                user.save()
            else:
                text = u"非常抱歉，你没有答对，继续努力吧少年！"
            userAnswer.save()
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, text)
    
Router.get_instance().set({
    'name' : u'答题',
    'pattern': r'^[1-9]\d*#[a-dA-D]$',
    'handler':answer
})
