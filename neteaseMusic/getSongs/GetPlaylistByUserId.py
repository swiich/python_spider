# coding=utf-8
"""
get details of playlist that you search in keyword 'ID'
"""

import json
import re

import requests
from lxml import etree
from tool import PageRequest
from tool import AES_encrypt


def GetTheNumberOfPl(uid):
    """get the number of playlists

    :return: (self-created，collected)

    """

    url = 'http://music.163.com/user/home?id=' + str(uid)
    selector = etree.HTML(PageRequest.GetHtml(url))

    content = selector.xpath('//*[@id="cHeader"]/h3/span/text()')[0]
    amountCreate = int(re.compile(r'\d+').findall(content)[0])

    content = selector.xpath('//*[@id="sHeader"]/h3/span/text()')[0]
    amountCollect = int(re.compile(r'\d+').findall(content)[0])

    return amountCreate, amountCollect


def GetPlaylistDetail_Respectively(uid):
    """
    return self_c and collected details respectively
    """

    PageRequest.headers['Referer'] = 'http://music.163.com/user/home?id=' + str(uid)
    url = 'http://music.163.com/weapi/user/playlist?csrf_token='

    post_data = AES_encrypt.crypt_api('playlists', uid)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')

    json_text = json.loads(content)
    playlist = json_text['playlist']

    n = GetTheNumberOfPl(uid)
    playlist_self = playlist[0:n[0]-1]
    playlist_collect = playlist[n[0]+n[1]-1:-(n[1]+2):-1]

    return playlist_self, playlist_collect


def GetPlaylistDetail_All(uid):
    """details of self_c and collected
    :return: playlistDetail_all

    """

    a = GetPlaylistDetail_Respectively(uid)
    return a[0] + a[1]


def GetPlaylistID_Respectively(uid):

    playlist = GetPlaylistDetail_All(uid)

    # slice ...separate from... you know
    n = GetTheNumberOfPl(uid)
    playlist_self = playlist[0:n[0]-1]
    playlist_collect = playlist[n[0]+n[1]-1:-(n[1]+2):-1]

    playlistID_self = [i['id'] for i in playlist_self]
    playlistID_collect = [i['id'] for i in playlist_collect]

    return playlistID_self, playlistID_collect


def GetPlaylistID_All(uid):
    """
    :return: playlist_all ( )

    """
    a = GetPlaylistID_Respectively(str(uid))
    return a[0] + a[1]


def GetPlaylistDetail_Self(uid):

    PageRequest.headers['Referer'] = 'http://music.163.com/user/home?id=' + str(uid)
    url = 'http://music.163.com/weapi/user/playlist?csrf_token='
    post_data = AES_encrypt.crypt_api('playlists', uid)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')

    json_text = json.loads(content)
    playlist = json_text['playlist']

    n = GetTheNumberOfPl(uid)
    playlist_self = playlist[0:n[0]-1]

    return playlist_self


def GetPlaylistID_Self(uid):

    playlist = GetPlaylistDetail_Self(uid)
    playlistID_self = [i['id'] for i in playlist]

    return playlistID_self
