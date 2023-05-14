from typing import Optional, Self

from pydantic import BaseModel


class JoinClause(BaseModel):
    table_name: str
    condition: str


class QueryConstructor:
    def __init__(self, table: str) -> None:
        self.from_table = table
        self.where_clauses: list[str] = []
        self.join_clauses: list[JoinClause] = []
        self.select: list[str] = []
        self.order: Optional[str] = None
        self.limit: Optional[int] = None
        self.params: list[str] = []

    def add_where_clause(self, query: str) -> Self:
        if query is None or query == "":
            return self
        self.where_clauses.append(query)
        return self

    def change_order_clause(self, orderQuery: str) -> Self:
        self.order = orderQuery
        return self

    def change_limit_clause(self, limitQuery: int) -> Self:
        self.limit = limitQuery
        return self

    def add_select(self, selectQuery: str) -> Self:
        self.select.append(selectQuery)
        return self

    def add_join(self, table: str, condition: str) -> Self:
        self.join_clauses.append(JoinClause(table_name=table, condition=condition))
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
        query = ""
        if len(self.select):
            query += "SELECT "
            query += ", ".join(self.select)
            query += "\n"
        else:
            query += "SELECT * \n"

        query += f"FROM {self.from_table}\n"
        for join_clause in self.join_clauses:
            query += f"JOIN {join_clause.table_name} ON {join_clause.condition} "

        if len(self.where_clauses):
            query += "WHERE "
            for index, where_clause in enumerate(self.where_clauses):
                if where_clause is None:
                    continue
                if index != 0:
                    query += f"AND {where_clause} "
                else:
                    query += f"{where_clause} "

        if self.order is not None:
            query += f"ORDER BY {self.order}\n"
        if self.limit is not None:
            query += f"LIMIT {self.limit};"
        return query
