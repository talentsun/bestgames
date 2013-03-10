from api.sina.weibo import  APIClient

class SinaAuth:
    _APP_ID = '1165281516'
    _APP_SECRET = '4360e65b0e9de717dfe3a0c127bc96b3'
#    _REDIRECT_URL = 'http://www.bestgames7.com'
    _REDIRECT_URL = 'http://127.0.0.1/token/login'

    client = APIClient(_APP_ID,_APP_SECRET,_REDIRECT_URL,'code','api.weibo.com','2')

    def __init__(self):
        pass

    def getAuthorizeUrl(self):
        return self.client.get_authorize_url()

    def getToken(self,code):
        return self.client.request_access_token(code)
