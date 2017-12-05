# coding=utf-8
'''多线程执行'''

import queue
import threading
import pymysql
import UserFollows
import time

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '1111',
    'db': 'cloudmusic',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
sql = "insert into users(uid,name) VALUES (%s,%s)"

SHARE_Q = queue.Queue(maxsize=3)
_WORK_THREAD_NUM = 3


class MyThread(threading.Thread):
    def __init__(self):
        # 调用父类构造函数
        super(MyThread, self).__init__()
        self._result = None

    def run(self):
        '''
        重写基类run方法
        '''
        # 13092967
        global SHARE_Q
        uid = 328111204
        if not SHARE_Q.empty():
            # 获取任务
            offset = SHARE_Q.get()
            state = InsertUsrFans_100(uid, offset)
            SHARE_Q.task_done()

            self._result = state

    def get_result(self):
        return self._result


def InsertUsrFans_100(uid, offset):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    fans = UserFollows.AnalyseUserFans(uid, offset)

    try:
        if fans:
            for k, v in fans.items():
                cursor.execute(sql, (k, v))
                db.commit()
            if len(fans) < 20:
                flag = False
            else:
                flag = True
        else:
            flag = False
    except Exception as e:
        print(e)
        # 出错则回滚
        db.rollback()
    finally:
        return flag
        db.close()


def setOffsetQ(offset):
    '''向offset队列中放入任务'''
    global SHARE_Q
    if SHARE_Q.empty():
        for i in range(offset, offset+60, 20):
            SHARE_Q.put(str(i))


def main():
    offset = 0
    setOffsetQ(offset)

    while True:
        results = []
        threads = []



        # 开启_WORK_THREAD_NUM个线程
        for i in range(_WORK_THREAD_NUM):
            thread = MyThread()
            # 开始处理任务
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            # 通过result判断是否爬取完粉丝列表
            results.append(str(thread.get_result()))

        if 'False' in results:
            break
        else:
            offset += 60
            setOffsetQ(offset)



if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('time costs: ', end-start)

