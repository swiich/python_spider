# coding=utf-8

import time

from pipeline import MyThread_Usrs, Multiproc_InsertSongs
from getSongs import GetPlaylistByUserId

# 代码整理规范
# 写个配置文件，将所有也许会修改的数据整合到一起
# 实现断点续传功能
# 实现日志记录

if __name__ == '__main__':

    uid = 29631520
    type = 'fans'

    start = time.time()
    # MyThread_Usrs.insertUsrs_1000(uid, type)
    # Multiproc_InsertSongs.insertSongsOfPlaylistFromUid(uid)
    a = GetPlaylistByUserId.GetPlaylistID_All(uid)
    print(a)
    end = time.time()

    print('time costs: ', end - start)

