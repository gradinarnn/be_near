from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filling_profile.CallbackData import meeting_feedback


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

def leave_feedback_buttons():
    return InlineKeyboardMarkup(
        row_width=5,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='👎',
                    callback_data=meeting_feedback.new(status="1")

                ),
                InlineKeyboardButton(
                    text='😒',
                    callback_data=meeting_feedback.new(status="2")

                ),
                InlineKeyboardButton(
                    text='🙂',
                    callback_data=meeting_feedback.new(status="3")

                ),

                InlineKeyboardButton(
                    text='😍',
                    callback_data=meeting_feedback.new(status="4")
                ),
                InlineKeyboardButton(
                    text='👍',
                    callback_data=meeting_feedback.new(status="5")
                )

            ]
        ]
    )