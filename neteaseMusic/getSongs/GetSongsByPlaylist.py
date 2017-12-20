# coding=utf-8

import re

from bs4 import BeautifulSoup
from lxml import etree

from tool import PageRequest


def GetSongsInfo(playlistId):
    '''
    :return: songInfo{id:name} , songcount int
    '''

    url = 'http://music.163.com/playlist?id=' + str(playlistId)
    html = PageRequest.GetHtml(url)
    soup = BeautifulSoup(html, 'html.parser')

    songInfo = soup.select('ul.f-hide li a')
    songName = [s.string for s in songInfo]
    songId = [re.compile('.*=(.*)').findall(s['href'])[0] for s in songInfo]

    # zip to dict
    songInfo = dict(map(lambda x, y: [x, y], songId, songName))

    return songInfo


def GetSongsInfoForTop100(playlistId):
    '''
    return 100 items or NULL if less than 100
    :return: songInfo{id:name}
    '''

    url = 'http://music.163.com/playlist?id=' + str(playlistId)
    html = PageRequest.GetHtml(url)
    soup = BeautifulSoup(html, 'html.parser')

    # the number of songs in playlist
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
    get top 100 songs in playlist, if it's not enough of 100 items then return NULL
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


def GetPlaylistMusicCount(playlistID):
    '''
    get the number of songs in playlist
    :param playlistID:
    :return: int count
    '''
    url = 'http://music.163.com/playlist?id=' + str(playlistID)
    selector = etree.HTML(PageRequest.GetHtml(url))
    content = selector.xpath('//*[@id="playlist-track-count"]/text()')[0]

    return int(content)
