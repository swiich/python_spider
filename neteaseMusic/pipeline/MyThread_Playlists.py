# coding=utf-8
'''获取用户歌单写入数据库'''

import queue
import threading
from pymongo import MongoClient

from getSongs import GetPlaylistByUserId

client = MongoClient('localhost', 27017)
db = client['test']
collection = db['cloudmusic']

_WORK_THREAD_NUM = 10


class PlaylistThread(threading.Thread):
    def __init__(self, uid):
        # 调用父类构造函数
        super(PlaylistThread, self).__init__()
        self.uid = uid
        self.result = None

    def run(self):
        '''
        重写基类run方法
        '''
        self.result = insert_playlist_one(self.uid)
        print('task----------', self.getName(), '----------done')

    def getResult(self):
        return self.result


def insert_playlist_one(uid):
    # 获取用户自创歌单列表
    playlist = GetPlaylistByUserId.GetPlaylistID_Self(uid)

    try:
        # 用户没有或只有一个歌单则不写入数据库库
        if len(playlist) > 1:
            post = {
                '_id': uid,
                'playlist': playlist
            }

            collection.insert_one(post)
            return True

        else:
            return False

    except Exception:
        return False

    finally:
        client.close()


def insert_playlist_many(task_queue):
    '''
    将队列中任务uid写入数据库
    :param task_queue:uid队列
    :return count:插入成功数量
    '''
    threads = []
    count = 0

    try:
        # 将task_queue中对象加入任务队列
        for i in range(_WORK_THREAD_NUM):
            if not task_queue.empty():
                thread = PlaylistThread(task_queue.get())

            else:
                # StopIteration 迭代器没有更多的值
                raise StopIteration
            # 开始处理任务
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            if thread.getResult():
                count += 1

    except KeyboardInterrupt:
        print('用户中断操作')

    except StopIteration:
        print('任务队列为空')

    finally:
        client.close()
        return count
