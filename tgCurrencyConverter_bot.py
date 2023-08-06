import telebot
from telebot import types,util
import re
import requests
import sys
import os

whitelist = None
if os.path.isfile('./whitelist.py'):
    from whitelist import whitelist

slang_starts = {
    'kkk'       :1000000000,
    'ккк'       :1000000000,
    'kk'        :1000000,
    'кк'        :1000000,
    'k'         :1000,
    'к'         :1000,
    'тыс'       :1000,
    'тыщ'       :1000,
    'косар'     :1000,
    'штук'      :1000,
    'thou'      :1000,
    'мульт'     :1000000,
    'мил'       :1000000,
    'млн'       :1000000,
    'мильё'     :1000000,
    'лям'       :1000000,
    'mil'       :1000000,
    'лярд'      :1000000000,
    'миллиар'   :1000000000,
    'bil'       :1000000000,
}

main_rule = r"((?:\d*[\.,]\d+|\d+))\s*(\w+)*\s*"

currencies = [
            ['UAH', r"(грив|грн|грi|griv|₴)"                , '₴'],
            ['EUR', r"(евр|eur|€)"                          , '€'],
            ['RUB', r"(руб|rub|₽)"                          , '₽'],
            ['USD', r"(дол|dol|бакс|бакин|bucks|бачин|\$)"  , '$'],
            ['KZT', r"(тен|teng|тең|₸)"                     , '₸'],
        ]

currencies_second = [
            ['CNY', r"(юан|yua|¥)"                          , '¥'],
            ['GBP', r"(фунт|pound|£)"                       , '£'],
            ['TRY', r"(лир|lir|₺)"                          , '₺'],
            ['JPY', r"(иен|йен|yen|¥)"                      , '¥'],
]

bot = telebot.TeleBot(sys.argv[1])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def convert(currencies, from_currency, to_currency, amount): 
    if from_currency != 'USD' : 
        amount = amount / currencies[from_currency] 
    amount = round(amount * currencies[to_currency], 4) 
    return amount

@bot.message_handler(content_types=["text"])
def handle_text(mes : telebot.types.Message):
    if whitelist and mes.from_user.id not in whitelist:
        return
    
    if has_numbers(mes.text):

        s = ''
        for c in currencies + currencies_second:
            res = re.search(main_rule + c[1], mes.text, re.IGNORECASE)
            if res:
                curr = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()['rates']
                try:
                    n = float(res[1])
                except ValueError:
                    break
                mult = 1
                if res[2]:
                    lowtext = res[2].lower()
                    try:
                        mult = [value for key, value in slang_starts.items() if key in lowtext][0]
                    except IndexError:
                        return
                    
                n *= mult
                s = f'{n}{c[2]} = '
                for nc in currencies:
                    if c[0] != nc[0]:
                        s += f'{convert(curr,c[0], nc[0], n):,.2f}{nc[2]}  '
                break
        
        if s != '':
            bot.send_message(mes.chat.id, s)
    
bot.infinity_polling(allowed_updates=util.update_types)