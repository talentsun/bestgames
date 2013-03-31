from weibo import  APIClient
import MySQLdb as mdb
import time
import datetime
import threading
import os

_APP_ID = '1483181040'
_APP_SECRET = '6f503ed72723bacf9f4a0f4902b62c24'

client = APIClient(_APP_ID, _APP_SECRET, 'http://account.wandoujia.com/v1/user/?do=platform_sina')
client.set_access_token('2.00wsGZQCqIR4cB8ac1f7170aj5evFC', '7809909')

try:
   client.statuses.upload.post(status='123' ,
                                  pic=open('/Users/huwei/1.png'))
   result = '1'
except:
   result = '2'

print result
