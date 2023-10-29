from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


admin = Router()


@admin.message(Command("ATP"))
async def add_track_to_playlist(message: Message):
    pass


@admin.message(Command("track_history"))
async def track_history(message: Message):
    pass


@admin.message(Command("ban"))
async def ban(message: Message):
    pass
