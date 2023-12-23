from vplaylist.app import app
from vplaylist.entities.analytics import Analytics
from vplaylist.repositories.analytics_repository import AnalyticsRepository


def create_analytics(analytics: Analytics) -> bool:
    analytics_repository = app(AnalyticsRepository)  # type: ignore
    return analytics_repository.save_analytics(analytics)
