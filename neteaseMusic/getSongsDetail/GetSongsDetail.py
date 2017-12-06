# coding=utf-8

from tool import PageRequest
from bs4 import BeautifulSoup

url = r'http://music.163.com/song?id='


def songsInfo(sid):
    '''
    :param sid: 歌曲ID
    :return: songDict {sName: [sSinger, sAlbum]}
    '''

    html = PageRequest.GetHtml(url+str(sid))
    bsObj = BeautifulSoup(html, 'html.parser')

    # 若出现歌曲信息不完整则返回空字典
    try:
    # tmp为歌手与专辑列表
        tmp = bsObj.select('div .cnt p')
        sName = bsObj.select('div .hd .tit em')[0].contents[0]
        sSinger = tmp[0].select('a')[0].contents[0]
        sAlbum = tmp[1].select('a')[0].contents[0]

    except Exception as e:
        print(e)
        songDict = {}
        return songDict

    else:
        singer_album = [sSinger, sAlbum]
        songDict = {sName: singer_album}

    return songDict
