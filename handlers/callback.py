"""Register handler callback. """

from handlers.price import price_handler_call

from handlers.wallet import wallet_handler_call

from handlers.buy import buy_handler_call

from handlers.sell import sell_handler_call

from handlers.search import search_handler_call

from handlers.info import info_handler_call

from handlers.analytics import analytics_handler_call

from aiogram import Dispatcher


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(price_handler_call, text='button_price')
    dp.register_callback_query_handler(buy_handler_call, text='button_buy')
    dp.register_callback_query_handler(sell_handler_call, text='button_sell')
    dp.register_callback_query_handler(search_handler_call, text='button_search')
    dp.register_callback_query_handler(info_handler_call, text='button_info')
    dp.register_callback_query_handler(analytics_handler_call, text='button_analytics')
    dp.register_callback_query_handler(wallet_handler_call, text='button_wallet')
