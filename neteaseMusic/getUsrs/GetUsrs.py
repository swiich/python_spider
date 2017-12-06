# coding=utf-8
'''获取用户关注列表'''

import json
import requests

from tool import PageRequest
from tool import AES_encrypt


class Argserror(BaseException):
    def __init__(self, arg):
        self.args = arg


def analyseUsrs(uid, type, offset=0):
    '''
    根据type解析用户关注或粉丝列表
    '''

    try:
        if type == 'follows':
            # 请求头与请求网址
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
            raise Argserror('type参数错误，只能为fans或follows')

    except Argserror as a:
        print(''.join(a.args))
        users = {}
        return users

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')
    # 解析json
    json_text = json.loads(content)

    users = {}
    # users = json_text['follow']      # 被关注者的所有信息
    for i in json_text[txt]:
        users[i['userId']] = i['nickname']

    return users
