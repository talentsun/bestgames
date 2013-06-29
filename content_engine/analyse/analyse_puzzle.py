#!/usr/local/bin/python2.7
#coding:utf8

import sys, traceback
sys.path.append("..")

from django.core.management import setup_environ
from content_engine import settings
setup_environ(settings)

import datetime
from weixin.models import UserAnswer, WeixinUser
from sets import Set
from analyse.models import *

from django.db import connection

if __name__ == '__main__':
    if len(sys.argv) == 2:
        delta_day = int(sys.argv[1])
    else:
        delta_day = 0
    cur = datetime.datetime.now() - datetime.timedelta(days = delta_day)
    cur_date = datetime.date.today() - datetime.timedelta(days = delta_day)
    start = cur - datetime.timedelta(hours=cur.hour, minutes=cur.minute, seconds=cur.second)
    end = start + datetime.timedelta(days = 1)

    cursor = connection.cursor()
    query = "select count(distinct userId_id) from user_answer where answerTime < '%s'" % end.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(query)
    all_number = cursor.fetchone()[0]
    print all_number

    users = WeixinUser.objects.filter(phone__gt = '')
    print len(users)

    try:
        AllPuzzleUserByDay.objects.filter(day=cur_date).delete()
    except:
        traceback.print_exc()
        pass
    obj = AllPuzzleUserByDay()
    obj.day = cur_date
    obj.answer_num = all_number
    obj.phone_num = len(users)
    obj.save()



    user_answers = UserAnswer.objects.filter(answerTime__range=(start, end))
    old_num = 0
    new_num = 0
    all_users = Set()
    for u in user_answers:
        if u.userId in all_users:
            continue
        all_users.add(u.userId)
        t_uas = UserAnswer.objects.filter(userId = u.userId, answerTime__lt=u.answerTime)
        if len(t_uas) > 0:
            old_num += 1
        else:
            new_num += 1

    print old_num, new_num
    try:
        DeltaPuzzleUserByDay.objects.filter(day=cur_date).delete()
    except:
        pass
    obj = DeltaPuzzleUserByDay()
    obj.day = cur_date
    obj.new_user = new_num
    obj.old_user= old_num
    obj.save()


    puzzle_num = {}
    for u in user_answers:
        if u.questionId not in puzzle_num:
            puzzle_num[u.questionId] = [0, 0] #oldNum, newNum

        t_uas = UserAnswer.objects.filter(userId = u.userId, answerTime__lt=u.answerTime)
        if len(t_uas) > 0:
            puzzle_num[u.questionId][0] += 1
        else:
            puzzle_num[u.questionId][1] += 1

    print puzzle_num
    for k, v in puzzle_num.items():
        try:
            obj = PuzzleUserByPuzzle.objects.get(puzzle = k)
        except:
            obj = PuzzleUserByPuzzle()
            obj.new_user = 0
            obj.old_user = 0
            obj.puzzle = k
        obj.new_user += v[1]
        obj.old_user += v[0]
        obj.save()



