# coding=utf-8

import time
import queue
import pymysql
from pymongo import MongoClient

from pipeline import MyThread_Usrs
from pipeline import Multiproc_InsertSongs
from pipeline import MyThread_Playlists
from getSongsDetail import GetSongsDetail
from getSongs import GetPlaylistByUserId


# 利用类将方法整合
# 代码整理规范        PEP 8  函数名不规范，应用小写加_，取名应短小   取名与思考尽量Pythonic
# 写个配置文件，将所有也许会修改的数据整合到一起
# 实现日志记录
# README


def get_users():
    """
    crawl users
    """

    config = MyThread_Usrs.config
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "select uid from users where crawled=0 limit 10"
    sql2 = 'update users set crawled=1 where crawled=0 limit 10'

    # initialize uid
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


def get_playlists():
    """crawl playlists"""

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


def get_songs():
    """crawl songs' ID and name"""

    uid_list = []
    client = MongoClient('localhost', 27017)
    db = client['test']
    collection = db['playlistInfo']

    cursor = collection.find()
    for i in cursor:
        uid_list.append(i['_id'])

    while not uid_list:
        Multiproc_InsertSongs.insertSongsOfPlaylistFromUid(uid_list.pop())


def songs_detail():
    """crawl detail information of songs
    ID,NAME,ALBUM
    LYRICS
    COMMENTS
    MP3_URL
    """

    # database connector
    client = MongoClient('localhost', 27017)
    db = client['test']
    collection = db['songsDetail']

    config = MyThread_Usrs.config
    dbm = pymysql.connect(**config)
    cursor = dbm.cursor()

    sql = "select sid from songid where crawled=0 limit 10"
    sql2 = 'update songid set crawled=1 where crawled=0 limit 10'

    task_queue = queue.Queue(maxsize=10)

    while True:
        data = cursor.execute(sql)
        # if cursor is not NONE
        if data:
            # if task_queue is empty, set task_queue
            if task_queue.empty():
                for i in cursor.fetchall():
                    task_queue.put(i['sid'])

                cursor.execute(sql2)
                dbm.commit()


            else:
                # task starts
                sid = task_queue.get()

                post_data = GetSongsDetail.all_info(sid)
                try:
                    collection.insert_one(post_data)
                    print('-----------------end-----------------')
                except Exception:
                    print('dulplicate')

        else:
            dbm.close()
            client.close()
            break


if __name__ == '__main__':
    print( GetPlaylistByUserId.GetPlaylistDetail_All(95031331))
