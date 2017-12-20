# coding=utf-8
"""multiprocessing"""

import multiprocessing
import queue

from pymongo import MongoClient
from getSongs import GetPlaylistByUserId
from getSongs import GetSongsByPlaylist

client = MongoClient('localhost', 27017)
db = client['test']
collection = db['songInfo']


def getTask_Q(uid):
    # set task queue
    playlistQue = queue.Queue()
    playlist_id = GetPlaylistByUserId.GetPlaylistID_All(uid)

    for task in playlist_id:
        playlistQue.put(str(task))

    return playlistQue


def insertSongsOfPlaylist_single(uid, pid):
    # put songs in pid into database, off operation and return false if none in playlist
    songInfo = GetSongsByPlaylist.GetSongsInfo(pid)

    try:
        if songInfo:
            post = {
                '_id': pid,
                'uid': uid,
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
    # set up process pool
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
