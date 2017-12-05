# coding=utf-8
'''多线程执行'''

import queue
import threading
import time

from pymongo import MongoClient

import GetSongsByPlaylist
import GetPlaylistByUserId

SHARE_Q = queue.Queue()
_WORK_THREAD_NUM = 10


class MyThread(threading.Thread):
    '''
    fuc: 线程逻辑函数
    '''
    def __init__(self, func):
        # 调用父类构造函数
        super(MyThread, self).__init__()
        # 传入线程逻辑函数
        self.func = func

    def run(self):
        '''
        重写基类run方法
        '''
        self.func()


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


def worker():
    '''
    工作逻辑，队列不为空则持续处理
    队列为空时检查队列
    queue中包含了wait，notify和lock，放任务和取任务时不需要加锁解锁
    '''
    global SHARE_Q
    while not SHARE_Q.empty():
        # 获取任务
        item = SHARE_Q.get()
        do_sth(item)
        SHARE_Q.task_done()


def main():
    global SHARE_Q
    threads = []
    playlist_id = GetPlaylistByUserId.GetPlaylistID_All('44590287')
    # 向队列中放入任务，可持续性放入
    for task in playlist_id:
        SHARE_Q.put(str(task))
    # 开启_WORK_THREAD_NUM个线程
    for i in range(_WORK_THREAD_NUM):
        thread = MyThread(worker)
        # 开始处理任务
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    # 等待所有任务完成
    SHARE_Q.join()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('time costs: ', end-start)

