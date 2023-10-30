from aiogram import types
from yandex_music import Track


def _get_track_selection_keyboard(
    tracks: list[Track], entity_id: int, from_: int, till: int
) -> types.InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(
                text=i.title, callback_data=f"track_selection_id_{i.id}"
            )
        ]
        for i in tracks[from_ : till if till <= len(tracks) else None]
        if i.title is not None
    ]

    next_previous = []

    if from_ > 0:
        next_previous.append(
            types.InlineKeyboardButton(
                text="<",
                callback_data=f"track_selection_backward_{entity_id}_{from_}_{till}",
            )
        )

    if till < len(tracks):
        next_previous.append(
            types.InlineKeyboardButton(
                text=">",
                callback_data=f"track_selection_forward_{entity_id}_{from_}_{till}",
            )
        )

    if next_previous is not None:
        buttons.append(next_previous)

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


TRACK_CONFIRMATION_KEYBOARD = lambda track_id: types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Добавить в очередь",
                callback_data=f"track_confirmation_true_{track_id}",
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Не тот трек", callback_data="track_confirmation_false"
            )
        ],
    ]
)

TRACK_SELECTION_KEYBOARD = (
    lambda tracs, entity_id, from_, till: _get_track_selection_keyboard(
        tracs, entity_id, from_, till
    )
)
