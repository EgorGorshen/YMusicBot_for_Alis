import re
from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from config import MAX_TRACKS_INLINE_KEYBORD

from src.api.YMusic import YMusic
from src.handlers.keyboards import TRACK_CONFIRMATION_KEYBOARD, TRACK_SELECTION_KEYBOARD
from src.utils import Logger, TypesOfSearchResults

users = Router()
client = YMusic()
users_tel_log = Logger("users_tel_log", "loges/users_tel.log")


@users.message(Command("add_track"))
@users_tel_log.log_function_call
async def add_track(message: Message) -> None:
    if not message.text:
        await message.answer("Сообщение не содержит текста")
        return

    match = re.match(r"(/[\w]+)\s*(.*)", message.text)
    if not match:
        await message.answer("Введите запрос в формате [/add_track <name>]")
        return

    request: str | None = match.group(2).strip()

    if request == "":
        await message.answer("Введите запрос в формате [/add_track <name>]")
        return

    search_result = await client.find(request)

    if not search_result:
        await message.answer("Не найдено, попробуй ещё раз.")
        return

    if search_result.type_of_result == TypesOfSearchResults.TRACK:
        artists: str = " [" + ", ".join(search_result.artist_name_if_track) + "]"
        text: str = (
            search_result.result if search_result.result else request
        ) + artists
        await message.answer(
            text=text, reply_markup=TRACK_CONFIRMATION_KEYBOARD(search_result.id)
        )
        return

    if search_result.type_of_result in [
        TypesOfSearchResults.ARTIST,
        TypesOfSearchResults.ALBUM,
    ]:
        tracks_list: Optional[list] = (
            await client.get_artist_track(search_result.id)
            if search_result.type_of_result == TypesOfSearchResults.ARTIST
            else await client.get_album_tracks(search_result.result)
        )
        if not tracks_list:
            await message.answer("Не найдено, попробуй ещё раз.")
            return
        await message.answer(
            text=f"Выбери трек артиста {search_result.result}",
            reply_markup=TRACK_SELECTION_KEYBOARD(
                tracks_list, search_result.id, 0, MAX_TRACKS_INLINE_KEYBORD
            ),
        )
        return

    if search_result.type_of_result == TypesOfSearchResults.PLAYLIST:
        tracks: list = []
        await message.edit_text(
            text=f"Выбери трек артиста {search_result.result}",
            reply_markup=TRACK_SELECTION_KEYBOARD(
                tracks, search_result.id, 0, len(tracks) - 1
            ),
        )
        return

    if search_result.type_of_result == TypesOfSearchResults.NONE:
        await message.answer("Не найдено, попробуй ещё раз.")


@users.callback_query(F.data.startswith("track_confirmation_false"))
@users_tel_log.log_function_call
async def question_to_add_track(callable: CallbackQuery):
    await callable.message.edit_text(text="Хорошо, попробуй найди что-нибудь другое.")


@users.callback_query(F.data.startswith("track_confirmation_true_"))
@users_tel_log.log_function_call
async def add_track_to_queue(callback: CallbackQuery):
    await callback.message.edit_text(text="Добавили")


@users.callback_query(F.data.startswith("track_selection_id_"))
async def track_confirmation(callback: CallbackQuery):
    if not callback.data:
        return

    track_id = int(callback.data.split("_")[-1])
    track = await client.get_track_by_id(track_id)

    if not (track and callback.message):
        await callback.message.edit_text(
            "Простите произошла ошибка, попробуйте ещё раз..."
        )
        return

    if track.title:
        await callback.message.edit_text(
            text=track.title,
            reply_markup=TRACK_CONFIRMATION_KEYBOARD(track_id),
        )
        return
    await callback.message.edit_text("Название трека не найдено.")


@users.callback_query(F.data.startswith("track_selection_forward_"))
@users_tel_log.log_function_call
async def scroll_forward_track_page(callback: CallbackQuery):
    if not callback.data:
        return

    client = YMusic()
    entity_id, from_, till = list(map(int, callback.data.split("_")[-3:]))

    tracks_list = await client.get_artist_track(entity_id)

    if not callback.message or not callback.message.text:
        return

    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=TRACK_SELECTION_KEYBOARD(
            tracks_list, entity_id, till, 2 * till - from_
        ),
    )

    return


@users.callback_query(F.data.startswith("track_selection_backward_"))
@users_tel_log.log_function_call
async def scroll_backward_track_page(callback: CallbackQuery):
    if not callback.data:
        return

    client = YMusic()
    entity_id, from_, till = list(map(int, callback.data.split("_")[-3:]))

    tracks_list = await client.get_artist_track(entity_id)

    if not callback.message or not callback.message.text:
        return

    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=TRACK_SELECTION_KEYBOARD(
            tracks_list, entity_id, 2 * from_ - till, from_
        ),
    )

    return


@users.message(Command("say_toast"))
async def say_toast(message: Message):
    pass


@users.message(Command("cancel_track"))
async def cancel_track(message: Message):
    pass


@users.message(F.photo)
async def get_photo(message: Message):
    pass
