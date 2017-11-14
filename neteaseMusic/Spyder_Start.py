import GetSongsByPlaylist
import GetPlaylistByUserId

if __name__ == '__main__':

    uid = 46543242

    total = 0
    # 5832286  28 `  34885501  118    108781179  41   46543242  177   44590287 473  41299404 202   3428554  1-0   29372996 932  29631520 1001  7004245  864
    playlist_id = GetPlaylistByUserId.GetPlaylistID_All(str(uid))

    # print(playlist_id)
    # print([i for i in list(set(playlist_id)) if playlist_id.count(i) == 2])    重复检测


    for i in playlist_id:
        songInfo = GetSongsByPlaylist.GetSongsInfo(str(i))
        for k, v in songInfo.items():
            print(k, '\t', v)
            total += 1

          
    print('当前爬取歌曲总数量: ', total)
    print('当前爬取歌单量: ', len(playlist_id))
    playlist_total = GetPlaylistByUserId.GetTheNumberOfPl(str(uid))
    print('歌单总量: ', playlist_total[0]+playlist_total[1])