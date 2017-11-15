import GetSongsByPlaylist
import GetPlaylistByUserId
import Mysql

if __name__ == '__main__':

    uid = 3428554

    # 5832286  28 `  34885501  118    108781179  41   46543242  177   44590287 473  41299404 202   3428554  1-0   29372996 932  29631520 1001  7004245  864
    playlist_id = GetPlaylistByUserId.GetPlaylistID_All(str(uid))[0]

    songIDs= []

    songInfo = GetSongsByPlaylist.GetSongsInfo_top100(str(playlist_id))
    if songInfo:
        for k, v in songInfo.items():
            Mysql.Insert_SongsInfo(k, v)
            songIDs.append(k)

        Mysql.insert_userLovesongs(uid, songIDs)
    else:
        print('用户喜欢歌单中歌曲不足100')