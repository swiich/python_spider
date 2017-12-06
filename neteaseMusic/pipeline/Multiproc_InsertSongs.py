# coding=utf-8
'''多进程执行用户歌曲写入'''

import multiprocessing
import queue

from pymongo import MongoClient
from getSongs import GetPlaylistByUserId
from getSongs import GetSongsByPlaylist

client = MongoClient('localhost', 27017)
db = client['test']
collection = db['cloudmusic']


def getTask_Q(uid):
    # 获取任务队列
    playlistQue = queue.Queue()
    playlist_id = GetPlaylistByUserId.GetPlaylistID_All(uid)

    for task in playlist_id:
        playlistQue.put(str(task))

    return playlistQue


def insertSongsOfPlaylist_single(uid, pid):
    # 将pid中歌曲写入数据库,如果歌单中无歌曲则不进行操作并返回false
    songInfo = GetSongsByPlaylist.GetSongsInfo(pid)

    try:
        if songInfo:
            post = {
                'uid': uid,
                'playlist_id': pid,
                'songsInfo': songInfo
            }

            collection.insert_one(post)

            return pid
        else:
            return False

    except Exception as e:
        print(e)

    finally:
        client.close()


def insertSongsOfPlaylistFromUid(uid):
    # 创建进程池
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    results = []
    playlistQue = getTask_Q(uid)

    for i in range(playlistQue.qsize()):
        results.append(pool.apply_async(insertSongsOfPlaylist_single, (uid, playlistQue.get(),)))

    pool.close()
    pool.join()

    for i in results:
        print(i.get())

    print('------------------jobs end------------------')
