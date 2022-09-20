"""Handler buy. """

from aiogram import Dispatcher, types


async def help_handler(message: types.Message):
    await message.answer_sticker("CAACAgIAAxkBAAEF4XJjKOC67Gss-AABuahWEWJMf4yKxBsAAoQWAAJliMlJW1GsEWSIU8EpBA")
    await message.answer(
        f"*{message.from_user.full_name}*, if you need help 🆘\n"
        f"Write to the owner📲 @[Your contact telegram]\n *I'm on vacation* 🏖",
    )
    await message.delete()


def register_handlers_help(dp: Dispatcher):
    dp.register_message_handler(help_handler, commands="help", state="*")
