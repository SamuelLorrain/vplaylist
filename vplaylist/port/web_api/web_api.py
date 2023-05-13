from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from vplaylist.entities.search_video import SearchVideo
from vplaylist.actions.create_playlist import create_playlist
from pydantic import BaseModel, conint
from typing import Literal
from vplaylist.entities.search_video import Webm, Quality, Sorting, SearchType

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
    quality: Quality = Quality.ALL.value
    limit: conint(ge=1, lt=1000) = 150
    shift: conint(ge=0, lt=1000) = 0
    sorting: Sorting = Sorting.SQL_RANDOM_FUNCTION.value
    should_permutate: bool = True
    should_use_synonyms: bool = True
    search_term: str = ""
    search_type: SearchType = SearchType.BASIC.value


class VideoResponse(BaseModel):
    path: str = ""
    uuid: str = ""


class CreatePlaylistResponse(BaseModel):
    playlist: list[VideoResponse] = []


@app.get("/playlist/create")
async def create_playlist_controller(
    create_playlist_params: CreatePlaylistParams = Depends(),
):
    search_video = SearchVideo(**dict(create_playlist_params))
    print(search_video)
    playlist = create_playlist(search_video)
    video_list = [VideoResponse(path=i.path, uuid=i.uuid) for i in playlist.playlist]
    return CreatePlaylistResponse(playlist=video_list)


@app.get("/playlist/clean")
async def clean_playlist_controller():
    pass


@app.get("/playlist/update")
async def update_playlist_controller():
    pass
