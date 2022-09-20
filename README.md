# **Bot Coin API v.1.0.0. Connected to the API cryptocurrencies market.**
# **This is a functional telegram bot. The aiogram library and FastAPI was used.**


### What the bot can do:
1. Welcomes new users with a graphical interface.
2. Сan track prices of any crypto assets and provide descriptions.
3. Create a user's wallet by user's ID. 
4. Creates a record of logs: buying and selling cryptocurrencies.
5. The Finite State Machine is used.
6. Provide support for calling certain commands and inline buttons. 
7. Preset filter of banned words (Russian and English).
8. Searching for cryptocurrency and getting information.
9. Saves data in json format.
10. Analytics under development.

***Directory files***:\
**./api/main.py** - API for sending get-requests and getting information about cryptocurrencies. Parse data from with [Coingecko](https://www.coingecko.com)\
**./buttons/buttons.py** - Buttons and their attributes\
**./handlers/.py** - Each command this is a separate handlers\
**./users_wallets/** - Storage of user json files: wallet, purchase and sales log - for data analytics\
**./filters/filters.py** - Word ban functionality\
**./filters/cens.json** - List filter of banned words (Russian and English)
**./requirements.txt** - Dependency\
**./config.py** - Your values are indicated: TOKEN - your bot\
**./Coin_Bot_API** - Bot launch\
**[COIN BOT](https://t.me/api_coin_bot)** - Working version.