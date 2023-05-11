class QueryConstructor:
    def __init__(self, table: str):
        self.fromTable = table
        self.baseQueryString = ""
        self.whereClauses = []
        self.joinClauses = []
        self.select = []
        self.order = None
        self.limit = None
        self.params = []

    def add_where_clause(self, query: str):
        if query is None or query == "":
            return self
        self.whereClauses.append(query)
        return self

    def change_order_clause(self, orderQuery: str):
        self.order = orderQuery
        return self

    def change_limit_clause(self, limitQuery: int):
        self.limit = limitQuery
        return self

    def add_select(self, selectQuery: str):
        self.select.append(selectQuery)
        return self

    def add_join(self, table, condition):
        self.joinClauses.append({"table": table, "condition": condition})
        return self

    def change_from(self, fromQuery):
        self.fromTable = fromQuery
        return self

    def add_param(self, param):
        self.params.append(param)
        return self

    def get_params(self):
        return self.params

    def get_query_string(self) -> str:
        query = ""
        if len(self.select):
            query += "SELECT "
            query += ", ".join(self.select)
            query += "\n"
        else:
            query += "SELECT * \n"

        query += f"FROM {self.fromTable}\n"
        for i in self.joinClauses:
            query += f"JOIN {i['table']} ON {i['condition']} "

        if len(self.whereClauses):
            query += "WHERE "
            for index, whereClause in enumerate(self.whereClauses):
                if whereClause is None:
                    continue
                if index != 0:
                    query += f"AND {whereClause} "
                else:
                    query += f"{whereClause} "

        if self.order is not None:
            query += f"ORDER BY {self.order}\n"
        if self.limit is not None:
            query += f"LIMIT {self.limit};"
        return query
