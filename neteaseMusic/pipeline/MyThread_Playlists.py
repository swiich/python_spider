# coding=utf-8
"""get playlists and write into database"""

import queue
import threading
from pymongo import MongoClient

from getSongs import GetPlaylistByUserId

client = MongoClient('localhost', 27017)
db = client['test']
collection = db['playlistDetailInfo']

_WORK_THREAD_NUM = 10


class PlaylistThread(threading.Thread):
    def __init__(self, uid):
        # invoke superclass init method
        super(PlaylistThread, self).__init__()
        self.uid = uid
        self.result = None

    def run(self):
        """
        override base class 'run' method
        """
        self.result = insert_playlist_one(self.uid)
        print('task----------', self.getName(), '----------done')

    def getResult(self):
        return self.result


def insert_playlist_one(uid):
    # get details of self-created playlist
    # playlist = GetPlaylistByUserId.GetPlaylistID_Self(uid)
    playlist = GetPlaylistByUserId.GetPlaylistDetail_Self(uid)

    try:
        # pass if none or just one playlist
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
    """
    put uids from task_queue into database
    :param task_queue:uid queue
    :return count:the number of successfully inserted
    """
    threads = []
    count = 0

    try:
        # add objects in task_queue into thread
        for i in range(_WORK_THREAD_NUM):
            if not task_queue.empty():
                thread = PlaylistThread(task_queue.get())

            else:
                # StopIteration - no more values in iterator
                raise StopIteration
            # tasks start
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            if thread.getResult():
                count += 1

    except KeyboardInterrupt:
        print('user interrupted')

    except StopIteration:
        print('empty task_queue')

    finally:
        client.close()
        return count
