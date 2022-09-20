"""Handler buy. """

import api.main

import json

from pathlib import Path

from buttons.buttons import *

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.utils.markdown import escape_md


class Buy(StatesGroup):
    name_currencies = State()
    amount_coins = State()


async def buy_handler(message: types.Message, state: FSMContext):
    user_wallet = f'{message.from_user.id}_wallet.json'
    path_wallet = Path(f'users_wallets/{message.from_user.id}/{user_wallet}')

    if Path.is_file(path_wallet) is not True:
        await message.delete()
        await message.answer("You have not created a wallet❌", reply_markup=wallet_button)
        await state.finish()
        return
    else:
        keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in crypto_currencies:
            keyboard_currencies.insert(name)
        await message.answer("Enter the name of the cryptocurrency or to use the keyboard👇",
                             reply_markup=keyboard_currencies)
        await message.delete()
        await state.set_state(Buy.name_currencies.state)


async def buy_handler_call(call: types.CallbackQuery, state: FSMContext):
    user_wallet = f'{call.from_user.id}_wallet.json'
    path_wallet = Path(f'users_wallets/{call.from_user.id}/{user_wallet}')

    if Path.is_file(path_wallet) is not True:
        await call.answer("You have not created a wallet❌")
        await state.finish()
        return
    else:
        keyboard_name_crypto = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in crypto_currencies:
            keyboard_name_crypto.insert(name)
        await call.answer("Go to the moon 🚀🌔👇")
        await call.message.answer("Enter the name of the cryptocurrency or to use the keyboard👇",
                                  reply_markup=keyboard_name_crypto)
        await state.set_state(Buy.name_currencies.state)


async def buy_cryptocurrency(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    keyboard_name_crypto = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in crypto_currencies:
        keyboard_name_crypto.insert(name)
    list_cryptocurrencies_api = api.main.list_coins_id("id")
    if message.text.lower() not in list_cryptocurrencies_api:
        await message.answer("You can search👇",
                             reply_markup=InlineKeyboardMarkup().add(inline_search))
        await message.answer("Please, enter the name of the cryptocurrency or to use the keyboard⌨️\n",
                             reply_markup=keyboard_name_crypto)
        return

    await state.update_data(buy_cryptocurrency=message.text.lower())

    keyboard_amount = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
    for value in amount:
        keyboard_amount.insert(value)
    await state.set_state(Buy.amount_coins.state)
    await message.answer("Enter the number of coins or use the keyboard👇", reply_markup=keyboard_amount)


async def buy_amount_coins(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

    # for response user, when not float - ValueError

    user_digits = message.text

    def is_number(user_digits):
        try:
            float(user_digits)
            return True
        except:
            return False

    if is_number(user_digits) is not True:
        keyboard_amount = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
        for value in amount:
            keyboard_amount.insert(value)
        await message.answer("Enter the number of coins or use the keyboard👇", reply_markup=keyboard_amount)
        return

    user_digits = abs(float(message.text))
    await state.update_data(buy_amount_coins=user_digits)

    # user dict

    data_buy_user = await state.get_data()
    data_name_coin = data_buy_user.get("buy_cryptocurrency")
    data_amount_coin = data_buy_user.get("buy_amount_coins")
    date = message.date
    data_user_dict = {f'buy_{date}': {data_name_coin: data_amount_coin}}

    user_wallet_buy = f'{message.from_user.id}_buy.json'
    user_wallet = f'{message.from_user.id}_wallet.json'
    path_wallet_buy = Path(f'users_wallets/{message.from_user.id}/{user_wallet_buy}')
    path_wallet = Path(f'users_wallets/{message.from_user.id}/{user_wallet}')

    if Path.is_file(path_wallet_buy) is not True:
        with open(path_wallet_buy, "w") as file_buy:
            file_buy.write('[')
            file_buy.seek(0, 1)
            json.dump(data_user_dict, file_buy)
            file_buy.write(']')

    else:
        with open(path_wallet_buy, "r") as file_buy:
            buy_add = json.load(file_buy)
            buy_add.append(data_user_dict)
        with open(path_wallet_buy, "w") as file_buy:
            json.dump(buy_add, file_buy)

    # update balance user. Except for None balance
    try:
        with open(path_wallet, "r") as file_wallet:
            wallet_app = json.load(file_wallet)
            wallet_app.update(
                {f"balance_{data_name_coin}": wallet_app.get(f"balance_{data_name_coin}") + data_amount_coin})
        with open(path_wallet, "w") as file_wallet:
            json.dump(wallet_app, file_wallet, indent=4)
    except:
        with open(path_wallet, "r") as file_wallet:
            wallet_app = json.load(file_wallet)
            wallet_app.update({f"balance_{data_name_coin}": data_amount_coin})
        with open(path_wallet, "w") as file_wallet:
            json.dump(wallet_app, file_wallet, indent=4)

    list_buttons = InlineKeyboardMarkup(row_width=1).add(inline_buy, inline_sell, inline_wallet)
    await message.answer(
        f"Done✅\nYou bought coins: {escape_md(data_amount_coin)} {escape_md(data_name_coin).upper()}💰\n"
        f"Your balance: {escape_md(wallet_app.get(f'balance_{data_name_coin}'))} {escape_md(data_name_coin).upper()}💰",
        reply_markup=list_buttons
    )

    await state.finish()


def register_handlers_buy(dp: Dispatcher):
    dp.register_message_handler(buy_handler, commands="buy", state="*")
    dp.register_message_handler(buy_cryptocurrency, state=Buy.name_currencies)
    dp.register_message_handler(buy_amount_coins, state=Buy.amount_coins)
