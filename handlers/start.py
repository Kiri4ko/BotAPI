"""Handler start. """

from buttons.buttons import *

from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import Text


async def command_start_handler(message: types.Message, state: FSMContext):
    await message.answer_sticker('CAACAgIAAxkBAAEF4AFjJ4JWO1pIKtf5I4jDPPXNz7eZgAAChwIAAladvQpC7XQrQFfQkCkE')
    await message.answer(
        f"Welcome, *{message.from_user.full_name}*✌\!\n"
        "This's a chat for working with the crypto market🪙\n"
        "Sale and purchase of cryptocurrencies, price monitoring⚒\n"
        "Calculation of profit or loss💰"
        f"\nGo to the moon 🚀🌔👇",
        reply_markup=inline_buttons
    )
    await message.delete()
    await state.finish()


async def cmd_cancel_handler(message: types.Message, state: FSMContext):
    await message.answer("The current action is canceled 🛑", reply_markup=types.ReplyKeyboardRemove())
    await message.bot.delete_message(message.chat.id, message.message_id)
    await state.finish()

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(command_start_handler, commands="start", state="*")
    dp.register_message_handler(cmd_cancel_handler, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel_handler, Text(equals="cancel", ignore_case=True), state="*")
