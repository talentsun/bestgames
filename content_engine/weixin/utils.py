import requests

TINYURL_API = 'http://tinyurl.com/api-create.php?url='

def shorten_url(url):
	global TINYURL_API

	req = requests.get(TINYURL_API + url)
	if req.status_code == 200:
		return req.text
	else:
		return None 

