import telebot
from telebot import types,util
import re
import requests
import sys

bot = telebot.TeleBot(sys.argv[1])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_num(str:str):
    return float(re.sub('[^0-9,.]', '', str))

def convert(currencies, from_currency, to_currency, amount): 
    if from_currency != 'USD' : 
        amount = amount / currencies[from_currency] 
    amount = round(amount * currencies[to_currency], 4) 
    return amount

@bot.message_handler(content_types=["text"])
def handle_text(mes : telebot.types.Message):
    if has_numbers(mes.text):
        mlc = mes.text.lower()
        
        #main_rule = r"(?:\d*[\.,]\d+|\d+)(\s*)"
        main_rule = r"((?:\d*[\.,]\d+|\d+)(\s*))*"
        currencies = [
            ['UAH', r"(грив|грн|грi|griv|₴)", '₴'],
            ['EUR', r"(евр|eur|€)"     , '€'],
            ['RUB', r"(руб|rub|₽)"     , '₽'],
            ['USD', r"(дол|dol|\$)"    , '$'],
            ['KZT', r"(тен|teng|₸)"     , '₸'],
        ]

        s = ''
        for c in currencies:
            res = re.search(main_rule + c[1], mlc)
            if res:
                curr = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()['rates']
                n = get_num(res[0])
                s = f'{n}{c[2]} = '
                for nc in currencies:
                    if c[0] != nc[0]:
                        s += f'{convert(curr,c[0], nc[0], n):.2f}{nc[2]}  '
                break
        
        if s != '':
            bot.send_message(mes.chat.id, s)
    
bot.infinity_polling(allowed_updates=util.update_types)