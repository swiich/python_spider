# coding=utf-8
'''
通过网易云音乐playlistID,获取歌单中歌曲与歌曲ID(ID 450041032,411349068歌曲name为none)
'''

from bs4 import BeautifulSoup
import re
import PageRequest
from lxml import etree


def GetSongsInfo(playlistId):
    '''
    获取歌单歌曲信息, 歌曲数量
    :param playlistId: 歌单ID
    :return: songInfo{id:name} , songcount int
    '''

    url = 'http://music.163.com/playlist?id=' + str(playlistId)

    html = PageRequest.GetHtml(url)

    soup = BeautifulSoup(html, 'html.parser')

    songInfo = soup.select('ul.f-hide li a')
    songName = [s.string for s in songInfo]
    songId = [re.compile('.*=(.*)').findall(s['href'])[0] for s in songInfo]

    # 将歌曲ID与曲名合并为字典
    songInfo = dict(map(lambda x, y: [x, y], songId, songName))

    return songInfo


def GetSongsInfoForTop100(playlistId):
    '''
    判断歌单中歌曲是否大于100，功能与GetSongsInfo稍重复，为避免函数GetSongsInfo_top100多次解析网页，小于100则返回空字典
    :param playlistId: 歌单ID
    :return: songInfo{id:name}
    '''

    url = 'http://music.163.com/playlist?id=' + str(playlistId)

    html = PageRequest.GetHtml(url)

    soup = BeautifulSoup(html, 'html.parser')

    # 歌单中歌曲数量
    songCount = int(soup.select('span#playlist-track-count')[0].string)
    if songCount >= 100:
        songInfo = soup.select('ul.f-hide li a')
        songName = [s.string for s in songInfo]
        songId = [re.compile('.*=(.*)').findall(s['href'])[0] for s in songInfo]
        songInfo = dict(map(lambda x, y: [x, y], songId, songName))
    else:
        songInfo = {}

    return songInfo


def GetSongsInfo_top100(playlistId):
    '''
    获取歌单前100首，不足100则返回空列表
    :param playlistId: 歌单ID
    :return: songsInfo_top100{id:name}
    '''

    songsInfo_100 = {}
    songsInfo_all = GetSongsInfoForTop100(playlistId)
    if songsInfo_all:
        for k, v in songsInfo_all.items():
            temp = {k: v}
            songsInfo_100.update(temp)
            if len(songsInfo_100) == 100:
                break

    return songsInfo_100


# def ParseHtmlMusicList(html):
#     '''
#     解析html网页得到歌曲ID与曲名的字典
#     '''
#
#     soup = BeautifulSoup(html, 'html.parser')
#
#     # 歌曲演唱者及专辑为java动态生成????content中并无专辑信息
#     songInfo = soup.select('ul.f-hide li a')
#     songName = [s.string for s in songInfo]
#     songId = [re.compile('.*=(.*)').findall(s['href'])[0] for s in songInfo]
#
#     # 将歌曲ID与曲名合并为字典
#     songDict = dict(map(lambda x, y: [x, y], songId, songName))
#     return songDict


def GetPlaylistMusicCount(playlistID):
    '''
    获取歌单中歌曲数量
    :param playlistID:
    :return: int count
    '''
    url = 'http://music.163.com/playlist?id=' + str(playlistID)
    selector = etree.HTML(PageRequest.GetHtml(url))
    content = selector.xpath('//*[@id="playlist-track-count"]/text()')[0]

    return int(content)