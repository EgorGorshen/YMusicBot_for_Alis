from dataclasses import dataclass
from enum import Enum
import logging, functools

from yandex_music import Album, Artist, Playlist, Track


class TypesOfSearchResults(Enum):
    ARTIST = "ARTIST"
    TRACK = "TRACK"
    ALBUM = "ALBUM"
    PLAYLIST = "PLAYLIST"
    NONE = None


class MusicStatus(Enum):
    PLAYED = "PLAYED"
    SHUT = "SHUT"
    TOAST = "TOAST"


async def get_type_of_result_and_title(result):
    if isinstance(result, Artist):
        return TypesOfSearchResults.ARTIST, result.name

    if isinstance(result, Track):
        return TypesOfSearchResults.TRACK, result.title

    if isinstance(result, Album):
        return TypesOfSearchResults.ALBUM, result.title

    if isinstance(result, Playlist):
        return TypesOfSearchResults.PLAYLIST, result.title

    return TypesOfSearchResults.NONE, None


@dataclass
class SearchResults:
    id: int
    result: str | None
    type_of_result: TypesOfSearchResults
    artist_name_if_track: list[str] | None


class Logger:
    def __init__(self, name, log_file, level=logging.INFO):
        """Function setup as many loggers as you want"""

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

    def log_function_call(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(
                f"Calling function {func.__name__} with arguments {args} and keyword arguments {kwargs}"
            )
            try:
                result = func(*args, **kwargs)
                self.logger.info(f"Function {func.__name__} completed successfully")
                return result
            except Exception as e:
                self.logger.error(f"Function {func.__name__} raised an error: {str(e)}")
                raise e  # re-raise the caught exception after logging it

        return wrapper
