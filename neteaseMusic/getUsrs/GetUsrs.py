# coding=utf-8
"""get fans or followings"""

import json
import requests

from tool import PageRequest
from tool import AES_encrypt


class Argserror(BaseException):
    def __init__(self, arg):
        self.args = arg


def analyseUsrs(uid, type, offset=0):
    '''
    analyse fans or following list depends on 'type' arg
    '''

    try:
        if type == 'follows':
            PageRequest.headers['Referer'] = 'http://music.163.com/user/follows?id=' + str(uid)
            url = 'http://music.163.com/weapi/user/getfollows/%s?csrf_token=' % uid
            post_data = AES_encrypt.crypt_api(type, uid, offset)
            txt = 'follow'

        elif type == 'fans':
            PageRequest.headers['Referer'] = 'http://music.163.com/user/fans?id=' + str(uid)
            url = 'http://music.163.com/weapi/user/getfolloweds?csrf_token='
            post_data = AES_encrypt.crypt_api(type, uid, offset)
            txt = 'followeds'

        else:
            raise Argserror('wrong type of "type"，only fans or follows')

    except Argserror as a:
        print(''.join(a.args))
        users = {}
        return users

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')
    # analyse json
    json_text = json.loads(content)

    users = {}
    # users = json_text['follow']      # detail information of ..
    for i in json_text[txt]:
        # ghost users shielded
        if i['followeds'] == 0 and i['follows'] <= 3:
            pass
        else:
            users[i['userId']] = [i['nickname'], i['follows'], i['followeds']]

    return users
