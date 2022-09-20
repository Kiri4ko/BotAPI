"""Handler sell. """

import json

from pathlib import Path

from buttons.buttons import *

from handlers.wallet import buy_list_cryptocurrencies

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.utils.markdown import escape_md


class Sell(StatesGroup):
    name_currencies = State()
    amount_coins = State()


async def sell_handler(message: types.Message, state: FSMContext):
    user_wallet_buy = f'{message.from_user.id}_buy.json'
    path_wallet_buy = Path(f'users_wallets/{message.from_user.id}/{user_wallet_buy}')

    if Path.is_file(path_wallet_buy) is not True:
        await message.delete()
        await message.answer("No cryptocurrencies on your balance sheet❌", reply_markup=buy_button)
        await state.finish()
        return
    else:
        keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in await buy_list_cryptocurrencies(message.from_user.id):
            keyboard_currencies.insert(name)
        await message.answer("Choose a cryptocurrency from your wallet🌎\nUsing the keyboard👇",
                             reply_markup=keyboard_currencies)
        await message.delete()
        await state.set_state(Sell.name_currencies.state)


async def sell_handler_call(call: types.CallbackQuery, state: FSMContext):
    user_wallet_buy = f'{call.from_user.id}_buy.json'
    path_wallet_buy = Path(f'users_wallets/{call.from_user.id}/{user_wallet_buy}')

    if Path.is_file(path_wallet_buy) is not True:
        await call.answer("No cryptocurrencies on your balance sheet❌")
        await state.finish()
        return
    else:
        keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in await buy_list_cryptocurrencies(call.from_user.id):
            keyboard_currencies.insert(name)
        await call.message.answer("Choose a cryptocurrency from your wallet🌎\nUsing the keyboard👇",
                                  reply_markup=keyboard_currencies)
        await state.set_state(Sell.name_currencies.state)


async def sell_cryptocurrency(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    if message.text.lower() not in await buy_list_cryptocurrencies(message.from_user.id):
        keyboard_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for name in await buy_list_cryptocurrencies(message.from_user.id):
            keyboard_currencies.insert(name)
        await message.answer("Please, choose a cryptocurrency from your wallet🌎\nUsing the keyboard👇",
                             reply_markup=keyboard_currencies)
        return

    await state.update_data(sell_cryptocurrency=message.text.lower())

    # balance inquiry

    user_wallet = f'{message.from_user.id}_wallet.json'
    path_wallet = Path(f'users_wallets/{message.from_user.id}/{user_wallet}')

    user_data = await state.get_data()
    user_cryptocurrency = user_data['sell_cryptocurrency']

    with open(path_wallet, "r") as wallet_file:
        data_wallet = json.load(wallet_file)
        wallet_balance = data_wallet.get(f"balance_{user_cryptocurrency}")

    global actual_balance
    actual_balance = wallet_balance

    keyboard_amount = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
    for value in amount:
        keyboard_amount.insert(value)

    await message.answer(f"Your balance: {escape_md(actual_balance)} {escape_md(user_cryptocurrency).upper()}💰\n"
                         "Enter the number of coins to sell or use the keyboard👇", reply_markup=keyboard_amount)
    await state.set_state(Sell.amount_coins.state)


async def sell_amount_coins(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    # for response user, when not float - ValueError
    user_digits = message.text

    def is_number(user_digits):
        try:
            float(user_digits)
            return True
        except:
            return False

    if is_number(user_digits) is not True or float(user_digits) > actual_balance:
        keyboard_amount = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
        for value in amount:
            keyboard_amount.insert(value)
        await message.answer("Enter the number of coins or use the keyboard\.\n"
                             "And do not exceed the value of your balance👇", reply_markup=keyboard_amount)
        return

    user_digits = abs(float(message.text))
    await state.update_data(sell_amount_coins=user_digits)

    # user dict sell

    data_sell_user = await state.get_data()
    data_name_coin = data_sell_user.get("sell_cryptocurrency")
    data_amount_coin = data_sell_user.get("sell_amount_coins")
    date = message.date
    data_user_dict = {f'sell_{date}': {data_name_coin: data_amount_coin}}

    user_wallet_sell = f'{message.from_user.id}_sell.json'
    user_wallet = f'{message.from_user.id}_wallet.json'
    path_wallet_sell = Path(f'users_wallets/{message.from_user.id}/{user_wallet_sell}')
    path_wallet = Path(f'users_wallets/{message.from_user.id}/{user_wallet}')

    # sales registration

    if Path.is_file(path_wallet_sell) is not True:
        with open(path_wallet_sell, "w") as file_sell:
            file_sell.write('[')
            file_sell.seek(0, 1)
            json.dump(data_user_dict, file_sell)
            file_sell.write(']')

    else:
        with open(path_wallet_sell, "r") as file_sell:
            sell_add = json.load(file_sell)
            sell_add.append(data_user_dict)
        with open(path_wallet_sell, "w") as file_sell:
            json.dump(sell_add, file_sell)

    # update balance user

    with open(path_wallet, "r") as file_wallet:
        wallet_app = json.load(file_wallet)
        wallet_app.update({f"balance_{data_name_coin}": wallet_app.get(f"balance_{data_name_coin}") - data_amount_coin})

    with open(path_wallet, "w") as file_wallet:
        json.dump(wallet_app, file_wallet, indent=4)

    list_buttons = InlineKeyboardMarkup(row_width=1).add(inline_wallet, inline_buy, inline_sell)
    await message.answer(
        f"Done✅\nYou sold coins: {escape_md(data_amount_coin)} {escape_md(data_name_coin).upper()}💰\n"
        f"Your balance: {escape_md(wallet_app.get(f'balance_{data_name_coin}'))} {escape_md(data_name_coin).upper()}💰",
        reply_markup=list_buttons
    )

    await state.finish()


def register_handlers_sell(dp: Dispatcher):
    dp.register_message_handler(sell_handler, commands="sell", state="*")
    dp.register_message_handler(sell_cryptocurrency, state=Sell.name_currencies)
    dp.register_message_handler(sell_amount_coins, state=Sell.amount_coins)
