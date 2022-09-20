"""Handler info. """

import api.main

from buttons.buttons import *

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.utils.markdown import escape_md


class Info(StatesGroup):
    name_cryptocurrency = State()


async def info_handler(message: types.Message, state: FSMContext):
    await message.delete()
    keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in crypto_currencies:
        keyboard_currencies.insert(name)
    await message.answer("Enter the name of the cryptocurrency or to use the keyboard👇",
                         reply_markup=keyboard_currencies)
    await state.set_state(Info.name_cryptocurrency.state)


async def info_handler_call(call: types.CallbackQuery, state: FSMContext):
    keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in crypto_currencies:
        keyboard_currencies.insert(name)
    await call.answer("Go to the moon 🚀🌔")
    await call.message.answer("Enter the name of the cryptocurrency or to use the keyboard👇",
                              reply_markup=keyboard_currencies)
    await state.set_state(Info.name_cryptocurrency.state)


async def cryptocurrency_info(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    list_cryptocurrencies_api = api.main.list_coins_id("id")
    keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in crypto_currencies:
        keyboard_currencies.insert(name)
    if message.text.lower() not in list_cryptocurrencies_api:
        await message.answer("No matches were found🙀 Try again♻️\n"
                             "You can search👇",
                             reply_markup=InlineKeyboardMarkup(row_width=1).add(inline_search))
        await message.answer("Please, enter the name of the cryptocurrency or to use the keyboard⌨️👇",
                             reply_markup=keyboard_currencies)
        return
    await state.update_data(chosen_cryptocurrency=message.text.lower())
    info_cryptocurrency_api = api.main.coin(message.text.lower())

    buttons = InlineKeyboardMarkup(row_width=1).add(inline_price, inline_buy, inline_sell)
    await message.answer(f"*{escape_md(message.text.upper())}* information:\n{escape_md(info_cryptocurrency_api)}🤓",
                         reply_markup=buttons)
    await state.finish()


def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(info_handler, commands="i", state="*")
    dp.register_message_handler(cryptocurrency_info, state=Info.name_cryptocurrency)
