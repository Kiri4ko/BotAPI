"""The handler analytics is being developed. """

import api.main

from buttons.buttons import *

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.utils.markdown import escape_md


async def analytics_handler(message: types.Message):
    await message.answer_sticker("CAACAgIAAxkBAAEF4XhjKOIXDK1pOAABfCEaA5IFdznSeecAAk4CAAJWnb0KMP5rbYEyA28pBA")
    await message.answer("Under development ⚒ ⚙ ️🚀 🌔 ", reply_markup=inline_buttons)
    await message.delete()


async def analytics_handler_call(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Under development ⚒ ⚙ ️🚀 🌔 ", show_alert=True)


def register_handlers_analytics(dp: Dispatcher):
    dp.register_message_handler(analytics_handler, commands="analytics", state="*")
