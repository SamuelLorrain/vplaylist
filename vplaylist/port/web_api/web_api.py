from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from vplaylist.actions.create_playlist import create_playlist
from vplaylist.actions.fetch_playable_video import fetch_playable_video
from vplaylist.entities.search_video import (
    Quality,
    SearchType,
    SearchVideo,
    Sorting,
    Webm,
)
from vplaylist.utils.custom_response import VideoStreamResponse

app = FastAPI()

origins = ["http://localhost:5173"]

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


class VideoResponse(BaseModel):
    path: str = ""
    uuid: str = ""


class CreatePlaylistResponse(BaseModel):
    playlist: list[VideoResponse] = []


@app.get("/playlist/create")
async def create_playlist_controller(
    create_playlist_params: CreatePlaylistParams = Depends(),  # noqa: B008
) -> CreatePlaylistResponse:
    search_video = SearchVideo(**dict(create_playlist_params))
    playlist = create_playlist(search_video)

    video_list = [
        VideoResponse(path=i.path.split("/")[-1], uuid=i.uuid)
        for i in playlist.playlist
    ]
    return CreatePlaylistResponse(playlist=video_list)


@app.get("/video/{uuid}")
async def play_video(uuid: UUID, req: Request) -> VideoStreamResponse:
    playable_video = fetch_playable_video(uuid)
    if not playable_video:
        raise HTTPException(status_code=404, detail="Not Found")
    return VideoStreamResponse(playable_video, range_asked=req.headers.get("Range"))

# TODO implement
# @app.get("/playlist/clean")
# async def clean_playlist_controller():
#     pass


# @app.get("/playlist/update")
# async def update_playlist_controller():
#     pass
