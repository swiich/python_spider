# coding=utf-8
"""
page request
"""

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
    """
    request specified page to get html
    :param url:requestPage
    :return:html
    """

    req = request.Request(url, headers=headers)
    content = urlopen(req).read()
    return content



