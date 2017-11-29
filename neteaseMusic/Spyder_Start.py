import GetSongsByPlaylist
import GetPlaylistByUserId
from pymongo import MongoClient
import time


if __name__ == '__main__':

    client = MongoClient('localhost', 27017)
    db = client['test']
    collection = db['cloudmusic']

    total = 0
    uid = 29372996

    start = time.time()
    try:
        playlist_id_all = GetPlaylistByUserId.GetPlaylistID_All(str(uid))

        for playlist_id in playlist_id_all:
            # 歌单中歌曲信息
            songInfo = GetSongsByPlaylist.GetSongsInfo_top100(str(playlist_id))

            if songInfo:
                post = {
                    'uid': uid,
                    'playlist_id': playlist_id,
                    'songs': songInfo
                }

                collection.insert_one(post)
                total += 1

                print('playlist -',playlist_id,'insert successfully')

        end = time.time()
        print(total,' playlists have successfully added into db')
        print('time costs : ', end-start)
    except Exception:
        print(Exception)