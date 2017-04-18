import requests, re

def get(username):
    url = 'http://acm.hdu.edu.cn/userstatus.php?user=%s' % username
    s = requests.get(url)
    r = re.findall(r'Problems .+?(\d+)', s.text)
    try:
        return {'solved': r[1], 'attempts': r[0]}
    except IndexError:
        return {'error': 'user not found'}
