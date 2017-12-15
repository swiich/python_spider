# 列表切片可能有误，重复检测
# playlist_id = [132831039, 952228112, 132831039, 362363365, 411145389, 477926226]
#
# print(playlist_id)
# print([i for i in list(set(playlist_id)) if playlist_id.count(i) == 2])

#
# for i in range(0, 101):
#     print("%s, ", end='')

# import pymongo
# import datetime
#
# client = pymongo.MongoClient('localhost', 27017)
# db = client['test']
# collection = db['runob']

# post = {"author": "aka",
#          "text": "My last blog post!",
#          "tags": ["mongodb", "python", "pymongo"],
#          "date": datetime.datetime.utcnow()}

# posts = db['posts']
# post_id = posts.insert_one(post).inserted_id
# print(p)


# 5832286  28 `  34885501  118    108781179  41   46543242  177   44590287 473  41299404 202   3428554  1-0   29372996 932  29631520 1001  7004245  864
# from GetSongsByPlaylist import *
# #
# # print(GetSongsByPlaylist.GetPlaylistMusicCount(379396654))
# s = GetSongsInfo(890410865)
# print(get)

# import PageRequest
# from bs4 import BeautifulSoup
# url = 'http://music.163.com/playlist?id=890410865'
#
# html = PageRequest.GetHtml(url)
#
# soup = BeautifulSoup(html, 'html.parser')
# songCount = soup.select('span#playlist-track-count')[0].string
# print(songCount)
# import queue
# q = queue.Queue(maxsize=3)
#
#
# offset = 0
# for i in range(offset, offset + 60, 20):
#     q.put(str(i))
# while not q.empty():
#     print(q.get())
# import pymysql
#
# config = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'password': '1111',
#     'db': 'cloudmusic',
#     'charset': 'utf8mb4',
#     'cursorclass': pymysql.cursors.DictCursor,
# }
# sql = "select uid from users where crawled=0 limit 10"
# db = pymysql.connect(**config)
# cursor = db.cursor()
# cursor.execute(sql)
# s= []
# for i, v in enumerate(cursor.fetchall()):
#     s.append(v[i]['uid'])
#
# db.close()
# print(s)
# import queue
#
# def popq(q):
#     while not q.empty():
#         print(q.get())
#
# q = queue.Queue()
# for i in range(10):
#     q.put(i)
#
# popq(q)
#
# print(q.qsize())

from pymongo import MongoClient
import pymysql

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '1111',
    'db': 'cloudmusic',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
sql = 'insert into songId (sid, sName) VALUES (%s, %s)'
dbm = pymysql.connect(**config)
cursor = dbm.cursor()

# client = MongoClient('localhost', 27017)
# db = client['test']
# collection = db['cloudmusic']

# count = 0
# for a in collection.find():
#     for i in a['playlist']:
#         count += 1
#
# print(count)
#
client = MongoClient('localhost', 27017)
db = client['test']
collection = db['songInfo']


for a in collection.find():
    for i,j in a['songsInfo'].items():
        cursor.execute(sql, (i, j))
        dbm.commit()



# try:
#     for a in collection.find():
#         for p in a['playlist']:
#             cursor.execute(sql, (p, 0))
#         dbm.commit()
# except Exception:
#     pass
#
# finally:
#     client.close()
#     dbm.close()


