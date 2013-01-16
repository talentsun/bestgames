'''
Created on 2013-1-8

@author: bridge
'''

from userinfo import update_users
from task import execute

def addfans():
    #update relationship
    update_users()
    
    #direct follow inactive users
    execute('direct-follow_0-60', 90)
    
    #refollow followers-wanting users
    execute('refollow_100-150', 150)
    
addfans()