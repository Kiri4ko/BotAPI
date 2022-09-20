"""Handler wallet. """

from pathlib import Path

import json

import shutil

from buttons.buttons import *

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.state import StatesGroup, State

from aiogram.dispatcher.filters import Text

from aiogram.utils.markdown import escape_md


# user data buy parsing

async def buy_list_cryptocurrencies(user_id: str):
    user_wallet_buy = f'{user_id}_buy.json'
    path_wallet_buy = Path(f'users_wallets/{user_id}/{user_wallet_buy}')

    with open(path_wallet_buy, "r") as file_buy:
        data_buy = json.load(file_buy)
        buy_list_items = [name for value in data_buy for name in value.values()]
        list_cryptocurrencies = list(
            set([key for items in buy_list_items for key, value in items.items()])

        )
    return list_cryptocurrencies


class Wallet(StatesGroup):
    chosen_command = State()
    chosen_cryptocurrency = State()


async def wallet_handler(message: types.Message, state: FSMContext):
    keyboard_commands = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for command in wallet_buttons:
        keyboard_commands.add(command)

    await message.delete()
    await message.answer(
        f"Select an action to use the keyboard👇",
        reply_markup=keyboard_commands
    )

    await state.set_state(Wallet.chosen_command.state)


async def wallet_handler_call(call: types.CallbackQuery, state: FSMContext):
    keyboard_commands = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    for command in wallet_buttons:
        keyboard_commands.add(command)
    await call.answer("Go to the moon 🚀🌔")
    await call.message.answer(
        f"Select an action to use the keyboard👇",
        reply_markup=keyboard_commands
    )
    await state.set_state(Wallet.chosen_command.state)


async def wallet_create(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

    path_directory = Path("users_wallets", f"{message.from_user.id}")
    user_wallet = f'{message.from_user.id}_wallet.json'

    path_wallet = Path(f"{path_directory}", f"{user_wallet}")

    if Path.is_file(path_wallet) is not True:
        user_info = json.loads(f"{message.from_user}")
        Path.mkdir(path_directory)  # Create a user directory

        with open(path_wallet, "w") as file_wallet:
            json.dump(user_info, file_wallet, indent=4)

        await message.delete()
        await message.answer("Well done👍\nThe wallet has been created✅", reply_markup=buy_button)
        await state.finish()
        return
    else:
        await message.delete()
        await message.answer("You have already created a wallet✅", reply_markup=buy_button)
        await state.finish()
        return


async def wallet_chosen_cryptocurrency(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    user_wallet_buy = f'{message.from_user.id}_buy.json'
    path_wallet = Path(f'users_wallets/{message.from_user.id}/{user_wallet_buy}')

    # user data parsing

    if Path.is_file(path_wallet) is True:
        keyboard_currencies_wallet = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for name in await buy_list_cryptocurrencies(message.from_user.id):
            keyboard_currencies_wallet.insert(name)

        await message.answer("Choose a cryptocurrency from your wallet🌎\nUsing the keyboard👇",
                             reply_markup=keyboard_currencies_wallet)

        await state.set_state(Wallet.chosen_cryptocurrency.state)
        return
    else:
        list_button = InlineKeyboardMarkup(row_width=1).add(inline_wallet, inline_buy)
        await message.delete()
        await message.answer("There are no assets on your balance sheet🪙\n"
                             "Or you have not created a wallet❌", reply_markup=list_button)
        await state.finish()
        return


async def wallet_balance(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    keyboard_currencies_wallet = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if message.text.lower() not in await buy_list_cryptocurrencies(message.from_user.id):
        await message.answer("Choose a cryptocurrency from your wallet🌎\nUsing the keyboard👇",
                             reply_markup=keyboard_currencies_wallet)
        return

    await state.update_data(wallet_cryptocurrency=message.text.lower())

    user_wallet_buy = f'{message.from_user.id}_wallet.json'
    path_wallet = Path(f'users_wallets/{message.from_user.id}/{user_wallet_buy}')

    user_data = await state.get_data()
    user_cryptocurrency = user_data.get('wallet_cryptocurrency')

    with open(path_wallet, "r") as wallet_file:
        data_wallet = json.load(wallet_file)
        balance = data_wallet.get(f"balance_{user_cryptocurrency}")

    list_button = InlineKeyboardMarkup(row_width=1).add(inline_price, inline_buy, inline_sell)
    await message.answer(f"Your balance: {escape_md(balance)} {escape_md(user_cryptocurrency).upper()}💰",
                         reply_markup=list_button)
    await state.finish()


async def wallet_delete(message: types.Message, state: FSMContext):
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    path_wallet = Path(f'users_wallets/{message.from_user.id}')

    if Path.is_dir(path_wallet) is True:
        shutil.rmtree(path_wallet)
        await message.delete()
        await message.answer("Done👍\nYour wallet has been deleted✅", reply_markup=wallet_button)
        await state.finish()
        return

    else:
        await message.delete()
        await message.answer(f"You have not created a wallet❌", reply_markup=wallet_button)
        await state.finish()
        return


def register_handlers_wallet(dp: Dispatcher):
    dp.register_message_handler(wallet_handler, commands="wallet", state="*")
    dp.register_message_handler(wallet_create, Text(equals="Create a wallet✅", ignore_case=True),
                                state=Wallet.chosen_command)
    dp.register_message_handler(wallet_chosen_cryptocurrency, Text(equals="View balance💰", ignore_case=True),
                                state=Wallet.chosen_command)
    dp.register_message_handler(wallet_balance, state=Wallet.chosen_cryptocurrency)
    dp.register_message_handler(wallet_delete, Text(equals="Delete a wallet❌", ignore_case=True),
                                state=Wallet.chosen_command)
