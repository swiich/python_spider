import AES_encrypt
import PageRequest
import requests
import json


def GetUserFollows(uid):
    '''
    获取用户关注列表
    :return: userFollows {}
    '''
    # 请求头与请求网址
    PageRequest.headers['Referer'] = 'http://music.163.com/user/follows?id=' + str(uid)
    url = 'http://music.163.com/weapi/user/getfollows/%s?csrf_token=' % uid

    post_data = AES_encrypt.crypt_api_userFollows(uid)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')
    # 解析json
    json_text = json.loads(content)

    userFollows = {}
    # userFollows = json_text['follow']      # 被关注者的所有信息
    for i in json_text['follow']:
        userFollows[i['userId']] = i['nickname']

    return userFollows


if __name__ == '__main__':
    uid = 5832286
    # 关注数量超过300只显示300，但是limit参数设置为1000，why
    '''58066-1127   6790397-404'''
    follows = GetUserFollows(uid)

    print(follows)
    print('amount of following :', len(follows))
