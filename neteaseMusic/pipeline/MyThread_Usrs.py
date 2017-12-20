# coding=utf-8
"""get the followings or fans of users, write into database"""

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
        # invoke superclass init method
        super(UsrThread, self).__init__()
        self.uid = uid
        self.type = type
        self.result = None

    def run(self):
        """
        override base class 'run' method
        """
        global SHARE_Q

        if not SHARE_Q.empty():
            # get tasks
            offset = SHARE_Q.get()
            self.result = insertUsrs_100(self.uid, self.type, offset)
            SHARE_Q.task_done()
            print('task----------', self.getName(), '----------done')

    def getResult(self):
        return self.result


def insertUsrs_100(uid, type, offset=0):
    """ write fans or followings depends on 'type' arg """

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
        # if errors, rollback
        db.rollback()

    finally:
        db.close()
        return result


def setOffsetQ():
    """put tasks into 'offset' queue"""

    global SHARE_Q
    if SHARE_Q.empty():
        for i in range(0, 1000, 100):
            SHARE_Q.put(str(i))


def insertUsrs_1000(uid, type):

    threads = []
    total = 0
    setOffsetQ()

    # activate the number of '_WORK_THREAD_NUM' threads
    for i in range(_WORK_THREAD_NUM):
        thread = UsrThread(uid, type)

        # task starts
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
        total += thread.getResult()

    return total


def showUsrs_100(uid, type):
    """show top 100 of fans or followings"""

    tmp = GetUsrs.analyseUsrs(uid, type)

    print('---------------start---------------')
    for k, v in tmp.items():
        print(k, '\t', v)
    print('---------------end---------------')
