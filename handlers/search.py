"""Handler search. """

import api.main

from buttons.buttons import *

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.utils.markdown import escape_md


class Search(StatesGroup):
    name_cryptocurrency = State()


async def search_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer("Enter the name of the cryptocurrency\.\.\.👀\n"
                         "Please enter more than two characters☝️\n"
                         "Example: bit or bitcoin✅")
    await state.set_state(Search.name_cryptocurrency.state)


async def search_handler_call(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Go to the moon 🚀🌔")
    await call.message.answer("Enter the name of the cryptocurrency\.\.\.👀\n"
                              "Please, enter more than two characters☝️\n"
                              "Example: bit or bitcoin✅")
    await state.set_state(Search.name_cryptocurrency.state)


async def cryptocurrency_search(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    list_cryptocurrencies_api = api.main.list_coins_id("id")
    search = [name for name in list_cryptocurrencies_api if name[0:len(message.text.lower())] == message.text.lower()]
    if len(search) == 0:
        await message.answer_sticker("CAACAgIAAxkBAAEF4WRjKNeZy-Ifq8vm5BBkElTsqfDwVgACeAIAAladvQr8ugi1kX0cDCkE")
        await message.answer("No matches were found🙀 Try again♻\n"
                             "Enter the name of the cryptocurrency\.\.\.👀\n"
                             "Please, enter more than two characters☝️\n*Example: bit or bitcoin*✅")
        return

    await state.update_data(chosen_cryptocurrency=message.text.lower())

    try:  # for limit message
        await message.answer(f"Look at the list according to your criteria👀:\n{escape_md(str(search))}",
                             reply_markup=inline_buy)
        await state.finish()

    except:
        url = 'https://fastapicoins.herokuapp.com/coins/list/id/'
        await message.answer(
            f"The list exceeds the allowable value, go to the **[LINK]({url})**🛰\n"
            "Or enter more than one letter of the coin name\!", reply_markup=inline_buy
        )
        await state.finish()


def register_handlers_search(dp: Dispatcher):
    dp.register_message_handler(search_handler, commands="search", state="*")
    dp.register_message_handler(cryptocurrency_search, state=Search.name_cryptocurrency)
