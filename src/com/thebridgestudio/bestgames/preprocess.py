'''
Created on 2012-12-15

@author: bridge
'''

import re
import MySQLdb
import sys

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

def read_raw_data(offset, limit):
    try:
        raw_conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames')
    except Exception, e:
        print e
        sys.exit()
    
    raw_cursor = raw_conn.cursor()
    
    raw_cursor.execute('select fromuid,propdata from weibo_info limit %s,%s' % (offset, limit))
    staging_data = []
    for row in raw_cursor.fetchall():
        uid = row[0]
        raw_propdata = row[1]
        if ('access_token' in raw_propdata):
            access_token = extract_access_token(raw_propdata)
            if access_token:
                staging_data.append((uid,2,access_token,None))
            else:
                print 'drop ' + uid + ' because of parse_error'
        elif ('oauth_token' in raw_propdata and 'oauth_token_secret' in raw_propdata):
            oauth_token = extract_oauth_token(raw_propdata)
            oauth_token_secret = extract_oauth_token_secret(raw_propdata)
            if oauth_token and oauth_token_secret:
                staging_data.append((uid,1,oauth_token,oauth_token_secret))
            else:
                print 'drop ' + uid + ' because of parse_error'
        else:
            print 'drop ' + uid + ' because of no v1_v2'

    raw_cursor.close()
    raw_conn.close()
    
    return staging_data
    
def write_staging_data(access_tokens):
    try:
        staging_conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames')
    except Exception, e:
        print e
    
    try:
        staging_cursor = staging_conn.cursor()
        n = staging_cursor.executemany('insert into access_token(uid,version,data1,data2) values(%s,%s,%s,%s)', access_tokens)
        staging_conn.commit()
        if n:
            print 'insert %d access_tokens' % n
    except Exception,e:
        print e
    
    staging_cursor.close()
    staging_conn.close()

if __name__ == '__main__':
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='nameLR9969', db='bestgames')
    except Exception, e:
        print e
        sys.exit()
    
    cursor = conn.cursor()
    total = cursor.execute('select * from weibo_info')
    cursor.close()
    conn.close()
    
    print total
    
    #for i in range(588, total / 1000):
    #    print 'processing %d-%d' % (i * 1000, i * 1000 + 1000)
    #    write_staging_data(read_raw_data(i * 1000, 1000))
    for i in range(588000, 589000):
        print i
        write_staging_data(read_raw_data(i, 1))

    
    
