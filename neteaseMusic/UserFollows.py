# coding=utf-8
'''获取用户关注列表'''

import AES_encrypt
import PageRequest
import requests
import json
import time


def AnalyseUserFollows(uid, offset=0):
    '''
    解析json用户关注列表
    '''
    # 请求头与请求网址
    PageRequest.headers['Referer'] = 'http://music.163.com/user/follows?id=' + str(uid)
    url = 'http://music.163.com/weapi/user/getfollows/%s?csrf_token=' % uid

    post_data = AES_encrypt.crypt_api_userFollows(uid, offset)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')
    # 解析json
    json_text = json.loads(content)

    userFollows = {}
    # userFollows = json_text['follow']      # 被关注者的所有信息
    for i in json_text['follow']:
        userFollows[i['userId']] = i['nickname']

    return userFollows


def AnalyseUserFans(uid, offset=0):
    '''
    解析json用户粉丝列表(与获取关注列表基本一模一样，也许有类似继承可以简化代码，有空再优化)
    '''
    PageRequest.headers['Referer'] = 'http://music.163.com/user/fans?id=' + str(uid)
    url = 'http://music.163.com/weapi/user/getfolloweds?csrf_token='
    post_data = AES_encrypt.crypt_api_userFans(uid, offset)
    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')
    json_text = json.loads(content)
    userFollows = {}
    for i in json_text['followeds']:
        userFollows[i['userId']] = i['nickname']
    return userFollows


def GetUserFollows(uid):
    '''
    获取用户关注列表
    '''
    follows = {}
    offset = 0

    # 判断用户关注列表是否爬取完
    flag = True
    while flag:
        temp = AnalyseUserFollows(uid, offset)
        follows.update(temp)

        if temp and len(temp) == 300:
            offset += 300
        else:
            flag = False

    return follows


# def GetUserFans(uid):
#     '''
#     获取用户关注列表
#     '''
#     followeds = {}
#     offset = 0
#
#     # 判断用户关注列表是否爬取完
#     flag = True
#     while flag:
#         temp = AnalyseUserFans(uid, offset)
#         followeds.update(temp)
#
#         if temp and len(temp) == 100:
#             offset += 100
#         else:
#             flag = False
#
#     return followeds


if __name__ == '__main__':
    uid = 58066
    # 58066-1127   6790397-404-fans 269714


    startT = time.time()
    follows = GetUserFollows(uid)

    for k,v in follows.items():
        print(k,'\t',v)

    endT = time.time()
    print('amount of following :', len(follows))
    print("time costs :", endT-startT)


    # startT = time.time()
    # followeds = AnalyseUserFans(uid, 200)
    # for k,v in followeds.items():
    #     print(k,'\t',v)
    #
    # endT = time.time()
    # print('amount of fans :', len(followeds))
    # print("time costs :", endT-startT)


