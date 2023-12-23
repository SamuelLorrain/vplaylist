import random
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.playlist import Playlist, RootPath, Video
from vplaylist.entities.search_video import SearchType, SearchVideo, Sorting
from vplaylist.utils.db_utils import (
    get_query_for_quality,
    get_query_for_sorting,
    get_query_for_webm,
)
from vplaylist.utils.query_constructor import QueryConstructor
from vplaylist.utils.regex_utils import (
    basic_regexp,
    regexp_alternative_from_list,
    regexp_permutate,
    synonyms_from_terms,
)


class PlaylistRepository(ABC):
    @abstractmethod
    def create_playlist(
        self, search: SearchVideo, filter_rootpath: list[RootPath]
    ) -> Playlist:
        raise NotImplementedError


class SqlitePlaylistRepository(PlaylistRepository):
    def __init__(self) -> None:
        self.config_registry = ConfigRegistry()
        self.best = self.config_registry.best
        self.db_file = self.config_registry.db_file

    def create_playlist(
        self, search: SearchVideo, filter_rootpath: list[RootPath]
    ) -> Playlist:
        query = self._convert_search_to_query(search, filter_rootpath)
        print(query.get_query_string())
        print(query.get_params())
        query_result = self._execute_query(query, search)
        print(query_result)
        return self._format_query_result_to_playlist(query_result)

    def _convert_search_to_query(
        self, search: SearchVideo, filter_rootpath: list[RootPath]
    ) -> QueryConstructor:
        # base query
        query = QueryConstructor("data_video")
        query = (
            query.add_select("data_rootpath.path")
            .add_select("data_video.path")
            .add_select("height")
            .add_select("width")
            .add_select("date_down")
            .add_select("uuid")
            .add_select("data_rootpath.id as data_rootpath_id")
            .add_join("data_rootpath", "data_video.rootpath_id = data_rootpath.id")
            .add_where_clause(get_query_for_webm(search.webm))
            .add_where_clause(get_query_for_quality(search.quality))
        )

        # TODO review usage
        query.change_limit_clause(search.limit)
        query.change_offset_clause(search.shift)

        if search.sorting != Sorting.ON_RAM_RANDOMIZE:
            query.change_order_clause(get_query_for_sorting(search.sorting))
        self._compute_search_term(query, search)

        query = query.add_where_clause(
            f"data_rootpath.id in ({('?,'*len(filter_rootpath))[:-1]})"
        )
        for i in filter_rootpath:
            query = query.add_param(str(i.id))

        return query

    def _compute_search_term(
        self,
        query: QueryConstructor,
        search: SearchVideo,
    ) -> QueryConstructor:
        match search.search_type:
            case SearchType.NO_SEARCH:
                pass
            case SearchType.BEST:
                best_reg = regexp_alternative_from_list(self.best)
                query = query.add_where_clause("data_video.path REGEXP ?")
                query = query.add_param(best_reg)
            case SearchType.BASIC:
                search_term = search.search_term
                # FIXME read safe terms!
                # if not is_safe_term_search(search_term):
                #     raise ValueError(search_term)
                if search.should_use_synonyms:
                    search_term = synonyms_from_terms(search_term)
                if search.should_permutate:
                    search_term = regexp_permutate(search_term)
                query = query.add_param(search_term)
                query = query.add_where_clause("data_video.path REGEXP ?")
        return query

    def _execute_query(
        self, query: QueryConstructor, search: SearchVideo
    ) -> list[list[Any]]:
        self.conn = sqlite3.connect(self.db_file)
        self.conn.create_function("REGEXP", 2, basic_regexp)
        params = query.get_params()
        if params:
            query_result = self.conn.execute(
                query.get_query_string(), params
            ).fetchall()
        else:
            query_result = self.conn.execute(query.get_query_string()).fetchall()
        self.conn.close()

        if search.sorting == Sorting.ON_RAM_RANDOMIZE:
            # FIXME mixin abstractions
            query_result = random.sample(query_result, k=len(query_result))
        return query_result

    def _format_query_result_to_playlist(
        self, query_result: list[list[Any]]
    ) -> Playlist:
        video_playlist = Playlist(
            Video(
                rootpath=RootPath(id=i[6], path=Path(i[0])),
                path=Path(i[1]),
                height=i[2],
                width=i[3],
                date_down=i[4],
                uuid=i[5],
            )
            for i in query_result
        )
        return video_playlist
