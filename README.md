# TgCurrencyConverter bot
Telegram bot for converting currencies in groups or private messages

## Features:
- Can seek any mention of currency and send message with converted value
- Can seek any types: int, float, divided by spaces ("10 dollar", "10 dol", "10.8 $", "100 00 00 eur") 
- Can work in groups or private chats
- No need special invoking. It reed all messages an search for expression: "|number| |first chars of currency name or sign|"
- You can add any currencies and any expression in source code at 'currencies' section
- Suffixes like K, KK, M, millo, billio, thous...
- Optional whitelist of user IDs to prevent unauthorized using

## Usage:
Add the bot into chat and open access to read all mesages, or just use PM. Then just use digit + currency in your message. 

    -Today I found 19$
    -19.0$ = 699.96₴  17.59€  1339.12₽  8702.95₸
    -And 5 eur
    -5.0€ = 198.92₴  380.56₽  5.40$  2473.27₸
    -5.3 million tenge
    -5300000.0₸ = 443,045.94₴  10,902.24€  1,082,548.09₽  11,993.66$  86,474.32¥

### Whitelist
Whitelist can be turned on optionally by creating python file near `tgCurrencyConverter_bot.py` a `whitelist.py` with code like:
```
whitelist = [12345, 12346]
```

## Installation
Setup requirements:
```
pip install -r requirements.txt
```
Run:
```
python tgCurrencyConverter_bot.py "<your tg bot token>"
```