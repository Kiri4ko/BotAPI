"""Bot Coin API v.1.0.0. Connected to the API cryptocurrencies market"""

import config

import asyncio

import logging

from handlers.callback import register_callback
from handlers.start import register_handlers_common
from handlers.wallet import register_handlers_wallet
from handlers.buy import register_handlers_buy
from handlers.sell import register_handlers_sell
from handlers.price import register_handlers_price
from handlers.search import register_handlers_search
from handlers.info import register_handlers_info
from handlers.help import register_handlers_help
from handlers.analytics import register_handlers_analytics
from filters.filters import register_handlers_filters

from aiogram.types.bot_command import BotCommand

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram import Bot, Dispatcher

from aiogram import types

logger = logging.getLogger(__name__)


# commands registration

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Go to the moon🚀🌔"),
        BotCommand(command="/price", description="Price of cryptocurrency📈"),
        BotCommand(command="/buy", description="Buy cryptocurrency for analytics🔋"),
        BotCommand(command="/sell", description="Sell cryptocurrency for analytics🪫"),
        BotCommand(command="/search", description="Search for cryptocurrency🔎"),
        BotCommand(command="/i", description="Info about cryptocurrencies💰"),
        BotCommand(command="/analytics", description="Analysis of possible profits and losses📊"),
        BotCommand(command="/wallet", description="Your wallet🏦"),
        BotCommand(command="/help", description="If you need help🆘"),
        BotCommand(command="/cancel", description="Cancel current action🛑")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # declaring and initializing bot and dispatcher objects

    bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # handler Registration

    register_callback(dp)
    register_handlers_common(dp)
    register_handlers_price(dp)
    register_handlers_buy(dp)
    register_handlers_wallet(dp)
    register_handlers_sell(dp)
    register_handlers_search(dp)
    register_handlers_info(dp)
    register_handlers_help(dp)
    register_handlers_analytics(dp)
    register_handlers_filters(dp)

    # bot commands installation

    await set_commands(bot)

    # launching Polling
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
