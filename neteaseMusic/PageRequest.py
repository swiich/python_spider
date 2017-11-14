'''
网页request
'''

from urllib import request
from urllib.request import urlopen

# header
headers = {
    'Cookie': 'appver=1.5.0.75771;',
    'Host': 'music.163.com',
    'Origin': 'http://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
}


def GetHtml(url):
    '''
    向指定网页发起请求获取html
    :param url:request网页
    :return:html
    '''

    req = request.Request(url, headers=headers)
    content = urlopen(req).read()
    return content



