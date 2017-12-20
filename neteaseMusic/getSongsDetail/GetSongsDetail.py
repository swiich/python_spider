# coding=utf-8

from tool import PageRequest, AES_encrypt
from bs4 import BeautifulSoup
import requests
import json


def songsInfo(sid):
    """
    :return: songDict {sName: [sSinger, sAlbum]}
    """
    url = r'http://music.163.com/song?id='

    html = PageRequest.GetHtml(url+str(sid))
    bsObj = BeautifulSoup(html, 'html.parser')

    # return NULL if not intact song information
    try:
        # tmp - singer and album list
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
    """
    get current number of hot comments，get 100 items if common comments are more than 100，
    current number of items if comments are less than 100
    """

    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=' % sid
    PageRequest.headers['Referer'] = 'http://music.163.com/song?id=' + str(sid)
    post_data = AES_encrypt.crypt_api('comments', sid, offset=0)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')

    json_text = json.loads(content)

    hts = []
    cs = []

    hotComments = (hotC for hotC in json_text['hotComments'])
    comments = (comm for comm in json_text['comments'])

    for i in hotComments:
        hts.append(i)
    for i in comments:
        cs.append(i)

    return hts, cs


def getLyric(sid):
    """crawl lyrics"""

    url = 'http://music.163.com/weapi/song/lyric?csrf_token='
    PageRequest.headers['Referer'] = 'http://music.163.com/song?id=' + str(sid)
    post_data = AES_encrypt.crypt_api('lyrics', sid)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')

    json_text = json.loads(content)

    # if lyrics NULL
    try:
        lrc = json_text['lrc']
        tlyric = json_text['tlyric']

    except KeyError:
        lrc = None
        tlyric = None


    return lrc, tlyric


def get_song_mp3(sid):
    # crawl MP3 url

    url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    PageRequest.headers['Referer'] = 'http://music.163.com/song?id=' + str(sid)
    post_data = AES_encrypt.crypt_api('mp3', sid)

    content = requests.post(url, headers=PageRequest.headers, data=post_data).content.decode('utf-8')

    json_text = json.loads(content)

    mp3_url = json_text['data'][0]['url']

    return mp3_url


def all_info(sid):
    # id,name,album,lyric,comments,mp3_url

    name_singr_albm = songsInfo(sid)
    lrc, tlyric = getLyric(sid)
    hotcs, comments = getComments(sid)
    mp3_url = get_song_mp3(sid)

    post_data = {
        '_id': sid,
        'n_s_a': name_singr_albm,
        'lrcs': [lrc, tlyric],
        'cmts': [hotcs, comments],
        'mp3_url': mp3_url
    }

    return post_data
