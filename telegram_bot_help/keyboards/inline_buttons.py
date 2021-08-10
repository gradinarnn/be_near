from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import edite_profile_callback, registration_callback


def change_profile_or_status_button(text_btn1, url1, text_btn2,m_id_value):
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text_btn1,
                    callback_data=edite_profile_callback.new(status="edite_profile"),
                    url=url1

                ),
                InlineKeyboardButton(
                    text=text_btn2,
                    callback_data=registration_callback.new(m_id_value=m_id_value)

                )
            ]
        ]
    )