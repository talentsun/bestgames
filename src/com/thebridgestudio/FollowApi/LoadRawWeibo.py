#!/usr/bin/python
import re

def GetAccessToken(info):
    accessTokenMatch = re.search(r'access_token";s:32:"([\w]+)"', info)
    if accessTokenMatch:
        return accessTokenMatch.group(1)
    return None


def GetOauthToken(info):
    oauthTokenMatch = re.search(r'oauth_token";s:32:"([\w]+)"', info)
    if oauthTokenMatch:
        return oauthTokenMatch.group(1)
    return None


def GetOauthTokenSecret(info):
    oauthTokenSecretMatch = re.search(r'oauth_token_secret";s:32:"([\w]+)"', info)
    if oauthTokenSecretMatch:
        return oauthTokenSecretMatch.group(1)
    return None


if __name__ == '__main__':
    print GetAccessToken('access_token";s:32:"abcded"')
    print GetOauthToken('oauth_token";s:32:"35d73a69da3556eede596930a767223d";s:18:')
    print GetOauthTokenSecret('6930a767223d";s:18:"oauth_token_secret";s:32:"7ff804a8c8c0fbe24b22833649a87e46";s:7:"use')
    
