# TgCurrencyConverter bot
Telegram bot for converting currencies in groups or private messages

## Features:
- Can seek any mention of currency and send message with converted value
- Can work in groups or private chats
- No need special invoking. It reed all messages an search for expression: "|number| |first chars of currency name or sign|"
- You can add any currencies and any expression in source code at 'currencies' section

## Usage:

    -Today I found 19$
    -19.0$ = 699.96₴  17.59€  1339.12₽  8702.95₸
    -And 5 eur
    -5.0€ = 198.92₴  380.56₽  5.40$  2473.27₸


## Installation
Setup requirements:
```
pip install -r requirements.txt
```
Run:
```
python tgCurrencyConverter_bot.py "<your tg bot token>"
```