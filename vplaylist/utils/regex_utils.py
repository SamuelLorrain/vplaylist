import re
import itertools
from vplaylist.config.config_registry import ConfigRegistry

def basic_regexp(expr: str, item) -> bool:
    reg = re.compile(expr, re.IGNORECASE)
    return reg.search(item) is not None


def regexp_permutate(expr) -> str:
    reg = ""
    for i in itertools.permutations(expr.split()):
        reg += "("
        for j in i:
            reg += j + ".*"
        reg = reg + ")|"
    return ".*" + reg[:-1] + ".*"


def regexp_alternative_from_list(terms: list[str]) -> str:
    reg = "|".join([i.lower() for i in terms])
    reg = reg[:-1]
    reg = "(" + reg + ")"
    return reg


def synonyms_from_terms(expr: str) -> str:
    config_registry = ConfigRegistry()
    if " " in expr:
        return expr

    # FIXME should be in the playlistService
    for i in config_registry.synonyms:
        for j in i:
            if expr == j:
                return "|".join(i)
    return expr
