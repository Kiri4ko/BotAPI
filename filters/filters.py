"""Handler filters. """

import string

from buttons.buttons import inline_buttons

import json

from aiogram import types

from aiogram import Dispatcher


async def filter_messages(message: types.Message):
    if {i.lower().translate(str.maketrans(' ', ' ', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('filters/cens.json')))) != set():
        await message.answer_sticker("CAACAgIAAxkBAAEF4YBjKOatae2HHFDk9OCDFARhDD8ptwACcQIAAladvQrClj8-xrRJVykE")
        await message.reply(
            f"Forbidden Word❌\!\!\!\nYou *{message.from_user.full_name}*\-wrong chat room😡\!",
            reply_markup=inline_buttons
        )
        await message.delete()


def register_handlers_filters(dp: Dispatcher):
    dp.register_message_handler(filter_messages, state="*")
