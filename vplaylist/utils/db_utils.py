import string
import itertools
from vplaylist.entities.search_video import Webm, Quality, Sorting

def is_safe_term_search(expr: str):
    """
    Check wether an expression is safe for orm purpose
    """
    for i in string.punctuation:
        if i in expr:
            return False
    return True


def get_query_for_webm(webm: Webm):
    match (webm):
        case Webm.NO_WEBM:
            return "data_video.path NOT LIKE '%webm'"
        case Webm.ONLY_WEBM:
            return "data_video.path LIKE '%webm'"
        case Webm.ALL:
            return ""


def get_query_for_quality(quality: Quality):
    match (quality):
        case Quality.ONLY_SD:
            return "width < 800 AND height < 600"
        case Quality.ONLY_HD:
            return "width >= 800 AND height >= 600"
        case Quality.ALL:
            return ""


def get_query_for_sorting(sorting: Sorting) -> str:
    match (sorting):
        case Sorting.SQL_RANDOM_FUNCTION:
            return "random()"
        case Sorting.LAST_BY_DATE_DOWN:
            return "date_down DESC"
        case Sorting.LAST_BY_ID:
            return "data_video.id DESC"
        case Sorting.ON_RAM_RANDOMIZE:
            return ""
