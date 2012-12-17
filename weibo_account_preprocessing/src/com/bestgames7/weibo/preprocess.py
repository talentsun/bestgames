'''
Created on 2012-12-15

@author: bridge
'''

import re
import MySQLdb

def extract_access_token(info):
    if not info:
        return None

    access_token_match = re.search(r"access_token\";s:32:\"([\.\w]+)\"", info)
    if access_token_match:
        return access_token_match.group(1)
    return None

def extract_oauth_token(info):
    if not info:
        return None
    
    oauth_token_match = re.search('s:11:\"oauth_token\";s:32:\"([\.\w]+)\"', info);
    if oauth_token_match:
        return oauth_token_match.group(1)
    return None

def extract_oauth_token_secret(info):
    if not info:
        return None
    
    oauth_token_secret_match = re.search('s:18:\"oauth_token_secret\";s:32:\"([\.\w]+)\"', info);
    if oauth_token_secret_match:
        return oauth_token_secret_match.group(1)
    return None

