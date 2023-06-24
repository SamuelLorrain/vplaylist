from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from dotenv import dotenv_values
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from vplaylist.actions.create_analytics import create_analytics
from vplaylist.actions.create_participant import create_participant
from vplaylist.actions.create_playlist import create_playlist
from vplaylist.actions.create_video_participant_relation import (
    create_video_participant_relation,
)
from vplaylist.actions.delete_video_participant_relation import (
    delete_video_participant_relation,
)
from vplaylist.actions.fetch_video import fetch_video
from vplaylist.actions.fetch_video_details import fetch_video_details
from vplaylist.actions.patch_video_details import modify_video_details
from vplaylist.actions.search_participant import search_participant
from vplaylist.entities.analytics import AnalyticEvent, Analytics
from vplaylist.entities.search_video import (
    Quality,
    SearchType,
    SearchVideo,
    Sorting,
    Webm,
)
from vplaylist.port.web_api.responses.create_playlist_response import (
    CreatePlaylistResponse,
    VideoResponse,
)
from vplaylist.port.web_api.responses.video_details_response import VideoDetailsResponse
from vplaylist.port.web_api.responses.video_stream_response import VideoStreamResponse

app = FastAPI()

dotenv_config = dotenv_values(".env")

origins = [dotenv_config["FRONT_HOST"]]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreatePlaylistParams(BaseModel):
    webm: Webm = Webm.ALL
    quality: Quality = Quality.ALL
    limit: int = 150
    shift: int = 0
    sorting: Sorting = Sorting.SQL_RANDOM_FUNCTION
    should_permutate: bool = True
    should_use_synonyms: bool = True
    search_term: str = ""
    search_type: SearchType = SearchType.BASIC


@app.get("/playlist/create")
async def create_playlist_controller(
    create_playlist_params: CreatePlaylistParams = Depends(),  # noqa: B008
) -> CreatePlaylistResponse:
    search_video = SearchVideo(**dict(create_playlist_params))
    playlist = create_playlist(search_video)

    video_list = [VideoResponse(path=str(i.path), uuid=str(i.uuid)) for i in playlist]
    return CreatePlaylistResponse(playlist=video_list)


@app.get("/video/{uuid}")
async def play_video(uuid: UUID, req: Request) -> VideoStreamResponse:
    playable_video = fetch_video(uuid)
    if not playable_video:
        raise HTTPException(status_code=404, detail="Not Found")
    return VideoStreamResponse(playable_video, range_asked=req.headers.get("Range"))


@app.get("/video/{uuid}/details")
async def get_video_details(uuid: UUID) -> VideoDetailsResponse:
    video_details = fetch_video_details(uuid)
    return video_details


class VideoDetailsParams(BaseModel):
    name: Optional[str]
    note: Optional[int]
    date_down: Optional[str]


@app.put("/video/{uuid}/details")
async def patch_video_details(
    uuid: UUID, video_details_params: VideoDetailsParams
) -> Response:
    modify_video_details(uuid, video_details_params)
    return Response("", status_code=201)


class VideoAnalyticsEventParams(BaseModel):
    event_type: str
    value: float
    timestamp: int


class VideoAnalyticsParams(BaseModel):
    timestamp: int
    events: list[VideoAnalyticsEventParams]


@app.post("/video/{uuid}/analytics")
async def upload_video_analytics(
    uuid: UUID, video_analytics_params: VideoAnalyticsParams
) -> Response:
    events = [
        AnalyticEvent(
            event_type=event.event_type,
            value=event.value,
            event_datetime=datetime.fromtimestamp(event.timestamp),
        )
        for event in video_analytics_params.events
    ]
    analytics = Analytics(
        video_uuid=uuid,
        date_analytics=datetime.fromtimestamp(video_analytics_params.timestamp),
        events=events,
    )
    create_analytics(analytics)
    return Response("", status_code=201)


class ParticipantParams(BaseModel):
    name: str


@app.post("/participant")
async def upload_participant(participant_params: ParticipantParams) -> BaseModel:
    return create_participant(participant_params.name)


@app.post("/video/{video_uuid}/participant/{participant_uuid}")
async def add_video_participant_relation(
    video_uuid: UUID, participant_uuid: UUID
) -> Response:
    create_video_participant_relation(video_uuid, participant_uuid)
    return Response("", status_code=201)


@app.delete("/video/{video_uuid}/participant/{participant_uuid}")
async def remove_video_participant_relation(
    video_uuid: UUID, participant_uuid: UUID
) -> Response:
    delete_video_participant_relation(video_uuid, participant_uuid)
    return Response("", status_code=201)


@app.get("/participant")
async def get_participants(search: str = "") -> Sequence[BaseModel]:
    search_result = []
    if search == "":
        search_result = search_participant(None)
    else:
        search_result = search_participant(search)
    return search_result
