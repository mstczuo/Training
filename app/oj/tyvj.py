import requests, re, json

def get(username):
    url = 'http://tyvj.cn/Status/GetStatuses?page=0&username=%s' % username
    s = requests.get(url)
    r = json.loads(s.text)
    try:
        url = 'http://tyvj.cn/User/%d' % r[0]['UserID']
    except IndexError:
        return {'error': 'no such user or no submissions'}
    s = requests.get(url)
    r = re.findall(r'tyvj-status-info-left.+?(\d+)', s.text)
    try:
        return {'solved': r[2], 'attempts': r[1]}
    except IndexError:
        return {'error': 'user not found'}
