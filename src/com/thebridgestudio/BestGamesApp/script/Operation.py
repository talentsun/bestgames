#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

import datetime

class Operation:
    FollowType = 1
    AtType = 2

    NotFinished = 0
    Finished = 1
    def __init__(self):
        self.uid = 0
        #type = 1, follow them
        #type = 2, at them
        self.type = 0
        self.ts = datetime.datetime.now()
        self.state = self.NotFinished
    @classmethod
    def FetchOp(cls, uid, type):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select uid, op_type, op_date, op_state from operation where uid = %d and op_type=%d" % (uid, type))
        row = cursor.fetchone()
        op = None
        if row != None: 
            op = Operation()
            op.uid = row[0]
            op.type = row[1]
            op.ts = row[2]
            op.state = row[3]

        cursor.close()
        conn.close()

        return op

    @classmethod
    def FetchOps(cls, uid):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("select uid, op_type, op_date, op_state from operation where uid = %d " % uid)
        ops = []
        for row in cursor.fetchall():
            op = Operation()
            op.uid = row[0]
            op.type = row[1]
            op.ts = row[2]
            op.state = row[3]
            ops.append(op)

        cursor.close()
        conn.close()

        return ops

    def Save(self):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
        cursor = conn.cursor()
        cursor.execute("delete from operation where uid = %d and op_type = %d" % (self.uid, self.type))
        cursor.execute("insert into operation values (%d, %d, '%s', %d)" % (self.uid, self.type, self.ts.strftime('%Y-%m-%d %H:%M:%S'), self.state))
        cursor.close()
        conn.close()

    @classmethod
    def FetchSomeDayOps(cls, type, day):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames', port=3306, charset='utf8')
        cursor = conn.cursor()
        someDay = datetime.date.today() - datetime.timedelta(days = day)
        someDayNextDay = datetime.date.today() - datetime.timedelta(days = (day - 1))
        cursor.execute("select uid, op_type, op_date from operation where op_type = %d and op_date > '%s' and op_date < '%s'" % (type, someDay.strftime('%Y-%m-%d %H:%M:%S'), someDayNextDay.strftime('%Y-%m-%d %H:%M:%S')))
        ops = []
        for row in cursor.fetchall():
            op = Operation()
            op.uid = row[0]
            op.type = row[1]
            op.ts = row[2]
            ops.append(op)

        cursor.close()
        conn.close()

        return ops
