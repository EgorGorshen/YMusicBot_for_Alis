import os, dotenv


dotenv.load_dotenv(".env")
TOKEN = os.getenv("BOT_TOKEN")
Y_MUSIC_TOKEN = os.getenv("Y_MUSIC_TOKEN")
MAX_TRACKS_INLINE_KEYBORD = os.getenv("MAX_TRACKS_INLINE_KEYBORD")
MAX_TRACKS_INLINE_KEYBORD = (
    int(MAX_TRACKS_INLINE_KEYBORD)
    if MAX_TRACKS_INLINE_KEYBORD is not None
    else MAX_TRACKS_INLINE_KEYBORD
)
DB_NAME = os.getenv("DB_NAME") if os.getenv("DB_NAME") is not None else ":memory:"
