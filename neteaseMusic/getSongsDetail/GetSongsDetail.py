# coding=utf-8

from tool import PageRequest, AES_encrypt
from bs4 import BeautifulSoup
import requests
import json


def songsInfo(sid):
    '''
    :param sid: 歌曲ID
    :return: songDict {sName: [sSinger, sAlbum]}
    '''
    url = r'http://music.163.com/song?id='

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


def getComments(sid):
    '''获取热门评论当前数量，普通评论大于100则获取100条，小于100则获取当前数量'''

    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=' % sid
    PageRequest.headers['Referer'] = 'http://music.163.com/song?id=' + str(sid)
    post_data = AES_encrypt.crypt_api('comments', sid, offset=0)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')

    json_text = json.loads(content)

    hotComments = (hotC for hotC in json_text['hotComments'])
    comments = (comm for comm in json_text['comments'])

    return hotComments, comments
