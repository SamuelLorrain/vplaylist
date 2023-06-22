from vplaylist.entities.analytics import Analytics
from vplaylist.repositories.analytics_repository import AnalyticsRepository


def create_analytics(analytics: Analytics) -> bool:
    analytics_repository = AnalyticsRepository()
    return analytics_repository.save_analytics(analytics)
