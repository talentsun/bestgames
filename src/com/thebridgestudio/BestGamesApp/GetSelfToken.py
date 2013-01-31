#!/usr/bin/env python

from weibo import APIClient
import sys
from AppValue import BGApp


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s code" % sys.argv[0]
        sys.exit()
    client = APIClient(BGApp.app_key, BGApp.app_secret)
    code = sys.argv[1]
    info = client.request_access_token(code, BGApp.redirect_uri)
    print info
    print info['access_token'], info['expires_in'], info['uid']
    
    
