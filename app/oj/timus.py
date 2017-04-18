import requests, re

def get(username):
    url = 'http://acm.timus.ru/search.aspx?Str=%s' % username
    s = requests.get(url)
    r = re.findall(r'author.aspx\?id=(\d+)', s.text)
    if len(r) == 0:
        return {'error': 'user not found'}
    url = 'http://acm.timus.ru/author.aspx?id=%s' % r[0]
    s = requests.get(url)
    r = re.findall(r'author_name"\>(.+?)\<', s.text)
    if len(r) == 0:
        return {'error': 'user not found'}
    r = re.findall(r'Problems solved.+?author.+?(\d+) out of (\d+)', s.text)
    try:
        return {'solved': r[0][0], 'attempts': r[0][1]}
    except IndexError:
        return {'error': 'unknown error'}

