from vplaylist.service.playlist import PlaylistService
from vplaylist.entities import SearchVideo

# def test__playlist_service_can_create_query_string():
#     search = SearchVideo()
#     playlist_service = PlaylistService(search)
#     query = playlist_service._convert_search_to_query()
#     assert query.get_query_string() == """SELECT data_rootpath.path, data_video.path, height, width, date_down
# FROM data_video
# JOIN data_rootpath ON data_video.rootpath_id = data_rootpath.id WHERE data_video.path.REGEXP ? ORDER BY date_down DESC
# LIMIT 150;"""


def test__playlist_service_can_execute_query():
    search = SearchVideo()
    playlist_service = PlaylistService(search)
    playlist_service.query = playlist_service._convert_search_to_query()
    result = playlist_service._execute_query()




