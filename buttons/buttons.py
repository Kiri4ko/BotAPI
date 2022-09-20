from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# buttons Inline

inline_price = InlineKeyboardButton(text='PRICE 📈', callback_data="button_price")
price_button = InlineKeyboardMarkup().add(inline_price)
inline_buy = InlineKeyboardButton(text='BUY 🔋', callback_data="button_buy")
buy_button = InlineKeyboardMarkup().add(inline_buy)
inline_sell = InlineKeyboardButton(text='SELL 🪫', callback_data="button_sell")
sell_button = InlineKeyboardMarkup().add(inline_sell)
inline_search = InlineKeyboardButton(text='SEARCH 🔎', callback_data="button_search")
search_button = InlineKeyboardMarkup().add(inline_search)
inline_info = InlineKeyboardButton(text='INFO 🗃', callback_data="button_info")
info_button = InlineKeyboardMarkup().add(inline_search)
inline_analytics = InlineKeyboardButton(text='ANALYTICS 📊', callback_data="button_analytics")
analytics_button = InlineKeyboardMarkup().add(inline_analytics)
inline_wallet = InlineKeyboardButton(text='WALLET 🏦️', callback_data="button_wallet")
wallet_button = InlineKeyboardMarkup().add(inline_wallet)

inline_buttons = InlineKeyboardMarkup(row_width=1)
inline_buttons.add(
    inline_price, inline_buy,
    inline_sell, inline_search,
    inline_info, inline_analytics,
    inline_wallet
)

# buttons Keyboard

crypto_currencies = [
    "Bitcoin", "Binancecoin", "Ethereum", "Tether", "Ripple",
    "Cardano", "Dogecoin", "Solana", "Litecoin", "eCash"
]
cross_rate = ["USD", "EUR", "GBP", "RUB"]
amount = ["0.05", "0.1", "0.2", "0.3", "0.5", "1", "2", "5", "10", "50", "100", "1000"]

wallet_buttons = ["Create a wallet✅", "View balance💰", "Delete a wallet❌"]

"""
Commands for Botfather

start - Go to the moon🚀🌔
price - Price of cryptocurrency📈
buy - Buy cryptocurrency for analytics🔋
sell - Sell cryptocurrency for analytics🪫
search - Search for cryptocurrency🔎
analytics - Analysis of possible profits and losses📊
wallet - Your wallet🏦
i - About the COIN💰BOT🤖
help - If you need help🆘
cancel - Cancel current action🛑
"""
