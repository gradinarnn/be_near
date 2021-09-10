from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def two_buttons(first_button_text,first_button_callback, second_button_text,second_button_callback):
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=first_button_text,
                    callback_data=first_button_callback,

                ),
                InlineKeyboardButton(
                    text=second_button_text,
                    callback_data=second_button_callback,

                )
            ]
        ]
    )