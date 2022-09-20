"""Handler price. """

import api.main

from buttons.buttons import *

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.utils.markdown import escape_md


class Price(StatesGroup):
    name_cryptocurrency = State()
    name_cross_rate = State()


async def price_handler(message: types.Message, state: FSMContext):
    keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in crypto_currencies:
        keyboard_currencies.insert(name)
    await message.answer("Enter the name of the cryptocurrency or to use the keyboard👇",
                         reply_markup=keyboard_currencies)
    await message.delete()
    await state.set_state(Price.name_cryptocurrency.state)


async def price_handler_call(call: types.CallbackQuery, state: FSMContext):
    keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in crypto_currencies:
        keyboard_currencies.insert(name)
    await call.answer("Go to the moon 🚀🌔👇")
    await call.message.answer("Enter the name of the cryptocurrency or to use the keyboard👇",
                              reply_markup=keyboard_currencies)
    await state.set_state(Price.name_cryptocurrency.state)


async def coin_handler(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    list_cryptocurrencies_api = api.main.list_coins_id("id")
    keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in crypto_currencies:
        keyboard_currencies.insert(name)
    if message.text.lower() not in list_cryptocurrencies_api:
        await message.answer("You can search👇",
                             reply_markup=InlineKeyboardMarkup(row_width=1).add(inline_search))
        await message.answer("Please, enter the name of the cryptocurrency or to use the keyboard⌨️👇",
                             reply_markup=keyboard_currencies)
        return
    await state.update_data(chosen_cryptocurrency=message.text.lower())

    keyboard_cross_rate = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for currency in cross_rate:
        keyboard_cross_rate.insert(currency)
    await state.set_state(Price.name_cross_rate.state)
    await message.answer(escape_md("Choose which currency to convert to...👇"), reply_markup=keyboard_cross_rate)


async def cross_rate_handler(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    if message.text not in cross_rate:
        await message.answer(escape_md("Please, choose which currency to convert to...👇"))
        return
    await state.update_data(chosen_cross_rate=message.text.lower())
    user_data = await state.get_data()
    await message.answer(escape_md(
        f"Price {user_data.get('chosen_cryptocurrency').lower()}: "
        f"{api.main.coins_price(user_data.get('chosen_cryptocurrency'), user_data.get('chosen_cross_rate'))} "
        f"{message.text}"),
        reply_markup=InlineKeyboardMarkup(row_width=1).add(inline_buy, inline_sell)
    )
    await state.finish()


def register_handlers_price(dp: Dispatcher):
    dp.register_message_handler(price_handler, commands="price", state="*")
    dp.register_message_handler(coin_handler, state=Price.name_cryptocurrency)
    dp.register_message_handler(cross_rate_handler, state=Price.name_cross_rate)
