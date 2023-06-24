import sqlite3

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.analytics import Analytics


class AnalyticsRepository:
    def __init__(self) -> None:
        self.config_registry = ConfigRegistry()
        self.db_file = self.config_registry.db_file

    def save_analytics(self, analytics: Analytics) -> bool:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # analytic
        insert_analytic_query = """
            INSERT INTO video_analytics(timestamp, video_uuid)
            VALUES (?, ?)
            RETURNING id;
        """
        cursor.execute(
            insert_analytic_query,
            (analytics.date_analytics.timestamp(), str(analytics.video_uuid)),
        )
        analytic_id = cursor.fetchall()
        conn.commit()

        # event
        insert_analytics_event_query = """
            INSERT INTO analytic_event(type, value, timestamp, video_analytics_id)
            VALUES
        """
        params_list = []
        for i in analytics.events:
            insert_analytics_event_query = (
                insert_analytics_event_query + "(?, ?, ?, ?),"
            )
            params_list.extend(
                [i.event_type, i.value, i.event_datetime.timestamp(), analytic_id[0][0]]
            )
        insert_analytics_event_query = insert_analytics_event_query[:-1] + ";"
        cursor.execute(insert_analytics_event_query, params_list)
        conn.commit()
        conn.close()
        return True
