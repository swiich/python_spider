# coding=utf-8


from tool import AES_encrypt, PageRequest
import json
import requests


def getRank(uid):
    # 获取用户听歌排行

    PageRequest.headers['Referer'] = 'http://music.163.com/user/home?id=' + str(uid)
    url = 'http://music.163.com/weapi/v1/play/record?csrf_token='

    post_data = AES_encrypt.crypt_api('ranks', uid)

    rank = []

    try:
        content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')
        json_text = json.loads(content)

        rank = json_text['allData']

    except Exception:
        print('无权限访问，用户已关闭所有人可见')

    finally:
        return rank
