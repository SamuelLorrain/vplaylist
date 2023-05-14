from io import FileIO
from typing import Generator

from fastapi.responses import StreamingResponse

from vplaylist.entities.video_file import PlayableVideo


class VideoStreamResponse(StreamingResponse):
    BYTES_PER_RESPONSE = 100000

    def _chunk_generator_from_stream(
        self, stream: FileIO, chunk_size: int, start: int, size: int
    ) -> Generator:
        bytes_read = 0
        stream.seek(start)
        while bytes_read < size:
            bytes_to_read = min(chunk_size, size - bytes_read)
            yield stream.read(bytes_to_read)
            bytes_read = bytes_read + bytes_to_read
        stream.close()

    def __init__(self, video: PlayableVideo, range_asked: str | None):
        total_size = video.get_size()
        start_byte_requested = (
            0 if not range_asked else int(range_asked.split("=")[-1][:-1])
        )
        end_byte_planned = min(
            start_byte_requested + self.BYTES_PER_RESPONSE, total_size
        )

        headers = {
            "Accept-Ranges": "bytes",
            "Content-Type": f"{video.get_media_type()}",
            "Content-Range": f"bytes {start_byte_requested}-{end_byte_planned}/{total_size}",
        }
        chunk_generator = self._chunk_generator_from_stream(
            video.get_stream(),
            chunk_size=10000,
            start=start_byte_requested,
            size=self.BYTES_PER_RESPONSE,
        )

        super().__init__(chunk_generator, headers=headers, status_code=206)
