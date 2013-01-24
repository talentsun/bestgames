'''
Created on 2013-1-24

@author: bridge
'''
from task import execute

def addfans():
    #refollow followers-wanting users
    execute('refollow_100-150', 150)
    
addfans()