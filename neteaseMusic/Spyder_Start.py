# coding=utf-8

import time

from pipeline import MyThread_Usrs

# 代码整理规范
# 写个配置文件，将所有也许会修改的数据整合到一起
# 实现断点续传功能

if __name__ == '__main__':

    uid = 45218094
    type = 'follows'

    start = time.time()
    MyThread_Usrs.insertUsrs_1000(uid, type)
    end = time.time()

    print('time costs: ', end - start)
