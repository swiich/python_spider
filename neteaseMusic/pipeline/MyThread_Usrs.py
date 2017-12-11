# coding=utf-8
'''获取用户关注或粉丝列表写入数据库'''

import queue
import threading
import pymysql

from getUsrs import GetUsrs

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '1111',
    'db': 'cloudmusic',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
sql = "insert into users(uid,name,follows,fans,crawled) VALUES (%s,%s,%s,%s,%s)"

SHARE_Q = queue.Queue()
_WORK_THREAD_NUM = 10


class UsrThread(threading.Thread):
    def __init__(self, uid, type):
        # 调用父类构造函数
        super(UsrThread, self).__init__()
        self.uid = uid
        self.type = type
        self.result = None

    def run(self):
        '''
        重写基类run方法
        '''
        global SHARE_Q

        if not SHARE_Q.empty():
            # 获取任务
            offset = SHARE_Q.get()
            self.result = insertUsrs_100(self.uid, self.type, offset)
            SHARE_Q.task_done()
            print('task----------', self.getName(), '----------done')

    def getResult(self):
        return self.result


def insertUsrs_100(uid, type, offset=0):
    '''根据type选择写入粉丝或关注列表,获取step 100'''

    db = pymysql.connect(**config)
    cursor = db.cursor()

    user = GetUsrs.analyseUsrs(uid, type, offset)

    result = 0
    try:
        if user:
            for k, v in user.items():
                cursor.execute(sql, (k, v[0], v[1], v[2], 0))
                db.commit()
                result += 1

    except pymysql.Error:
        # 出错则回滚
        db.rollback()

    finally:
        db.close()
        return result


def setOffsetQ():
    '''向offset队列中放入任务'''
    global SHARE_Q
    if SHARE_Q.empty():
        for i in range(0, 1000, 100):
            SHARE_Q.put(str(i))


def insertUsrs_1000(uid, type):

    threads = []
    total = 0
    setOffsetQ()

    # 开启_WORK_THREAD_NUM个线程
    for i in range(_WORK_THREAD_NUM):
        thread = UsrThread(uid, type)

        # 开始处理任务
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        total += thread.getResult()

    return total


def showUsrs_100(uid, type):
    '''显示关注或粉丝列表前100'''

    tmp = GetUsrs.analyseUsrs(uid, type)

    print('---------------start---------------')
    for k, v in tmp.items():
        print(k, '\t', v)
    print('---------------end---------------')
