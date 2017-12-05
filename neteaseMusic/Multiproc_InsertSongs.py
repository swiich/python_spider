# coding=utf-8
'''多进程执行'''

import multiprocessing
import queue
import time

from pymongo import MongoClient

import GetSongsByPlaylist
import GetPlaylistByUserId


def do_sth(item):
    client = MongoClient('localhost', 27017)
    db = client['test']
    collection = db['cloudmusic']

    songInfo = GetSongsByPlaylist.GetSongsInfo_top100(item)
    # for k, v in songInfo.items():
    #     print(k, '\t', v)
    if songInfo:
        post = {
            'playlist_id': item,
            'songsInfo': songInfo
        }

        collection.insert_one(post)
        print('playlist -', item, 'insert successfully')


if __name__ == '__main__':
    start = time.time()

    playlistQue = queue.Queue()
    playlist_id = GetPlaylistByUserId.GetPlaylistID_All('44590287')

    for task in playlist_id:
        playlistQue.put(str(task))

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    for i in range(playlistQue.qsize()):
        pool.apply_async(do_sth, (playlistQue.get(),))

    pool.close()
    pool.join()

    end = time.time()
    print('time costs: ', end-start)
