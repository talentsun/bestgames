#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
from follow import Bestgames
from follow import follow_v1
from follow import follow_v2
from follow import is_followed_by_v1
from follow import is_follow_v2
from follow import is_followed_by_v2
import time
from db import *

class TaskType:
    FOLLOW_THEM = 'follow_them'
    FOLLOW_ME = 'follow_me'
    
class TaskState:
    NEW = 0
    PROCESSED = 1

def execute(task, limit):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='bestgames_weibo', port=3306, charset='utf8')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        staging_cursor.execute('select users.uid, users.token_version, users.token_data1, users.token_data2, tasks.type from tasks inner join users on tasks.uid=users.uid where tasks.name=%s and state=0 limit %s', (task, limit))
        
        index = 1
        for row in staging_cursor.fetchall():
            uid = row[0]
            version = row[1]
            taskType = row[4]
            
            print '%d: process %s' % (index, uid)
            if taskType == TaskType.FOLLOW_ME:
                if version == 1:
                    if is_followed_by_v2(Bestgames.ACCESS_TOKENS[index%8], Bestgames.UID, uid):
                        print '%s already follow me' % (uid)
                        db_follow_me(uid)
                        db_task_processed(task, uid)
                    else:
                        follow_v1(row[2], row[3], Bestgames.UID)
                        if is_followed_by_v2(Bestgames.ACCESS_TOKENS[index%8], Bestgames.UID, uid):
                            print '%s follow me' % (uid)
                            db_follow_me(uid)
                            db_task_processed(task, uid)
                        else:
                            print 'follow me failed'
                    time.sleep(2 * 60)
                elif version == 2:
                    if is_followed_by_v2(Bestgames.ACCESS_TOKENS[index%8], Bestgames.UID, uid):
                        print '%s already follow me' % (uid)
                        db_follow_me(uid)
                        db_task_processed(task, uid)
                    else:
                        follow_v2(row[2], Bestgames.UID)
                        if is_followed_by_v2(Bestgames.ACCESS_TOKENS[index%8], Bestgames.UID, uid):
                            print '%s follow me' % (uid)
                            db_follow_me(uid)
                            db_task_processed(task, uid)
                        else:
                            print 'follow me failed'
                        time.sleep(2 * 60)
            elif taskType == TaskType.FOLLOW_THEM:
                if is_follow_v2(Bestgames.ACCESS_TOKENS[index%8], Bestgames.UID, uid):
                    print '%s already follow them' % (uid)
                    db_follow_them(uid)
                    db_task_processed(task, uid)
                else:
                    follow_v2(Bestgames.ACCESS_TOKENS[index%8], uid)
                    if is_follow_v2(Bestgames.ACCESS_TOKENS[index%8], Bestgames.UID, uid):
                        print 'follow %s' % (uid)
                        db_follow_them(uid)
                        db_task_processed(task, uid)
                    else:
                        print 'follow %s failed' % (uid)
                    time.sleep(15)
            index = index+1
    except Exception,e:
        print e
        
    staging_cursor.close()
    staging_conn.close()
    
if __name__ == '__main__':
    execute('direct-follow_0-60', 40)
    execute('refollow_100-150', 150)