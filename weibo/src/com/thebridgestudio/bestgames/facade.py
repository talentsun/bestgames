'''
Created on 2013-1-8

@author: bridge
'''

from userinfo import update_users
from task import execute

def addfans():
    #direct follow inactive users
    execute('direct-follow_0-60', 250)

    #update relationship
    update_users()
    
    #refollow followers-wanting users
    #execute('refollow_100-150', 150)
    
addfans()
