from vplaylist.entities.playlist import Playlist, Video, RootPath

def test__playlist_is_a_value_object():
    rootpath = RootPath("/my_root_path")
    # Don't refacto by thinking
    # code is duplicated, that's
    # exactly what we meant to test
    playlist_a = Playlist([
        Video(path="my/path", rootpath=rootpath, height=10, width=10, name="video_1"),
        Video(path="my/path", rootpath=rootpath, height=10, width=10, name="video_2")
    ])
    playlist_b = Playlist([
        Video(path="my/path", rootpath=rootpath, height=10, width=10, name="video_1"),
        Video(path="my/path", rootpath=rootpath, height=10, width=10, name="video_2")
    ])

    assert playlist_a == playlist_b



