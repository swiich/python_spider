'''
通过网易云音乐playlistID,获取歌单中歌曲与歌曲ID(偶尔有歌单中歌曲name为none)
'''

from bs4 import BeautifulSoup
import re
import PageRequest


def GetSongsInfo(playlistId):
    '''
    获取歌单歌曲信息
    :param playlistId: 歌单ID
    :return: songInfo{id:name}
    '''

    url = 'http://music.163.com/playlist?id=' + playlistId

    html = PageRequest.GetHtml(url)
    songInfo = ParseHtmlMusicList(html)
    return songInfo


def GetSongsInfo_top100(playlistId):
    '''
    获取歌单前100首，不足100则返回空列表
    :param playlistId: 歌单ID
    :return: songsInfo_top100{id:name}
    '''

    songsInfo_100 = {}
    songsInfo_all = GetSongsInfo(playlistId)
    if len(songsInfo_all) > 100:
        for k, v in songsInfo_all.items():
            temp = {k: v}
            songsInfo_100.update(temp)
            if len(songsInfo_100) == 100:
                break

    return songsInfo_100


def ParseHtmlMusicList(html):
    '''解析html网页得到歌曲ID与曲名的字典'''

    soup = BeautifulSoup(html, 'html.parser')

    # 歌曲演唱者及专辑为java动态生成????content中并无专辑信息
    songInfo = soup.select('ul.f-hide li a')
    songName = [s.string for s in songInfo]
    songId = [re.compile('.*=(.*)').findall(s['href'])[0] for s in songInfo]

    # 将歌曲ID与曲名合并为字典
    songDict = dict(map(lambda x, y: [x, y], songId, songName))
    return songDict
