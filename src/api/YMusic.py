from aiogram import client
from yandex_music import Client, ClientAsync, Playlist, Track, Video
from src.utils import Logger, SearchResults, get_type_of_result_and_title
from config import Y_MUSIC_TOKEN

# Логгер
music_api_log = Logger("music_api_log", "loges/music_api.log")


class YMusic:
    def __init__(self):
        self.API_TOKEN = Y_MUSIC_TOKEN
        self.client = None

    async def _get_client(self):
        if not self.client:
            self.client = await ClientAsync(self.API_TOKEN).init()
        return self.client

    @music_api_log.log_function_call
    async def find(self, request):
        client = await self._get_client()
        search_result = await client.search(text=request, playlist_in_best=True)

        if not search_result or not search_result.best or not search_result.best.result:
            return None

        result = search_result.best.result

        if isinstance(result, Video):
            return None

        result_id = result.kind if isinstance(result, Playlist) else result.id
        if result_id is None:
            return None
        if isinstance(result_id, str):
            result_id = int(result_id)

        type_, title = await get_type_of_result_and_title(result)
        artist_name_if_track = (
            result.artists_name() if isinstance(result, Track) else None
        )

        if None in (result_id, type_, title):
            return None

        return SearchResults(result_id, title, type_, artist_name_if_track)

    @music_api_log.log_function_call
    async def get_artist_track(self, result: int):
        client = await self._get_client()
        tracks = await client.artists_tracks(result)
        return tracks.tracks if tracks else None

    @music_api_log.log_function_call
    async def get_album_tracks(self, result):
        pass

    @music_api_log.log_function_call
    async def get_playlist_tracks(self, result):
        pass

    @music_api_log.log_function_call
    async def get_track_by_id(self, track_id: int) -> Track | None:
        client = await self._get_client()
        tracks = await client.tracks(track_id)
        return tracks[0]

    # Управление воспроизведением
    @music_api_log.log_function_call
    async def track_on(self):
        pass

    @music_api_log.log_function_call
    async def add_track_to_queue(self):
        pass

    @music_api_log.log_function_call
    async def bun_track(self):
        pass

    @music_api_log.log_function_call
    async def pass_track(self):
        pass
