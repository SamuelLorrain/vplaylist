from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AnalyticEvent(BaseModel):
    event_datetime: datetime
    event_type: str
    value: float


class Analytics(BaseModel):
    video_uuid: UUID
    date_analytics: datetime
    events: list[AnalyticEvent]
