# coding=utf-8

import time
import queue
import pymysql
from pymongo import MongoClient

from pipeline import MyThread_Usrs, Multiproc_InsertSongs, MyThread_Playlists
from getSongsDetail import GetSongsDetail


# 代码整理规范   PEP 8
# 写个配置文件，将所有也许会修改的数据整合到一起
# 实现断点续传功能
# 实现日志记录


def GetUsrs():

    config = MyThread_Usrs.config
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "select uid from users where crawled=0 limit 10"
    sql2 = 'update users set crawled=1 where crawled=0 limit 10'

    # 起始uid
    start_uid = [1]

    total = 0
    start = time.time()
    try:
        while True:
            curr = 0
            uid = start_uid.pop()
            curr += MyThread_Usrs.insertUsrs_1000(uid, 'fans')
            curr += MyThread_Usrs.insertUsrs_1000(uid, 'follows')

            if not start_uid:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    start_uid.append(i['uid'])
                cursor.execute(sql2)
                db.commit()

            time.sleep(1)
            print("------------------------------currently crawled :" + str(curr) + "------------------------------")
            print('------------------------------section    '+str(uid)+'    end------------------------------')
            total += curr

    except KeyboardInterrupt:
        db.close()
        end = time.time()
        print('time costs: ', end - start)
        print('totally crawled :' + str(total))

    except Exception as e:
        db.close()
        print(e)


def GetPlaylists():

    config = MyThread_Usrs.config
    db = pymysql.connect(**config)
    cursor = db.cursor()

    sql = "select uid from users where crawled_p=0 limit 10"
    sql2 = 'update users set crawled_p=1 where crawled_p=0 limit 10'

    task_queue = queue.Queue()

    count = 0
    try:
        while True:
            cursor.execute(sql)
            for i in cursor.fetchall():
                task_queue.put(i['uid'])
            cursor.execute(sql2)
            db.commit()

            if not task_queue.empty():
                count += MyThread_Playlists.insert_playlist_many(task_queue)

    except Exception as e:
        print(e)

    finally:
        db.close()
        return count


def GetSongs():
    # uid_list = [317081492, 119777169, 480431733, 62879556, 104388569, 647259377,
    #             129593031, 74029445, 136616, 115260210, 68014748]
    uid_list = []
    client = MongoClient('localhost', 27017)
    db = client['test']
    collection = db['playlistInfo']

    cursor = collection.find()
    for i in cursor:
        uid_list.append(i['_id'])

    while not uid_list:
        Multiproc_InsertSongs.insertSongsOfPlaylistFromUid(uid_list.pop())


def tmp():
    Multiproc_InsertSongs.insertSongsOfPlaylistFromUid(58037)
    Multiproc_InsertSongs.insertSongsOfPlaylistFromUid(58039)


if __name__ == '__main__':
    a = GetSongsDetail.get_song_mp3(27598482)
    print(a)

