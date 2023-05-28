from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional, Self


@dataclass
class JoinClause:
    table_name: str
    condition: str


class QueryConstructor:
    def __init__(self, table: str) -> None:
        self.from_table: str = table
        self.where_clauses: list[str] = []
        self.join_clauses: list[JoinClause] = []
        self.outer_join_clauses: list[JoinClause] = []
        self.select: list[str] = []
        self.order: Optional[str] = None
        self.limit: Optional[int] = None
        self.offset: Optional[int] = None
        self.params: list[str] = []
        self.group_by: Optional[str] = None

    def add_where_clause(self, query: str) -> Self:
        if query is None or query == "":
            return self
        self.where_clauses.append(query)
        return self

    def add_group_by_clause(self, query: str) -> Self:
        if query == "":
            return self
        self.group_by = query
        return self

    def change_order_clause(self, orderQuery: str) -> Self:
        self.order = orderQuery
        return self

    def change_limit_clause(self, limitQuery: int) -> Self:
        self.limit = limitQuery
        return self

    def change_offset_clause(self, offset_query: int) -> Self:
        self.offset = offset_query
        return self

    def add_select(self, select_query: str | Iterable[str]) -> Self:
        if isinstance(select_query, str):
            self.select.append(select_query)
        else:
            for i in select_query:
                self.select.append(i)
        return self

    def add_join(self, table: str, condition: str) -> Self:
        self.join_clauses.append(JoinClause(table_name=table, condition=condition))
        return self

    def add_outer_join(self, table: str, condition: str) -> Self:
        self.outer_join_clauses.append(
            JoinClause(table_name=table, condition=condition)
        )
        return self

    def change_from(self, from_table: str) -> Self:
        self.from_table = from_table
        return self

    def add_param(self, param: str) -> Self:
        self.params.append(param)
        return self

    def get_params(self) -> list[str]:
        return self.params

    def get_query_string(self) -> str:
        query = self._compute_select()
        query += self._compute_from()
        query += self._compute_join()
        query += self._compute_outer_join()
        query += self._compute_where()
        query += self._compute_group_by()
        query += self._compute_order()
        query += self._compute_limit()
        return query + ";"

    def _compute_where(self) -> str:
        if len(self.where_clauses) == 0:
            return ""

        where_query = "WHERE "
        for index, where_clause in enumerate(self.where_clauses):
            if where_clause is None:
                continue
            if index != 0:
                where_query += f"AND {where_clause} "
            else:
                where_query += f"{where_clause} "
        return where_query

    def _compute_group_by(self) -> str:
        if self.group_by is None:
            return ""
        return f"GROUP BY {self.group_by}\n"

    def _compute_order(self) -> str:
        if self.order is not None:
            return f"ORDER BY {self.order}\n"
        return ""

    def _compute_limit(self) -> str:
        limit = ""
        if self.limit is not None:
            limit += f"LIMIT {self.limit}"
        if self.offset is not None:
            limit += f" OFFSET {self.offset}"
        return limit

    def _compute_select(self) -> str:
        select_query = ""
        if len(self.select):
            select_query += "SELECT "
            select_query += ", ".join(self.select)
            select_query += "\n"
        else:
            select_query += "SELECT * \n"
        return select_query

    def _compute_join(self) -> str:
        join_query = ""
        for join_clause in self.join_clauses:
            join_query += f"JOIN {join_clause.table_name} ON {join_clause.condition}\n"
        return join_query

    def _compute_outer_join(self) -> str:
        join_query = ""
        for join_clause in self.outer_join_clauses:
            join_query += (
                f"LEFT OUTER JOIN {join_clause.table_name} ON {join_clause.condition}\n"
            )
        return join_query

    def _compute_from(self) -> str:
        return f"FROM {self.from_table}\n"
