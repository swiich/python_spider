# coding=utf-8
'''
获取所查询ID用户的歌单详情
'''

import json
import re

import requests
from lxml import etree
from tool import PageRequest
from tool import AES_encrypt


def GetTheNumberOfPl(uid):
    '''
    获取用户歌单数量
    :param uid: 用户ID
    :return: (自创歌单数量，收藏歌单数量)
    '''
    url = 'http://music.163.com/user/home?id=' + str(uid)
    selector = etree.HTML(PageRequest.GetHtml(url))
    content = selector.xpath('//*[@id="cHeader"]/h3/span/text()')[0]
    # 用户自创歌单
    amountCreate = int(re.compile(r'\d+').findall(content)[0])
    content = selector.xpath('//*[@id="sHeader"]/h3/span/text()')[0]
    # 用户收藏歌单
    amountCollect = int(re.compile(r'\d+').findall(content)[0])

    return amountCreate, amountCollect


def GetPlaylistDetail_Separately(uid):
    '''
    分别返回自创与收藏歌单详细信息
    :param uid: 用户ID
    :return: (playlist_detail 自创, playlist_detail 收藏)
    '''
    PageRequest.headers['Referer'] = 'http://music.163.com/user/home?id=' + uid
    # playlist所请求网址
    url = 'http://music.163.com/weapi/user/playlist?csrf_token='

    post_data = AES_encrypt.crypt_api('playlists', uid)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')
    # 解析json
    json_text = json.loads(content)
    playlist = json_text['playlist']

    n = GetTheNumberOfPl(uid)
    playlist_self = playlist[0:n[0]-1]
    playlist_collect = playlist[n[0]+n[1]-1:-(n[1]+2):-1]

    return playlist_self, playlist_collect


def GetPlaylistDetail_All(uid):
    '''
    自创与收藏歌单详细信息
    :param uid:
    :return: playlistDetail_all
    '''
    a = GetPlaylistDetail_Separately(uid)
    return a[0] + a[1]


def GetPlaylistID_Separately(uid):
    '''
    解析json,提取playlist的ID（自创与收藏分别返回)
    :param uid: 用户ID
    :return: (playlist_self 自创歌单,playlist_collect 收藏歌单)
    '''
    # playlist 歌单详情,包含大量歌单信息
    playlist = GetPlaylistDetail_All(uid)

    # 利用列表切片分离出自创歌单与收藏歌单
    n = GetTheNumberOfPl(uid)
    playlist_self = playlist[0:n[0]-1]
    playlist_collect = playlist[n[0]+n[1]-1:-(n[1]+2):-1]

    # playlist_id ，此处暂只取歌单ID, 列表
    playlistID_self = [i['id'] for i in playlist_self]
    playlistID_collect = [i['id'] for i in playlist_collect]

    return playlistID_self, playlistID_collect


def GetPlaylistID_All(uid):
    '''
    获取自创与收藏所有的所有歌单ID
    :param uid: 用户ID
    :return: playlist_all ( )
    '''
    a = GetPlaylistID_Separately(str(uid))
    return a[0] + a[1]
