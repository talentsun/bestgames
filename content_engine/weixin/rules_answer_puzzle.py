#coding: utf8
from router import Router
from message_builder import MessageBuilder, BuildConfig

from models import WeixinUser, UserAnswer
from portal.models import Puzzle
import datetime

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
        user.src = info.sp
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
        #one user only can answer two question
        today = datetime.date.today()
        userAnswers = UserAnswer.objects.filter(userId = user.pk, answerTime__gte=datetime.datetime(today.year, today.month, today.day))
        if len(userAnswers) >= 2:
            text = u'您今天已经答了两道了，明天再来吧'
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
                    text = u'恭喜您，答对了，您当前的积分：%d\n回复"礼品"进入积分商城兑换礼品' % user.integral
                    user.save()
                else:
                    text = u'这不科学，答错了，您当前的积分：%d\n回复"礼品"进入积分商城兑换礼品' % user.integral
                userAnswer.save()
    return BuildConfig(MessageBuilder.TYPE_RAW_TEXT, None, text)
    
Router.get_instance().set({
    'name' : u'答题',
    'pattern': r'^[1-9]\d*#[a-dA-D]$',
    'handler':answer
})
