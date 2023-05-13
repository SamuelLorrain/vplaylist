from vplaylist.entities.search_video import (
    SearchVideo,
    Sorting,
    SearchType,
)
from vplaylist.entities.playlist import (
    Playlist,
    Video,
    RootPath,
)
from vplaylist.utils.query_constructor import QueryConstructor
from vplaylist.utils.db_utils import (
    get_query_for_webm,
    get_query_for_quality,
    is_safe_term_search,
    get_query_for_sorting,
)
from vplaylist.utils.regex_utils import (
    synonyms_from_terms,
    regexp_permutate,
    basic_regexp,
    regexp_alternative_from_list,
)
from vplaylist.config.config_registry import ConfigRegistry
import sqlite3
import random

class CreatePlaylistService:
    def __init__(self, search: SearchVideo):
        self.search = search
        self.query = None
        self.config_registry = ConfigRegistry()
        self.config_best = self.config_registry.best

    def create_playlist(self) -> Playlist:
        self.query = self._convert_search_to_query()
        query_result = self._execute_query()
        return self._format_query_result_to_playlist(query_result)

    def _convert_search_to_query(self) -> str:
        # base query
        query = QueryConstructor("data_video")
        query = (
            query.add_select("data_rootpath.path")
            .add_select("data_video.path")
            .add_select("height")
            .add_select("width")
            .add_select("date_down")
            .add_select("uuid")
            .add_join("data_rootpath", "data_video.rootpath_id = data_rootpath.id")
            .add_where_clause(get_query_for_webm(self.search.webm))
            .add_where_clause(get_query_for_quality(self.search.quality))
        )

        if self.search.limit is not None:
            query.change_limit_clause(self.search.limit + self.search.shift)
        if self.search.sorting != Sorting.ON_RAM_RANDOMIZE:
            query.change_order_clause(get_query_for_sorting(self.search.sorting))
        self._compute_search_term(query)

        return query

    def _compute_search_term(self, query) -> QueryConstructor:
        match self.search.search_type:
            case SearchType.NO_SEARCH:
                pass
            case SearchType.BEST:
                best_reg = regexp_alternative_from_list(self.config_best)
                query = query.add_where_clause("data_video.path REGEXP ?")
                query = query.add_param(best_reg)
            case SearchType.BASIC:
                search_term = self.search.search_term
                # FIXME read safe terms!
                # if not is_safe_term_search(search_term):
                #     raise ValueError(search_term)
                if self.search.should_use_synonyms:
                    search_term = synonyms_from_terms(search_term)
                if self.search.should_permutate:
                    search_term = regexp_permutate(search_term)
                query = query.add_param(search_term)
                query = query.add_where_clause("data_video.path REGEXP ?")
        return query

    def _execute_query(self):
        # FIXME put all the connection login in another service
        self.conn = sqlite3.connect("db.sqlite3")
        self.conn.create_function("REGEXP", 2, basic_regexp)
        params = self.query.get_params()
        if params:
            query_result = self.conn.execute(
                self.query.get_query_string(), params
            ).fetchall()
        else:
            query_result = self.conn.execute(self.query.get_query_string()).fetchall()
        self.conn.close()

        if self.search.sorting == Sorting.ON_RAM_RANDOMIZE:
            # FIXME mixin abstractions
            query_result = random.sample(query_result, k=len(query_result))
        return query_result

    def _format_query_result_to_playlist(self, query_result) -> Playlist:
        video_playlist = [
            Video(
                rootpath=RootPath(path=i[0]),
                path=i[1],
                height=i[2],
                width=i[3],
                date_down=i[4],
                uuid=i[5],
            )
            for i in query_result
        ]
        return Playlist(playlist=video_playlist)
